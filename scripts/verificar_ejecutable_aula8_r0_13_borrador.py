#!/usr/bin/env python3
"""Pruebas del formato candidato AEX1. Todo corre en el HOST; cero CPU Aula."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from modelo_bloques_aula8_r0_12 import BLOCK_SIZE, FileBlockImage
from modelo_ejecutable_aula8_r0_13 import (
    AexError, HEADER_SIZE, KIND_PRACTICE, KIND_TOOL, MAGIC, TARGET_AULA8, VERSION,
    crc16_ccitt_false, decode_aex, pack_aex, preview_load_ram, stage_from_block_image,
)

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "simulador-javafx/EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.json").read_text(encoding="utf-8"))
STATE = json.loads((ROOT / "ESTADO_PORTABLE.json").read_text(encoding="utf-8"))
TOOL = ROOT / "scripts/empaquetar_aex_aula8_r0_13.py"


def patch_header(blob: bytes, *, offset: int, data: bytes, checksum: bool = True) -> bytes:
    mutable = bytearray(blob)
    mutable[offset:offset + len(data)] = data
    if checksum:
        mutable[18:20] = crc16_ccitt_false(mutable[:18]).to_bytes(2, "little")
    return bytes(mutable)


class Contract(unittest.TestCase):
    def test_file_signature_and_version(self) -> None:
        aex = pack_aex(b"\x00", kind=KIND_PRACTICE, origin=0x6000, entry=0x6000)
        self.assertEqual(aex[:4], MAGIC)
        self.assertEqual(aex[4:6], bytes([VERSION, TARGET_AULA8]))
        self.assertEqual((aex[6], aex[7]), (KIND_PRACTICE, 0))
        self.assertEqual(aex[8:18], bytes.fromhex("006000600100F0E10100"))
        self.assertEqual(aex[20:HEADER_SIZE], bytes(12))
        self.assertEqual(len(aex), 256)

    def test_crc_known_reference(self) -> None:
        self.assertEqual(crc16_ccitt_false(b"123456789"), 0x29B1)

    def test_structural_spec(self) -> None:
        self.assertEqual(SPEC["release"], "R0.13")
        self.assertEqual(SPEC["status"], "propuesta_no_aprobada")
        self.assertEqual(SPEC["format"]["magic"], "AEX1")
        self.assertEqual(SPEC["format"]["header_bytes"], 32)
        self.assertEqual(SPEC["format"]["sector_bytes"], BLOCK_SIZE)
        self.assertEqual(SPEC["format"]["target_cpu_code"], 8)
        self.assertEqual(SPEC["format"]["maximum_blocks"], 32)
        self.assertEqual(SPEC["format"]["crc_variant"], "CRC-16/CCITT-FALSE")
        self.assertEqual(SPEC["format"]["header_crc_scope"], "bytes_00_to_11_hex_inclusive")
        self.assertEqual(SPEC["kind_to_window"], {"01": ["6000", "6FFF"], "02": ["1000", "2FFF"]})
        self.assertIs(SPEC["host_reference_tests_only"], True)
        for key in ("cpu_executed", "native_loader_implemented",
                    "firmware_implemented", "assembler_implemented", "filesystem_implemented"):
            self.assertIs(SPEC[key], False)
        self.assertEqual(STATE["architecture"]["aula16"]["external_data_bus_bits"], 16)

    def test_first_sector_layout_all_offsets(self) -> None:
        payload = bytes.fromhex("11 00 2A 02")
        blob = pack_aex(payload, kind=KIND_PRACTICE, origin=0x6000, entry=0x6002)
        self.assertEqual(blob[8:10], b"\x00\x60")
        self.assertEqual(blob[10:12], b"\x02\x60")
        self.assertEqual(blob[12:14], b"\x04\x00")
        self.assertEqual(blob[14:16], crc16_ccitt_false(payload).to_bytes(2, "little"))
        self.assertEqual(blob[16:18], b"\x01\x00")
        self.assertEqual(blob[18:20], crc16_ccitt_false(blob[:18]).to_bytes(2, "little"))
        self.assertEqual(blob[32:36], payload)
        self.assertEqual(blob[36:], bytes(220))


class ContainerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.code = bytes(range(256)) * 2
        self.blob = pack_aex(self.code, kind=KIND_PRACTICE, origin=0x6000, entry=0x6002)

    def assert_bad(self, blob: bytes, expected: str) -> None:
        with self.assertRaisesRegex(AexError, expected):
            decode_aex(blob)

    def test_round_trip(self) -> None:
        obj = decode_aex(self.blob)
        self.assertEqual(obj.payload, self.code)
        self.assertEqual((obj.origin, obj.entry, obj.total_blocks), (0x6000, 0x6002, 3))

    def test_tool_overlay(self) -> None:
        code = b"\x11" * 8160
        obj = decode_aex(pack_aex(code, kind=KIND_TOOL, origin=0x1000, entry=0x1000))
        self.assertEqual(obj.total_blocks, 32)
        self.assertEqual(len(obj.payload), 8160)
        self.assertEqual(obj.origin, 0x1000)

    def test_practice_maximum_payload(self) -> None:
        obj = decode_aex(pack_aex(b"R" * 4064, kind=KIND_PRACTICE, origin=0x6000, entry=0x6000))
        self.assertEqual(obj.total_blocks, 16)

    def test_payload_first_block_limit(self) -> None:
        self.assertEqual(len(pack_aex(b"x" * 224, kind=1, origin=0x6000, entry=0x6000)), 256)
        self.assertEqual(len(pack_aex(b"x" * 225, kind=1, origin=0x6000, entry=0x6000)), 512)

    def test_bad_type(self) -> None:
        with self.assertRaisesRegex(AexError, "TIPO_INVALIDO"):
            pack_aex(b"x", kind=3, origin=0x6000, entry=0x6000)

    def test_not_bytes(self) -> None:
        with self.assertRaisesRegex(AexError, "PAYLOAD_NO_BYTES"):
            pack_aex(bytearray(b"x"), kind=1, origin=0x6000, entry=0x6000)

    def test_empty_payload(self) -> None:
        with self.assertRaisesRegex(AexError, "LONGITUD_INVALIDA"):
            pack_aex(b"", kind=1, origin=0x6000, entry=0x6000)

    def test_excessive_payload(self) -> None:
        with self.assertRaisesRegex(AexError, "FUERA_DE_VENTANA_RAM"):
            pack_aex(b"x" * 4097, kind=1, origin=0x6000, entry=0x6000)

    def test_payload_fits_ram_but_not_sector_budget(self) -> None:
        with self.assertRaisesRegex(AexError, "DEMASIADOS_BLOQUES_PARA_TIPO"):
            pack_aex(b"x" * 4096, kind=1, origin=0x6000, entry=0x6000)

    def test_unaligned_origin(self) -> None:
        with self.assertRaisesRegex(AexError, "ORIGEN_NO_ALINEADO"):
            pack_aex(b"x", kind=1, origin=0x6001, entry=0x6001)

    def test_wrong_kind_for_window(self) -> None:
        with self.assertRaisesRegex(AexError, "FUERA_DE_VENTANA_RAM"):
            pack_aex(b"x", kind=2, origin=0x6000, entry=0x6000)

    def test_crosses_window(self) -> None:
        with self.assertRaisesRegex(AexError, "FUERA_DE_VENTANA_RAM"):
            pack_aex(b"x" * 257, kind=1, origin=0x6F00, entry=0x6F00)

    def test_entry_before_payload(self) -> None:
        with self.assertRaisesRegex(AexError, "ENTRADA_FUERA_DE_CODIGO"):
            pack_aex(b"x", kind=1, origin=0x6000, entry=0x5FFF)

    def test_entry_at_end_exclusive(self) -> None:
        with self.assertRaisesRegex(AexError, "ENTRADA_FUERA_DE_CODIGO"):
            pack_aex(b"x", kind=1, origin=0x6000, entry=0x6001)

    def test_corrupt_magic(self) -> None:
        self.assert_bad(patch_header(self.blob, offset=0, data=b"BAD!"), "FIRMA_INVALIDA")

    def test_corrupt_version(self) -> None:
        self.assert_bad(patch_header(self.blob, offset=4, data=b"\x02"), "VERSION_NO_SOPORTADA")

    def test_wrong_cpu_even_with_valid_header_crc(self) -> None:
        self.assert_bad(patch_header(self.blob, offset=5, data=b"\x10"), "CPU_INCORRECTA")

    def test_crc_header_failure(self) -> None:
        self.assert_bad(patch_header(self.blob, offset=8, data=b"\x01", checksum=False), "CRC_CABECERA_INVALIDO")

    def test_crc_payload_failure(self) -> None:
        data = bytearray(self.blob)
        data[HEADER_SIZE] ^= 0x10
        self.assert_bad(bytes(data), "CRC_PAYLOAD_INVALIDO")

    def test_reserved_flag(self) -> None:
        self.assert_bad(patch_header(self.blob, offset=7, data=b"\x01"), "CAMPOS_RESERVADOS_NO_CERO")

    def test_reserved_area(self) -> None:
        self.assert_bad(patch_header(self.blob, offset=20, data=b"\x01"), "CAMPOS_RESERVADOS_NO_CERO")

    def test_bad_sector_count(self) -> None:
        self.assert_bad(patch_header(self.blob, offset=16, data=b"\x02\x00"), "CONTEO_DE_BLOQUES_INVALIDO")

    def test_bad_endianness_origin(self) -> None:
        self.assert_bad(patch_header(self.blob, offset=8, data=b"\x60\x00"), "ORIGEN_NO_ALINEADO")

    def test_bad_truncated(self) -> None:
        self.assert_bad(self.blob[:-BLOCK_SIZE], "CONTENEDOR_TRUNCADO_O_EXTRA")

    def test_non_sector_length(self) -> None:
        self.assert_bad(self.blob[:-1], "LONGITUD_DE_CONTENEDOR_INVALIDA")

    def test_trailing_extra_sector(self) -> None:
        self.assert_bad(self.blob + bytes(BLOCK_SIZE), "CONTENEDOR_TRUNCADO_O_EXTRA")

    def test_nonzero_padding(self) -> None:
        data = bytearray(self.blob)
        data[-1] = 1
        self.assert_bad(bytes(data), "RELLENO_NO_CERO")

    def test_wrong_cpu_explicit_expectation(self) -> None:
        with self.assertRaisesRegex(AexError, "CPU_INCORRECTA"):
            decode_aex(self.blob, expected_target=16)


class HostReference(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="aula_r013_")
        self.addCleanup(tmp.cleanup)
        self.folder = Path(tmp.name)
        self.image = FileBlockImage.create(self.folder / "device.raw", 32)
        self.payload = bytes(range(64)) * 6
        self.blob = pack_aex(self.payload, kind=KIND_PRACTICE, origin=0x6000, entry=0x6000)

    def install_for_test(self, first: int, blob: bytes) -> None:
        for offset in range(0, len(blob), BLOCK_SIZE):
            self.image.write_block(first + offset // BLOCK_SIZE, blob[offset:offset + BLOCK_SIZE])

    def test_round_trip_from_block_image(self) -> None:
        self.install_for_test(2, self.blob)
        read = stage_from_block_image(FileBlockImage(self.image.path), 2)
        self.assertEqual(read.payload, self.payload)
        self.assertEqual(read.total_blocks, 2)

    def test_crossing_source_image_boundary(self) -> None:
        self.install_for_test(31, self.blob[:BLOCK_SIZE])
        with self.assertRaisesRegex(AexError, "IMAGEN_SIN_BLOQUES_SUFICIENTES"):
            stage_from_block_image(self.image, 31)

    def test_invalid_start_sector(self) -> None:
        with self.assertRaisesRegex(AexError, "BLOQUE_INICIAL_FUERA_DE_RANGO"):
            stage_from_block_image(self.image, 32)

    def test_wrong_raw_image(self) -> None:
        with self.assertRaisesRegex(AexError, "FIRMA_INVALIDA"):
            stage_from_block_image(self.image, 0)

    def test_source_corruption_prevents_any_ram_write(self) -> None:
        self.install_for_test(3, self.blob)
        sector = bytearray(self.image.read_block(4))
        sector[0] ^= 1
        self.image.write_block(4, bytes(sector))
        ram = b"\xAA" * 32768
        with self.assertRaisesRegex(AexError, "CRC_PAYLOAD_INVALIDO"):
            staged = stage_from_block_image(self.image, 3)
            ram = preview_load_ram(ram, staged)
        self.assertEqual(ram, b"\xAA" * 32768)

    def test_preview_copies_only_payload(self) -> None:
        self.install_for_test(3, self.blob)
        staged = stage_from_block_image(self.image, 3)
        original = b"\xA5" * 32768
        loaded = preview_load_ram(original, staged)
        self.assertEqual(original, b"\xA5" * 32768)
        self.assertEqual(loaded[0x6000:0x6000 + len(self.payload)], self.payload)
        self.assertEqual(loaded[:0x6000], original[:0x6000])
        self.assertEqual(loaded[0x6000 + len(self.payload):], original[0x6000 + len(self.payload):])
        self.assertEqual(loaded[0x5FFF], 0xA5)

    def test_preview_rejects_wrong_ram_size(self) -> None:
        with self.assertRaisesRegex(AexError, "TAMANIO_RAM_INVALIDO"):
            preview_load_ram(bytes(100), decode_aex(self.blob))

    def test_preview_revalidates_staged_checksum(self) -> None:
        staged = decode_aex(self.blob)
        tampered = replace(staged, payload=bytes([staged.payload[0] ^ 1]) + staged.payload[1:])
        with self.assertRaisesRegex(AexError, "CRC_PAYLOAD_INVALIDO"):
            preview_load_ram(bytes(32768), tampered)

    def test_cli_create_inspect_and_no_overwrite(self) -> None:
        source = self.folder / "programa.bin"
        output = self.folder / "programa.aex"
        source.write_bytes(b"\x11\x00\x2a\x02")
        cmd = [sys.executable, str(TOOL), "crear", "--bin", str(source), "--out", str(output),
               "--origen", "6000", "--entrada", "6000", "--tipo", "practica"]
        first = subprocess.run(cmd, text=True, capture_output=True, check=False)
        self.assertEqual(first.returncode, 0, first.stderr)
        inspect = subprocess.run([sys.executable, str(TOOL), "inspeccionar", "--archivo", str(output)],
                                 text=True, capture_output=True, check=False)
        self.assertEqual(inspect.returncode, 0, inspect.stderr)
        self.assertIn("AEX1 válido", inspect.stdout)
        before = output.read_bytes()
        second = subprocess.run(cmd, text=True, capture_output=True, check=False)
        self.assertEqual(second.returncode, 2)
        self.assertEqual(before, output.read_bytes())

    def test_cli_invalid_input_does_not_create_output(self) -> None:
        source = self.folder / "programa.bin"
        output = self.folder / "programa.aex"
        source.write_bytes(b"X")
        failed = subprocess.run(
            [sys.executable, str(TOOL), "crear", "--bin", str(source), "--out", str(output),
             "--origen", "6001", "--entrada", "6001", "--tipo", "practica"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(failed.returncode, 2)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main(verbosity=1)
