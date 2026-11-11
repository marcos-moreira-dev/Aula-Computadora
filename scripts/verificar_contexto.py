#!/usr/bin/env python3
"""Verificación documental del contexto portable, sin dependencias externas."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md",
    "AGENTS.md",
    "CONTEXTO_MAESTRO.md",
    "DECISIONES.md",
    "ARQUITECTURA.md",
    "HOJA_DE_RUTA.md",
    "MATRIZ_TRAZABILIDAD.md",
    "POLITICA_CALIDAD.md",
    "REFERENCIAS.md",
    "PUBLICAR_GITHUB.md",
    "ESTADO_PORTABLE.json",
    "libro/README.md",
    "libro/CONTRATO_EDITORIAL.md",
    "libro/CURRICULO.md",
    "simulador-javafx/README.md",
    "simulador-javafx/ESPECIFICACION_FUNCIONAL.md",
    "simulador-javafx/ISA_Y_COMPILADORES.md",
    "simulador-javafx/FIRMWARE_Y_ALMACENAMIENTO.md",
    "simulador-javafx/PROGRAMACION_DESDE_CERO.md",
    "simulador-javafx/PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md",
    "simulador-javafx/ISA_AULA8_CANDIDATA.md",
    "simulador-javafx/ISA_AULA8_CANDIDATA.json",
    "scripts/verificar_isa_aula8_borrador.py",
    "simulador-javafx/MICROARQUITECTURA_AULA8_BORRADOR.md",
    "simulador-javafx/MICROTRAZA_AULA8_BORRADOR.json",
    "scripts/verificar_microtraza_aula8_borrador.py",
    "simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md",
    "simulador-javafx/MICROSECUENCIAS_AULA8_BORRADOR.json",
    "scripts/verificar_microsecuencias_aula8_borrador.py",
    "simulador-javafx/CONTROL_FLUJO_PILA_AULA8_BORRADOR.md",
    "simulador-javafx/MICROFLUJO_AULA8_R0_6_BORRADOR.json",
    "scripts/verificar_flujo_aula8_r0_6_borrador.py",
    "simulador-javafx/PILA_Y_BANDERAS_AULA8_BORRADOR.md",
    "simulador-javafx/MICRODATOS_PILA_FLAGS_AULA8_R0_7_BORRADOR.json",
    "scripts/verificar_pila_flags_aula8_r0_7_borrador.py",
    "simulador-javafx/DIRECCIONAMIENTO_INDEXADO_AULA8_BORRADOR.md",
    "simulador-javafx/MICROINDICES_AULA8_R0_8_BORRADOR.json",
    "scripts/verificar_indices_aula8_r0_8_borrador.py",
    "simulador-javafx/AJUSTES_X_SP_Y_MARCOS_AULA8_BORRADOR.md",
    "simulador-javafx/MICROAJUSTES_AULA8_R0_9_BORRADOR.json",
    "scripts/verificar_ajustes_aula8_r0_9_borrador.py",
    "simulador-javafx/ABI_MINIC_AULA8_R0_10_BORRADOR.md",
    "simulador-javafx/ABI_MINIC_AULA8_R0_10_BORRADOR.json",
    "scripts/verificar_abi_minic_aula8_r0_10_borrador.py",
    "simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.md",
    "simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.json",
    "scripts/verificar_rom_monitor_aula8_r0_11_borrador.py",
    "simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md",
    "simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.json",
    "scripts/modelo_bloques_aula8_r0_12.py",
    "scripts/verificar_bloques_aula8_r0_12_borrador.py",
    "simulador-javafx/EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md",
    "simulador-javafx/EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.json",
    "scripts/modelo_ejecutable_aula8_r0_13.py",
    "scripts/empaquetar_aex_aula8_r0_13.py",
    "scripts/verificar_ejecutable_aula8_r0_13_borrador.py",
    "simulador-javafx/LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md",
    "simulador-javafx/LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.json",
    "scripts/modelo_loadx_aula8_r0_14.py",
    "scripts/verificar_loadx_aula8_r0_14_borrador.py",
    "libro/ESTADO_Y_PENDIENTES_R0_14.md",
)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"Falta: {relative}")

    try:
        state = json.loads((ROOT / "ESTADO_PORTABLE.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"ESTADO_PORTABLE.json inválido: {exc}")
        state = {}

    if state:
        architecture = state.get("architecture", {})
        if architecture.get("aula16", {}).get("external_data_bus_bits") != 16:
            errors.append("Aula-16 debe conservar el bus EXTERNO de 16 bits")
        if architecture.get("aula8", {}).get("external_data_bus_bits") != 8:
            errors.append("Aula-8 debe conservar el bus EXTERNO de 8 bits")
        if architecture.get("addressable_bytes") != 65536:
            errors.append("Las dos CPU deben mantener 64 KiB de espacio direccionable")
        if state.get("repositories", {}).get("desired_github_repository_count") != 1:
            errors.append("El libro y la aplicación deben compartir un GitHub")
        if state.get("editorial", {}).get("independent_of_javafx") is not True:
            errors.append("El libro debe ser autónomo y no referenciar JavaFX")
        programming = state.get("programming_from_zero", {})
        if programming.get("native_line_editor_on_aula8") != "confirmado_no_implementado":
            errors.append("Conservar editor de líneas nativo Aula-8 como confirmado y pendiente")
        if programming.get("native_assembler_on_aula8") != "confirmado_no_implementado":
            errors.append("Conservar ensamblador nativo Aula-8 como confirmado y pendiente")
        if programming.get("minic_native_compiler_v1") is not False:
            errors.append("No exigir MiniC nativo en V1")
        if programming.get("native_execution_must_run_on_aula_cpu") is not True:
            errors.append("Las herramientas nativas deben correr en CPU Aula")
        budget = state.get("software_memory_budget_proposal", {})
        if budget.get("status") != "provisional_not_measured":
            errors.append("El presupuesto de RAM/ROM sigue siendo una propuesta no medida")
        if sum(budget.get("firmware_rom_budget_sections_bytes", [])) != 8192:
            errors.append("La suma de presupuesto ROM debe dar exactamente 8192 B")
        if sum(budget.get("aula8_ram_partition_bytes", [])) != 32768:
            errors.append("La suma de particiones RAM debe dar exactamente 32768 B")
        if budget.get("native_editor_and_assembler_same_overlay") is not True:
            errors.append("La propuesta conserva una región overlay compartida")
        candidate = state.get("aula8_isa_candidate", {})
        if candidate.get("status") != "propuesta_no_aprobada":
            errors.append("La ISA de Aula-8 aún es PROPUESTA, no aprobada")
        if candidate.get("opcode_count") != 36 or candidate.get("sample_program_count") != 3:
            errors.append("Conservar los 36 opcodes y tres muestras candidatas R0.3")
        if candidate.get("cpu_execution_verified") is not False:
            errors.append("No atribuir ejecución real a la verificación documental de ISA")
        micro = state.get("aula8_microarchitecture_candidate", {})
        if micro.get("status") != "propuesta_no_aprobada":
            errors.append("La microarquitectura de Aula-8 sigue siendo propuesta")
        if micro.get("address_bus_bits") != 16 or micro.get("external_data_bus_bits") != 8:
            errors.append("No modificar buses de Aula-8 en la propuesta de datapath")
        if micro.get("bus_trace_events_expected") != 9:
            errors.append("El ejemplo previsto cuenta con ocho lecturas y una escritura")
        if micro.get("bus_trace_executed") is not False or micro.get("microcode_implemented") is not False:
            errors.append("No declarar ejecución o microcódigo inexistentes")
        control = state.get("aula8_control_candidate", {})
        if control.get("status") != "propuesta_no_aprobada":
            errors.append("Las secuencias de control R0.5 no están aprobadas")
        if control.get("logical_sequence_names") != ["LDI", "ST_ABS", "HALT"]:
            errors.append("El alcance R0.5 debe permanecer en tres rutas lógicas")
        if control.get("logical_actions_not_clock_cycles") is not True:
            errors.append("No confundir acciones lógicas con ciclos físicos")
        if control.get("control_rom_word_bits") is not None or control.get("cpu_executed") is not False:
            errors.append("No declarar microcódigo o ejecución física inexistente")
        flow = state.get("aula8_control_flow_candidate", {})
        if flow.get("status") != "propuesta_no_aprobada":
            errors.append("CALL/RET/saltos R0.6 no son especificación aprobada")
        if flow.get("microcontrol_executed") is not False or flow.get("physical_validation") is not False:
            errors.append("No se ha ejecutado microcontrol o medido hardware R0.6")
        if flow.get("expected_bus_transactions") != {"read": 10, "write": 2}:
            errors.append("La traza de CALL/RET R0.6 debe contar diez lecturas y dos escrituras")
        if flow.get("call_return_byte_order") != "little_endian_low_at_sp":
            errors.append("El retorno CALL/RET debe conservar low byte en [SP]")
        stackflags = state.get("aula8_stack_flags_candidate", {})
        if stackflags.get("status") != "propuesta_no_aprobada":
            errors.append("Pila/flags R0.7 siguen siendo propuestas")
        if stackflags.get("inc_dec_preserve_c") is not True:
            errors.append("INC/DEC deben preservar C en ISA candidata")
        if stackflags.get("cpu_executed") is not False or stackflags.get("electrical_validation") is not False:
            errors.append("No atribuir implementación física a los controles R0.7")
        if stackflags.get("expected_bus_transactions") != {"read": 14, "write": 1}:
            errors.append("La traza de R0.7 debe tener catorce lecturas y una escritura")
        indexed = state.get("aula8_indexed_addressing_candidate", {})
        if indexed.get("status") != "propuesta_no_aprobada":
            errors.append("R0.8 y sus direcciones X/SP siguen siendo propuesta documental")
        if indexed.get("address_bits") != 16 or indexed.get("external_data_bus_bits") != 8:
            errors.append("Conservar las direcciones de 16 bits y datos de 8 bits de Aula-8")
        if indexed.get("signed_range") != [-128, 127] or indexed.get("address_calculation") != "two_pass_alu8_private_carry":
            errors.append("Conservar extensión de signo y dos pasos ALU8 con acarreo privado")
        if indexed.get("flags_preserved") is not True or indexed.get("cpu_executed") is not False:
            errors.append("No modificar flags ni declarar CPU ejecutada en R0.8")
        if indexed.get("adjsp_microcontrol_implemented") is not False or indexed.get("electrical_validation") is not False:
            errors.append("No declarar ADJSP o electrónica implementada")
        if indexed.get("mathematical_address_checks") != 526592 or indexed.get("expected_bus_transactions") != {"read": 14, "write": 1}:
            errors.append("Mantener cobertura y transacciones documentales R0.8")
        adjust = state.get("aula8_stack_frame_candidate", {})
        if adjust.get("status") != "propuesta_no_aprobada":
            errors.append("R0.9 y sus ajustes de X/SP deben permanecer candidatos")
        if adjust.get("logical_sequence_names") != ["LEAX", "ADDXW", "SETSP", "ADJSP", "XFROMSP"]:
            errors.append("R0.9 debe conservar las cinco instrucciones de la ISA candidata")
        if adjust.get("datapath_bits") != 8 or adjust.get("address_bits") != 16 or adjust.get("external_data_bus_bits") != 8:
            errors.append("R0.9 debe conservar datapath8 y direcciones16 de Aula-8")
        if adjust.get("abi_final") is not False or adjust.get("stack_overflow_hardware_detection") is not False:
            errors.append("No declarar ABI final ni protecciones físicas de pila")
        if adjust.get("cpu_executed") is not False or adjust.get("electrical_validation") is not False:
            errors.append("No declarar implementación CPU o eléctrica inexistente")
        if adjust.get("visible_flags_preserved") is not True or adjust.get("private_address_carry") is not True:
            errors.append("Aritmética de ajustes debe preservar flags y usar carry privado")
        if adjust.get("mathematical_checks") != 1572864 or adjust.get("expected_bus_transactions") != {"read": 29, "write": 5}:
            errors.append("Cobertura y transacciones documentales R0.9 incoherentes")
        abi = state.get("aula8_minic_abi_candidate", {})
        if abi.get("status") != "propuesta_no_aprobada":
            errors.append("R0.10 y su ABI deben seguir siendo propuestas no aprobadas")
        if abi.get("parameter_slot_bytes") != 2 or abi.get("maximum_parameters") != 4:
            errors.append("MiniC debe conservar ranuras de 2B y máximo candidato de cuatro parámetros")
        if abi.get("push_word_order") != ["high", "low"] or abi.get("arguments_order") != "right_to_left":
            errors.append("Orden de argumentos y bytes incompatible con pila descendente")
        if abi.get("caller_cleanup") is not True or abi.get("callee_saved") != ["R2", "R3", "X"]:
            errors.append("Restauración de registros y limpieza de parámetros incorrectas")
        if abi.get("fixed_frame_first_argument_offset") != 6 or abi.get("u16_return") != "R1_high_R0_low":
            errors.append("Offsets de marco o retorno u16 inconsistentes")
        if abi.get("aula16_external_data_bus_bits") != 16 or abi.get("cpu_executed") is not False:
            errors.append("No alterar Aula-16 ni declarar CPU ejecutada")
        if abi.get("compiler_implemented") is not False or abi.get("abi_final") is not False:
            errors.append("No declarar MiniC o ABI aprobada inexistentes")
        if abi.get("frame_layout_checks") != 640 or abi.get("expected_bus_transactions") != {"read": 73, "write": 10}:
            errors.append("Cobertura y transacciones ABI documental R0.10 incoherentes")
        firmware = state.get("aula8_rom_monitor_candidate", {})
        if firmware.get("status") != "propuesta_no_aprobada":
            errors.append("R0.11 y su firmware/monitor siguen siendo propuestas no aprobadas")
        if firmware.get("table_start") != "0xFF00" or firmware.get("table_reserved_bytes") != 128:
            errors.append("R0.11: 32 entradas de 4 B deben empezar en FF00")
        if firmware.get("defined_public_services") != ["FW_PUTC", "FW_GETC", "FW_PUTS", "FW_STATUS"]:
            errors.append("Conservar cuatro nombres de rutinas ROM")
        if firmware.get("reset_vector") != "0xFFFC-0xFFFD":
            errors.append("RESET debe conservar FFFC/FFFD")
        if firmware.get("monitor_run_method") != "CALL" or firmware.get("halt_returns_to_prompt") is not False:
            errors.append("RUN=CALL y HALT no equivale a RET")
        if firmware.get("poke_window") != "0x6000-0x6FFF":
            errors.append("La ventana POKE candidata debe ser memoria de práctica")
        if firmware.get("monitor_parser_vectors") != 30 or firmware.get("load_and_reg_available") is not False:
            errors.append("Se esperan 30 vectores y REG/LOAD pendientes en R0.11")
        if firmware.get("firmware_implemented") is not False or firmware.get("cpu_executed") is not False:
            errors.append("No declarar ROM ni CPU ejecutadas en R0.11")
        if firmware.get("aula16_external_data_bus_bits") != 16:
            errors.append("Aula-16 continúa con bus externo de 16 bits")
        storage = state.get("aula8_block_storage_candidate", {})
        if storage.get("status") != "propuesta_no_aprobada":
            errors.append("R0.12 debe declarar almacenamiento candidato, no aprobado")
        if storage.get("mmio_range") != "0xC010-0xC01F" or storage.get("block_bytes") != 256:
            errors.append("Conservar controlador C010-C01F y bloques de 256 B")
        if storage.get("register_count") != 8 or storage.get("controller_hardware_implemented") is not False:
            errors.append("Ocho registros propuestos; sin controlador físico")
        if storage.get("load_implemented") is not False or storage.get("filesystem_implemented") is not False:
            errors.append("LOAD y sistema de archivos continúan sin implementación")
        if storage.get("reference_tests") != 20 or storage.get("host_reference_model_tested") is not True:
            errors.append("R0.12 exige veinte pruebas de modelo anfitrión")
        if storage.get("cpu_executed") is not False or storage.get("aula16_external_data_bus_bits") != 16:
            errors.append("No declarar CPU ejecutada ni cambiar bus de Aula-16")
        aex = state.get("aula8_aex1_executable_candidate", {})
        if aex.get("status") != "propuesta_no_aprobada":
            errors.append("R0.13 debe declarar AEX1 candidato, no aprobado")
        if aex.get("format_magic") != "AEX1" or aex.get("header_bytes") != 32 or aex.get("sector_bytes") != 256:
            errors.append("AEX1 exige cabecera de 32 B sobre bloques de 256 B")
        if aex.get("target_cpu_id") != 8 or aex.get("maximum_blocks") != 32:
            errors.append("AEX1 R0.13 se diseñó solo para Aula-8, máximo 32 bloques")
        if aex.get("practice_window") != "0x6000-0x6FFF" or aex.get("tool_overlay_window") != "0x1000-0x2FFF":
            errors.append("Ventanas RAM por tipo AEX1 incorrectas")
        if aex.get("practice_max_payload_bytes") != 4064 or aex.get("tool_max_payload_bytes") != 8160:
            errors.append("Presupuesto de payload AEX1 incorrecto")
        if aex.get("header_and_payload_crc") != "CRC-16/CCITT-FALSE":
            errors.append("Mantener CRC16 sobre cabecera y payload")
        if aex.get("firmware_staging_buffer_bytes") != 3584 or aex.get("atomic_native_load_demonstrated") is not False:
            errors.append("No afirmar staging nativo atómico en 3584 B")
        if aex.get("host_reference_test_count") != 42 or aex.get("host_reference_tested") is not True:
            errors.append("AEX1 R0.13 exige 42 pruebas Python de anfitrión")
        if not aex.get("raw_load_preserved"):
            errors.append("R0.13 nunca sustituye LOAD crudo por LOADX")
        for field in ("loadx_implemented", "native_loader_implemented", "firmware_implemented", "assembler_implemented", "cpu_executed"):
            if aex.get(field) is not False:
                errors.append(f"AEX1 solo propone; {field} debe ser false")
        if aex.get("aula16_external_data_bus_bits") != 16:
            errors.append("Aula-16 conserva bus externo 16 bits")
        loadx = state.get("aula8_loadx_two_pass_candidate", {})
        if state.get("baseline") != "R0.14" or loadx.get("status") != "propuesta_no_aprobada":
            errors.append("R0.14 debe conservar LOADX de dos pasadas NO aprobado")
        if loadx.get("first_pass") != "verify_entire_package_incremental_crc":
            errors.append("LOADX primera pasada debe verificar todo sin escribir RAM")
        if loadx.get("second_pass") != "copy_payload_incremental_crc":
            errors.append("LOADX segunda pasada debe revalidar CRC incremental")
        if loadx.get("staging_block_bytes") != 256 or loadx.get("full_tool_staging_required") is not False:
            errors.append("No exigir staging completo del programa de herramientas")
        if loadx.get("ram_fully_atomic") is not False or loadx.get("preflight_error_writes_program_ram") is not False:
            errors.append("LOADX no es atómico; preflight debe conservar RAM")
        if loadx.get("second_pass_error_may_leave_partial_ram") is not True:
            errors.append("No ocultar RAM parcial tras fallo de segunda pasada")
        if loadx.get("execution_gate_implemented_in_firmware") is not False:
            errors.append("No declarar control RUN de firmware inexistente")
        if loadx.get("cpu_executed") is not False or loadx.get("native_loader_implemented") is not False:
            errors.append("No atribuir CPU ni cargador nativo a modelo Python R0.14")
        if loadx.get("host_reference_test_count") != 30 or loadx.get("host_reference_tested") is not True:
            errors.append("LOADX exige 30 pruebas de anfitrión")
        if loadx.get("aula16_external_data_bus_bits") != 16:
            errors.append("Aula-16 conserva bus externo de 16 bits")
        book = state.get("book_readiness_r014", {})
        if book.get("curriculum_chapters") != 24 or book.get("chapters_finished") != 0:
            errors.append("Libro: currículo 24, capítulos terminados 0")
        if book.get("manuscript_docx_ready") is not False or book.get("final_pdf_ready") is not False:
            errors.append("No declarar Word/PDF del libro completados")
        if book.get("cover_excluded_from_audit") is not True or book.get("can_begin_chapter_one_now") is not True:
            errors.append("Auditoría libro excluye portada y permite empezar capítulo uno")

    checked_links = 0
    docs = list(ROOT.rglob("*.md"))
    for md in docs:
        contents = md.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(contents):
            target = match.group(1)
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            local_target = target.split("#", 1)[0]
            if not local_target:
                continue
            checked_links += 1
            if not (md.parent / local_target).exists():
                errors.append(f"Enlace roto: {md.relative_to(ROOT)} -> {target}")

    print(f"{state.get('baseline', 'R0')}: {len(docs)} documentos Markdown; {checked_links} enlaces locales comprobados.")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("CONTEXTO Y ESTRUCTURA: APROBADOS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
