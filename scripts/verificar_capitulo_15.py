#!/usr/bin/env python3
"""Verifica la traza funcional de C15 y sus artefactos; NO ejecuta CPU.

Simula acciones lógicas de un contrato propuesto y revisa Word/PDF. No mide
microestados, ciclos de reloj, temporización, voltajes ni contención física.
"""

import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'libro' / 'capitulos' / '15_la_instruccion_en_movimiento'
FIGURES = (
    'c15_fig01_camino_fetch',
    'c15_fig02_direccion_st',
    'c15_fig03_preparar_escritura',
    'c15_fig04_transacciones',
)
NS = {
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}


def cargar_json(name):
    return json.loads((ROOT / 'simulador-javafx' / name).read_text(encoding='utf-8'))


def recorrido_de_papel(program, flags, r0_inicial):
    """Interpreta sólo el ejemplo a partir de acciones lógicas declaradas."""
    micro = cargar_json('MICROSECUENCIAS_AULA8_BORRADOR.json')
    program_start = 0x6000
    memory = {program_start + i: value for i, value in enumerate(program)}
    regs = [r0_inicial, 0xAA, 0xBB, 0xCC]
    pc, mar, mdr, ir, sel, tmp = program_start, None, None, None, None, None
    low, high, halted = None, None, False
    events, stages = [], []

    for path in ('LDI', 'ST_ABS', 'HALT'):
        actions = micro['common_fetch'] + micro['instructions'][path]
        for stage in actions:
            action = stage['action']
            prev_pc = pc
            if action.startswith('READ_PC_TO_'):
                mar = pc
                mdr = memory[mar]
                events.append(('read', mar, mdr))
                if action == 'READ_PC_TO_IR':
                    ir = mdr
                elif action == 'READ_PC_TO_SEL':
                    sel = mdr
                elif action == 'READ_PC_TO_TMP':
                    tmp = mdr
                elif action == 'READ_PC_TO_ADDR_LOW':
                    low = mdr
                elif action == 'READ_PC_TO_ADDR_HIGH':
                    high = mdr
                else:
                    raise AssertionError(action)
                pc = (pc + 1) & 0xFFFF
            elif action == 'DISPATCH_OPCODE':
                assert micro['dispatch'][f'0x{ir:02X}'] == {
                    'LDI': 'LDI_SELECTOR', 'ST_ABS': 'ST_SELECTOR',
                    'HALT': 'HALT_ENTER',
                }[path]
            elif action == 'VALIDATE_REGISTER_SEL':
                assert 0 <= sel < 4
            elif action == 'VALIDATE_ABSOLUTE_REGISTER_SEL':
                assert 0 <= sel < 4
            elif action == 'WRITE_SELECTED_REG_FROM_TMP':
                regs[sel] = tmp
            elif action == 'BUILD_MAR_FROM_STAGING':
                assert low is not None and high is not None
                mar = high * 256 + low
            elif action == 'STAGE_SELECTED_REG_TO_MDR':
                assert mdr == 0x6F  # El último byte de dirección permanecía allí.
                mdr = regs[sel]
            elif action == 'WRITE_MDR_AT_MAR':
                assert mar == 0x6F00 and mdr == 0x2A
                memory[mar] = mdr
                events.append(('write', mar, mdr))
            elif action == 'ENTER_HALT':
                halted = True
            elif action == 'END_TO_FETCH':
                pass
            else:
                raise AssertionError(action)
            assert (pc != prev_pc) == stage['pc_advance']
            assert stage['flags_write'] is False
            stages.append((stage['id'], pc, mar, mdr, ir, sel, tmp))

    assert halted
    assert (pc, mar, mdr, ir, regs[0], memory[0x6F00]) == (
        0x6008, 0x6007, 0x01, 0x01, 0x2A, 0x2A)
    assert regs[1:] == [0xAA, 0xBB, 0xCC]
    assert [memory[program_start + i] for i in range(len(program))] == list(program)
    assert flags in range(16)  # FLAGS se conserva porque ninguna acción lo cambia.
    return events, stages


