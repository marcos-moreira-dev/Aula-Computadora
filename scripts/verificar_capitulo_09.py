#!/usr/bin/env python3
"""Controla organización, selección y entregables del capítulo 9.

Comprobaciones matemáticas y documentales, no eléctricas ni de CPU.
"""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'libro' / 'capitulos' / '09_ram_y_rom_reales'
FIGURES = (
    'c09_fig01_celda_sram_conceptual',
    'c09_fig02_sram_pines',
    'c09_fig03_mapa_64k_ejemplo',
    'c09_fig04_expansion_profundidad_anchura',
)
NS = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}


def decode_example(address):
    if not 0 <= address < 65536:
        raise ValueError('Dirección fuera de 16 bits')
    if not (address & 0x8000):
        return ('SRAM', address & 0x7FFF)
    if (address >> 13) == 0b111:
        return ('EEPROM', address & 0x1FFF)
    return ('SIN_ASIGNAR', None)


def sram_mode(ce, oe, we):
    assert ce in (0, 1) and oe in (0, 1) and we in (0, 1)
    if ce:
        return 'Z'
    if not we:
        return 'DIN'
    if oe:
        return 'Z'
    return 'DOUT'


def main():
    checks = 0
    assert 32 * 1024 * 8 == 262144
    assert (32 * 1024 * 8) // 8 == 32768
    assert 2 ** 15 == 32768
    assert 8 * 1024 * 8 == 65536
    assert 2 ** 13 == 8192
    assert 32768 + 24576 + 8192 == 65536
    assert 65536 // 1024 == 64
    assert 0xE123 - 0xE000 == 0x123 == 291
    checks += 8

    # Una sola ventana responde para cada dirección de 16 bits.
    counts = {'SRAM': 0, 'EEPROM': 0, 'SIN_ASIGNAR': 0}
    for address in range(65536):
        kind, offset = decode_example(address)
        counts[kind] += 1
        assert kind in counts
        checks += 1
        if kind == 'SRAM':
            assert 0 <= offset < 32768 and offset == address
            assert ((address >> 15) & 1) == 0
            checks += 2
        elif kind == 'EEPROM':
            assert 0 <= offset < 8192 and offset == address - 0xE000
            assert ((address >> 13) & 0b111) == 0b111
            checks += 2
        else:
            assert offset is None and 0x8000 <= address <= 0xDFFF
            checks += 1
    assert counts == {'SRAM': 32768, 'EEPROM': 8192, 'SIN_ASIGNAR': 24576}
    assert decode_example(0x1200) == ('SRAM', 0x1200)
    assert decode_example(0x1201) == ('SRAM', 0x1201)
    assert decode_example(0xE123) == ('EEPROM', 0x123)
    for invalid in (-1, 65536):
        try:
            decode_example(invalid)
            raise AssertionError('Se admitió dirección fuera de intervalo')
        except ValueError:
            pass
        checks += 1
    checks += 4

    # Combinaciones de CE/OE/WE del fabricante: WE bajo tiene prioridad en escritura.
    expected = {(1, a, b): 'Z' for a in (0, 1) for b in (0, 1)}
    expected.update({(0, 0, 0): 'DIN', (0, 1, 0): 'DIN',
                     (0, 0, 1): 'DOUT', (0, 1, 1): 'Z'})
    for controls, mode in expected.items():
        assert sram_mode(*controls) == mode
        checks += 1

    # Dos chips expandidos en profundidad: A15 selecciona uno, nunca dos.
    for address in range(65536):
        low_selected = (address >> 15) == 0
        high_selected = (address >> 15) == 1
        assert low_selected != high_selected
        assert (address & 0x7FFF) < 32768
        checks += 2
    # Dos chips expandidos en anchura: recomponer 16 bits desde dos bytes.
    for value in range(65536):
        low = value & 255
        high = (value >> 8) & 255
        assert ((high << 8) | low) == value
        checks += 1

    # Copia supuesta de RAM no modifica la dirección vecina.
    memory = {0x1200: 0x41, 0x1201: 0x00}
    memory[0x1201] = 0x53
    assert memory == {0x1200: 0x41, 0x1201: 0x53}
    assert sum(int(bit) * (1 << (7 - i)) for i, bit in enumerate('01010011')) == 83
    checks += 2

    manuscript = BASE.with_suffix('.md').read_text(encoding='utf-8')
    assert manuscript.startswith('# Capítulo 9. RAM y ROM reales')
    assert '*Parte III' in manuscript
    assert 'JavaFX' not in manuscript
    assert manuscript.count('[[EQ:') == 10
    assert manuscript.count('[[FIG:') == 4
    checks += 5
    for i in range(1, 13):
        assert f'**Ejercicio {i} ' in manuscript
        assert f'**{i}.**' in manuscript
        checks += 2
    for word in ('AS6C62256', 'AT28C64B', 'A14', 'A12', 'DQ0',
                 'CE#', 'OE#', 'WE#', '32K × 8', '8K × 8', '64 KiB',
                 '0xE000', '0x7FFF', '0xDFFF', '0x0123', '0xE123',
                 '0x1200', '0x1201', '0x41', '0x53', 'SRAM', 'EEPROM',
                 'volátil', 'alta impedancia', '55 ns', '10 ms',
                 'capítulo 10', 'capítulo 22', 'Solucionario del capítulo 9'):
        assert word.lower() in manuscript.lower(), word
        checks += 1
    for figure in FIGURES:
        for ext, minimum in (('.svg', 1400), ('.png', 10000)):
            path = ROOT / 'libro' / 'figuras' / f'{figure}{ext}'
            assert path.exists() and path.stat().st_size > minimum, path
            checks += 1
        assert f'[[FIG:{figure}|' in manuscript
        checks += 1

    with zipfile.ZipFile(BASE.with_suffix('.docx')) as archive:
        assert archive.testzip() is None
        root = ET.fromstring(archive.read('word/document.xml'))
        equations = root.findall('.//m:oMath', NS)
        figures = root.findall('.//wp:inline', NS)
        assert len(equations) == 10, len(equations)
        assert len(figures) == 4, len(figures)
        assert all(f.find('wp:docPr', NS).get('descr') for f in figures)
        headers = [name for name in archive.namelist()
                   if name.startswith('word/header') and name.endswith('.xml')]
        assert headers and any(b'PARTE III' in archive.read(name) for name in headers)
        checks += 5

    pdf = BASE.with_suffix('.pdf')
    assert pdf.exists() and pdf.stat().st_size > 50000
    info = subprocess.run(['pdfinfo', str(pdf)], capture_output=True,
                          check=True, text=True).stdout
    pages = re.search(r'^Pages:\s*(\d+)', info, flags=re.M)
    assert pages and 7 <= int(pages.group(1)) <= 12
    pdf_text = subprocess.run(['pdftotext', str(pdf), '-'], capture_output=True,
                              check=True, text=True).stdout
    assert len(pdf_text) > 15000
    for token in ('RAM y ROM reales', 'Figura 1.', 'Figura 2.',
                  'Figura 3.', 'Figura 4.', 'Solucionario del capítulo 9',
                  'AS6C62256', 'AT28C64B', '0xE123', '64 KiB'):
        assert token in pdf_text, token
        checks += 1
    checks += 3
    print(f'Capítulo 9: {checks} controles matemáticos y documentales; '
          f'{pages.group(1)} páginas, 10 ecuaciones OMML, 4 figuras, 12 ejercicios.')
    print('Sin ensayos de SRAM/EEPROM físicas, mapa aprobado, CPU ni control temporal construido.')


if __name__ == '__main__':
    main()
