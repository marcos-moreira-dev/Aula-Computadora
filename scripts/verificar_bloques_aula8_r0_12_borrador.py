#!/usr/bin/env python3
"""Pruebas documentales y del modelo anfitrión de bloques Aula-8 R0.12.

NO ejecutan firmware, bus Aula, controlador electrónico ni CPU.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from modelo_bloques_aula8_r0_12 import (
    BLOCK_SIZE, COMMAND, ERROR, REGISTER_MAP, STATUS,
    BlockController, FileBlockImage, plan_future_load,
)


ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.json").read_text(encoding="utf-8"))
ROM = json.loads((ROOT / "simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.json").read_text(encoding="utf-8"))
STATE = json.loads((ROOT / "ESTADO_PORTABLE.json").read_text(encoding="utf-8"))


class StorageContract(unittest.TestCase):
    def test_architecture_and_evidence(self) -> None:
        self.assertEqual(SPEC["release"], "R0.12")
        self.assertEqual(SPEC["status"], "propuesta_no_aprobada")
        self.assertEqual(SPEC["architecture"], "Aula-8")
        self.assertEqual(SPEC["aula8_external_data_bus_bits"], 8)
        self.assertEqual(SPEC["aula16_external_data_bus_bits"],
                         STATE["architecture"]["aula16"]["external_data_bus_bits"])
        self.assertEqual(SPEC["aula16_external_data_bus_bits"], 16)
        for field in ("controller_hardware_implemented", "cpu_executed",
                      "firmware_implemented", "native_loader_implemented",
                      "filesystem_implemented", "physical_power_loss_safe"):
            with self.subTest(field=field):
                self.assertIs(SPEC[field], False)
        self.assertIs(SPEC["host_reference_model_executed_in_tests"], True)

    def test_registers_and_terminal_do_not_overlap(self) -> None:
        mmio = SPEC["mmio"]
        self.assertEqual((mmio["start"], mmio["end"]), ("C010", "C01F"))
        self.assertEqual(mmio["register_width_bits"], 8)
        self.assertTrue(mmio["only_even_addresses"])
        self.assertEqual(mmio["terminal_data_address"], "C000")
        self.assertEqual(mmio["terminal_status_address"], "C002")
        entries = mmio["registers"]
        self.assertEqual(len(entries), 8)
        self.assertEqual({item["name"]: int(item["address"], 16) for item in entries}, REGISTER_MAP)
        self.assertEqual({item["access"] for item in entries},
                         {"write", "read", "read_write", "read_write_state_dependent"})
        for address in REGISTER_MAP.values():
            self.assertGreaterEqual(address, 0xC010)
            self.assertLessEqual(address, 0xC01F)
            self.assertEqual(address % 2, 0)
            self.assertNotIn(address, (0xC000, 0xC002))

    def test_opcode_error_and_state_constants(self) -> None:
        self.assertEqual({key: int(val, 16) for key, val in SPEC["commands"].items()}, COMMAND)
        self.assertEqual({key: int(val, 16) for key, val in SPEC["status_masks"].items()}, STATUS)
        self.assertEqual({key: int(val, 16) for key, val in SPEC["error_codes"].items()}, ERROR)
        self.assertEqual({key: int(val, 16) for key, val in SPEC["nominal_status"].items()},
                         {"idle": 0, "transfer": 3, "done": 4, "error": 8})
        self.assertEqual(SPEC["transfer"]["block_bytes"], BLOCK_SIZE)
        self.assertEqual(SPEC["transfer"]["count_at_completion_hex"], "0100")
        self.assertEqual(SPEC["transfer"]["maximum_addressable_blocks"], 65536)
        self.assertEqual(SPEC["transfer"]["block_number_endian"], "little")
        self.assertEqual(SPEC["transfer"]["count_endian"], "little")
        self.assertTrue(SPEC["transfer"]["incomplete_write_is_discarded"])

    def test_raw_format_and_rom_separation(self) -> None:
        image = SPEC["image"]
        self.assertEqual(image["format_candidate"], "raw_fixed_size_256B_blocks_no_header")
        self.assertEqual(image["suggested_demo_block_count"] * BLOCK_SIZE, 65536)
        self.assertEqual(image["demonstration_test_block_count"], 8)
        self.assertIs(image["real_hardware_power_loss_safety_tested"], False)
        self.assertIs(image["per_block_crc_defined"], False)
        self.assertIs(image["directory_defined"], False)
        self.assertIs(image["executable_header_defined"], False)
        rom_compat = SPEC["rom_compatibility"]
        self.assertEqual(rom_compat["public_slots_reserved"], ROM["rom"]["public_table"]["reserved_slot_count"])
        self.assertEqual(rom_compat["public_slots_defined_in_r011"], len(ROM["public_services"]))
        self.assertIs(rom_compat["block_services_slots_assigned"], False)
        self.assertEqual(rom_compat["firmware_rom_bytes"], 8192)
        self.assertIs(rom_compat["mmio_not_part_of_rom"], True)
        self.assertEqual(rom_compat["rom_vector"], "FFFC")
        self.assertIs(SPEC["future_load"]["implemented"], False)
        self.assertFalse(ROM["monitor_candidate"]["command_registry"][-1]["available_candidate"])


class ReferenceModel(unittest.TestCase):
    def setUp(self) -> None:
        self.folder = tempfile.TemporaryDirectory(prefix="aula_r012_test_")
        self.addCleanup(self.folder.cleanup)
        self.image_path = Path(self.folder.name) / "blocks.img"
        self.image = FileBlockImage.create(self.image_path, 8)
        self.controller = BlockController(self.image)

    def select_block(self, value: int) -> None:
        self.controller.write(REGISTER_MAP["BLOCK_LO"], value & 0xFF)
        self.controller.write(REGISTER_MAP["BLOCK_HI"], value >> 8)

    def begin(self, operation: str, number: int) -> None:
        self.select_block(number)
        self.controller.write(REGISTER_MAP["COMMAND"], COMMAND[operation])

    def test_image_creation_and_invalid_size(self) -> None:
        self.assertEqual(self.image_path.stat().st_size, 8 * BLOCK_SIZE)
        self.assertEqual(self.image.read_block(0), bytes(BLOCK_SIZE))
        with self.assertRaises(FileExistsError):
            FileBlockImage.create(self.image_path, 8)
        bad = Path(self.folder.name) / "bad.img"
        bad.write_bytes(b"not a whole block")
        with self.assertRaises(ValueError):
            FileBlockImage(bad)
        with self.assertRaises(ValueError):
            FileBlockImage.create(Path(self.folder.name) / "empty.img", 0)

    def test_read_256_bytes_count_and_done(self) -> None:
        sample = bytes(range(256))
        self.image.write_block(2, sample)
        self.begin("READ", 2)
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), 0x03)
        got = bytes(self.controller.read(REGISTER_MAP["DATA"]) for _ in range(255))
        self.assertEqual(got, sample[:255])
        self.assertEqual(self.controller.read(REGISTER_MAP["COUNT_LO"]), 0xFF)
        self.assertEqual(self.controller.read(REGISTER_MAP["COUNT_HI"]), 0)
        got += bytes([self.controller.read(REGISTER_MAP["DATA"])])
        self.assertEqual(got, sample)
        self.assertEqual(self.controller.read(REGISTER_MAP["COUNT_LO"]), 0)
        self.assertEqual(self.controller.read(REGISTER_MAP["COUNT_HI"]), 1)
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), 0x04)
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), 0)
        self.assertEqual(FileBlockImage(self.image_path).read_block(2), sample)

    def test_read_after_done_is_error_not_replay(self) -> None:
        self.begin("READ", 0)
        for _ in range(256):
            self.controller.read(REGISTER_MAP["DATA"])
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["DONE"])
        self.controller.read(REGISTER_MAP["DATA"])
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["ERROR"])
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["DATA_DIRECTION_OR_STATE"])

    def test_write_then_close_and_reopen(self) -> None:
        self.begin("WRITE", 3)
        sample = bytes((i * 7 + 3) % 256 for i in range(256))
        for value in sample[:-1]:
            self.controller.write(REGISTER_MAP["DATA"], value)
        self.assertEqual(self.image.read_block(3), bytes(256))
        self.assertEqual(self.controller.read(REGISTER_MAP["COUNT_LO"]), 255)
        self.controller.write(REGISTER_MAP["DATA"], sample[-1])
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["DONE"])
        self.assertEqual(self.controller.read(REGISTER_MAP["COUNT_HI"]), 1)
        # La segunda instancia fuerza una lectura del archivo persistido.
        reopened = FileBlockImage(self.image_path)
        self.assertEqual(reopened.read_block(3), sample)
        self.assertEqual(reopened.read_block(4), bytes(256))

    def test_reset_after_255_bytes_discards_write(self) -> None:
        old = bytes([0x5A] * 256)
        self.image.write_block(1, old)
        self.begin("WRITE", 1)
        for i in range(255):
            self.controller.write(REGISTER_MAP["DATA"], i)
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), 3)
        self.controller.write(REGISTER_MAP["COMMAND"], COMMAND["RESET"])
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), 0)
        self.assertEqual(self.controller.read(REGISTER_MAP["COUNT_LO"]), 0)
        self.assertEqual(FileBlockImage(self.image_path).read_block(1), old)

    def test_reconfigure_busy_aborts_without_disk_change(self) -> None:
        self.begin("WRITE", 2)
        for i in range(200):
            self.controller.write(REGISTER_MAP["DATA"], i)
        self.controller.write(REGISTER_MAP["BLOCK_HI"], 1)
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["ERROR"])
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["BUSY_RECONFIGURED"])
        self.assertEqual(self.controller.read(REGISTER_MAP["COUNT_LO"]), 200)
        self.assertEqual(self.image.read_block(2), bytes(256))

    def test_new_command_busy_aborts(self) -> None:
        self.begin("READ", 0)
        self.controller.write(REGISTER_MAP["COMMAND"], COMMAND["WRITE"])
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["BUSY_RECONFIGURED"])
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["ERROR"])
        self.begin("READ", 0)
        self.controller.write(REGISTER_MAP["COMMAND"], COMMAND["NOP"])
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["BUSY_RECONFIGURED"])
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["ERROR"])

    def test_invalid_command_and_recovery(self) -> None:
        self.controller.write(REGISTER_MAP["COMMAND"], 0x7F)
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["BAD_COMMAND"])
        self.begin("READ", 0)
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["NONE"])
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), 0x03)
        self.controller.write(REGISTER_MAP["COMMAND"], COMMAND["RESET"])
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), 0)

    def test_out_of_range_sector_detected(self) -> None:
        self.begin("READ", 8)
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), 0x08)
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["BLOCK_OUT_OF_RANGE"])
        self.begin("WRITE", 0x0102)
        self.assertEqual(self.controller.read(REGISTER_MAP["BLOCK_LO"]), 2)
        self.assertEqual(self.controller.read(REGISTER_MAP["BLOCK_HI"]), 1)
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["BLOCK_OUT_OF_RANGE"])
        self.assertEqual(self.image_path.stat().st_size, 2048)

    def test_wrong_data_direction_and_odd_register(self) -> None:
        self.begin("WRITE", 0)
        self.controller.read(REGISTER_MAP["DATA"])
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["DATA_DIRECTION_OR_STATE"])
        self.begin("READ", 0)
        self.controller.write(REGISTER_MAP["DATA"], 0x41)
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["DATA_DIRECTION_OR_STATE"])
        self.controller.write(0xC011, 0x22)
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["ERROR"])
        self.assertEqual(self.image.read_block(0), bytes(256))

    def test_injected_image_failure_keeps_old_content(self) -> None:
        original = bytes([0xCA] * 256)
        self.image.write_block(5, original)
        self.image.inject_failure_before_replace = True
        self.begin("WRITE", 5)
        for index in range(256):
            self.controller.write(REGISTER_MAP["DATA"], index)
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["ERROR"])
        self.assertEqual(self.controller.read(REGISTER_MAP["ERROR"]), ERROR["IMAGE_IO_FAILURE"])
        self.assertEqual(FileBlockImage(self.image_path).read_block(5), original)
        self.image.inject_failure_before_replace = False
        self.begin("WRITE", 5)
        for index in range(256):
            self.controller.write(REGISTER_MAP["DATA"], index)
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["DONE"])
        self.assertEqual(FileBlockImage(self.image_path).read_block(5), bytes(range(256)))

    def test_extra_write_after_done_is_error(self) -> None:
        self.begin("WRITE", 0)
        for i in range(256):
            self.controller.write(REGISTER_MAP["DATA"], i)
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["DONE"])
        self.controller.write(REGISTER_MAP["DATA"], 0x99)
        self.assertEqual(self.controller.read(REGISTER_MAP["STATUS"]), STATUS["ERROR"])
        self.assertEqual(FileBlockImage(self.image_path).read_block(0), bytes(range(256)))


class FutureLoad(unittest.TestCase):
    def test_overlay_and_program_plan(self) -> None:
        proposed = SPEC["future_load"]
        self.assertFalse(proposed["implemented"])
        self.assertEqual(proposed["ram_destination_alignment_bytes"], 256)
        self.assertEqual(proposed["existing_r011_run_window"], ["6000", "6FFF"])
        self.assertTrue(proposed["staging_one_complete_block_before_destination_copy"])
        self.assertFalse(proposed["whole_multi_block_load_atomic"])
        self.assertFalse(proposed["execute_on_partial_error"])
        self.assertFalse(proposed["named_files_supported"])
        self.assertFalse(proposed["cpu_binary_target_identification_supported"])
        self.assertTrue(proposed["overlay_requires_future_supervised_entry"])
        self.assertEqual(plan_future_load("LOAD 0002 1000 02", 8, proposed),
                         [(2, 0x1000), (3, 0x1100)])
        self.assertEqual(plan_future_load("load 0001 6000 01", 8, proposed),
                         [(1, 0x6000)])

    def test_boundaries_for_overlay_and_program(self) -> None:
        proposed = SPEC["future_load"]
        self.assertEqual(len(plan_future_load("LOAD 0000 1000 20", 32, proposed)), 32)
        self.assertEqual(len(plan_future_load("LOAD 0000 6000 10", 16, proposed)), 16)
        self.assertEqual(plan_future_load("LOAD 0000 2F00 01", 2, proposed), [(0, 0x2F00)])
        self.assertEqual(plan_future_load("LOAD 0000 6F00 01", 2, proposed), [(0, 0x6F00)])
        self.assertEqual(plan_future_load("LOAD FFFF 6000 01", 65536, proposed),
                         [(65535, 0x6000)])

    def test_rejection_cases(self) -> None:
        proposed = SPEC["future_load"]
        probes = {
            "LOAD 0000 1000 00": "LOAD_CANTIDAD",
            "LOAD 0000 1000 21": "LOAD_CANTIDAD",
            "LOAD 0000 1001 01": "LOAD_ALINEACION",
            "LOAD 0000 0F00 01": "LOAD_DESTINO",
            "LOAD 0000 3000 01": "LOAD_DESTINO",
            "LOAD 0000 5000 01": "LOAD_DESTINO",
            "LOAD 0000 7000 01": "LOAD_DESTINO",
            "LOAD 0000 C000 01": "LOAD_DESTINO",
            "LOAD 0000 E000 01": "LOAD_DESTINO",
            "LOAD 0000 2F00 02": "LOAD_DESTINO",
            "LOAD 0000 6F00 02": "LOAD_DESTINO",
            "LOAD 0007 6000 02": "LOAD_BLOQUE_FUERA",
            "LOAD FFFF 6000 02": "LOAD_BLOQUE_FUERA",
            "LOAD 0000 6000 ZZ": "LOAD_FORMATO",
            "LOAD 0 6000 01": "LOAD_FORMATO",
            "LOAD 0000 6000": "LOAD_FORMATO",
            "POKE 0000 6000 01": "LOAD_FORMATO",
        }
        for text, expected in probes.items():
            with self.subTest(command=text):
                with self.assertRaisesRegex(ValueError, expected):
                    plan_future_load(text, 8, proposed)

    def test_example_program_is_from_r011(self) -> None:
        sample = SPEC["acceptance_sample"]
        self.assertEqual(sample["source_block"], "0001")
        self.assertEqual(sample["destination"], "6000")
        self.assertEqual(sample["count_blocks"], 1)
        self.assertEqual(sample["initial_code_hex"], ROM["reference_program"]["bytes_hex"])
        self.assertEqual(len(bytes.fromhex(sample["initial_code_hex"])) + sample["trailing_bytes"], 256)
        self.assertEqual(sample["expected_program_output_if_cpu_and_rom_exist"], "A")
        self.assertIs(sample["executable_tested_on_aula_cpu"], False)


def main() -> int:
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for group in (StorageContract, ReferenceModel, FutureLoad):
        suite.addTests(loader.loadTestsFromTestCase(group))
    report = unittest.TextTestRunner(verbosity=1).run(suite)
    if not report.wasSuccessful():
        return 1
    print(f"R0.12: {report.testsRun} pruebas de contrato/modelo anfitrión correctas.")
    print("Persistencia comprobada solo en archivo temporal de referencia; NO CPU ni controlador Aula.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
