#!/usr/bin/env python3
"""Contrasta el borrador R0.9 contra aritmética y trazas de escritorio; no ejecuta CPU."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "simulador-javafx"
EXPECTED_OPCODES = {
    "LEAX": ("15", "disp8", 1),
    "ADDXW": ("16", "none", 0),
    "SETSP": ("17", "imm16", 2),
    "ADJSP": ("18", "disp8", 1),
    "XFROMSP": ("19", "none", 0),
}
EXPECTED_ACTIONS = {
    "LEAX": ["READ_PC_TO_DISP8", "SIGN_EXTEND_DISP8", "LATCH_X_AND_SIGNED_DISP16",
             "ALU8_LOW_TO_TMP_AND_PRIVATE_CARRY", "ALU8_HIGH_WITH_PRIVATE_CARRY_TO_TMP",
             "COMMIT_TMP16_TO_X", "END_TO_FETCH"],
    "ADJSP": ["READ_PC_TO_DISP8", "SIGN_EXTEND_DISP8", "LATCH_SP_AND_SIGNED_DISP16",
              "ALU8_LOW_TO_TMP_AND_PRIVATE_CARRY", "ALU8_HIGH_WITH_PRIVATE_CARRY_TO_TMP",
              "COMMIT_TMP16_TO_SP", "END_TO_FETCH"],
    "ADDXW": ["LATCH_X_AND_R1_R0_WORD", "ALU8_LOW_TO_TMP_AND_PRIVATE_CARRY",
              "ALU8_HIGH_WITH_PRIVATE_CARRY_TO_TMP", "COMMIT_TMP16_TO_X", "END_TO_FETCH"],
    "SETSP": ["READ_PC_TO_TMP_LOW", "READ_PC_TO_TMP_HIGH", "COMMIT_TMP16_TO_SP", "END_TO_FETCH"],
    "XFROMSP": ["LATCH_SP16_TO_TMP", "COMMIT_TMP16_TO_X", "END_TO_FETCH"],
}


def signed8(raw: int) -> int:
    return raw - 256 if raw & 0x80 else raw


def add16_using_alu8(base: int, operand16: int) -> int:
    """Versión de dos pasadas; fuente no se pisa hasta terminar ambas."""
    low_total = (base & 0xFF) + (operand16 & 0xFF)
    low_result = low_total & 0xFF
    private_carry = low_total >> 8
    high_result = ((base >> 8) + (operand16 >> 8) + private_carry) & 0xFF
    return (high_result << 8) | low_result


def parsehex(value: str) -> int:
    return int(value, 16)


def main() -> int:
    try:
        candidate = json.loads((ROOT / "MICROAJUSTES_AULA8_R0_9_BORRADOR.json").read_text(encoding="utf-8"))
        isa = json.loads((ROOT / "ISA_AULA8_CANDIDATA.json").read_text(encoding="utf-8"))
        previous = json.loads((ROOT / "MICROINDICES_AULA8_R0_8_BORRADOR.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR de lectura JSON: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []

    def check(condition: bool, explanation: str) -> None:
        if not condition:
            errors.append(explanation)

    check(candidate.get("project_release") == "R0.9" and
          candidate.get("status") == "propuesta_no_aprobada", "R0.9 debe seguir candidata")
    check(candidate.get("granularity") == "acciones_logicas_no_ciclos_de_reloj",
          "No asumir ciclos a partir de microacciones")
    check(candidate.get("cpu_executed") is False and
          candidate.get("microcode_compiled") is False and
          candidate.get("electrical_validation") is False and
          candidate.get("clock_cycles_known") is False,
          "No declarar hardware o CPU que no existen")
    check(candidate.get("datapath_bits") == 8 and candidate.get("address_bits") == 16 and
          candidate.get("external_data_bus_bits") == 8, "No alterar el contrato de Aula-8")
    check(candidate.get("private_address_carry") is True and
          candidate.get("arithmetic_modulus") == 65536 and
          candidate.get("signed_disp8_range") == [-128, 127],
          "Aritmética de direcciones propuesta inconsistente")
    check(candidate.get("visible_flags_preserved") == ["Z", "N", "C", "V"],
          "Las instrucciones de ajustes deben preservar FLAGS")
    check(candidate.get("register_pair_for_addxw") == {"low": "R0", "high": "R1"},
          "ADDXW debe tomar palabra R1:R0 little-endian")
    check(candidate.get("stack_overflow_hardware_detection") is False and
          candidate.get("abi_final") is False and
          candidate.get("initial_stack_pointer_sentinel") == "8000",
          "No aprobar ABI ni protección de pila")
    check(isa.get("status") == "propuesta_no_aprobada" and
          previous.get("status") == "propuesta_no_aprobada",
          "ISA anterior e indexación siguen candidatas")

    opcodes = {it["mnemonic"]: (it["opcode"], it["format"])
               for it in isa.get("instructions", [])}
    routes = candidate.get("routes", {})
    check(set(routes) == set(EXPECTED_OPCODES), "Rutas incompletas o desconocidas")
    identifiers: list[str] = []
    logical_external_operand_reads = 0
    for name, (opcode, fmt, extra_reads) in EXPECTED_OPCODES.items():
        check(opcodes.get(name) == (opcode, fmt), f"Opcode o formato R0.3 incompatible: {name}")
        route = routes.get(name, {})
        check((route.get("opcode"), route.get("format")) == (opcode, fmt),
              f"Ruta {name} contradice la ISA")
        states = route.get("states", [])
        actions = [s.get("action") for s in states]
        check(actions == EXPECTED_ACTIONS[name], f"Orden de microacciones incorrecto: {name}")
        logical_external_operand_reads += extra_reads
        check(sum(s.get("bus") == "read" for s in states) == extra_reads,
              f"{name}: cantidad de lecturas de operandos incorrecta")
        check(states and states[-1].get("next") == "FETCH_OPCODE",
              f"{name}: no regresa al fetch común")
        for step in states:
            state_id = step.get("id")
            identifiers.append(state_id)
            act = step.get("action")
            bus = step.get("bus")
            expected_read = act.startswith("READ_PC_TO_")
            check(bus == ("read" if expected_read else "none"),
                  f"{name}: escritura o lectura no justificada del bus")
            check(step.get("pc_advance") is expected_read, f"{name}: PC avanzado incorrectamente")
            check(step.get("flags_write") is False, f"{name}: FLAGS no se preservan")
            check(step.get("next") in
                  {s.get("id") for s in states} | {"FETCH_OPCODE"},
                  f"{name}: estado de destino no existe")
    check(len(identifiers) == len(set(identifiers)) and all(identifiers),
          "Estados de microcontrol duplicados o vacíos")
    check(logical_external_operand_reads == 4,
          "Se esperan cuatro lecturas de operandos de las cinco rutas revisadas")

    checked_math = 0
    signed_offsets = (0, 1, 2, 3, 4, 7, 15, 31, 63, 127, 128, 129, 192, 240, 254, 255)
    for base in range(65536):
        for raw in signed_offsets:
            displacement16 = signed8(raw) & 0xFFFF
            actual = add16_using_alu8(base, displacement16)
            check(actual == (base + signed8(raw)) & 0xFFFF,
                  f"ALU8 signextend error: {base:04X} + {raw:02X}")
            checked_math += 1
    for base in (0, 1, 255, 256, 0x7FFE, 0x7FFF, 0x8000, 0xFFFF):
        for pair in range(65536):
            actual = add16_using_alu8(base, pair)
            check(actual == (base + pair) & 0xFFFF,
                  f"ADDXW high:low error: {base:04X} + {pair:04X}")
            checked_math += 1
    check(checked_math == 1572864, "La cobertura matemática debe ser reproducible")

    vectors = candidate.get("boundary_vectors", {})
    for row in vectors.get("signed_disp", []):
        base, raw = parsehex(row["base"]), parsehex(row["raw_disp"])
        actual = add16_using_alu8(base, signed8(raw) & 0xFFFF)
        check(actual == parsehex(row["result"]), f"Vector signed: {row}")
    for row in vectors.get("word_add", []):
        base = parsehex(row["base"])
        pair = (parsehex(row["r1"]) << 8) | parsehex(row["r0"])
        check(add16_using_alu8(base, pair) == parsehex(row["result"]),
              f"Vector ADDXW: {row}")
    for start_sp in (0x7002, 0x7F00, 0x7F7F, 0x8000):
        for raw in range(256):
            result = add16_using_alu8(start_sp, signed8(raw) & 0xFFFF)
            restored = add16_using_alu8(result, (-signed8(raw)) & 0xFFFF)
            check(restored == start_sp, f"ADJSP reserva/libera no reversible: {start_sp:04X}")

    sample = candidate.get("reference_program", {})
    program = [int(byte, 16) for byte in sample.get("bytes_hex", "").split()]
    check(parsehex(sample.get("origin", "0")) == 0x6000 and len(program) == 24,
          "Programa completo debe ocupar 24 bytes en 0x6000")
    expected_layout = [
        (0x6000, [0x17, 0x00, 0x80], []),
        (0x6003, [0x35, 0x07, 0x60], [("write", 0x7FFE, 0x06),
                                       ("write", 0x7FFF, 0x60)]),
        (0x6007, [0x1C], [("write", 0x7FFC, 0x00), ("write", 0x7FFD, 0x6F)]),
        (0x6008, [0x19], []),
        (0x6009, [0x18, 0xFF], []),
        (0x600B, [0x11, 0x00, 0x2A], []),
        (0x600E, [0x13, 0x08, 0x00], [("write", 0x7FFB, 0x2A)]),
        (0x6011, [0x12, 0x09, 0x00], [("read", 0x7FFB, 0x2A)]),
        (0x6014, [0x18, 0x01], []),
        (0x6016, [0x1D], [("read", 0x7FFC, 0x00), ("read", 0x7FFD, 0x6F)]),
        (0x6017, [0x02], [("read", 0x7FFE, 0x06), ("read", 0x7FFF, 0x60)]),
        (0x6006, [0x01], [])
    ]
    expected_trace: list[tuple[str, int, int]] = []
    for pc, ins_bytes, side_effects in expected_layout:
        check(program[pc - 0x6000:pc - 0x6000 + len(ins_bytes)] == ins_bytes,
              f"Bytes en {pc:04X} no coinciden con la ISA")
        expected_trace.extend(("read", pc + offset, byte)
                              for offset, byte in enumerate(ins_bytes))
        expected_trace.extend(side_effects)
    observed_trace = [(row.get("op"), parsehex(row["addr"]), parsehex(row["value"]))
                      for row in sample.get("expected_trace", [])]
    check(observed_trace == expected_trace, "Traza R0.9 no coincide con recorrido del programa")
    counts = Counter(operation for operation, _, _ in expected_trace)
    check(counts == {"read": 29, "write": 5} and
          sample.get("external_reads_expected") == 29 and
          sample.get("external_writes_expected") == 5,
          "La prueba debe tener 29 lecturas y 5 escrituras")
    check(all(0x7000 <= addr <= 0x7FFF for op, addr, _ in expected_trace if op == "write"),
          "Las escrituras de pila y local deben quedar en RAM candidata")
    check(all(0x6000 <= addr <= 0x6017 for op, addr, _ in expected_trace
              if op == "read" and addr < 0x7000),
          "La búsqueda de instrucciones debe permanecer en la región de programa")
    final = sample.get("expected_final", {})
    check({field: final.get(field) for field in ("pc", "sp", "x", "r0", "r1")} ==
          {"pc": "6007", "sp": "8000", "x": "6F00", "r0": "2A", "r1": "2A"},
          "Estado final SP/X/PC/R0/R1 no coincide con el contrato")
    expected_residue = {"7FFB": "2A", "7FFC": "00", "7FFD": "6F",
                        "7FFE": "06", "7FFF": "60"}
    check(final.get("memory_residue") == expected_residue and
          sample.get("cpu_executed") is False and final.get("halted") is True and
          final.get("flags") == "preserved_unknown",
          "Residuo de pila, flags o condición de CPU incorrectos")
    check((0x8000 - 2 - 2 - 1) == 0x7FFB and
          (0x7FFB + 1 + 2 + 2) == 0x8000,
          "Disposición ilustrativa del marco no equilibra SP")

    if errors:
        for error in errors[:20]:
            print(f"ERROR: {error}", file=sys.stderr)
        if len(errors) > 20:
            print(f"... {len(errors) - 20} errores adicionales", file=sys.stderr)
        return 1
    print("AJUSTES Aula-8 R0.9: LEAX, ADJSP, ADDXW, SETSP y XFROMSP coherentes")
    print(f"Dos pasadas ALU8: {checked_math} casos matemáticos contrastados")
    print(f"Función y marco: {counts['read']} lecturas + {counts['write']} escrituras esperadas")
    print("CONTROL DOCUMENTAL: APROBADO (sin CPU, micro-ROM ni electricidad ejecutadas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
