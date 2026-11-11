#!/usr/bin/env python3
"""Contrasta suma bit a bit y valida artefactos editoriales del capítulo 10.

No modela tiempos eléctricos, conexiones físicas ni CPU Aula ejecutable.
"""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'libro' / 'capitulos' / '10_el_circuito_que_suma'
FIGURES = (
    'c10_fig01_medio_sumador',
    'c10_fig02_sumador_completo',
    'c10_fig03_suma_trece_mas_nueve',
    'c10_fig04_cadena_y_dos_bytes',
)
NS = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def half_adder(a, b):
    assert a in (0, 1) and b in (0, 1)
    return a ^ b, a & b


def full_adder(a, b, carry_in):
    p, g = half_adder(a, b)
    s, h = half_adder(p, carry_in)
    return s, g | h


def ripple_8(a, b, carry_in=0):
    assert 0 <= a <= 255 and 0 <= b <= 255
    assert carry_in in (0, 1)
    carry = carry_in
    stages = []
    result = 0
    for i in range(8):
        bit_a, bit_b = (a >> i) & 1, (b >> i) & 1
        s, carry_out = full_adder(bit_a, bit_b, carry)
        stages.append((bit_a, bit_b, carry, s, carry_out))
        result |= s << i
        carry = carry_out
    overflow = stages[7][2] ^ stages[7][4]
    return result, carry, overflow, stages


def main():
    checks = 0
    for a in (0, 1):
        for b in (0, 1):
            sum_bit, carry = half_adder(a, b)
            assert a + b == sum_bit + 2 * carry
            checks += 1
            for cin in (0, 1):
                s, cout = full_adder(a, b, cin)
                assert a + b + cin == s + 2 * cout
                assert cout == (1 if a + b + cin >= 2 else 0)
                checks += 2
    assert half_adder(1, 1) == (0, 1)
    assert full_adder(1, 1, 1) == (1, 1)
    checks += 2

    # Contraste exhaustivo de las 131072 sumas A+B+Cin de ocho bits.
    # Incluye acarreo sin signo, overflow con signo, Z y N.
    for a in range(256):
        for b in range(256):
            for cin in (0, 1):
                total = a + b + cin
                result, carry, overflow, stages = ripple_8(a, b, cin)
                assert result == (total & 0xFF)
                assert carry == (total >> 8)
                expected_v = int(((~(a ^ b)) & (a ^ result) & 0x80) != 0)
                assert overflow == expected_v
                assert int(result == 0) == (1 if total % 256 == 0 else 0)
                assert (result >> 7) == int(result >= 128)
                assert all(x + y + entry == out + 2 * exit_
                           for x, y, entry, out, exit_ in stages)
                checks += 6

    result_13, carry_13, overflow_13, stages_13 = ripple_8(13, 9)
    assert (result_13, carry_13, overflow_13) == (22, 0, 0)
    assert [t[2] for t in stages_13] == [0, 1, 0, 0, 1, 0, 0, 0]
    assert [t[4] for t in stages_13] == [1, 0, 0, 1, 0, 0, 0, 0]
    assert ripple_8(45, 23)[0] == 68
    assert ripple_8(250, 10)[:3] == (4, 1, 0)
    assert ripple_8(127, 1)[:3] == (128, 0, 1)
    assert ripple_8(255, 1)[:3] == (0, 1, 0)
    low, carry_low, _, _ = ripple_8(0xFF, 0x01)
    high, carry_high, _, _ = ripple_8(0x01, 0x00, carry_low)
    assert (high << 8) | low == 0x0200 and carry_high == 0
    checks += 8

    manuscript = BASE.with_suffix('.md').read_text(encoding='utf-8')
    assert manuscript.startswith('# Capítulo 10. El circuito que suma')
    assert '*Parte III' in manuscript
    assert 'JavaFX' not in manuscript
    assert manuscript.count('[[EQ:') == 17
    assert manuscript.count('[[FIG:') == 4
    checks += 5
    for n in range(1, 13):
        assert f'**Ejercicio {n} ' in manuscript
        assert f'**{n}.**' in manuscript
        checks += 2
    for token in ('half-adder', 'full-adder', 'XOR', 'AND', 'Cin', 'Cout',
                  'carry', '13 + 9', '00001101', '00001001', '00010110',
                  '250 + 10', '127 + 1', '0x01FF', '0x0200', 'CD74HC283',
                  'SN74HC86', 'overflow', 'complemento a dos', 'capítulo 11'):
        assert token.casefold() in manuscript.casefold(), token
        checks += 1
    for figure in FIGURES:
        assert f'[[FIG:{figure}|' in manuscript
        for ext, minimum in (('.svg', 1400), ('.png', 10000)):
            path = ROOT / 'libro' / 'figuras' / f'{figure}{ext}'
            assert path.is_file() and path.stat().st_size > minimum, path
            checks += 1
        checks += 1

    with zipfile.ZipFile(BASE.with_suffix('.docx')) as archive:
        assert archive.testzip() is None
        root = ET.fromstring(archive.read('word/document.xml'))
        formulas = root.findall('.//m:oMath', NS)
        figures = root.findall('.//wp:inline', NS)
        tables = root.findall('.//w:tbl', NS)
        assert len(formulas) == 17, len(formulas)
        assert len(figures) == 4, len(figures)
        assert len(tables) >= 4, len(tables)
        assert all(img.find('wp:docPr', NS).get('descr') for img in figures)
        headers = [key for key in archive.namelist()
                   if key.startswith('word/header') and key.endswith('.xml')]
        assert headers and any(b'PARTE III' in archive.read(key) for key in headers)
        checks += 5

    pdf = BASE.with_suffix('.pdf')
    assert pdf.is_file() and pdf.stat().st_size > 60000
    info = subprocess.run(['pdfinfo', str(pdf)], capture_output=True,
                          check=True, text=True).stdout
    m = re.search(r'^Pages:\s*(\d+)', info, flags=re.M)
    assert m and 8 <= int(m.group(1)) <= 14
    text = subprocess.run(['pdftotext', str(pdf), '-'], capture_output=True,
                          check=True, text=True).stdout
    assert len(text) > 16000, len(text)
    for token in ('El circuito que suma', 'Figura 1.', 'Figura 2.',
                  'Figura 3.', 'Figura 4.', 'Solucionario del capítulo 10',
                  '00010110', 'CD74HC283', '13 + 9', '0x0200'):
        assert token in text, token
        checks += 1
    checks += 3
    print(f'Capítulo 10: {checks} controles matemáticos/documentales; '
          f'{m.group(1)} páginas, 17 OMML, cuatro figuras y 12 ejercicios.')
    print('NO se probaron tiempos, alimentación, chips montados, ALU ni CPU física.')


if __name__ == '__main__':
    main()
