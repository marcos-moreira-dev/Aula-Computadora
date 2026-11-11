#!/usr/bin/env python3
"""Contrasta ROM, tabla, RESET, monitor y retornos propuestos en R0.11.

No ejecuta una CPU ni genera una imagen de EEPROM lista para usar.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.json"
ISA = ROOT / "simulador-javafx/ISA_AULA8_CANDIDATA.json"
STATE = ROOT / "ESTADO_PORTABLE.json"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def value(text: str) -> int:
    return int(text, 16)


def parse_hex(token: str, min_digits: int, max_digits: int) -> int:
    if not min_digits <= len(token) <= max_digits or re.fullmatch(r"[0-9a-fA-F]+", token, flags=re.ASCII) is None:
        raise ValueError("HEX_INVALIDO")
    return int(token, 16)


def read_allowed(first: int, count: int, regions: list[tuple[int, int]]) -> bool:
    last = first + count - 1
    return any(lo <= first <= last <= hi for lo, hi in regions)


def parse_monitor(line: str, spec: dict) -> tuple[str, dict]:
    """Planifica una orden: NO toca memoria ni invoca rutinas CPU."""
    try:
        words = line.strip().split()
        if not words:
            return "ERROR", {"error": "COMANDO_DESCONOCIDO"}
        command = words[0].upper()
        registry = {item["name"]: item for item in spec["command_registry"]}
        if command not in registry:
            return "ERROR", {"error": "COMANDO_DESCONOCIDO"}

        if command in ("REG", "LOAD"):
            if len(words) != 1:
                return "ERROR", {"error": "ARGUMENTOS"}
            return "NO_DISPONIBLE", {"command": command}
        if command == "HELP":
            if len(words) != 1:
                return "ERROR", {"error": "ARGUMENTOS"}
            return "HELP", {}
        if command == "MEM":
            if len(words) not in (2, 3):
                return "ERROR", {"error": "ARGUMENTOS"}
            start = parse_hex(words[1], 4, 4)
            count = (parse_hex(words[2], 1, 4) if len(words) == 3
                     else value(spec["mem_default_count_hex"]))
            if count < 1 or count > value(spec["mem_max_count_hex"]):
                return "ERROR", {"error": "MEM_LONGITUD_INVALIDA"}
            if start + count > 0x10000:
                return "ERROR", {"error": "MEM_DESBORDE"}
            regions = [(value(lo), value(hi)) for lo, hi in spec["mem_read_regions"]]
            if not read_allowed(start, count, regions):
                return "ERROR", {"error": "MEM_REGION_NO_LEGIBLE"}
            return "MEM", {"address": start, "count": count}
        if command == "POKE":
            if len(words) != 3:
                return "ERROR", {"error": "ARGUMENTOS"}
            address = parse_hex(words[1], 4, 4)
            byte = parse_hex(words[2], 2, 2)
            low, high = map(value, spec["poke_window"])
            if not low <= address <= high:
                return "ERROR", {"error": "POKE_FUERA_DE_VENTANA"}
            return "POKE", {"address": address, "byte": byte}
        if command == "RUN":
            if len(words) != 2:
                return "ERROR", {"error": "ARGUMENTOS"}
            address = parse_hex(words[1], 4, 4)
            low, high = map(value, spec["run_window"])
            if not low <= address <= high:
                return "ERROR", {"error": "RUN_FUERA_DE_VENTANA"}
            return "RUN", {"address": address, "mode": spec["run_uses"]}

        return "ERROR", {"error": "COMANDO_DESCONOCIDO"}
    except ValueError as exc:
        return "ERROR", {"error": str(exc)}


def check_rom(spec: dict, isa: dict, state: dict) -> int:
    rom = spec["rom"]
    base, end = value(rom["start"]), value(rom["end"])
    check(base == 0xE000 and end == 0xFFFF, "La ROM debe estar en E000-FFFF")
    check(end - base + 1 == rom["capacity_bytes"] == 8192, "Capacidad ROM incorrecta")
    check(rom["control_rom_is_distinct"], "No confundir µROM con firmware")
    check(not rom["firmware_binary_size_measured"], "Sin mapa de enlace no se mide tamaño")
    budget = rom["firmware_budget_sections_bytes"]
    check(budget == state["software_memory_budget_proposal"]["firmware_rom_budget_sections_bytes"], "Divergencia del presupuesto")
    check(sum(budget) == 8192, "El presupuesto de ROM debe sumar 8192 bytes")

    table = rom["public_table"]
    start, stop, slot = value(table["start"]), value(table["end"]), table["slot_size_bytes"]
    check(start == 0xFF00 and stop == 0xFF7F, "Tabla pública fuera de lugar")
    check(start >= base and stop <= end, "Tabla fuera de ROM")
    check(slot == 4 and table["reserved_slot_count"] == 32, "Ranuras incompatibles")
    check(stop - start + 1 == slot * table["reserved_slot_count"] == 128, "Reservas incorrectas")
    check(table["defined_slot_count"] == 4 and not table["future_slots_callable"], "Slots públicos no asignados")

    vector = rom["reset_vector"]
    lo_addr, hi_addr = value(vector["address_low"]), value(vector["address_high"])
    check((lo_addr, hi_addr) == (0xFFFC, 0xFFFD), "RESET debe ocupar FFFC-FFFD")
    check(stop < lo_addr and value(rom["reserved_tail"][0]) == 0xFFFE and value(rom["reserved_tail"][1]) == 0xFFFF,
          "Tabla y vector deben permanecer separados")
    check(vector["endian"] == "little", "RESET debe leerse little endian")
    check(len(rom["public_table"]) > 0, "Tabla sin datos")

    opcodes = {entry["mnemonic"]: int(entry["opcode"], 16) for entry in isa["instructions"]}
    check(opcodes["JMP"] == 0x30 and opcodes["NOP"] == 0x00 and opcodes["CALL"] == 0x35
          and opcodes["RET"] == 0x02 and opcodes["HALT"] == 0x01, "La ISA candidata cambió")
    check(isa["formats"]["imm16"]["bytes"] == 3, "JMP debe tener tres bytes")

    # Imagen temporal con 0xFF como relleno de prueba: NO representa firmware funcional.
    fixture = bytearray([0xFF] * (end - base + 1))
    defined = spec["public_services"]
    check([item["name"] for item in defined] == ["FW_PUTC", "FW_GETC", "FW_PUTS", "FW_STATUS"],
          "Orden de los cuatro servicios públicos cambiado")
    for index, item in enumerate(defined):
        address = value(item["slot"])
        target = value(item["illustrative_target"])
        raw = bytes.fromhex(item["illustrative_slot_bytes_hex"])
        check(address == start + index * slot, f"Ranura {item['name']} desplazada")
        check(base <= target < start, f"Destino ilustrativo de {item['name']} no cabe en zona de código ROM")
        check(len(raw) == slot and raw[0] == opcodes["JMP"] and raw[3] == opcodes["NOP"],
              f"{item['name']} no codifica JMP+NOP")
        check((raw[2] << 8) | raw[1] == target, "Dirección little endian del salto inválida")
        fixture[address - base:address - base + slot] = raw

    vector_bytes = bytes.fromhex(vector["illustrative_bytes_hex"])
    check(len(vector_bytes) == 2, "RESET ocupa dos bytes")
    fixture[lo_addr - base:hi_addr - base + 1] = vector_bytes
    boot = fixture[lo_addr - base] | (fixture[hi_addr - base] << 8)
    check(boot == value(vector["illustrative_boot_address"]) == base, "Vector RESET no apunta al arranque ilustrativo")
    check(all(b == 0xFF for b in fixture[stop - base + 1:lo_addr - base]),
          "La tabla no debe invadir la zona posterior")
    check(budget[0] - slot * table["reserved_slot_count"] - len(vector_bytes) == 382,
          "Margen del rubro de vector/tabla mal calculado")
    return len(defined)


def check_abi_and_return(spec: dict, isa: dict) -> int:
    abi = spec["firmware_abi_candidate"]
    check(abi["entry_mechanism"] == "CALL_to_public_slot", "Entrada ROM debe usar CALL")
    check(abi["slot_mechanism"] == "JMP_to_firmware_impl", "Slot ROM debe usar JMP")
    check(abi["exit_mechanism"] == "RET" and abi["stack_balanced"], "Rutina ROM debe regresar y equilibrar pila")
    check(abi["callee_saved_registers"] == ["R2", "R3", "X"], "Registros callee-saved divergentes")
    check(abi["caller_clobbered_registers"] == ["R0", "R1"], "R0/R1 deben ser volátiles")
    check(abi["caller_clobbered_flags"] == ["Z", "N", "C", "V"], "Flags ROM deben ser volátiles")
    check(not abi["requires_minic_stack_argument_slots"] and not abi["requires_minic_fixed_frame_prologue"],
          "La ABI ROM es distinta de la ABI MiniC")

    reference = spec["reference_program"]
    raw = bytes.fromhex(reference["bytes_hex"])
    check(value(reference["origin"]) == 0x6000, "El ejemplo debe estar en RAM de práctica")
    check(raw == bytes.fromhex("11 00 41 35 00 FF 02"), "Programa de muestra alterado")
    opcodes = {entry["mnemonic"]: int(entry["opcode"], 16) for entry in isa["instructions"]}
    offset = 0
    for ins in reference["instructions"]:
        check(value(ins["address"]) == 0x6000 + offset, "Dirección de instrucción errónea")
        check(raw[offset] == opcodes[ins["mnemonic"]], "Opcode de muestra no coincide con ISA")
        offset += ins["length"]
    check(offset == len(raw) == 7, "El programa debe medir siete bytes")
    check((raw[5] << 8) | raw[4] == 0xFF00, "CALL debe apuntar al slot FW_PUTC")
    check(reference["expected_output_ascii"] == "A", "La salida del programa debe ser A")

    # Modelo aritmético de dos CALL y dos RET, sin ejecutar instrucciones.
    monitor_return_address = 0xE345  # sitio ficticio del monitor tras CALL a RUN
    sp = 0x8000
    stack: dict[int, int] = {}
    for ret in (monitor_return_address, 0x6006):
        sp -= 2
        stack[sp] = ret & 0xFF
        stack[sp + 1] = ret >> 8
    check(sp == 0x7FFC, "Dos CALL deberían reservar cuatro bytes de RAM")
    first_ret = stack[sp] | (stack[sp + 1] << 8)
    sp += 2
    check(first_ret == value(reference["first_return_to_program"]), "Primer RET no vuelve a 6006")
    second_ret = stack[sp] | (stack[sp + 1] << 8)
    sp += 2
    check(second_ret == monitor_return_address and sp == 0x8000,
          "Segundo RET debe devolver al monitor y restaurar SP")

    monitor = spec["monitor_candidate"]
    check(monitor["run_uses"] == "CALL" and "return_to_monitor" in monitor["on_program_ret"],
          "RUN debería poder volver tras RET")
    check(monitor["on_program_halt"] == "cpu_halted_no_prompt_reset_needed",
          "HALT NO debe aparecer como RET o vuelta al prompt")
    return 2


def check_monitor(spec: dict) -> int:
    candidate = spec["monitor_candidate"]
    check(candidate["address_hex_digits"] == 4 and candidate["byte_hex_digits"] == 2,
          "Formato de entrada hexadecimal cambiado")
    check(candidate["numbers_prefix"] == "none" and candidate["commands_case_insensitive"],
          "Sintaxis de monitor divergente")
    check(candidate["mem_default_count_hex"] == "10" and candidate["mem_max_count_hex"] == "100",
          "MEM debe limitar lecturas entre 1 y 256 bytes")
    check(candidate["mem_read_regions"] == [["0000", "7FFF"], ["E000", "FFFF"]],
          "MEM no debe leer E/S mapeada o expansión")
    check(candidate["poke_window"] == ["6000", "6FFF"] and candidate["run_window"] == ["6000", "6FFF"],
          "Ventanas de práctica no coinciden")
    check(not candidate["parser_implemented"] and not candidate["directory_or_named_files_implemented"],
          "No existe parser grabado ni directorio")
    check({item["name"] for item in candidate["command_registry"]} ==
          {"HELP", "MEM", "POKE", "RUN", "REG", "LOAD"}, "Registro de comandos cambiado")
    for item in candidate["command_registry"]:
        check(item["available_candidate"] == (item["name"] not in ("REG", "LOAD")),
              "REG y LOAD siguen pendientes de infraestructura")

    vectors = spec["example_monitor_vectors"]
    check(len(vectors) == 30, "Se esperan exactamente 30 vectores públicos reproducibles")
    for vector in vectors:
        result, details = parse_monitor(vector["line"], candidate)
        check(result == vector["result"], f"Comando {vector['line']!r}: {result} != {vector['result']}")
        if "error" in vector:
            check(details.get("error") == vector["error"],
                  f"Comando {vector['line']!r}: error incorrecto {details}")
        if "count" in vector:
            check(details.get("count") == vector["count"], f"Lectura MEM incorrecta: {vector['line']}")
    # Controles que no dependen del JSON de vectores.
    for probe in ("POKE E000 00", "POKE FF00 00", "POKE 0000 00", "POKE C002 00"):
        check(parse_monitor(probe, candidate)[0] == "ERROR", f"POKE indebidamente admitido: {probe}")
    for probe in ("MEM BFFF", "MEM 7FFF 10", "MEM FFFF 02", "MEM 6000 0"):
        check(parse_monitor(probe, candidate)[0] == "ERROR", f"MEM inválido admitido: {probe}")
    for probe in ("REG", "LOAD"):
        check(parse_monitor(probe, candidate)[0] == "NO_DISPONIBLE", f"{probe} no debe fingir hardware")
    return len(vectors) + 10


def main() -> None:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    isa = json.loads(ISA.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))
    check(spec["status"] == "propuesta_no_aprobada" and spec["release"] == "R0.11",
          "R0.11 debe seguir siendo borrador")
    check(spec["architecture"] == "Aula-8" and spec["aula8_external_data_bus_bits"] == 8,
          "La ROM propuesta es Aula-8")
    check(spec["aula16_external_data_bus_bits"] == state["architecture"]["aula16"]["external_data_bus_bits"] == 16,
          "Aula-16 debe conservar su bus externo de 16 bits")
    for field in ("firmware_implemented", "cpu_executed", "microcode_compiled",
                  "electrical_validation", "rom_image_built"):
        check(spec[field] is False, f"No se permite afirmar {field}")
    check(spec["terminal"]["memory_mapped_data"] == "C000"
          and spec["terminal"]["memory_mapped_status"] == "C002"
          and not spec["terminal"]["hardware_controller_implemented"],
          "Terminal MMIO coherente, aún sin controlador")

    entries = check_rom(spec, isa, state)
    returns = check_abi_and_return(spec, isa)
    commands = check_monitor(spec)
    print(f"R0.11: {entries} ranuras públicas comprobadas en reserva de 32; vector RESET 0xFFFC-0xFFFD coherente.")
    print(f"R0.11: {returns} rutas teóricas RET/HALT; {commands} comprobaciones de sintaxis/límites de monitor.")
    print("APROBADA la coherencia documental; NO hay ROM, CPU, monitor ni hardware ejecutados.")


if __name__ == "__main__":
    main()
