#!/usr/bin/env python3
"""Modelo LOADX de dos pasadas: pruebas solo de HOST, no de CPU Aula."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from modelo_bloques_aula8_r0_12 import BLOCK_SIZE, FileBlockImage, ImageIOError
from modelo_ejecutable_aula8_r0_13 import (
    AexError, KIND_PRACTICE, KIND_TOOL, crc16_ccitt_false, crc16_ccitt_update,
    pack_aex,
)
from modelo_loadx_aula8_r0_14 import _check_sector, loadx_two_pass_host

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "simulador-javafx/LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.json").read_text(encoding="utf-8"))
STATE = json.loads((ROOT / "ESTADO_PORTABLE.json").read_text(encoding="utf-8"))


class BrokenReader:
    def __init__(self, real: FileBlockImage, *, break_on_read: int, short: bool = False) -> None:
        self.real = real
        self.blocks = real.blocks
        self.break_on_read = break_on_read
        self.short = short
        self.reads = 0

    def read_block(self, number: int) -> bytes:
        self.reads += 1
        if self.reads == self.break_on_read:
            if self.short:
                return bytes(128)
            raise ImageIOError("ERROR_INYECTADO")
        return self.real.read_block(number)


class LoadXTests(unittest.TestCase):
    def setUp(self) -> None:
        holder = tempfile.TemporaryDirectory(prefix="aula_r014_")
        self.addCleanup(holder.cleanup)
        self.image = FileBlockImage.create(Path(holder.name) / "bloques.raw", 64)
        self.ram = b"\xA5" * 32768
        self.payload = bytes(range(256)) * 2
        self.blob = pack_aex(self.payload, kind=KIND_PRACTICE, origin=0x6000, entry=0x6002)
        self.place(2, self.blob)

    def place(self, first: int, blob: bytes) -> None:
        for offset in range(0, len(blob), 256):
            self.image.write_block(first + offset // 256, blob[offset:offset + 256])

    def modify_block(self, number: int, offset: int, data: int) -> None:
        block = bytearray(self.image.read_block(number))
        block[offset] = data
        self.image.write_block(number, bytes(block))

    def test_contract(self) -> None:
        self.assertEqual(SPEC["release"], "R0.14")
        self.assertEqual(SPEC["status"], "propuesta_no_aprobada")
        self.assertEqual(SPEC["staging_block_bytes"], 256)
        self.assertEqual(SPEC["first_pass"], "verify_entire_package_incremental_crc")
        self.assertEqual(SPEC["second_pass"], "copy_payload_incremental_crc")
        self.assertIs(SPEC["fully_atomic_ram_commit"], False)
        self.assertIs(SPEC["cpu_executed"], False)
        self.assertEqual(STATE["architecture"]["aula16"]["external_data_bus_bits"], 16)

    def test_crc_incremental_known_vector(self) -> None:
        self.assertEqual(crc16_ccitt_update(0xFFFF, b"1234"), 0x5349)
        rolling = crc16_ccitt_update(crc16_ccitt_update(0xFFFF, b"1234"), b"56789")
        self.assertEqual(rolling, 0x29B1)
        self.assertEqual(rolling, crc16_ccitt_false(b"123456789"))

    def test_simple_success(self) -> None:
        report = loadx_two_pass_host(self.image, 2, self.ram)
        self.assertEqual(report.status, "ready")
        self.assertTrue(report.eligible_for_supervised_execution)
        self.assertEqual(report.entry_if_ready, 0x6002)
        self.assertEqual(report.kind_if_ready, KIND_PRACTICE)
        self.assertEqual(report.bytes_copied, len(self.payload))
        self.assertEqual(report.verified_blocks, 3)

    def test_success_does_not_mutate_original_ram(self) -> None:
        report = loadx_two_pass_host(self.image, 2, self.ram)
        self.assertEqual(self.ram, bytes([0xA5]) * 32768)
        self.assertEqual(report.ram[0x6000:0x6200], self.payload)
        self.assertEqual(report.ram[:0x6000], self.ram[:0x6000])
        self.assertEqual(report.ram[0x6200:], self.ram[0x6200:])

    def test_header_never_copied(self) -> None:
        report = loadx_two_pass_host(self.image, 2, self.ram)
        self.assertEqual(report.ram[0x6000:0x6004], self.payload[:4])
        self.assertNotEqual(report.ram[0x6000:0x6004], b"AEX1")

    def test_staging_does_not_require_full_program(self) -> None:
        report = loadx_two_pass_host(self.image, 2, self.ram)
        self.assertEqual(report.max_temporary_block_bytes, 256)
        self.assertLess(report.max_temporary_block_bytes, 3584)

    def test_single_block_payload(self) -> None:
        blob = pack_aex(b"Z", kind=1, origin=0x6000, entry=0x6000)
        self.place(9, blob)
        report = loadx_two_pass_host(self.image, 9, self.ram)
        self.assertEqual((report.status, report.bytes_copied), ("ready", 1))

    def test_first_block_full_payload(self) -> None:
        blob = pack_aex(b"Z" * 224, kind=1, origin=0x6000, entry=0x6000)
        self.place(9, blob)
        report = loadx_two_pass_host(self.image, 9, self.ram)
        self.assertEqual((report.status, report.bytes_copied, report.verified_blocks), ("ready", 224, 1))

    def test_one_byte_over_first_block(self) -> None:
        blob = pack_aex(b"Z" * 225, kind=1, origin=0x6000, entry=0x6000)
        self.place(9, blob)
        report = loadx_two_pass_host(self.image, 9, self.ram)
        self.assertEqual((report.status, report.bytes_copied, report.verified_blocks), ("ready", 225, 2))

    def test_maximum_practice(self) -> None:
        blob = pack_aex(b"P" * 4064, kind=1, origin=0x6000, entry=0x6000)
        self.place(2, blob)
        report = loadx_two_pass_host(self.image, 2, self.ram)
        self.assertEqual((report.status, report.verified_blocks, report.bytes_copied), ("ready", 16, 4064))
        self.assertEqual(report.ram[0x6FDF], ord("P"))

    def test_maximum_tool(self) -> None:
        blob = pack_aex(b"T" * 8160, kind=KIND_TOOL, origin=0x1000, entry=0x1000)
        self.place(2, blob)
        report = loadx_two_pass_host(self.image, 2, self.ram)
        self.assertEqual((report.status, report.verified_blocks, report.bytes_copied), ("ready", 32, 8160))
        self.assertEqual(report.max_temporary_block_bytes, 256)
        self.assertEqual(report.entry_if_ready, 0x1000)
        self.assertEqual(report.ram[0x1000:0x1002], b"TT")
        self.assertEqual(report.ram[0x2FDF], ord("T"))
        self.assertEqual(report.ram[0x2FE0], 0xA5)

    def test_different_aligned_origin(self) -> None:
        blob = pack_aex(b"H" * 400, kind=1, origin=0x6D00, entry=0x6D05)
        self.place(10, blob)
        report = loadx_two_pass_host(self.image, 10, self.ram)
        self.assertEqual((report.status, report.entry_if_ready), ("ready", 0x6D05))
        self.assertEqual(report.ram[0x6D00:0x6E90], b"H" * 400)

    def test_first_block_invalid(self) -> None:
        report = loadx_two_pass_host(self.image, 0, self.ram)
        self.assertEqual(report.status, "preflight_error")
        self.assertFalse(report.eligible_for_supervised_execution)
        self.assertEqual(report.bytes_copied, 0)
        self.assertEqual(report.ram, self.ram)

    def test_header_cpu_corrupt_prevents_copy(self) -> None:
        self.modify_block(2, 5, 0x10)
        report = loadx_two_pass_host(self.image, 2, self.ram)
        self.assertEqual(report.status, "preflight_error")
        self.assertEqual(report.ram, self.ram)

    def test_missing_last_block_prevents_copy(self) -> None:
        self.place(63, self.blob[:256])
        report = loadx_two_pass_host(self.image, 63, self.ram)
        self.assertEqual(report.status, "preflight_error")
        self.assertEqual(report.bytes_copied, 0)

    def test_crc_bad_first_pass_prevents_copy(self) -> None:
        self.modify_block(3, 1, 7)
        report = loadx_two_pass_host(self.image, 2, self.ram)
        self.assertEqual(report.status, "preflight_error")
        self.assertIn("CRC_PAYLOAD_INVALIDO", report.reason)
        self.assertEqual(report.ram, self.ram)

    def test_nonzero_padding_prevents_copy(self) -> None:
        self.modify_block(4, 255, 7)
        report = loadx_two_pass_host(self.image, 2, self.ram)
        self.assertEqual(report.status, "preflight_error")
        self.assertIn("RELLENO_NO_CERO", report.reason)
        self.assertEqual(report.ram, self.ram)

    def test_change_header_between_passes(self) -> None:
        report = loadx_two_pass_host(self.image, 2, self.ram,
                                     between_passes=lambda: self.modify_block(2, 20, 1))
        self.assertEqual(report.status, "copy_error")
        self.assertIn("CABECERA_CAMBIO_ENTRE_LECTURAS", report.reason)
        self.assertEqual(report.bytes_copied, 0)
        self.assertIsNone(report.entry_if_ready)

    def test_change_payload_between_passes_blocks_execution(self) -> None:
        report = loadx_two_pass_host(self.image, 2, self.ram,
                                     between_passes=lambda: self.modify_block(3, 12, 0xEE))
        self.assertEqual(report.status, "copy_error")
        self.assertIn("CRC_PAYLOAD_INVALIDO", report.reason)
        self.assertGreater(report.bytes_copied, 0)
        self.assertIsNone(report.entry_if_ready)
        self.assertFalse(report.eligible_for_supervised_execution)
        self.assertNotEqual(report.ram, self.ram)

    def test_change_padding_between_passes_blocks_execution(self) -> None:
        report = loadx_two_pass_host(self.image, 2, self.ram,
                                     between_passes=lambda: self.modify_block(4, 255, 2))
        self.assertEqual(report.status, "copy_error")
        self.assertIn("RELLENO_NO_CERO", report.reason)
        self.assertGreater(report.bytes_copied, 0)
        self.assertFalse(report.eligible_for_supervised_execution)

    def test_second_pass_read_error_blocks_execution(self) -> None:
        reader = BrokenReader(self.image, break_on_read=7)  # 1 encabezado+3 preflight+3 pase2.
        report = loadx_two_pass_host(reader, 2, self.ram)
        self.assertEqual(report.status, "copy_error")
        self.assertIn("ERROR_INYECTADO", report.reason)
        self.assertGreater(report.bytes_copied, 0)
        self.assertFalse(report.eligible_for_supervised_execution)

    def test_first_pass_read_error_keeps_ram(self) -> None:
        reader = BrokenReader(self.image, break_on_read=3)
        report = loadx_two_pass_host(reader, 2, self.ram)
        self.assertEqual(report.status, "preflight_error")
        self.assertEqual(report.ram, self.ram)
        self.assertEqual(report.bytes_copied, 0)

    def test_short_sector_first_pass(self) -> None:
        reader = BrokenReader(self.image, break_on_read=3, short=True)
        report = loadx_two_pass_host(reader, 2, self.ram)
        self.assertEqual(report.status, "preflight_error")
        self.assertEqual(report.ram, self.ram)

    def test_short_sector_second_pass(self) -> None:
        reader = BrokenReader(self.image, break_on_read=6, short=True)
        report = loadx_two_pass_host(reader, 2, self.ram)
        self.assertEqual(report.status, "copy_error")
        self.assertFalse(report.eligible_for_supervised_execution)

    def test_invalid_ram_size(self) -> None:
        with self.assertRaisesRegex(AexError, "TAMANIO_RAM_INVALIDO"):
            loadx_two_pass_host(self.image, 2, bytes(100))

    def test_block_negative(self) -> None:
        with self.assertRaisesRegex(AexError, "BLOQUE_INICIAL_FUERA_DE_RANGO"):
            loadx_two_pass_host(self.image, -1, self.ram)

    def test_block_above_capacity(self) -> None:
        with self.assertRaisesRegex(AexError, "BLOQUE_INICIAL_FUERA_DE_RANGO"):
            loadx_two_pass_host(self.image, 64, self.ram)

    def test_mutated_data_never_automatically_runs(self) -> None:
        report = loadx_two_pass_host(self.image, 2, self.ram)
        self.assertTrue(report.eligible_for_supervised_execution)
        self.assertEqual(report.status, "ready")
        # Únicamente se entrega un PC candidato; jamás se invoca CPU.
        self.assertEqual(report.entry_if_ready, 0x6002)

    def test_check_sector_without_whole_image(self) -> None:
        self.assertEqual(_check_sector(self.blob[:256], 0, 3, 512), self.payload[:224])

    def test_check_sector_rejects_short_sector(self) -> None:
        with self.assertRaisesRegex(AexError, "SECTOR_INCOMPLETO"):
            _check_sector(bytes(2), 0, 1, 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
