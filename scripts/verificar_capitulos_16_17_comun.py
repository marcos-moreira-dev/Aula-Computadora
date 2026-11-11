#!/usr/bin/env python3
"""Inspección reutilizable de capítulos del libro; no valida hardware."""

from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NS = {
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}


def verificar_documentos(numero, slug, figuras, paginas, claves, ecuaciones=12):
    base = ROOT / 'libro' / 'capitulos' / f'{numero}_{slug}'
    source = base.with_suffix('.md').read_text(encoding='utf-8')
    assert source.startswith(f'# Capítulo {int(numero)}.'), numero
    assert source.count('[[EQ:') == ecuaciones
    assert source.count('[[FIG:') == 4
    assert source.count('**Ejercicio ') == 12
    assert 'JavaFX' not in source
    checks = 16

    for num in range(1, 13):
        assert f'**Ejercicio {num} ' in source
        assert f'**{num}.**' in source
        checks += 2
    for token in claves:
        assert token in source, token
        checks += 1
    for fig in figuras:
        assert f'[[FIG:{fig}|' in source
        for extension, minimum in (('.svg', 800), ('.png', 10000)):
            path = ROOT / 'libro' / 'figuras' / (fig + extension)
            assert path.is_file() and path.stat().st_size > minimum, path
            checks += 1
        ET.parse(ROOT / 'libro' / 'figuras' / (fig + '.svg'))
        checks += 1

    with zipfile.ZipFile(base.with_suffix('.docx')) as archive:
        assert archive.testzip() is None
        tree = ET.fromstring(archive.read('word/document.xml'))
        maths = tree.findall('.//m:oMath', NS)
        images = tree.findall('.//wp:inline', NS)
        tables = tree.findall('.//w:tbl', NS)
        assert len(maths) == ecuaciones, len(maths)
        assert len(images) == 4, len(images)
        assert len(tables) >= 3, len(tables)
        assert all(im.find('wp:docPr', NS).get('descr') for im in images)
        checks += 6

    pdf = base.with_suffix('.pdf')
    assert pdf.is_file() and pdf.stat().st_size > 60000
    info = subprocess.run(['pdfinfo', str(pdf)], text=True,
                          capture_output=True, check=True).stdout
    match = re.search(r'^Pages:\s*(\d+)', info, re.M)
    assert match and int(match.group(1)) == paginas, info
    content = subprocess.run(['pdftotext', str(pdf), '-'], text=True,
                             capture_output=True, check=True).stdout
    assert len(content) > 11000, len(content)
    for token in (f'Capítulo {int(numero)}', 'Figura 1.', 'Figura 2.',
                  'Figura 3.', 'Figura 4.', f'Solucionario del capítulo {int(numero)}'):
        assert token in content, token
        checks += 1
    checks += 3
    return checks
