#!/usr/bin/env python3
"""Verifica el capítulo 13 y las microsecuencias CANDIDATAS que explica.

Las propiedades se prueban con modelos Python en anfitrión; no se ejecutan
instrucciones en una CPU Aula ni se miden estados eléctricos o de reloj.
"""

import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'libro' / 'capitulos' / '13_la_unidad_de_control'
FIGURES = (
    'c13_fig01_unidad_control',
    'c13_fig02_macro_lectura',
    'c13_fig03_despacho',
    'c13_fig04_escritura_segura',
)
NS = {
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}


def cargar_json(name):
    return json.loads((ROOT / 'simulador-javafx' / name).read_text(encoding='utf-8'))


def aplicar_ldi_ideal(registros, selector, inmediato):
    """Solo modela selección, validación previa y efecto final de una LDI."""
    siguiente = list(registros)
    if selector < len(registros):
        siguiente[selector] = inmediato
        return siguiente, True
    return siguiente, False


def main():
    checks = 0

    micro = cargar_json('MICROSECUENCIAS_AULA8_BORRADOR.json')
    isa = cargar_json('ISA_AULA8_CANDIDATA.json')
    assert micro['status'] == isa['status'] == 'propuesta_no_aprobada'
    assert micro['granularity'] == 'acciones_logicas_no_ciclos_de_reloj'
    assert micro['exact_clock_cycles'] is None
    assert micro['micro_rom_control_word_bits'] is None
    assert micro['micro_rom_capacity_bytes'] is None
    assert micro['cpu_executed'] is False and micro['electrical_validation'] is False
    assert set(micro['extra_candidate_latches']) == {'ADDR_LO', 'ADDR_HI'}
    checks += 7

    # Se prueban 256 selectores por los 256 posibles valores inmediatos.
    # No se permite una escritura cuando el selector no cabe en R0–R3.
    inicio = [0x91, 0x83, 0x45, 0x37]
    for selector in range(256):
        for inmediato in range(256):
            regs, valido = aplicar_ldi_ideal(inicio, selector, inmediato)
            assert valido == (selector < 4)
            assert regs == [inmediato if selector == i else val
                            for i, val in enumerate(inicio)]
            checks += 2

    # Cualquier dirección de 16 bits se recompone con bajo y alto.
    for addr in range(0x10000):
        low, high = addr & 0xFF, addr >> 8
        assert (high << 8) | low == addr
        checks += 1

    fetch = micro['common_fetch']
    instructions = micro['instructions']
    assert [s['action'] for s in fetch] == ['READ_PC_TO_IR', 'DISPATCH_OPCODE']
    assert set(instructions) == {'LDI', 'ST_ABS', 'HALT'}
    assert micro['dispatch']['0x11'] == 'LDI_SELECTOR'
    assert micro['dispatch']['0x13'] == 'ST_SELECTOR'
    assert micro['dispatch']['0x01'] == 'HALT_ENTER'
    assert micro['dispatch']['unknown'] == 'FAULT'
    assert micro['dispatch']['known_but_unmodeled'] == 'PENDING_ROUTE'
    checks += 7

    estados = {step['id']: step for part in [fetch, *instructions.values()]
               for step in part}
    assert estados['LDI_CHECK']['on_invalid'] == 'FAULT'
    assert estados['ST_CHECK']['on_invalid'] == 'FAULT'
    assert estados['LDI_CHECK']['next'] == 'LDI_IMMEDIATE'
    assert estados['LDI_IMMEDIATE']['next'] == 'LDI_COMMIT'
    assert estados['ST_ADDR_LOW']['next'] == 'ST_ADDR_HIGH'
    assert estados['ST_ADDR_HIGH']['next'] == 'ST_BUILD_MAR'
    assert estados['ST_BUILD_MAR']['next'] == 'ST_STAGE_DATA'
    assert estados['ST_STAGE_DATA']['next'] == 'ST_WRITE'
    assert estados['ST_STAGE_DATA']['action'] == 'STAGE_SELECTED_REG_TO_MDR'
    assert estados['ST_WRITE']['action'] == 'WRITE_MDR_AT_MAR'
    assert estados['ST_WRITE']['bus'] == 'write'
    assert estados['HALT_ENTER']['next'] == 'HALTED'
    checks += 12

    for step in estados.values():
        assert step['bus'] in {'read', 'write', 'none'}
        assert step['flags_write'] is False
        if step['action'].startswith('READ_PC_TO_'):
            assert step['bus'] == 'read' and step['pc_advance']
        else:
            assert not step['pc_advance']
        checks += 3

    events = [step['bus'] for part in ('LDI', 'ST_ABS', 'HALT')
              for step in (fetch + instructions[part])]
    assert (events.count('read'), events.count('write')) == (8, 1)
    assert micro['expected_example_external_transactions'] == {'read': 8, 'write': 1}
    checks += 2

    program = bytes.fromhex('11 00 2A 13 00 00 6F 01')
    example = next(e for e in isa['examples'] if e['name'] == 'depositar_42')
    assert program == bytes.fromhex(example['bytes_hex'])
    pc = 0x6000
    memory = {}
    registers = [0, 0, 0, 0]
    flags = 0b1010
    # Recorrido funcional DE PAPEL: 3 lecturas de LDI, 4 de ST y 1 de HALT.
    assert program[0] == 0x11
    registers, accepted = aplicar_ldi_ideal(registers, program[1], program[2])
    assert accepted and registers[0] == 42
    pc += 3
    assert pc == 0x6003 and program[pc-0x6000] == 0x13
    destination = (program[6] << 8) | program[5]
    assert destination == 0x6F00
    # Al terminar de leer el byte alto, MDR=0x6F. Escribirlo sería un error.
    mdr_after_high = program[6]
    assert mdr_after_high == 0x6F and mdr_after_high != registers[program[4]]
    mdr_staged = registers[program[4]]
    memory[destination] = mdr_staged
    assert memory == {0x6F00: 0x2A}
    pc += 4
    assert program[pc-0x6000] == 0x01
    pc += 1
    assert pc == 0x6008 and flags == 0b1010
    checks += 10

    source = BASE.with_suffix('.md').read_text(encoding='utf-8')
    assert source.startswith('# Capítulo 13. La unidad de control')
    assert 'JavaFX' not in source
    assert source.count('[[EQ:') == 8
    assert source.count('[[FIG:') == 4
    for token in ('microoperación', 'ROM de control', 'µPC', 'MAR', 'MDR',
                  'FLAGS', 'PENDING_ROUTE', 'FAULT', 'LDI_COMMIT',
                  'ADDR_LO', 'ADDR_HI', 'ST_STAGE_DATA', 'HALTED',
                  '0x6008', '0x6F00', '8 lecturas', '1 escritura',
                  'capítulo 14'):
        assert token in source, token
        checks += 1
    for number in range(1, 13):
        assert f'**Ejercicio {number} ' in source
        assert f'**{number}.**' in source
        checks += 2
    for ident in FIGURES:
        assert f'[[FIG:{ident}|' in source
        for ext, minimum in (('.svg', 800), ('.png', 15000)):
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
        assert len(maths) == 8, len(maths)
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
    assert len(fulltext) > 14000, len(fulltext)
    for token in ('La unidad de control', 'Figura 1.', 'Figura 2.',
                  'Figura 3.', 'Figura 4.', 'Solucionario del capítulo 13',
                  'PENDING_ROUTE', '0x6008', 'ST_STAGE_DATA', 'Para continuar'):
        assert token in fulltext, token
        checks += 1
    checks += 3
    print(f'Capítulo 13: {checks:,} comprobaciones de modelo/documento; '
          f'{match.group(1)} páginas, 8 OMML, 4 figuras y 12 ejercicios.')
    print('Modelo de microoperaciones candidatas; sin ejecutar CPU, micro-ROM, '
          'firmware, ciclos ni electrónica física.')


if __name__ == '__main__':
    main()