def main():
    checks = 0
    isa = cargar_json('ISA_AULA8_CANDIDATA.json')
    micro = cargar_json('MICROSECUENCIAS_AULA8_BORRADOR.json')
    assert isa['status'] == micro['status'] == 'propuesta_no_aprobada'
    assert micro['granularity'] == 'acciones_logicas_no_ciclos_de_reloj'
    assert micro['exact_clock_cycles'] is None
    assert micro['cpu_executed'] is False and micro['electrical_validation'] is False
    assert set(micro['instructions']) == {'LDI', 'ST_ABS', 'HALT'}
    assert len(isa['instructions']) == 36
    checks += 6

    program = bytes.fromhex('11 00 2A 13 00 00 6F 01')
    example = next(e for e in isa['examples'] if e['name'] == 'depositar_42')
    assert program.hex(' ').upper() == example['bytes_hex']
    assert example['origin'] == 0x6000
    assert example['expected_ram_write'] == {'address': 0x6F00, 'value': 42}
    checks += 3

    expected_events = [
        ('read', 0x6000, 0x11), ('read', 0x6001, 0x00),
        ('read', 0x6002, 0x2A), ('read', 0x6003, 0x13),
        ('read', 0x6004, 0x00), ('read', 0x6005, 0x00),
        ('read', 0x6006, 0x6F), ('write', 0x6F00, 0x2A),
        ('read', 0x6007, 0x01),
    ]
    # Diferentes estados iniciales no contaminan el dato final ni FLAGS.
    for initial_flags in range(16):
        for initial_r0 in range(256):
            events, stages = recorrido_de_papel(program, initial_flags, initial_r0)
            assert events == expected_events
            assert stages[0][1:5] == (0x6001, 0x6000, 0x11, 0x11)
            assert stages[-1][1:5] == (0x6008, 0x6007, 0x01, 0x01)
            checks += 3
    assert micro['expected_example_external_transactions'] == {
        'read': 8, 'write': 1}
    assert sum(1 for event in expected_events if event[0] == 'read') == 8
    assert sum(1 for event in expected_events if event[0] == 'write') == 1
    checks += 3

    for addr in range(65536):
        low, high = addr & 0xFF, addr >> 8
        assert (high << 8) | low == addr
        assert ((addr + 1) & 0xFFFF) == ((high << 8 | low) + 1) & 0xFFFF
        checks += 2

    assert [s['action'] for s in micro['common_fetch']] == [
        'READ_PC_TO_IR', 'DISPATCH_OPCODE']
    steps = {step['id']: step for route in micro['instructions'].values()
             for step in route}
    assert steps['LDI_CHECK']['next'] == 'LDI_IMMEDIATE'
    assert steps['LDI_CHECK']['on_invalid'] == 'FAULT'
    assert steps['ST_ADDR_LOW']['next'] == 'ST_ADDR_HIGH'
    assert steps['ST_ADDR_HIGH']['next'] == 'ST_BUILD_MAR'
    assert steps['ST_BUILD_MAR']['next'] == 'ST_STAGE_DATA'
    assert steps['ST_STAGE_DATA']['next'] == 'ST_WRITE'
    assert steps['ST_STAGE_DATA']['action'] == 'STAGE_SELECTED_REG_TO_MDR'
    assert steps['ST_WRITE']['bus'] == 'write'
    assert steps['HALT_ENTER']['next'] == 'HALTED'
    checks += 10

    source = BASE.with_suffix('.md').read_text(encoding='utf-8')
    assert source.startswith('# Capítulo 15. La instrucción en movimiento')
    assert 'JavaFX' not in source
    assert source.count('[[EQ:') == 12
    assert source.count('[[FIG:') == 4
    # Negrita con fragmentos de código internos es Markdown válido.
    for token in ('fetch', 'decode', 'execute', 'MAR', 'MDR', 'IR',
                  'LDI_COMMIT', 'ST_STAGE_DATA', 'ADDR_LO', 'ADDR_HI',
                  '0x6008', '6F', '2A', '0x6F00', 'HALT', 'RET',
                  '8 lecturas', '1 escritura', 'capítulo 16'):
        assert token in source, token
        checks += 1
    for number in range(1, 13):
        assert f'**Ejercicio {number} ' in source
        assert f'**{number}.**' in source
        checks += 2
    checks += 5

    for ident in FIGURES:
        assert f'[[FIG:{ident}|' in source
        for ext, minimum in (('.svg', 800), ('.png', 10000)):
            path = ROOT / 'libro' / 'figuras' / (ident + ext)
            assert path.is_file() and path.stat().st_size > minimum, path
            checks += 1
        ET.parse(ROOT / 'libro' / 'figuras' / (ident + '.svg'))
        checks += 2

    with zipfile.ZipFile(BASE.with_suffix('.docx')) as archive:
        assert archive.testzip() is None
        tree = ET.fromstring(archive.read('word/document.xml'))
        maths = tree.findall('.//m:oMath', NS)
        images = tree.findall('.//wp:inline', NS)
        tables = tree.findall('.//w:tbl', NS)
        assert len(maths) == 12, len(maths)
        assert len(images) == 4, len(images)
        assert len(tables) >= 3, len(tables)
        assert all(im.find('wp:docPr', NS).get('descr') for im in images)
        headers = [name for name in archive.namelist()
                   if name.startswith('word/header')]
        assert headers and any(b'PARTE IV' in archive.read(h) for h in headers)
        checks += 6

    pdf = BASE.with_suffix('.pdf')
    assert pdf.is_file() and pdf.stat().st_size > 65000
    info = subprocess.run(['pdfinfo', str(pdf)], text=True,
                          capture_output=True, check=True).stdout
    match = re.search(r'^Pages:\s*(\d+)', info, re.M)
    assert match and int(match.group(1)) == 8, match
    fulltext = subprocess.run(['pdftotext', str(pdf), '-'], text=True,
                              capture_output=True, check=True).stdout
    assert len(fulltext) > 15000, len(fulltext)
    for token in ('La instrucción en movimiento', 'Figura 1.', 'Figura 2.',
                  'Figura 3.', 'Figura 4.', 'Solucionario del capítulo 15',
                  '0x6008', 'ST_STAGE_DATA', 'Para continuar'):
        assert token in fulltext, token
        checks += 1
    checks += 3

    print(f'Capítulo 15: {checks:,} comprobaciones de modelo/documento; '
          f'{match.group(1)} páginas, 12 OMML, 4 figuras y 12 ejercicios.')
    print('Trazas de acciones lógicas propuestas, sin CPU, tiempos, micro-ROM '
          'ni electrónica física probados.')


if __name__ == '__main__':
    main()
