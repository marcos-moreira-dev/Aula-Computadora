#!/usr/bin/env python3
"""Verifica coherencia de especificaciones R0.6: NO ejecuta CPU ni micro-ROM."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "simulador-javafx"

ROUTE_ACTIONS = {
    "CALL": ["READ_PC_TO_ADDR_LO", "READ_PC_TO_ADDR_HI", "COPY_PC_LO_TO_RET_LO",
             "COPY_PC_HI_TO_RET_HI", "SUB_TWO_FROM_SP", "LOAD_MAR_FROM_SP",
             "LOAD_MDR_FROM_RET_LO", "WRITE_MDR_AT_MAR",
             "LOAD_MAR_FROM_SP_PLUS_ONE", "LOAD_MDR_FROM_RET_HI",
             "WRITE_MDR_AT_MAR", "LOAD_PC_FROM_ADDR_LO_HI", "END_TO_FETCH"],
    "RET": ["LOAD_MAR_FROM_SP", "READ_MAR_TO_RET_LO", "LOAD_MAR_FROM_SP_PLUS_ONE",
            "READ_MAR_TO_RET_HI", "ADD_TWO_TO_SP", "LOAD_PC_FROM_RET_LO_HI",
            "END_TO_FETCH"],
    "JMP": ["READ_PC_TO_ADDR_LO", "READ_PC_TO_ADDR_HI",
            "LOAD_PC_FROM_ADDR_LO_HI", "END_TO_FETCH"],
}


def main() -> int:
    try:
        spec = json.loads((ROOT / "MICROFLUJO_AULA8_R0_6_BORRADOR.json").read_text(encoding="utf-8"))
        isa = json.loads((ROOT / "ISA_AULA8_CANDIDATA.json").read_text(encoding="utf-8"))
        control = json.loads((ROOT / "MICROSECUENCIAS_AULA8_BORRADOR.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR de archivo/JSON: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []

    def require(ok: bool, message: str) -> None:
        if not ok:
            errors.append(message)

    require(spec.get("status") == "propuesta_no_aprobada", "La especificación no está aprobada")
    require(spec.get("project_release") == "R0.6", "Release incorrecto")
    require(spec.get("granularity") == "acciones_logicas_no_ciclos_de_reloj",
            "No equiparar acciones con ciclos físicos")
    require(spec.get("control_rom_word_bits") is None and spec.get("exact_clock_cycles") is None,
            "No inventar tamaño de ROM de control ni ciclos")
    require(spec.get("cpu_executed") is False and spec.get("electrical_validation") is False,
            "La verificación no debe declarar CPU o electricidad probadas")
    require(control.get("status") == "propuesta_no_aprobada",
            "R0.5 aún tiene estados no aprobados")
    require([s["action"] for s in control.get("common_fetch", [])] ==
            ["READ_PC_TO_IR", "DISPATCH_OPCODE"], "Cambió fetch común")
    require(isa.get("status") == "propuesta_no_aprobada", "ISA aún no aprobada")

    stack = spec.get("stack_convention", {})
    require(stack.get("initial_sp_candidate") == 0x8000, "SP inicial incompatible con R0.3")
    require(stack.get("call_subtracts_from_sp") == 2 and stack.get("ret_adds_to_sp") == 2,
            "CALL/RET deben mover SP dos bytes")
    require(stack.get("return_low_at_sp") is True and stack.get("return_high_at_sp_plus_one") is True,
            "Retorno debe ser little-endian contiguo")
    require(stack.get("ret_does_not_clear_memory") is True, "RET no limpia automáticamente RAM")
    require(stack.get("stack_bounds_hardware_checked") is False,
            "No se ha construido protección de límites de pila")
    require(set(spec.get("extra_candidate_latches", [])) == {"RET_LO", "RET_HI"},
            "Se necesitan latches de retorno propuestos")
    require(set(spec.get("reuse_candidate_latches", [])) == {"ADDR_LO", "ADDR_HI"},
            "Se debe conservar dirección de destino al escribir la pila")

    isa_ops = {item["mnemonic"]: (item["opcode"], item["format"])
               for item in isa.get("instructions", [])}
    for name, expected_opcode, expected_format in [
        ("CALL", "35", "imm16"), ("RET", "02", "none"),
        ("JMP", "30", "imm16"), ("JZ", "31", "imm16"),
        ("JNZ", "32", "imm16"), ("JC", "33", "imm16"),
        ("JNC", "34", "imm16")
    ]:
        require(isa_ops.get(name) == (expected_opcode, expected_format),
                f"Opcode/formato cambió: {name}")

    routes = spec.get("routes", {})
    require(set(routes) == set(ROUTE_ACTIONS), "Rutas explícitas R0.6 inesperadas")
    all_steps: list[dict] = []
    for name, expected in ROUTE_ACTIONS.items():
        route = routes.get(name, {})
        require(route.get("opcode") == isa_ops.get(name, (None,))[0],
                f"Opcode de ruta incorrecto: {name}")
        steps = route.get("states", [])
        require([s.get("action") for s in steps] == expected,
                f"Orden de microacciones incorrecto: {name}")
        all_steps.extend(steps)
        if steps:
            require(steps[-1].get("next") == "FETCH_OPCODE", f"{name} no retorna a fetch")

    branches = spec.get("conditional_branches", [])
    expected_branches = {"JZ": ("31", "Z", 1), "JNZ": ("32", "Z", 0),
                         "JC": ("33", "C", 1), "JNC": ("34", "C", 0)}
    require({b.get("mnemonic") for b in branches} == set(expected_branches),
            "Faltan condiciones de salto")
    for branch in branches:
        name = branch.get("mnemonic")
        require((branch.get("opcode"), branch.get("flag"), branch.get("equals")) ==
                expected_branches.get(name), f"Condición incorrecta: {name}")

    template = spec.get("conditional_branch_shared_route", [])
    require([s.get("action") for s in template] ==
            ["READ_PC_TO_ADDR_LO", "READ_PC_TO_ADDR_HI", "CHECK_FLAG",
             "LOAD_PC_FROM_ADDR_LO_HI", "END_TO_FETCH"],
            "Plantilla de branch debe consumir dos operandos antes de evaluar")
    all_steps.extend(template)
    ids = [s.get("id") for s in all_steps]
    require(len(ids) == len(set(ids)) and all(isinstance(i, str) and i for i in ids),
            "Identificadores duplicados o vacíos")
    allowed_targets = set(ids) | {"FETCH_OPCODE"}
    for step in all_steps:
        state = step.get("id", "?")
        action = step.get("action", "")
        bus = step.get("bus")
        require(bus in {"read", "write", "none"}, f"{state}: conflicto o bus inválido")
        require(step.get("flags_write") is False, f"{state}: control de flujo altera flags")
        if action.startswith("READ_PC_TO_"):
            require(bus == "read" and step.get("pc_advance") is True,
                    f"{state}: lectura de operando sin avance de PC")
        elif action.startswith("READ_MAR_TO_"):
            require(bus == "read" and step.get("pc_advance") is False,
                    f"{state}: leer pila no incrementa PC")
        elif action == "WRITE_MDR_AT_MAR":
            require(bus == "write" and step.get("pc_advance") is False,
                    f"{state}: escritura de pila inválida")
        else:
            require(bus == "none" and step.get("pc_advance") is False,
                    f"{state}: operación interna usa bus o incrementa PC")
        targets = [step.get(k) for k in ("next", "next_taken", "next_not_taken") if k in step]
        require(bool(targets) and all(t in allowed_targets for t in targets),
                f"{state}: transición sin destino válido")

    test = next((s for s in template if s.get("id") == "BR_TEST"), {})
    require(test.get("next_taken") == "BR_COMMIT" and
            test.get("next_not_taken") == "BR_END", "Un salto no tomado no debe cargar PC")

    call_steps = routes.get("CALL", {}).get("states", [])
    require(sum(s.get("bus") == "write" for s in call_steps) == 2,
            "CALL escribe exactamente dos bytes en pila")
    ret_steps = routes.get("RET", {}).get("states", [])
    require(sum(s.get("bus") == "read" for s in ret_steps) == 2,
            "RET lee exactamente dos bytes desde pila")
    for name in ("JMP",):
        require(sum(s.get("bus") == "read" for s in routes.get(name, {}).get("states", [])) == 2,
                "JMP lee ambos bytes de destino")
    require(sum(s.get("bus") == "read" for s in template) == 2,
            "Cada salto condicional lee ambos bytes incluso si no salta")

    # Reconstrucción estructural de una traza esperada a partir de bytes y ABI,
    # NO emulación de una CPU. Se contrasta una especificación contra otra.
    example = spec.get("example", {})
    memory: dict[int, int] = {}
    for seg in example.get("segments", []):
        code = bytes.fromhex(seg.get("bytes_hex", ""))
        for i, value in enumerate(code):
            address = seg["origin"] + i
            require(address not in memory, "Segmentos solapados en ejemplo")
            memory[address] = value

    start = example.get("initial_pc", -1)
    sp = example.get("initial_sp", -1)
    require((start, sp) == (0x6000, 0x8000), "Inicio del ejemplo incompatibile")
    require(memory.get(start) == 0x35, "El ejemplo debe comenzar con CALL")
    require(memory.get(start + 3) == 0x01, "Al volver, debe ejecutarse HALT")
    require(memory.get(0x6010) == 0x11 and memory.get(0x6011) == 0x00 and
            memory.get(0x6013) == 0x02, "La subrutina debe cargar R0 y retornar")
    target = memory.get(start + 1, 0) | (memory.get(start + 2, 0) << 8)
    return_pc = start + 3
    require(target == 0x6010, "Destino de CALL mal codificado")
    low, high = return_pc & 255, return_pc >> 8
    pushed_sp = sp - 2
    require(0 <= pushed_sp <= 0x7FFE, "Pila de prueba fuera de RAM")
    if memory.get(target + 2) is None:
        errors.append("Falta inmediato de subrutina")
    loaded_value = memory.get(target + 2, -1)

    expected_trace: list[dict[str, int | str]] = []

    def read(address: int, value: int) -> None:
        expected_trace.append({"operation": "read", "address": address, "value": value})

    def write(address: int, value: int) -> None:
        expected_trace.append({"operation": "write", "address": address, "value": value})

    for pos in (start, start + 1, start + 2):
        read(pos, memory.get(pos, -1))
    write(pushed_sp, low)
    write(pushed_sp + 1, high)
    for pos in (target, target + 1, target + 2, target + 3):
        read(pos, memory.get(pos, -1))
    read(pushed_sp, low)
    read(pushed_sp + 1, high)
    read(return_pc, memory.get(return_pc, -1))
    require(example.get("expected_trace") == expected_trace,
            "La traza de 12 transacciones no corresponde a programa/pila R0.6")
    require((sum(t["operation"] == "read" for t in expected_trace),
             sum(t["operation"] == "write" for t in expected_trace)) == (10, 2),
            "Se esperaban diez lecturas y dos escrituras")
    require(example.get("expected_final") == {
        "pc": return_pc + 1,
        "sp": sp,
        "r0": loaded_value,
        "halted": True,
        "flags": "preserved_unknown_initial",
        "stack_residual_bytes": {"low_at": pushed_sp, "low": low,
                                 "high_at": pushed_sp + 1, "high": high}
    }, "Estado final documental inconsistente")
    require(example.get("exact_clock_cycles") is None, "Ningún ciclo físico calculado")

    branch = spec.get("branch_example", {})
    encoded = bytes.fromhex(branch.get("encoded_bytes", ""))
    require(len(encoded) == 3 and encoded[0] == 0x32, "JNZ tiene tres bytes")
    if len(encoded) == 3:
        require(branch.get("target") == encoded[1] | (encoded[2] << 8),
                "Destino JNZ debe ser little-endian")
        require(branch.get("fallthrough") == branch.get("instruction_address", 0) + 3,
                "JNZ no tomado consume tres bytes")
    z_values = branch.get("observed_z_assumed_from_dec", [])
    require(branch.get("mnemonic") == "JNZ" and branch.get("expected_taken") ==
            [z == 0 for z in z_values] and z_values == [0, 0, 1],
            "JNZ debe tomar dos saltos y dejar pasar el tercero")
    require(branch.get("dec_microcontrol_implemented") is False,
            "No atribuir microcódigo a DEC todavía")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("FLUJO Aula-8 R0.6 BORRADOR: CALL/RET/JMP/JZ/JNZ/JC/JNC coherentes")
    print("Ejemplo: 10 lecturas + 2 escrituras, retorno 6003, SP recuperado, R0=42")
    print("JNZ: dos saltos tomados y uno no tomado; sin ejecución de CPU ni ciclos medidos")
    print("CONTROL DOCUMENTAL: APROBADO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
