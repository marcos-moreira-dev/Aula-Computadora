#!/usr/bin/env python3
"""Prueba de escritorio de ABI MiniC-Aula8 R0.10. No ejecuta CPU ni micro-ROM."""

from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "simulador-javafx"
LAYOUT = [
    (0x6000, "SETSP", [0x17, 0x00, 0x80]),
    (0x6003, "LDI", [0x11, 0x02, 0x01]),
    (0x6006, "PUSH", [0x1A, 0x02]),
    (0x6008, "LDI", [0x11, 0x03, 0xFF]),
    (0x600B, "PUSH", [0x1A, 0x03]),
    (0x600D, "CALL", [0x35, 0x13, 0x60]),
    (0x6010, "ADJSP", [0x18, 0x02]),
    (0x6012, "HALT", [0x01]),
    (0x6013, "PUSHX", [0x1C]),
    (0x6014, "PUSH", [0x1A, 0x02]),
    (0x6016, "PUSH", [0x1A, 0x03]),
    (0x6018, "XFROMSP", [0x19]),
    (0x6019, "ADJSP", [0x18, 0xFE]),
    (0x601B, "LD", [0x12, 0x04, 0x06]),
    (0x601E, "LD", [0x12, 0x05, 0x07]),
    (0x6021, "LDI", [0x11, 0x02, 0x01]),
    (0x6024, "ADD", [0x20, 0x02]),
    (0x6026, "LDI", [0x11, 0x02, 0x00]),
    (0x6029, "ADC", [0x21, 0x06]),
    (0x602B, "ST", [0x13, 0x04, 0xFE]),
    (0x602E, "ST", [0x13, 0x05, 0xFF]),
    (0x6031, "LD", [0x12, 0x04, 0xFE]),
    (0x6034, "LD", [0x12, 0x05, 0xFF]),
    (0x6037, "ADJSP", [0x18, 0x02]),
    (0x6039, "POP", [0x1B, 0x03]),
    (0x603B, "POP", [0x1B, 0x02]),
    (0x603D, "POPX", [0x1D]),
    (0x603E, "RET", [0x02]),
]
EXPECTED_PC_ORDER = [
    0x6000, 0x6003, 0x6006, 0x6008, 0x600B, 0x600D,
    0x6013, 0x6014, 0x6016, 0x6018, 0x6019, 0x601B,
    0x601E, 0x6021, 0x6024, 0x6026, 0x6029, 0x602B,
    0x602E, 0x6031, 0x6034, 0x6037, 0x6039, 0x603B,
    0x603D, 0x603E, 0x6010, 0x6012
]


def from_hex(value: str) -> int:
    return int(value, 16)


def signed8(byte: int) -> int:
    return byte - 256 if byte & 0x80 else byte


