#!/usr/bin/env python3
"""Contrasta caracteres, programas y artefactos C18 sin ejecutar CPU Aula-8."""

import json
from verificar_capitulos_16_17_comun import ROOT, verificar_documentos
from generar_diagramas_tecnicos_aula8 import check_contracts
from verificar_rom_monitor_aula8_r0_11_borrador import parse_monitor


def interpretacion_en_papel(program, origin=0x6000):
    """Lee solo LDI/ST/CALL/RET/SETX para comprobar bytes y direcciones.

    No simula las rutinas de ROM ni una máquina de estados de CPU.
    """
    pos = 0
    instructions = []
    while pos < len(program):
        start = origin+pos
        op = program[pos]
        if op in (0x11,):
            assert pos+3 <= len(program)
            assert 0 <= program[pos+1] <= 3
            instructions.append((start, 'LDI', (program[pos+1], program[pos+2])))
            pos += 3
        elif op == 0x13:
            assert pos+4 <= len(program)
            selector = program[pos+1]
            assert selector <= 3  # registro absoluto modo 0
            addr = program[pos+2] | program[pos+3] << 8
            instructions.append((start, 'ST', (selector, addr)))
            pos += 4
        elif op in (0x14, 0x35):
            assert pos+3 <= len(program)
            addr = program[pos+1] | program[pos+2] << 8
            instructions.append((start, 'SETX' if op == 0x14 else 'CALL', (addr,)))
            pos += 3
        elif op == 0x02:
            instructions.append((start, 'RET', ()))
            pos += 1
        else:
            raise AssertionError(f'opcode inesperado {op:02X}')
    return instructions


def main():
    rom, storage, services, _ = check_contracts()
    isa = json.loads((ROOT/'simulador-javafx/ISA_AULA8_CANDIDATA.json').read_text(encoding='utf-8'))
    assert isa['status'] == 'propuesta_no_aprobada'
    assert not rom['firmware_implemented'] and not rom['cpu_executed']
    assert not storage['controller_hardware_implemented']
    assert rom['firmware_abi_candidate']['callee_saved_registers'] == ['R2', 'R3', 'X']
    checks = 4

    programs = {
        'mostrar_a': bytes.fromhex('11 00 41 35 00 FF 02'),
        'eco': bytes.fromhex('35 04 FF 35 00 FF 02'),
        'eco_con_variable': bytes.fromhex('35 04 FF 13 00 00 6F 35 00 FF 02'),
        'puts_hola': bytes.fromhex('14 00 61 35 08 FF 02'),
    }
    assert programs['mostrar_a'].hex(' ').upper() == rom['reference_program']['bytes_hex']
    assert len(programs['mostrar_a']) == len(programs['eco']) == len(programs['puts_hola']) == 7
    assert len(programs['eco_con_variable']) == 11
    assert interpretacion_en_papel(programs['mostrar_a']) == [
        (0x6000, 'LDI', (0, 0x41)), (0x6003, 'CALL', (0xFF00,)), (0x6006, 'RET', ())]
    assert interpretacion_en_papel(programs['eco']) == [
        (0x6000, 'CALL', (0xFF04,)), (0x6003, 'CALL', (0xFF00,)), (0x6006, 'RET', ())]
    assert interpretacion_en_papel(programs['eco_con_variable']) == [
        (0x6000, 'CALL', (0xFF04,)), (0x6003, 'ST', (0, 0x6F00)),
        (0x6007, 'CALL', (0xFF00,)), (0x600A, 'RET', ())]
    assert interpretacion_en_papel(programs['puts_hola']) == [
        (0x6000, 'SETX', (0x6100,)), (0x6003, 'CALL', (0xFF08,)), (0x6006, 'RET', ())]
    checks += 8

    for data in range(256):
        # Proyección semántica de byte devuelto por GETC, ST y PUTC.
        ram = {0x6F00: data}
        emitted = data  # PUTC puede alterar R0 DESPUÉS de consumir el parámetro.
        assert ram[0x6F00] == emitted
        assert (data & 0xFF) == data
        checks += 2

    name_to_slot = {item['name']: int(item['slot'], 16) for item in rom['public_services']}
    for name in ('FW_GETC', 'FW_PUTC', 'FW_PUTS', 'FW_STATUS'):
        assert name_to_slot[name] == int(services[name], 16)
        assert 0xFF00 <= name_to_slot[name] <= 0xFF0C
        checks += 2
    for text in ('A', 'HOLA'):
        code = text.encode('ascii')
        assert len(code) == len(text)
        assert all(byte < 0x80 for byte in code)
        checks += 2
    hola = b'HOLA\x00'
    assert hola == bytes.fromhex('48 4F 4C 41 00')
    assert hola[-1] == 0 and len(hola) == 5
    checks += 2

    for case in rom['example_monitor_vectors']:
        command, info = parse_monitor(case['line'], rom['monitor_candidate'])
        assert command == case['result'], case
        if 'count' in case:
            assert info['count'] == case['count']
        if 'error' in case:
            assert info['error'] == case['error']
        checks += 1

    checks += verificar_documentos('18', 'hablar_con_la_maquina', (
        'c18_fig01_terminal_y_mmio','c18_fig02_llamada_publica_rom',
        'c18_fig03_eco_con_variable','c18_fig04_cadena_terminada',
    ), 8, ('FW_PUTC', 'FW_GETC', 'FW_PUTS', 'FW_STATUS', 'RAM[',
           '0xC000', '0xC002', 'CALL', 'RET', '00', 'capítulo 19'), ecuaciones=14)
    print(f'Capítulo 18: {checks} comprobaciones correctas de bytes/contratos/Word/PDF; no CPU ni terminal ejecutados.')


if __name__ == '__main__':
    main()
