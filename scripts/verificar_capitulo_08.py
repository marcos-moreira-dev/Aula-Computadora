#!/usr/bin/env python3
"""Verifica matemáticas, bus lógico y entregables del capítulo 8.

No comprueba electrónica, temporización física o CPU Aula implementada.
"""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'libro' / 'capitulos' / '08_direcciones_y_buses'
FIGURES = (
    'c08_fig01_decodificador_dos_bits',
    'c08_fig02_buses_separados',
    'c08_fig03_lectura_escritura',
    'c08_fig04_aula8_aula16',
)
NS = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}


def selected_cell(a1: int, a0: int) -> int:
    assert a1 in (0, 1) and a0 in (0, 1)
    return a1 * 2 + a0


def drive(cpu: int | None, memory: int | None) -> int | None:
    if cpu is not None and memory is not None:
        raise ValueError('Contención: CPU y memoria conducen el bus')
    return cpu if cpu is not None else memory


def main():
    count = 0
    # Todas las direcciones de 16 bits: binario y hexadecimal conservan valor.
    for address in range(1 << 16):
        bits = f'{address:016b}'
        hexadecimal = f'{address:04X}'
        assert int(bits, 2) == address
        assert int(hexadecimal, 16) == address
        assert sum(int(bit) * (1 << (15 - position))
                   for position, bit in enumerate(bits)) == address
        assert len(bits) == 16 and len(hexadecimal) == 4
        count += 4
    assert 2 ** 16 == 65536 and 65536 // 1024 == 64
    assert int('1200', 16) == 4608
    assert int('1201', 16) == 4609
    assert int('FFFF', 16) == 65535
    assert int('10000', 16) == 65536
    assert f'{0x1200:016b}' == '0001001000000000'
    assert f'{0x1201:016b}' == '0001001000000001'
    assert 1 * 4096 + 2 * 256 + 0 * 16 + 0 == 4608
    count += 8

    # Decodificador 2->4 de salida activa en alto.
    for a1 in (0, 1):
        for a0 in (0, 1):
            outputs = [int(i == selected_cell(a1, a0)) for i in range(4)]
            assert sum(outputs) == 1
            assert outputs[selected_cell(a1, a0)] == 1
            count += 2

    # Un byte por posición; leer y escribir no reescribe vecinos.
    ram = {0b00: 0x12, 0b01: 0xA5, 0b10: 0x3C, 0b11: 0xFF}
    for position, stored in ram.items():
        assert ram[selected_cell((position >> 1) & 1, position & 1)] == stored
        count += 1
    ram[0b01] = 0x7E
    assert ram == {0: 0x12, 1: 0x7E, 2: 0x3C, 3: 0xFF}
    count += 1

    # Compartir un bus con un conductor como máximo: Z -> None, no cero.
    for value in range(256):
        assert drive(value, None) == value
        assert drive(None, value) == value
        count += 2
    assert drive(None, None) is None
    try:
        drive(0x00, 0xFF)
        raise AssertionError('No se detectó la contención')
    except ValueError:
        pass
    count += 2

    # Reglas abstractas de control y operación.
    assert (0, 0, 1) != (0, 1, 0)
    assert (0, 0, 0) not in {(0, 0, 1), (0, 1, 0)}
    content = {0x1200: 0x41, 0x1201: 0x00}
    assert drive(None, content[0x1200]) == 0x41
    content[0x1201] = drive(0x53, None)
    assert content == {0x1200: 0x41, 0x1201: 0x53}
    assert int('01010011', 2) == 83
    count += 5

    # Aula-8/Aula-16: igual dirección, dos anchos de dato y little-endian.
    for word in range(65536):
        low = word & 0xFF
        high = word >> 8
        assert low in range(256) and high in range(256)
        assert low + (high << 8) == word
        assert word.to_bytes(2, 'little') == bytes((low, high))
        count += 3
    assert 0x1234 == 0x12 * 256 + 0x34 == 4660
    assert (0x2000 % 2) == 0 and (0x2001 % 2) == 1
    count += 2

    manuscript = BASE.with_suffix('.md').read_text(encoding='utf-8')
    assert manuscript.startswith('# Capítulo 8. Direcciones y buses')
    assert '*Parte III' in manuscript
    assert 'JavaFX' not in manuscript
    assert manuscript.count('[[EQ:') == 11
    assert manuscript.count('[[FIG:') == 4
    count += 5
    for index in range(1, 13):
        assert f'**Ejercicio {index} ' in manuscript
        assert f'**{index}.**' in manuscript
        count += 2
    for token in ('0x1200', '0x1201', '0x41', '0x53', '0xFFFF',
                  '0x10000', '65 536', '64 KiB', 'A15', 'D7',
                  'decodificador', 'multiplexor', 'SN74HC138',
                  'AS6C62256', 'CS_n', 'RD_n', 'WR_n', 'alta impedancia',
                  'Aula-8', 'Aula-16', 'little-endian', 'byte bajo',
                  'byte alto', 'alineados', 'Solucionario del capítulo 8',
                  'capítulo 9'):
        assert token.lower() in manuscript.lower(), token
        count += 1
    for name in FIGURES:
        for ext, min_size in (('.svg', 1300), ('.png', 10000)):
            file = ROOT / 'libro' / 'figuras' / (name + ext)
            assert file.is_file() and file.stat().st_size > min_size, file
            count += 1
        assert f'[[FIG:{name}|' in manuscript
        count += 1

    with zipfile.ZipFile(BASE.with_suffix('.docx')) as archive:
        assert archive.testzip() is None
        xml = ET.fromstring(archive.read('word/document.xml'))
        maths = xml.findall('.//m:oMath', NS)
        pictures = xml.findall('.//wp:inline', NS)
        assert len(maths) == 11, len(maths)
        assert len(pictures) == 4, len(pictures)
        assert all(p.find('wp:docPr', NS).get('descr') for p in pictures)
        headers = [p for p in archive.namelist()
                   if p.startswith('word/header') and p.endswith('.xml')]
        assert headers and any(b'PARTE III' in archive.read(p) for p in headers)
        count += 5

    pdf = BASE.with_suffix('.pdf')
    assert pdf.is_file() and pdf.stat().st_size > 50_000
    info = subprocess.run(['pdfinfo', str(pdf)], text=True,
                          capture_output=True, check=True).stdout
    pages = re.search(r'^Pages:\s*(\d+)', info, flags=re.M)
    assert pages and 7 <= int(pages.group(1)) <= 12
    text = subprocess.run(['pdftotext', str(pdf), '-'], text=True,
                          capture_output=True, check=True).stdout
    assert len(text) > 12500
    for token in ('Direcciones y buses', 'Figura 1.', 'Figura 2.',
                  'Figura 3.', 'Figura 4.', 'Solucionario del capítulo 8',
                  '0x1200', '0x1201', '0x1234', '64 KiB'):
        assert token in text, token
        count += 1
    count += 3
    print(f'Capítulo 8: {count} controles matemáticos y documentales correctos; '
          f'{pages.group(1)} páginas, 11 ecuaciones OMML, 4 figuras, 12 ejercicios.')
    print('La validación NO equivale a un bus eléctrico, memoria, CPU o firmware implementados.')


if __name__ == '__main__':
    main()
