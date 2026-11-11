#!/usr/bin/env python3
"""Verifica traza externa declarada de un ejemplo; no ejecuta ni emula Aula-8."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "simulador-javafx" / "MICROTRAZA_AULA8_BORRADOR.json"
ISA = ROOT / "simulador-javafx" / "ISA_AULA8_CANDIDATA.json"


def main() -> int:
    errors: list[str] = []
    try:
        trace = json.loads(MODEL.read_text(encoding="utf-8"))
        isa = json.loads(ISA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: archivo JSON ausente o inválido: {exc}", file=sys.stderr)
        return 1

    if trace.get("status") != "traza_esperada_no_ejecutada":
        errors.append("La traza no puede declararse ejecutada")
    if trace.get("isa_status") != "propuesta_no_aprobada":
        errors.append("No se ha aprobado la ISA de Aula-8")
    bus = trace.get("external_bus", {})
    if bus.get("address_bits") != 16 or bus.get("data_bits") != 8:
        errors.append("Anchos de bus incorrectos para Aula-8")
    if bus.get("panel_isolated") is not True or bus.get("address_driver") != "cpu":
        errors.append("Al ejecutar debe conducir direcciones la CPU, no el panel")

    examples = {e["name"]: e for e in isa["examples"]}
    name = trace.get("program_name")
    if name not in examples:
        errors.append(f"Programa no encontrado en ISA: {name}")
        example = None
    else:
        example = examples[name]

    if example is not None:
        code = bytes.fromhex(example["bytes_hex"])
        origin = example["origin"]
        # Solo reconoce este ejemplo fijo: LDI R0, imm; ST absoluto R0; HALT.
        # No se implementa el conjunto de instrucciones ni su ejecución.
        if not (len(code) == 8 and code[:2] == bytes([0x11, 0x00])
                and code[3:5] == bytes([0x13, 0x00]) and code[7] == 0x01):
            errors.append("El ejemplo dejó de tener la forma didáctica LDI/ST/HALT")
        else:
            address = code[5] | (code[6] << 8)
            value = code[2]
            expected = []
            for i in range(7):
                expected.append(("read", origin + i, code[i], "memory"))
            expected.append(("write", address, value, "cpu"))
            expected.append(("read", origin + 7, code[7], "memory"))

            actual = trace.get("transactions", [])
            if len(actual) != len(expected):
                errors.append(f"Transacciones: se esperaban {len(expected)}, hay {len(actual)}")
            for i, event in enumerate(actual):
                if i >= len(expected):
                    break
                operation, addr, data, driver = expected[i]
                observed = (event.get("operation"), event.get("address"),
                            event.get("value"), event.get("data_driver"))
                if observed != (operation, addr, data, driver):
                    errors.append(f"Transacción {i+1}: {observed} != {(operation, addr, data, driver)}")
                if event.get("order") != i + 1:
                    errors.append(f"Orden incorrecto en evento {i+1}")
                if event.get("read_active") is not (operation == "read"):
                    errors.append(f"Control RD incorrecto en evento {i+1}")
                if event.get("write_active") is not (operation == "write"):
                    errors.append(f"Control WR incorrecto en evento {i+1}")

            final = trace.get("expected_end_state", {})
            if final.get("pc") != origin + len(code) or final.get("halted") is not True:
                errors.append("PC tras HALT o estado final inconsistentemente documentado")
            if final.get("r0") != value or final.get("ram_write") != {"address": address, "value": value}:
                errors.append("Registro o dirección/dato final no coincide con los bytes de muestra")
            if final.get("flags") != "preserved_unknown_initial":
                errors.append("No se debe inventar un estado inicial concreto de flags")

    if trace.get("exact_clock_cycles") is not None:
        errors.append("Los ciclos de reloj aún no están medidos o asignados")
    if trace.get("electrical_validation") != "not_performed":
        errors.append("No declarar validación eléctrica inexistente")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("MICROTRAZA Aula-8 BORRADOR: 9 transacciones externas consistentes")
    print("Propiedad del bus y lectura/escritura: coherentes con el ejemplo JSON")
    print("CONTROL DOCUMENTAL: APROBADO (NO se ejecutó CPU ni se midió electricidad)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
