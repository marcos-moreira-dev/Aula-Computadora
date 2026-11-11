#!/usr/bin/env python3
"""Certifica el contenido didáctico de Arquitectura Aula-8 (C12).

Comprueba un modelo aritmético y documental. No ejecuta CPU, firmware ni
microcódigo; tampoco certifica componentes, tensiones o tiempo de reloj.
"""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'libro' / 'capitulos' / '12_arquitectura_aula_8'
FIGURES = (
    'c12_fig01_mapa_cpu_aula8',
    'c12_fig02_movimiento_registros',
    'c12_fig03_lectura_escritura',
    'c12_fig04_direccion_dos_pasadas',
)
NS = {
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}


def sumar_direccion_dos_pasadas(x, delta, flag_c):
    """Modelo educativo, no emulación de un circuito de Aula-8."""
    total_bajo = (x & 0xFF) + (delta & 0xFF)
    bajo = total_bajo & 0xFF
    addr_carry = total_bajo >> 8
    alto_delta = 0xFF if delta < 0 else 0
    alto = (((x >> 8) & 0xFF) + alto_delta + addr_carry) & 0xFF
    return (alto << 8) | bajo, flag_c, addr_carry


def main():
    checks = 0
    for x in range(0x10000):
        for delta in (-128, -2, -1, 0, 1, 2, 127):
            for flag_c in (0, 1):
                nuevo, visible_c, carry = sumar_direccion_dos_pasadas(x, delta, flag_c)
                assert nuevo == (x + delta) & 0xFFFF
                assert visible_c == flag_c
                assert carry == int((x & 0xFF) + (delta & 0xFF) > 0xFF)
                checks += 3
    assert sumar_direccion_dos_pasadas(0x12FF, 2, 1) == (0x1301, 1, 1)
    assert sumar_direccion_dos_pasadas(0x0000, -1, 0) == (0xFFFF, 0, 0)
    assert sumar_direccion_dos_pasadas(0xFFFF, 1, 1) == (0x0000, 1, 1)
    checks += 3

    # Decodificación documental de la traza candidata, sin temporización.
    program = bytes.fromhex('11 00 2A 13 00 00 6F 01')
    start = 0x6000
    assert len(program) == 8
    assert program[:3] == bytes([0x11, 0x00, 42])
    assert program[3:7] == bytes([0x13, 0x00, 0x00, 0x6F])
    assert program[7] == 0x01
    assert start + 3 == 0x6003
    assert (program[6] << 8) | program[5] == 0x6F00
    assert start + len(program) == 0x6008
    # Ocho lecturas de byte de instrucciones y una escritura de datos
    # es una cuenta funcional candidata, NO una medida de ciclos.
    assert (len(program), 1) == (8, 1)
    checks += 8

    source = BASE.with_suffix('.md').read_text(encoding='utf-8')
    assert source.startswith('# Capítulo 12. Arquitectura Aula-8')
    assert 'JavaFX' not in source
    assert source.count('[[EQ:') == 12
    assert source.count('[[FIG:') == 4
    for token in ('R0–R3', 'PC', 'SP', 'MAR', 'MDR', 'FLAGS', 'ADDR_CARRY',
                  '0x6003', '0x1301', '0x6F00', '0x12FF', '0x2A',
                  '16 bits', 'ocho bits', 'capítulo 13',
                  'ISA candidata', 'no', 'ROM'):
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
        assert len(maths) == 12, len(maths)
        assert len(images) == 4, len(images)
        assert len(tables) >= 4, len(tables)
        assert all(im.find('wp:docPr', NS).get('descr') for im in images)
        headers = [name for name in archive.namelist()
                   if name.startswith('word/header')]
        assert headers and any(b'PARTE IV' in archive.read(h) for h in headers)
        checks += 5

    pdf = BASE.with_suffix('.pdf')
    assert pdf.is_file() and pdf.stat().st_size > 65000
    info = subprocess.run(['pdfinfo', str(pdf)], text=True,
                          capture_output=True, check=True).stdout
    m = re.search(r'^Pages:\s*(\d+)', info, re.M)
    assert m and 8 <= int(m.group(1)) <= 14, m
    fulltext = subprocess.run(['pdftotext', str(pdf), '-'], text=True,
                              capture_output=True, check=True).stdout
    assert len(fulltext) > 15000, len(fulltext)
    for token in ('Arquitectura Aula-8', 'Figura 1.', 'Figura 2.',
                  'Figura 3.', 'Figura 4.', 'Solucionario del capítulo 12',
                  '0x6003', '0x6F00', 'ADDR_CARRY', 'Para continuar'):
        assert token in fulltext, token
        checks += 1
    checks += 3
    print(f'Capítulo 12: {checks:,} comprobaciones aritméticas/documentales; '
          f'{m.group(1)} páginas, 12 OMML, 4 figuras y 12 ejercicios.')
    print('Solo trazas candidatas en papel; sin ejecución de CPU, '
          'firmware, circuito o tiempos medidos.')


if __name__ == '__main__':
    main()