def model_reference_frame() -> tuple[list[tuple[int, str, int, int]], dict, dict, int]:
    """Modelo específico del marco, no intérprete genérico de instrucciones de Aula-8."""
    memory: dict[int, int] = {}
    events: list[tuple[int, str, int, int]] = []
    x, sp = 0x6F00, 0x8000
    r0, r1, r2, r3 = 0, 0, 0, 0
    flags = {"Z": 0, "N": 0, "C": 0, "V": 0}
    frame_x = -1
    sp_local = -1

    def write(pc: int, address: int, byte: int) -> None:
        assert 0x7000 <= address <= 0x7FFF, "Escritura fuera del área de pila"
        memory[address] = byte & 0xFF
        events.append((pc, "write", address, byte & 0xFF))

    def read(pc: int, address: int) -> int:
        assert address in memory, f"Lectura de pila sin dato definido: {address:04X}"
        value = memory[address]
        events.append((pc, "read", address, value))
        return value

    def pushbyte(pc: int, byte: int) -> None:
        nonlocal sp
        sp -= 1
        write(pc, sp, byte)

    def popbyte(pc: int) -> int:
        nonlocal sp
        byte = read(pc, sp)
        sp += 1
        return byte

    # El llamador deposita alto, luego bajo. Cada PUSH disminuye SP en uno.
    r2 = 0x01
    pushbyte(0x6006, r2)
    r3 = 0xFF
    pushbyte(0x600B, r3)
    # CALL conserva retorno ya avanzado y escribe little-endian.
    sp -= 2
    write(0x600D, sp, 0x10)
    write(0x600D, sp + 1, 0x60)
    # Prólogo fijo: PUSHX (2B), PUSH R2, PUSH R3, XFROMSP.
    sp -= 2
    write(0x6013, sp, x & 0xFF)
    write(0x6013, sp + 1, x >> 8)
    pushbyte(0x6014, r2)
    pushbyte(0x6016, r3)
    x = sp
    frame_x = x
    # Dos bytes de local u16. ADJSP no inicializa memoria.
    sp += signed8(0xFE)
    sp_local = sp
    # Acceso de parámetros mediante offsets fijos del marco.
    r0 = read(0x601B, x + 6)
    r1 = read(0x601E, x + 7)
    # ADD bajo y ADC alto, comprobando que LDI posterior no borra C.
    r2 = 1
    low_sum = r0 + r2
    r0 = low_sum & 0xFF
    carry = (low_sum >> 8) & 1
    r2 = 0
    high_sum = r1 + r2 + carry
    r1 = high_sum & 0xFF
    flags = {
        "Z": int(r1 == 0),
        "N": (r1 >> 7) & 1,
        "C": int(high_sum > 0xFF),
        "V": int((~(0x01 ^ (r2 + carry) & 0xFF) & (0x01 ^ r1) & 0x80) != 0)
    }
    # Guardar y leer local u16 bajo, alto.
    write(0x602B, x - 2, r0)
    write(0x602E, x - 1, r1)
    r0 = read(0x6031, x - 2)
    r1 = read(0x6034, x - 1)
    # Epílogo: liberar local, restaurar no volátiles, RET.
    sp += 2
    r3 = popbyte(0x6039)
    r2 = popbyte(0x603B)
    low_x, high_x = read(0x603D, sp), read(0x603D, sp + 1)
    x = low_x | (high_x << 8)
    sp += 2
    low_ret, high_ret = read(0x603E, sp), read(0x603E, sp + 1)
    pc_after_ret = low_ret | (high_ret << 8)
    sp += 2
    # Limpieza de argumento hecha por el llamador, no por RET.
    sp += 2
    assert pc_after_ret == 0x6010
    final = {
        "pc": "6013", "sp": f"{sp:04X}", "x": f"{x:04X}",
        "r0": f"{r0:02X}", "r1": f"{r1:02X}",
        "r2": f"{r2:02X}", "r3": f"{r3:02X}",
        "flags": flags, "halted": True
    }
    return events, final, {f"{addr:04X}": f"{value:02X}"
                            for addr, value in sorted(memory.items())}, frame_x << 16 | sp_local


def validate_multiple_parameters(check) -> int:
    rng = random.Random(1010)
    cases = 0
    for number_of_args in range(5):
        for _ in range(128):
            values = [rng.randrange(65536) for _ in range(number_of_args)]
            memory: dict[int, int] = {}
            sp = 0x8000
            # Caller pushes right to left, high before low.
            for value in reversed(values):
                sp -= 1
                memory[sp] = value >> 8
                sp -= 1
                memory[sp] = value & 0xFF
            sp -= 2  # CALL
            memory[sp] = 0x34
            memory[sp + 1] = 0x12
            sp -= 2  # PUSHX
            memory[sp] = 0x00
            memory[sp + 1] = 0x6F
            sp -= 1
            memory[sp] = 0x55  # R2
            sp -= 1
            memory[sp] = 0xAA  # R3
            x_frame = sp
            for idx, expected in enumerate(values):
                base = x_frame + 6 + 2 * idx
                actual = memory[base] | memory[base + 1] << 8
                check(actual == expected,
                      f"Parámetro {idx} en marco de {number_of_args} parámetros")
            check(x_frame == 0x8000 - 6 - 2 * number_of_args,
                  "Prólogo fijo o número de argumentos incoherente")
            check((x_frame + 6 + 2 * number_of_args) == 0x8000,
                  "El tamaño teórico de pila debe recuperarse en caller")
            cases += 1
    return cases


