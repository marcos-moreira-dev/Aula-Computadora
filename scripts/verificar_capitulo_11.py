#!/usr/bin/env python3
"""Prueba la ALU matemática de 8 bits y la integridad Word/PDF C11.

No simula tiempos, transistores, opcodes ni hardware físico Aula.
"""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'libro' / 'capitulos' / '11_la_unidad_aritmetico_logica'
FIGURES = ('c11_fig01_resta_complemento_dos', 'c11_fig02_alu_selector',
           'c11_fig03_logica_por_bits', 'c11_fig04_comparaciones_banderas')
NS = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def signed(byte):
    return byte if byte < 128 else byte - 256


def alu_sub(a, b):
    """Sumador reutilizado: A + (~B & 255) + 1, convención C=préstamo."""
    total = a + (b ^ 0xFF) + 1
    result = total & 0xFF
    cout = int(total > 255)
    borrow = 1 - cout
    z = int(result == 0)
    n = (result >> 7) & 1
    v = int(bool((a ^ b) & (a ^ result) & 0x80))
    return result, cout, borrow, z, n, v


def main():
    checks = 0
    for a in range(256):
        for b in range(256):
            s, cout, c, z, n, v = alu_sub(a, b)
            mathematical = signed(a) - signed(b)
            assert s == (a - b) % 256
            assert cout == int(a >= b)
            assert c == int(a < b)
            assert z == int(a == b)
            assert n == (s >> 7)
            assert v == int(not -128 <= mathematical <= 127)
            assert (c == 1) == (a < b)       # unsigned less
            assert (z == 0 and c == 0) == (a > b)
            assert bool(n ^ v) == (signed(a) < signed(b))
            assert (z == 0 and (n ^ v) == 0) == (signed(a) > signed(b))
            assert (a & b) == sum((((a >> i) & 1) & ((b >> i) & 1)) << i
                                   for i in range(8))
            assert (a ^ b) == sum((((a >> i) & 1) ^ ((b >> i) & 1)) << i
                                   for i in range(8))
            checks += 12
    assert alu_sub(13, 9) == (4, 1, 0, 0, 0, 0)
    assert alu_sub(9, 13) == (252, 0, 1, 0, 1, 0)
    assert alu_sub(0x80, 1) == (127, 1, 0, 0, 0, 1)
    assert alu_sub(0x2A, 0x2A) == (0, 1, 0, 1, 0, 0)
    assert alu_sub(0xFF, 1) == (0xFE, 1, 0, 0, 1, 0)
    assert (0x5A & 0x3C, 0x5A | 0x3C, 0x5A ^ 0x3C, 0x5A ^ 0xFF) == (
        0x18, 0x7E, 0x66, 0xA5)
    checks += 6

    source = BASE.with_suffix('.md').read_text(encoding='utf-8')
    assert source.startswith('# Capítulo 11. La unidad aritmético-lógica')
    assert 'JavaFX' not in source
    assert source.count('[[EQ:') == 21
    assert source.count('[[FIG:') == 4
    assert 'préstamo = 1 − Cout interno' in source
    assert 'operaciones AND, OR, XOR y NOT' in source
    assert 'capítulo 12' in source
    checks += 7
    for i in range(1, 13):
        assert f'**Ejercicio {i} ' in source
        assert f'**{i}.**' in source
        checks += 2
    for token in ('11110110', '11110111', '00000100', '11111100',
                  '0x80', '0x7F', '0x5A', '0x3C', '0x18', '0x7E', '0x66',
                  '0xA5', '0xFF', 'N ⊕ V', 'SN74HC157', 'CD74HC283',
                  'SN74HC86', 'CMP', 'multiplexor', 'sin signo', 'con signo'):
        assert token in source, token
        checks += 1
    for figure in FIGURES:
        assert f'[[FIG:{figure}|' in source
        for ext, min_size in (('.svg', 1000), ('.png', 15000)):
            img = ROOT / 'libro' / 'figuras' / (figure + ext)
            assert img.is_file() and img.stat().st_size > min_size, img
            checks += 1
        ET.parse(ROOT / 'libro' / 'figuras' / (figure + '.svg'))
        checks += 2

    with zipfile.ZipFile(BASE.with_suffix('.docx')) as archive:
        assert archive.testzip() is None
        document = ET.fromstring(archive.read('word/document.xml'))
        omml = document.findall('.//m:oMath', NS)
        pics = document.findall('.//wp:inline', NS)
        tables = document.findall('.//w:tbl', NS)
        assert len(omml) == 21, len(omml)
        assert len(pics) == 4, len(pics)
        assert len(tables) >= 4, len(tables)
        assert all(p.find('wp:docPr', NS).get('descr') for p in pics)
        headers = [name for name in archive.namelist() if name.startswith('word/header')]
        assert headers and any(b'PARTE III' in archive.read(h) for h in headers)
        checks += 5

    pdf = BASE.with_suffix('.pdf')
    assert pdf.is_file() and pdf.stat().st_size > 65000
    info = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True,
                          check=True).stdout
    pages = re.search(r'^Pages:\s*(\d+)', info, re.M)
    assert pages and 8 <= int(pages.group(1)) <= 14
    fulltext = subprocess.run(['pdftotext', str(pdf), '-'],
                              capture_output=True, text=True, check=True).stdout
    assert len(fulltext) > 16000, len(fulltext)
    for token in ('La unidad aritmético-lógica', 'Figura 1.', 'Figura 2.',
                  'Figura 3.', 'Figura 4.', 'Solucionario del capítulo 11',
                  '0xFC', '0x7F', 'SN74HC157', 'Para continuar'):
        assert token in fulltext, token
        checks += 1
    checks += 3
    print(f'Capítulo 11: {checks} comprobaciones matemáticas/documentales; '
          f'{pages.group(1)} páginas, 21 OMML, 4 figuras y 12 ejercicios.')
    print('Sin montaje, simulador de circuitos, firmware ni ejecución de CPU.')


if __name__ == '__main__':
    main()
