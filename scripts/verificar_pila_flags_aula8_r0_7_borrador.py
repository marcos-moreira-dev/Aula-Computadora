#!/usr/bin/env python3
"""Comprueba ISA y fórmulas candidatas; NO ejecuta CPU, netlist ni micro-ROM."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "simulador-javafx"
EXPECTED_ACTIONS = {
    "PUSH": ["READ_PC_TO_SEL", "CHECK_REG_SELECTOR", "SUB_ONE_FROM_SP",
             "LOAD_MAR_FROM_SP", "LOAD_MDR_FROM_SELECTED_REG", "WRITE_MDR_AT_MAR", "END_TO_FETCH"],
    "POP": ["READ_PC_TO_SEL", "CHECK_REG_SELECTOR", "LOAD_MAR_FROM_SP",
            "READ_MAR_TO_TMP", "LOAD_SELECTED_REG_FROM_TMP", "ADD_ONE_TO_SP", "END_TO_FETCH"],
    "PUSHX": ["SUB_TWO_FROM_SP", "LOAD_MAR_FROM_SP", "LOAD_MDR_FROM_X_LO", "WRITE_MDR_AT_MAR",
              "LOAD_MAR_FROM_SP_PLUS_ONE", "LOAD_MDR_FROM_X_HI", "WRITE_MDR_AT_MAR", "END_TO_FETCH"],
    "POPX": ["LOAD_MAR_FROM_SP", "READ_MAR_TO_ADDR_LO", "LOAD_MAR_FROM_SP_PLUS_ONE",
             "READ_MAR_TO_ADDR_HI", "LOAD_X_FROM_ADDR_LO_HI", "ADD_TWO_TO_SP", "END_TO_FETCH"],
    "INC": ["READ_PC_TO_SEL", "CHECK_REG_SELECTOR", "INC_SELECTED_REG_AND_ZNV_PRESERVE_C", "END_TO_FETCH"],
    "DEC": ["READ_PC_TO_SEL", "CHECK_REG_SELECTOR", "DEC_SELECTED_REG_AND_ZNV_PRESERVE_C", "END_TO_FETCH"],
}


def signed8(value: int) -> int:
    return value - 256 if value & 128 else value


def flags_by_bit_logic(op: str, a: int, b: int, cin: int) -> dict[str, int]:
    if op == "INC":
        result = (a + 1) & 255
        carry, overflow = cin, int(a == 0x7F)
    elif op == "DEC":
        result = (a - 1) & 255
        carry, overflow = cin, int(a == 0x80)
    elif op in {"ADD", "ADC"}:
        raw = a + b + (cin if op == "ADC" else 0)
        result = raw & 255
        carry = int(raw > 255)
        overflow = int(bool((~(a ^ b) & (a ^ result)) & 128))
    elif op in {"SUB", "SBC", "CMP"}:
        raw = a - b - (cin if op == "SBC" else 0)
        result = raw & 255
        carry = int(raw < 0)  # C = préstamo, NO 'no préstamo'.
        overflow = int(bool(((a ^ b) & (a ^ result)) & 128))
    elif op == "AND":
        result, carry, overflow = a & b, cin, 0
    elif op == "OR":
        result, carry, overflow = a | b, cin, 0
    elif op == "XOR":
        result, carry, overflow = a ^ b, cin, 0
    elif op == "NOT":
        result, carry, overflow = (~a) & 255, cin, 0
    elif op == "SHL":
        result, carry, overflow = (a << 1) & 255, (a >> 7) & 1, 0
    elif op == "SHR":
        result, carry, overflow = a >> 1, a & 1, 0
    else:
        raise ValueError(f"No existe operación: {op}")
    return {"result": result, "Z": int(result == 0), "N": (result >> 7) & 1,
            "C": carry, "V": overflow}


def flags_by_integer_reference(op: str, a: int, b: int, cin: int) -> dict[str, int]:
    # Comparación aritmética independiente por rango entero, no por la fórmula de bits.
    if op in {"ADD", "ADC", "SUB", "SBC", "CMP"}:
        extra = cin if op in {"ADC", "SBC"} else 0
        if op in {"ADD", "ADC"}:
            unsigned = a + b + extra
            signed = signed8(a) + signed8(b) + extra
            carry = int(unsigned > 255)
        else:
            unsigned = a - b - extra
            signed = signed8(a) - signed8(b) - extra
            carry = int(unsigned < 0)
        result = unsigned & 255
        return {"result": result, "Z": int(result == 0), "N": int(result >= 128),
                "C": carry, "V": int(not (-128 <= signed <= 127))}
    if op in {"INC", "DEC"}:
        signed = signed8(a) + (1 if op == "INC" else -1)
        result = signed & 255
        return {"result": result, "Z": int(result == 0), "N": int(result >= 128),
                "C": cin, "V": int(not (-128 <= signed <= 127))}
    raise ValueError(op)


def main() -> int:
    try:
        model = json.loads((ROOT / "MICRODATOS_PILA_FLAGS_AULA8_R0_7_BORRADOR.json").read_text(encoding="utf-8"))
        isa = json.loads((ROOT / "ISA_AULA8_CANDIDATA.json").read_text(encoding="utf-8"))
        flow = json.loads((ROOT / "MICROFLUJO_AULA8_R0_6_BORRADOR.json").read_text(encoding="utf-8"))
        fetch = json.loads((ROOT / "MICROSECUENCIAS_AULA8_BORRADOR.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR al cargar archivos: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    check(model.get("project_release") == "R0.7", "Release incorrecta")
    check(model.get("status") == "propuesta_no_aprobada", "La ISA sigue en borrador")
    check(model.get("granularity") == "acciones_logicas_no_ciclos_de_reloj", "Acciones confundidas con ciclos")
    check(model.get("cpu_executed") is False and model.get("microcode_compiled") is False and
          model.get("electrical_validation") is False and model.get("exact_clock_cycles") is None,
          "No presentar verificación documental como ejecución o medición")
    check(model.get("flags") == ["Z", "N", "C", "V"], "Flags Z/N/C/V incongruentes")
    check(fetch.get("status") == "propuesta_no_aprobada" and flow.get("status") == "propuesta_no_aprobada",
          "Versiones R0.5/R0.6 aún son propuestas")
    check(flow.get("stack_convention", {}).get("call_subtracts_from_sp") == 2,
          "El convenio little-endian de R0.6 debe preservarse")
    check(isa.get("status") == "propuesta_no_aprobada", "ISA aún sin aprobar")
    isa_ops = {item["mnemonic"]: (item["opcode"], item["format"])
               for item in isa["instructions"]}
    routes = model.get("routes", {})
    expected_formats = {"PUSH": "reg", "POP": "reg", "PUSHX": "none", "POPX": "none",
                        "INC": "reg", "DEC": "reg"}
    check(set(routes) == set(EXPECTED_ACTIONS), "Rutas R0.7 incompletas")
    ids: list[str] = []
    all_steps: list[dict] = []
    for name, actions in EXPECTED_ACTIONS.items():
        route = routes.get(name, {})
        check((route.get("opcode"), expected_formats[name]) == isa_ops.get(name),
              f"Opcode de {name} no coincide con ISA")
        steps = route.get("states", [])
        check([s.get("action") for s in steps] == actions, f"Acciones de {name} alteradas")
        if steps:
            check(steps[-1].get("next") == "FETCH_OPCODE", f"{name} no termina en fetch")
        ids.extend(s.get("id", "") for s in steps)
        all_steps.extend(steps)
    check(len(ids) == len(set(ids)) and all(ids), "Microestados duplicados o vacíos")
    allowed = set(ids) | {"FETCH_OPCODE", "FAULT"}

    for step in all_steps:
        state = step.get("id", "?")
        action = step.get("action", "")
        bus = step.get("bus")
        check(bus in {"read", "write", "none"}, f"{state}: bus ilegal o contención RD/WR")
        check(step.get("next") in allowed, f"{state}: transición no identificada")
        if "on_invalid" in step:
            check(step["on_invalid"] == "FAULT", f"{state}: falta fallo de selector")
        if action == "READ_PC_TO_SEL":
            check(bus == "read" and step.get("pc_advance") is True,
                  f"{state}: leer selector debe avanzar PC")
        elif action.startswith("READ_MAR_TO_"):
            check(bus == "read" and step.get("pc_advance") is False,
                  f"{state}: lectura de datos de pila no debe avanzar PC")
        elif action == "WRITE_MDR_AT_MAR":
            check(bus == "write" and step.get("pc_advance") is False,
                  f"{state}: escritura con señales incorrectas")
        else:
            check(bus == "none" and step.get("pc_advance") is False,
                  f"{state}: operación interna utiliza el bus externo")
        expected_flags = action in {"INC_SELECTED_REG_AND_ZNV_PRESERVE_C",
                                    "DEC_SELECTED_REG_AND_ZNV_PRESERVE_C"}
        check(step.get("flags_write") is expected_flags,
              f"{state}: PUSH/POP deben conservar flags; INC/DEC deben escribir Z/N/V")

    for name in ("PUSH", "PUSHX"):
        expected_writes = 1 if name == "PUSH" else 2
        check(sum(s.get("bus") == "write" for s in routes.get(name, {}).get("states", [])) == expected_writes,
              f"{name} necesita {expected_writes} escritura(s) de RAM")
    for name in ("POP", "POPX"):
        expected_reads = 2 if name == "POP" else 2  # POP: selector+memoria; POPX: dos lecturas RAM.
        check(sum(s.get("bus") == "read" for s in routes.get(name, {}).get("states", [])) == expected_reads,
              f"{name} necesita {expected_reads} lectura(s) tras fetch")

    # Vectores declarados contra semántica; fórmulas comparadas exhaustivamente con enteros matemáticos.
    for vector in model.get("edge_vectors", []):
        op = vector["operation"]
        result = flags_by_bit_logic(op, vector["a"], vector.get("b", 0), vector.get("carry_in", 0))
        for field, value in result.items():
            check(vector.get(field) == value, f"Vector {op} a={vector['a']}: {field} no coincide")

    checked_flag_cases = 0
    for op in ("ADD", "ADC", "SUB", "SBC", "CMP"):
        for a in range(256):
            for b in range(256):
                for cin in (0, 1) if op in {"ADC", "SBC"} else (0,):
                    calculated = flags_by_bit_logic(op, a, b, cin)
                    reference = flags_by_integer_reference(op, a, b, cin)
                    checked_flag_cases += 1
                    if calculated != reference:
                        errors.append(f"ALU {op} a={a} b={b} carry={cin}: {calculated} != {reference}")
                        break
                if errors:
                    break
            if errors:
                break
    for op in ("INC", "DEC"):
        for a in range(256):
            for cin in (0, 1):
                checked_flag_cases += 1
                check(flags_by_bit_logic(op, a, 0, cin) == flags_by_integer_reference(op, a, 0, cin),
                      f"INC/DEC inconsistente {op} {a}, C={cin}")

    examples = model.get("examples", {})
    push_example = examples.get("push_pop_dec", {})
    code = bytes.fromhex(push_example.get("bytes_hex", ""))
    expected_bytes = bytes([0x11, 0x00, 0x2A, 0x1A, 0x00, 0x11, 0x00, 0x00,
                            0x1B, 0x00, 0x2A, 0x00, 0x01])
    check(code == expected_bytes, "El ejemplo PUSH/POP/DEC cambió codificación candidata")
    origin, sp = push_example.get("origin"), push_example.get("initial_sp")
    check((origin, sp) == (0x6000, 0x8000), "Direcciones iniciales incorrectas")
    if code == expected_bytes and origin == 0x6000 and sp == 0x8000:
        expected_trace = []

        def read_pc(i: int) -> None:
            expected_trace.append({"operation": "read", "address": origin + i, "value": code[i]})

        for i in range(5):
            read_pc(i)
        expected_trace.append({"operation": "write", "address": sp - 1, "value": code[2]})
        for i in range(5, 10):
            read_pc(i)
        expected_trace.append({"operation": "read", "address": sp - 1, "value": code[2]})
        for i in range(10, len(code)):
            read_pc(i)
        check(push_example.get("expected_trace") == expected_trace,
              "Traza de PUSH/POP/DEC no coincide con bytes y pila")
        check((sum(t["operation"] == "read" for t in expected_trace),
               sum(t["operation"] == "write" for t in expected_trace)) == (14, 1),
              "Se esperan catorce lecturas y una escritura")
        final = push_example.get("expected_final", {})
        check(final == {"pc": origin + len(code), "sp": sp, "r0": code[2] - 1,
                        "stack_byte_address": sp - 1, "stack_byte_residual": code[2],
                        "flags": {"Z": 0, "N": 0, "C": "preserved_initial", "V": 0},
                        "halted": True}, "Estado final PUSH/POP/DEC no coincide")

    x_example = examples.get("pushx_popx", {})
    initial_sp = x_example.get("initial_sp", -1)
    initial_x = x_example.get("initial_x", -1)
    check(initial_sp == 0x8000 and initial_x == 0x12AB,
          "Ejemplo PUSHX/POPX debe comenzar con X=0x12AB y SP=0x8000")
    check(x_example.get("after_pushx_sp") == initial_sp - 2 and
          x_example.get("after_popx_sp") == initial_sp and
          x_example.get("stack_low") == initial_x & 255 and
          x_example.get("stack_high") == (initial_x >> 8) and
          x_example.get("after_popx_x") == initial_x and
          x_example.get("flags") == "preserved_initial", "Prueba little-endian PUSHX/POPX no coincide")

    loop = examples.get("dec_jnz_3", {})
    values = [loop.get("initial_r0", -1)]
    for _ in range(3):
        values.append((values[-1] - 1) & 255)
    zeros = [int(v == 0) for v in values[1:]]
    check(loop.get("after_dec") == values[1:] and loop.get("Z_after_dec") == zeros and
          loop.get("JNZ_taken") == [z == 0 for z in zeros] and
          loop.get("C") == "preserved_initial", "Bucle DEC→JNZ documentado incorrectamente")
    check(flow.get("branch_example", {}).get("expected_taken") == loop.get("JNZ_taken"),
          "El bucle R0.7 contradice la propuesta de saltos R0.6")

    if errors:
        for error in errors[:30]:
            print(f"ERROR: {error}", file=sys.stderr)
        if len(errors) > 30:
            print(f"... y {len(errors)-30} errores adicionales", file=sys.stderr)
        return 1
    print("PILA Y FLAGS Aula-8 R0.7: PUSH/POP/PUSHX/POPX/INC/DEC coherentes")
    print(f"Fórmulas Z/N/C/V: {checked_flag_cases} casos matemáticos comparados")
    print("Programa: 14 lecturas + 1 escritura; SP y R0=41 esperados; DEC→JNZ correcto")
    print("CONTROL DOCUMENTAL: APROBADO (NO se ejecutó CPU ni electrónica)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
