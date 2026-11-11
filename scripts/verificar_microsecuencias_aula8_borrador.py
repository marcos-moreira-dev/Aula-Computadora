#!/usr/bin/env python3
"""Comprueba consistencia de microsecuencias en papel; NO ejecuta microcódigo ni CPU."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "simulador-javafx"

EXPECTED_ACTIONS = {
    "LDI": ["READ_PC_TO_SEL", "VALIDATE_REGISTER_SEL", "READ_PC_TO_TMP",
            "WRITE_SELECTED_REG_FROM_TMP", "END_TO_FETCH"],
    "ST_ABS": ["READ_PC_TO_SEL", "VALIDATE_ABSOLUTE_REGISTER_SEL",
               "READ_PC_TO_ADDR_LOW", "READ_PC_TO_ADDR_HIGH",
               "BUILD_MAR_FROM_STAGING", "STAGE_SELECTED_REG_TO_MDR",
               "WRITE_MDR_AT_MAR", "END_TO_FETCH"],
    "HALT": ["ENTER_HALT"],
}


def main() -> int:
    try:
        model = json.loads((ROOT / "MICROSECUENCIAS_AULA8_BORRADOR.json").read_text(encoding="utf-8"))
        isa = json.loads((ROOT / "ISA_AULA8_CANDIDATA.json").read_text(encoding="utf-8"))
        trace = json.loads((ROOT / "MICROTRAZA_AULA8_BORRADOR.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR de lectura/JSON: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    check(model.get("project_release") == "R0.5", "Release de microsecuencias inesperada")
    check(model.get("status") == "propuesta_no_aprobada", "Microcontrol no está aprobado")
    check(isa.get("status") == "propuesta_no_aprobada", "ISA no está aprobada")
    check(model.get("granularity") == "acciones_logicas_no_ciclos_de_reloj", "Se confunden acciones con ciclos")
    check(model.get("micro_rom_control_word_bits") is None, "No fijar ancho de ROM de control")
    check(model.get("micro_rom_capacity_bytes") is None, "No fijar capacidad de ROM de control")
    check(model.get("exact_clock_cycles") is None, "No atribuir ciclos eléctricos")
    check(model.get("cpu_executed") is False, "Ninguna CPU ha ejecutado la secuencia")
    check(model.get("electrical_validation") is False, "Ninguna placa ha sido medida")
    check(set(model.get("extra_candidate_latches", [])) == {"ADDR_LO", "ADDR_HI"},
          "ST absoluto necesita conservar ambos bytes de dirección")

    fetch = model.get("common_fetch", [])
    instructions = model.get("instructions", {})
    check(isinstance(fetch, list), "Fetch debe ser una lista")
    check(isinstance(instructions, dict), "Instrucciones deben ser un diccionario")
    if not isinstance(fetch, list) or not isinstance(instructions, dict):
        return report(errors)

    check([s.get("action") for s in fetch] == ["READ_PC_TO_IR", "DISPATCH_OPCODE"],
          "Fetch compartido debe leer IR y despachar")
    check(set(instructions) == set(EXPECTED_ACTIONS), "Solamente LDI, ST absoluto y HALT deben estar detalladas")

    for name, expected in EXPECTED_ACTIONS.items():
        steps = instructions.get(name, [])
        check(isinstance(steps, list), f"{name}: se esperaban estados en lista")
        if not isinstance(steps, list):
            continue
        check([s.get("action") for s in steps] == expected, f"{name}: secuencia incompleta o reordenada")

    all_steps = fetch + [step for steps in instructions.values() if isinstance(steps, list) for step in steps]
    ids = [s.get("id") for s in all_steps]
    check(len(ids) == len(set(ids)) and all(isinstance(id_, str) for id_ in ids),
          "Identificadores de microestado únicos y no vacíos")
    terminal = set(model.get("terminal_states", []))
    check(terminal == {"HALTED", "FAULT"}, "Estados terminales incorrectos")

    for step in all_steps:
        name = step.get("id", "sin_id")
        action = step.get("action", "")
        bus = step.get("bus")
        check(bus in {"read", "write", "none"}, f"{name}: bus no válido (RD/WR simultáneos)")
        check(step.get("flags_write") is False, f"{name}: no debe cambiar Z/N/C/V")
        check(step.get("next") in set(ids) | terminal | {"DISPATCH"}, f"{name}: salto inexistente")
        if action.startswith("READ_PC_TO_"):
            check(bus == "read" and step.get("pc_advance") is True,
                  f"{name}: lectura de PC necesita RD y avance")
        else:
            check(step.get("pc_advance") is False, f"{name}: PC cambia fuera de lectura")
        if action == "WRITE_MDR_AT_MAR":
            check(bus == "write", "ST_WRITE: falta WR de datos")
        elif not action.startswith("READ_PC_TO_"):
            check(bus == "none", f"{name}: solo lectura/escritura declarada pueden usar bus")
        if "on_invalid" in step:
            check(step["on_invalid"] == "FAULT", f"{name}: selector inválido sin destino de fallo")

    dispatch = model.get("dispatch", {})
    opcodes = {item["mnemonic"]: int(item["opcode"], 16) for item in isa["instructions"]}
    check(dispatch.get("unknown") == "FAULT", "Opcode desconocido no produce FAULT")
    check(dispatch.get("known_but_unmodeled") == "PENDING_ROUTE",
          "OpCodes conocidos pendientes no deben confundirse con opcodes ilegales")
    check(dispatch.get("0x11") == "LDI_SELECTOR" and opcodes.get("LDI") == 0x11,
          "Despacho LDI incompatible con la ISA candidata")
    check(dispatch.get("0x13") == "ST_SELECTOR" and opcodes.get("ST") == 0x13,
          "Despacho ST incompatible con la ISA candidata")
    check(dispatch.get("0x01") == "HALT_ENTER" and opcodes.get("HALT") == 0x01,
          "Despacho HALT incompatible con la ISA candidata")
    check(fetch[0].get("next") == "DECODE" and fetch[1].get("next") == "DISPATCH",
          "Fetch no conduce al despacho")
    for inst_name in ("LDI", "ST_ABS"):
        steps = instructions.get(inst_name, [])
        if steps:
            check(steps[-1].get("next") == "FETCH_OPCODE", f"{inst_name} no retorna a fetch")
    halt = instructions.get("HALT", [])
    if halt:
        check(halt[-1].get("next") == "HALTED", "HALT no debe retornar al fetch")

    # Recuento de transacciones, comparado con el programa de bytes de R0.3 y la traza R0.4.
    read_count = 0
    write_count = 0
    for section in ("LDI", "ST_ABS", "HALT"):
        path = fetch + instructions.get(section, [])
        read_count += sum(step["bus"] == "read" for step in path)
        write_count += sum(step["bus"] == "write" for step in path)
    check((read_count, write_count) == (8, 1), "No se obtienen ocho lecturas y una escritura")
    check(model.get("expected_example_external_transactions") == {"read": 8, "write": 1},
          "Resumen de transacciones incorrecto")
    operations = [event.get("operation") for event in trace.get("transactions", [])]
    check((operations.count("read"), operations.count("write")) == (read_count, write_count),
          "Microsecuencias y microtraza no coinciden")

    example = next((e for e in isa["examples"] if e["name"] == "depositar_42"), None)
    check(example is not None, "Falta programa de muestra depositar_42")
    if example:
        code = bytes.fromhex(example["bytes_hex"])
        check(len(code) == 8 and code[:2] == b"\x11\x00" and code[3:5] == b"\x13\x00"
              and code[7] == 0x01, "Cambió formato del programa de muestra")
        if len(code) == 8:
            check(code[5] | code[6] << 8 == example["expected_ram_write"]["address"],
                  "Bytes de dirección ST no coinciden con ejemplo")
            check(code[2] == example["expected_ram_write"]["value"],
                  "El inmediato LDI no coincide con el dato escrito")

    return report(errors)


def report(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("MICROSECUENCIAS Aula-8 BORRADOR: fetch, LDI, ST absoluto y HALT coherentes")
    print("8 lecturas, 1 escritura; rutas, retención de dirección y flags revisadas")
    print("CONTROL DOCUMENTAL: APROBADO (sin CPU, microcódigo, ciclos ni electrónica ejecutados)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
