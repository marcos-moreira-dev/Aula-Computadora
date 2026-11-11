#!/usr/bin/env python3
"""Comprueba los bytes y documentos del C14; no ejecuta una CPU Aula-8.

Los cálculos se realizan en Python y representan exclusivamente el contrato
matemático/documental de una ISA propuesta, no buses ni hardware medidos.
"""

import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'libro' / 'capitulos' / '14_de_numeros_a_instrucciones'
FIGURES = (
    'c14_fig01_un_byte_tres_lecturas',
    'c14_fig02_mapa_programa',
    'c14_fig03_modos_direccion',
    'c14_fig04_panel_seguro',
)
NS = {
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}


def depositar(memoria, direccion, dato, *, cpu_detenida, propietario_bus):
    """Modelo deliberadamente mínimo de una escritura segura del panel."""
    if not cpu_detenida or propietario_bus != 'panel':
        return False
    if not (0x6000 <= direccion <= 0x6FFF) or not (0 <= dato < 256):
        return False
    memoria[direccion] = dato
    return True


def main():
    checks = 0
    isa = json.loads((ROOT / 'simulador-javafx' / 'ISA_AULA8_CANDIDATA.json')
                     .read_text(encoding='utf-8'))
    assert isa['architecture'] == 'Aula-8'
    assert isa['status'] == 'propuesta_no_aprobada'
    assert isa['encoding']['opcode_bits'] == 8
    assert isa['encoding']['address_bits'] == 16
    assert isa['encoding']['immediate_word_byte_order'] == 'little_endian'
    assert isa['encoding']['cpu_reset'] == 'vector_de_rom_0xFFFC'
    assert len(isa['instructions']) == 36
    checks += 7

    opcodes = {i['mnemonic']: int(i['opcode'], 16)
               for i in isa['instructions']}
    assert {mn: opcodes[mn] for mn in ('HALT', 'LDI', 'LD', 'ST', 'JNZ')} == {
        'HALT': 0x01, 'LDI': 0x11, 'LD': 0x12,
        'ST': 0x13, 'JNZ': 0x32,
    }
    assert len(set(opcodes.values())) == 36
    assert isa['formats']['reg_imm8']['bytes'] == 3
    assert isa['formats']['memory']['bytes_by_mode'] == {'0': 4, '1': 3, '2': 3}
    checks += 4

    # Exhaustivo sobre todos los bytes: valor, dos nibbles y binario.
    for value in range(256):
        high, low = value >> 4, value & 0x0F
        assert 16 * high + low == value
        assert int(f'{high:X}{low:X}', 16) == value
        assert int(f'{value:08b}', 2) == value
        checks += 3
    assert int('00101010', 2) == 42 == int('2A', 16)
    assert int('42', 16) == 66
    assert bytes('42', 'ascii') == bytes.fromhex('34 32')
    checks += 3

    # Separamos y reconstruimos todas las direcciones de 16 bits.
    for addr in range(0x10000):
        low, high = addr & 0xFF, addr >> 8
        assert (high << 8) | low == addr
        assert bytes([low, high]) == addr.to_bytes(2, 'little')
        checks += 2

    # Los dos bits bajos seleccionan R0-R3; 3 es modo reservado.
    for mode in range(3):
        for register in range(4):
            selector = (mode << 2) | register
            assert (selector >> 2, selector & 3) == (mode, register)
            checks += 1
    for selector in range(12, 256):
        assert (selector >> 2) >= 3
        checks += 1
    assert ((1 << 2) | 1) == 0x05
    assert ((2 << 2) | 2) == 0x0A
    checks += 2

    # Desplazamientos en complemento a dos, incluyendo FF=-1.
    for disp_byte in range(256):
        signed = disp_byte if disp_byte < 128 else disp_byte - 256
        assert -128 <= signed <= 127
        assert signed & 0xFF == disp_byte
        assert ((0x6004 + signed) & 0xFFFF) == (
            (0x6004 + (disp_byte if disp_byte < 128 else disp_byte - 256))
            & 0xFFFF
        )
        checks += 3
    assert (0x6004 - 1) & 0xFFFF == 0x6003
    assert bytes.fromhex('12 05 FF') == bytes([opcodes['LD'], 0x05, 0xFF])
    assert bytes.fromhex('12 0A 06') == bytes([opcodes['LD'], 0x0A, 6])
    assert bytes.fromhex('32 03 60') == bytes([opcodes['JNZ'], 3, 0x60])
    checks += 4

    # Depósito y examen: nadie escribe RAM mientras la CPU posee el bus.
    example = next(e for e in isa['examples'] if e['name'] == 'depositar_42')
    program = bytes.fromhex('11 00 2A 13 00 00 6F 01')
    assert program == bytes.fromhex(example['bytes_hex'])
    assert example['origin'] == 0x6000
    ram = {}
    assert not depositar(ram, 0x6000, 0x11,
                        cpu_detenida=False, propietario_bus='cpu')
    assert not depositar(ram, 0x6000, 0x11,
                        cpu_detenida=True, propietario_bus='cpu')
    assert not depositar(ram, 0xE000, 0x11,
                        cpu_detenida=True, propietario_bus='panel')
    assert not ram
    checks += 6
    for offset, value in enumerate(program):
        assert depositar(ram, 0x6000 + offset, value,
                        cpu_detenida=True, propietario_bus='panel')
        assert ram[0x6000 + offset] == value  # EXAMINE conceptual.
        checks += 2

    # Sólo decodificación estática y efectos ideales sobre papel.
    pc = 0x6000
    registers = [0] * 4
    observed = []
    while pc < 0x6008:
        opcode = ram[pc]
        if opcode == opcodes['LDI']:
            assert ram[pc + 1] < 4
            registers[ram[pc + 1]] = ram[pc + 2]
            size, mnemonic = 3, 'LDI'
        elif opcode == opcodes['ST']:
            assert ram[pc + 1] == 0
            addr = (ram[pc + 3] << 8) | ram[pc + 2]
            assert addr == 0x6F00
            ram[addr] = registers[0]
            size, mnemonic = 4, 'ST'
        elif opcode == opcodes['HALT']:
            size, mnemonic = 1, 'HALT'
        else:
            raise AssertionError('Opcode no esperado en este ejemplo')
        observed.append({'pc': pc, 'mnemonic': mnemonic, 'size': size})
        pc += size
        checks += 1
    assert observed == example['expected_decode']
    assert (pc, registers[0], ram[0x6F00]) == (0x6008, 42, 42)
    assert example['expected_ram_write'] == {'address': 0x6F00, 'value': 42}
    assert len(program) == 8 and len(observed) == 3
    checks += 4

    source = BASE.with_suffix('.md').read_text(encoding='utf-8')
    assert source.startswith('# Capítulo 14. De números a instrucciones')
    assert 'JavaFX' not in source
    assert source.count('[[EQ:') == 12
    assert source.count('[[FIG:') == 4
    assert '**`' not in source and '`**' not in source
    for token in ('nibble', 'little-endian', '36 opcodes', '2A',
                  '11 00 2A', '13 00 00 6F', 'FF', 'selector',
                  'DEPOSIT', 'EXAMINE', 'POKE', 'HALT y RET',
                  '0x6008', 'JNZ', 'capítulo 15', 'ISA candidata'):
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
        assert len(tables) >= 4, len(tables)
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
    assert match and int(match.group(1)) == 9, match
    fulltext = subprocess.run(['pdftotext', str(pdf), '-'], text=True,
                              capture_output=True, check=True).stdout
    assert len(fulltext) > 16000, len(fulltext)
    for token in ('De números a instrucciones', 'Figura 1.', 'Figura 2.',
                  'Figura 3.', 'Figura 4.', 'Solucionario del capítulo 14',
                  '0x6008', 'DEPOSIT', 'EXAMINE', 'Para continuar'):
        assert token in fulltext, token
        checks += 1
    checks += 3

    print(f'Capítulo 14: {checks:,} comprobaciones de modelo/documento; '
          f'{match.group(1)} páginas, 12 OMML, 4 figuras y 12 ejercicios.')
    print('Panel y trazas modelados en Python; no hay CPU, arbitraje eléctrico, '
          'monitor nativo, ensamblador ni ejecución física verificados.')


if __name__ == '__main__':
    main()
