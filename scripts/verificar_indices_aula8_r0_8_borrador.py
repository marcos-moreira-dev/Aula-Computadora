#!/usr/bin/env python3
"""Valida direccionamiento indexado escrito; no ejecuta CPU ni simula electrónica."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "simulador-javafx"
EXPECTED_ACTIONS = {
    "SETX": ["READ_PC_TO_ADDR_LO", "READ_PC_TO_ADDR_HI", "LOAD_X_FROM_ADDR_LO_HI", "END_TO_FETCH"],
    "LD_INDEXED": ["READ_PC_TO_SEL", "VALIDATE_MODE1_OR2_REGISTER_SEL",
                   "READ_PC_TO_SIGNED_DISP8", "SELECT_BASE_X_OR_SP_BY_MODE",
                   "ADD_BASE_LOW_DISP_TO_ADDR_LO_CARRY",
                   "ADD_BASE_HIGH_SIGN_CARRY_TO_ADDR_HI", "LOAD_MAR_FROM_ADDR_LO_HI",
                   "READ_MAR_TO_MDR", "LOAD_SELECTED_REG_FROM_MDR", "END_TO_FETCH"],
    "ST_INDEXED": ["READ_PC_TO_SEL", "VALIDATE_MODE1_OR2_REGISTER_SEL",
                   "READ_PC_TO_SIGNED_DISP8", "SELECT_BASE_X_OR_SP_BY_MODE",
                   "ADD_BASE_LOW_DISP_TO_ADDR_LO_CARRY",
                   "ADD_BASE_HIGH_SIGN_CARRY_TO_ADDR_HI", "LOAD_MAR_FROM_ADDR_LO_HI",
                   "STAGE_SELECTED_REG_TO_MDR", "WRITE_MDR_AT_MAR", "END_TO_FETCH"],
}


def decode_disp(raw: int) -> int:
    return raw - 256 if raw >= 128 else raw


def two_pass_address(base: int, raw_disp: int) -> int:
    low_total = (base & 0xFF) + raw_disp
    addr_low = low_total & 0xFF
    private_carry = low_total >> 8
    high_extension = 0xFF if raw_disp >= 128 else 0x00
    addr_high = ((base >> 8) + high_extension + private_carry) & 0xFF
    return (addr_high << 8) | addr_low


def main() -> int:
    try:
        model = json.loads((ROOT / "MICROINDICES_AULA8_R0_8_BORRADOR.json").read_text(encoding="utf-8"))
        isa = json.loads((ROOT / "ISA_AULA8_CANDIDATA.json").read_text(encoding="utf-8"))
        micro = json.loads((ROOT / "MICROSECUENCIAS_AULA8_BORRADOR.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR cargando documentos JSON: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []

    def check(ok: bool, message: str) -> None:
        if not ok:
            errors.append(message)

    check(model.get("project_release") == "R0.8" and
          model.get("status") == "propuesta_no_aprobada", "R0.8 aún es propuesta")
    check(model.get("granularity") == "acciones_logicas_no_ciclos_de_reloj", "No fijar ciclos de reloj")
    check(model.get("cpu_executed") is False and model.get("microcode_compiled") is False and
          model.get("electrical_validation") is False and model.get("clock_cycles_known") is False,
          "No presentar comprobaciones documentales como ejecución física")
    check(model.get("word_size_address_bits") == 16 and model.get("external_data_bus_bits") == 8,
          "Los buses externos de Aula-8 no deben cambiar")
    check(model.get("displacement_bits") == 8 and model.get("displacement_signed_range") == [-128, 127] and
          model.get("effective_address_modulus") == 65536, "Desplazamiento y módulo inválidos")
    check(model.get("private_address_carry") is True and
          model.get("preserve_visible_flags") == ["Z", "N", "C", "V"] and
          model.get("preserve_index_and_stack_base_on_ld_st") is True,
          "La aritmética de dirección no debe cambiar X/SP ni Z/N/C/V")
    check(isa.get("status") == "propuesta_no_aprobada" and
          micro.get("status") == "propuesta_no_aprobada", "ISA y microsecuencias siguen candidatas")

    selectors = model.get("selector_convention", {})
    check(selectors.get("absolute_mode") == 0 and selectors.get("x_relative_mode") == 1 and
          selectors.get("sp_relative_mode") == 2 and selectors.get("reserved_mode") == 3,
          "Selector de modo no coincide con R0.3")
    check(selectors.get("allowed_registers") == [0, 1, 2, 3] and
          selectors.get("valid_indexed_selector_ranges") == [[4, 7], [8, 11]],
          "Selector de registro/base indexada incorrecto")
    indexed_valid = 0
    for selector in range(256):
        mode, reg = (selector >> 2) & 0x03, selector & 0x03
        high_nibble_clear = (selector & 0xF0) == 0
        actual_valid = high_nibble_clear and mode in (1, 2) and reg in range(4)
        expected_valid = 4 <= selector <= 11
        check(actual_valid == expected_valid, f"Selector incorrecto 0x{selector:02X}")
        indexed_valid += int(actual_valid)
    check(indexed_valid == 8, "Deben existir cuatro registros por cada uno de dos modos indexados")

    isa_ops = {item["mnemonic"]: (item["opcode"], item["format"])
               for item in isa.get("instructions", [])}
    check(isa_ops.get("SETX") == ("14", "imm16") and
          isa_ops.get("LD") == ("12", "memory") and
          isa_ops.get("ST") == ("13", "memory"), "Opcodes/formato no coinciden con ISA")
    routes = model.get("routes", {})
    check(set(routes) == set(EXPECTED_ACTIONS), "Rutas SETX/LD_INDEXED/ST_INDEXED incompletas")
    all_steps: list[dict] = []
    for name, expected_actions in EXPECTED_ACTIONS.items():
        route = routes.get(name, {})
        opcode = {"SETX": "14", "LD_INDEXED": "12", "ST_INDEXED": "13"}[name]
        check(route.get("opcode") == opcode, f"Opcode de ruta incorrecto: {name}")
        steps = route.get("states", [])
        check([s.get("action") for s in steps] == expected_actions, f"Ruta desordenada: {name}")
        if steps:
            check(steps[-1].get("next") == "FETCH_OPCODE", f"{name} no vuelve a fetch")
        all_steps.extend(steps)

    ids = [s.get("id") for s in all_steps]
    check(len(ids) == len(set(ids)) and all(isinstance(s, str) and s for s in ids),
          "Microestados faltantes/duplicados")
    allowed = set(ids) | {"FETCH_OPCODE", "FAULT"}
    for step in all_steps:
        label = step.get("id", "?")
        act = step.get("action", "")
        bus = step.get("bus")
        check(bus in {"read", "write", "none"}, f"{label}: bus externo indeterminado")
        check(step.get("flags_write") is False, f"{label}: debe preservar flags visibles")
        check(step.get("next") in allowed, f"{label}: destino microcontrol inexistente")
        if "on_invalid" in step:
            check(step["on_invalid"] == "FAULT", f"{label}: selector incorrecto sin ruta de error")
        if act.startswith("READ_PC_TO_"):
            check(bus == "read" and step.get("pc_advance") is True,
                  f"{label}: lectura de operando no incrementa PC")
        elif act.startswith("READ_MAR_TO_"):
            check(bus == "read" and step.get("pc_advance") is False,
                  f"{label}: carga de RAM no debe avanzar PC")
        elif act == "WRITE_MDR_AT_MAR":
            check(bus == "write" and step.get("pc_advance") is False,
                  f"{label}: escritura sin control de bus WR")
        else:
            check(bus == "none" and step.get("pc_advance") is False,
                  f"{label}: microacción interna usa bus externo")

    check(model.get("candidate_alu8_address_steps") == [
        "SIGN_EXTEND_DISP8_TO_HIGH_FF_OR_00",
        "ADD_BASE_LOW_PLUS_DISP_TO_ADDR_LO_AND_PRIVATE_CARRY",
        "ADD_BASE_HIGH_PLUS_SIGN_PLUS_PRIVATE_CARRY_TO_ADDR_HI",
        "LOAD_MAR_FROM_ADDR_LO_HI",
    ], "Cálculo de dirección de dos pasadas incompleto")

    checked_addresses = 0
    # Bordes para TODAS las bases; todos los desplazamientos para bases representativas.
    for base in range(65536):
        for displacement in (0, 1, 2, 127, 128, 254, 255, 64):
            actual = two_pass_address(base, displacement)
            expected = (base + decode_disp(displacement)) & 0xFFFF
            checked_addresses += 1
            if actual != expected:
                errors.append(f"Dirección base=0x{base:04X}, disp={displacement}: {actual} != {expected}")
                break
        if errors:
            break
    for base in (0x0000, 0x0001, 0x00FF, 0x0100, 0x1200, 0x12FF, 0x7FEE, 0x8000, 0xFFFF):
        for displacement in range(256):
            actual = two_pass_address(base, displacement)
            expected = (base + decode_disp(displacement)) & 0xFFFF
            checked_addresses += 1
            if actual != expected:
                errors.append(f"Caso exhaustivo base=0x{base:04X}, disp={displacement}")
                break
        if errors:
            break
    for vector in model.get("edge_vectors", []):
        base, displacement, expected = vector["base"], vector["disp8"], vector["effective"]
        check(two_pass_address(base, displacement) == expected and
              (base + decode_disp(displacement)) & 0xFFFF == expected,
              f"Vector de borde incorrecto: {vector}")

    examples = model.get("examples", {})
    sample = examples.get("x_store_load_42", {})
    code = bytes.fromhex(sample.get("bytes_hex", ""))
    expected_bytes = bytes.fromhex("14 00 6F 11 00 2A 13 04 01 12 05 01 01")
    origin = sample.get("origin")
    check(origin == 0x6000 and code == expected_bytes,
          "El programa indexado de 13 bytes cambió sin revalidación")
    if origin == 0x6000 and code == expected_bytes:
        x = code[1] | (code[2] << 8)
        reg_value = code[5]
        st_selector, st_disp = code[7], code[8]
        ld_selector, ld_disp = code[10], code[11]
        check(st_selector == 0x04 and ld_selector == 0x05,
              "Selectores deben codificar ST R0 y LD R1 modo X")
        effective_store = (x + decode_disp(st_disp)) & 0xFFFF
        effective_load = (x + decode_disp(ld_disp)) & 0xFFFF
        check(effective_store == effective_load == 0x6F01,
              "ST/LD no alcanzan la misma dirección RAM")
        check(0x0000 <= effective_store <= 0x7FFF, "El ejemplo debe acceder RAM, no ROM/E/S")
        expected_trace = []

        def read_instruction(i: int) -> None:
            expected_trace.append({"operation": "read", "address": origin + i, "value": code[i]})

        for i in range(9):
            read_instruction(i)
        expected_trace.append({"operation": "write", "address": effective_store, "value": reg_value})
        for i in range(9, 12):
            read_instruction(i)
        expected_trace.append({"operation": "read", "address": effective_load, "value": reg_value})
        read_instruction(12)
        check(sample.get("expected_trace") == expected_trace,
              "La traza de programa indexado no coincide con sus bytes")
        check((sum(e["operation"] == "read" for e in expected_trace),
               sum(e["operation"] == "write" for e in expected_trace)) == (14, 1),
              "Se esperan 14 lecturas y 1 escritura")
        check(sample.get("expected_final") == {
            "pc": origin + len(code), "x": x, "r0": reg_value, "r1": reg_value,
            "ram_address": effective_store, "ram_value": reg_value,
            "flags": "unknown_preserved", "halted": True
        }, "Estado final declarativo erróneo")
        check(sample.get("initial_flags") == "unknown_preserved",
              "No se deben inventar flags iniciales")

    frame = examples.get("sp_local_frame", {})
    initial_sp, reserve = frame.get("initial_sp", -1), frame.get("reserve_bytes", -1)
    frame_sp = (initial_sp - reserve) & 0xFFFF
    check(initial_sp == 0x7FF0 and reserve == 2 and frame_sp == 0x7FEE,
          "Marco local de ejemplo mal inicializado")
    check(frame.get("sp_after_reservation") == frame_sp and
          frame.get("sp_after_release") == initial_sp,
          "ADJSP -2/+2 debe restituir SP")
    check(frame.get("store_selector") == (2 << 2) | 2 and
          frame.get("load_selector") == (2 << 2) | 3,
          "R2/R3 SP-relativos mal codificados")
    check(frame.get("displacement") == 0 and
          two_pass_address(frame_sp, 0) == frame_sp and
          frame.get("r2_value") == frame.get("r3_after_load") == 0x35,
          "Datos/dirección del marco local incoherentes")
    check(frame.get("adjsp_microcontrol_implemented") is False,
          "ADJSP del ejemplo es solo proyección semántica")

    if errors:
        for error in errors[:25]:
            print(f"ERROR: {error}", file=sys.stderr)
        if len(errors) > 25:
            print(f"... y {len(errors)-25} errores adicionales", file=sys.stderr)
        return 1
    print("INDICES Aula-8 R0.8: SETX, LD/ST por X/SP y selectores coherentes")
    print(f"Direcciones de dos pasadas: {checked_addresses} casos matemáticos contrastados")
    print("Ejemplo SETX/LDI/ST/LD/HALT: 14 lecturas + 1 escritura esperadas")
    print("CONTROL DOCUMENTAL: APROBADO (sin CPU, micro-ROM ni placa ejecutadas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