def main() -> int:
    try:
        proposal = json.loads((ROOT / "ABI_MINIC_AULA8_R0_10_BORRADOR.json").read_text(encoding="utf-8"))
        isa = json.loads((ROOT / "ISA_AULA8_CANDIDATA.json").read_text(encoding="utf-8"))
        r09 = json.loads((ROOT / "MICROAJUSTES_AULA8_R0_9_BORRADOR.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR leyendo documentación: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []

    def check(cond: bool, error: str) -> None:
        if not cond:
            errors.append(error)

    check(proposal.get("project_release") == "R0.10" and
          proposal.get("status") == "propuesta_no_aprobada" and
          proposal.get("abi_final") is False, "ABI R0.10 no está aprobada")
    check(all(proposal.get(k) is False for k in
              ("cpu_executed", "compiler_implemented", "microcode_compiled", "physical_validation")),
          "No declarar CPU, compilador, micro-ROM ni electrónica inexistentes")
    check(proposal.get("aula8_external_data_bus_bits") == 8 and
          proposal.get("aula16_external_data_bus_bits") == 16,
          "Se deben conservar ambos buses externos")
    check(isa.get("status") == "propuesta_no_aprobada" and
          r09.get("status") == "propuesta_no_aprobada",
          "Las instrucciones no constituyen ISA aprobada")
    stack = proposal.get("stack", {})
    check(stack.get("initial_sp") == "8000" and stack.get("ram_high") == "7FFF" and
          stack.get("candidate_stack_low") == "7000" and
          stack.get("direction") == "descending" and
          stack.get("memory_byte_order") == "little_endian" and
          stack.get("hardware_overflow_detection") is False,
          "La pila candidata es descendente y sin protección física")
    calls = proposal.get("calls", {})
    check(calls.get("parameter_slot_bytes") == 2 and
          calls.get("maximum_v1_parameters") == 4 and
          calls.get("arguments_order") == "right_to_left" and
          calls.get("each_word_push_order") == ["high", "low"] and
          calls.get("caller_cleans_argument_bytes") is True,
          "Convención de parámetros incorrecta")
    check(calls.get("callee_saved_registers") == ["R2", "R3", "X"] and
          calls.get("caller_clobbered_registers") == ["R0", "R1"] and
          calls.get("caller_clobbered_flags") == ["Z", "N", "C", "V"],
          "Preservación de registros/flags incoherente con MiniC")
    check(calls.get("u8_parameter_high_byte") == "00" and
          calls.get("u16_return") == "R1_high_R0_low" and
          calls.get("local_u8_bytes") == 1 and calls.get("local_u16_bytes") == 2,
          "Tamaños y retornos de MiniC incorrectos")
    frame = proposal.get("fixed_frame", {})
    check(frame.get("prologue") == ["PUSHX", "PUSH R2", "PUSH R3", "XFROMSP", "ADJSP -L"] and
          frame.get("epilogue") == ["ADJSP +L", "POP R3", "POP R2", "POPX", "RET"],
          "Prólogo/epílogo no simétricos")
    offsets = frame.get("x_relative_offsets", {})
    check(offsets == {
        "saved_r3": 0, "saved_r2": 1, "saved_x_low": 2, "saved_x_high": 3,
        "return_address_low": 4, "return_address_high": 5,
        "first_parameter_low": 6, "first_parameter_high": 7,
        "second_parameter_low": 8, "second_parameter_high": 9,
        "third_parameter_low": 10, "third_parameter_high": 11,
        "fourth_parameter_low": 12, "fourth_parameter_high": 13
    } and frame.get("callee_save_bytes") == 4 and frame.get("return_address_bytes") == 2,
          "Offsets fijos incompatibles con guardados y retorno")

    sample = proposal.get("reference_program", {})
    isa_by_name = {it["mnemonic"]: it for it in isa.get("instructions", [])}
    supplied_instructions = sample.get("instructions", [])
    check(len(supplied_instructions) == len(LAYOUT),
          "Cantidad de instrucciones de ejemplo inconsistente")
    full_code = bytearray()
    for (address, mnemonic, encoded), actual in zip(LAYOUT, supplied_instructions):
        bytes_from_json = [int(value, 16) for value in actual.get("bytes_hex", "").split()]
        check(actual.get("pc") == f"{address:04X}" and
              actual.get("mnemonic") == mnemonic and bytes_from_json == encoded,
              f"Instrucción en {address:04X} no coincide con el contrato R0.10")
        if mnemonic in isa_by_name:
            check(isa_by_name[mnemonic]["opcode"] == f"{encoded[0]:02X}",
                  f"Opcode incompatible R0.3: {mnemonic} en {address:04X}")
            fmt = isa_by_name[mnemonic]["format"]
            if fmt != "memory":
                check(isa["formats"][fmt]["bytes"] == len(encoded),
                      f"Tamaño de instrucción incoherente: {address:04X}")
            else:
                selector = encoded[1]
                mode = (selector >> 2) & 0x03
                check(isa["formats"]["memory"]["bytes_by_mode"].get(str(mode)) == len(encoded),
                      f"Modo memoria incoherente: {address:04X}")
        check(address == 0x6000 + len(full_code), "Programa no contiguo")
        full_code.extend(encoded)
    check(len(full_code) == 63 and sample.get("instruction_read_bytes") == 63,
          "Longitud binaria del programa esperado: 63 B")
    observed_pc = [from_hex(pc) for pc in sample.get("expected_execution_pc_order", [])]
    check(observed_pc == EXPECTED_PC_ORDER and
          sample.get("entry_function") == "6013" and
          sample.get("return_address") == "6010" and
          sample.get("halt_address") == "6012",
          "Control de flujo CALL/RET/HALT incorrecto")

    events, actual_final, residue, encoded_frame = model_reference_frame()
    supplied_events = [(from_hex(it["at_pc"]), it["op"], from_hex(it["addr"]),
                        from_hex(it["value"]))
                       for it in sample.get("expected_data_bus_trace", [])]
    check(supplied_events == events,
          "Traza de datos no coincide con la semántica de escritorio de pila/función")
    count = Counter(operation for _, operation, _, _ in events)
    check(count == {"read": 10, "write": 10} and
          sample.get("expected_external_bus_transactions") == {"read": 73, "write": 10},
          "Bus: 63 lecturas de código + 10 datos y 10 escrituras")
    check(sample.get("expected_final") == actual_final and
          sample.get("stack_residue") == residue and
          sample.get("cpu_executed") is False,
          "Estado final/residuo o estatus de ejecución no coincide")
    frame_x, sp_local = encoded_frame >> 16, encoded_frame & 0xFFFF
    check(sample.get("expected_stack_frame") == {
        "x": f"{frame_x:04X}", "sp_with_local": f"{sp_local:04X}"
    }, "X de marco y SP local no coinciden")
    check((actual_final["r1"], actual_final["r0"]) == ("02", "00") and
          (actual_final["r2"], actual_final["r3"], actual_final["x"]) ==
          ("01", "FF", "6F00"), "El resultado/restauración de registros debe ser exacto")
    multicases = validate_multiple_parameters(check)
    check(multicases == 640, "Cobertura de argumentos determinista incorrecta")

    recursion = proposal.get("recursion_budget_example", {})
    theoretical = (recursion.get("one_u16_parameter_bytes", 0) +
                   recursion.get("return_address_bytes", 0) +
                   recursion.get("fixed_callee_save_bytes", 0) +
                   recursion.get("two_byte_local", 0))
    check(theoretical == 10 and recursion.get("total_per_level_bytes_theoretical") == 10 and
          recursion.get("candidate_stack_capacity_bytes") == 4096 and
          recursion.get("idealized_depth_max") == 409 and
          recursion.get("safe_depth_certified") is False,
          "Recursividad: cálculo teórico no debe significar certificación")
    check(0x8000 - 409 * theoretical >= 0x7000 and
          0x8000 - 410 * theoretical < 0x7000,
          "Límite teórico de niveles incongruente")

    if errors:
        for error in errors[:25]:
            print(f"ERROR: {error}", file=sys.stderr)
        if len(errors) > 25:
            print(f"... {len(errors) - 25} errores más", file=sys.stderr)
        return 1
    print("ABI MiniC-Aula8 R0.10: parámetros 2B, caller cleanup, marco X fijo, retornos u8/u16")
    print(f"Programa: {len(full_code)} bytes, 73 lecturas y 10 escrituras esperadas")
    print(f"Marcos de 0..4 parámetros: {multicases} disposiciones reproducidas")
    print("CONTROL DOCUMENTAL: APROBADO (modelo de escritorio, sin CPU ni compilador)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
