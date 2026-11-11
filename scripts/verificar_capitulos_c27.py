#!/usr/bin/env python3
"""Comprueba que los 26 fascículos corresponden a sus fuentes C27."""

from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import re
import subprocess

from generar_libro_maestro import ORDER, parse

OMML = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'


def main():
    paginas = ecuaciones = figuras = 0
    for source in ORDER:
        blocks = parse(source.read_text(encoding='utf-8'))
        title = next(val for typ, val in blocks if typ == 'title')
        eq_count = sum(typ == 'eq' for typ, _ in blocks)
        fig_count = sum(typ == 'fig' for typ, _ in blocks)
        assert sum(typ == 'paragraph' and val.startswith('**Ejercicio ')
                   for typ, val in blocks) == 12, source
        docx = source.with_suffix('.docx')
        pdf = source.with_suffix('.pdf')
        assert docx.is_file() and pdf.is_file(), source
        with ZipFile(docx) as z:
            assert z.testzip() is None
            tree = ET.fromstring(z.read('word/document.xml'))
            actual_eq = len(tree.findall('.//' + OMML + 'oMathPara'))
            actual_pictures = sum(name.startswith('word/media/') for name in z.namelist())
            assert actual_eq == eq_count, (source.name, actual_eq, eq_count)
            assert actual_pictures >= fig_count, (source.name, actual_pictures, fig_count)
        info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
        p = int(re.search(r'^Pages:\s*(\d+)', info, re.M).group(1))
        assert 5 <= p <= 40, (source.name, p)
        raw = subprocess.check_output(['pdftotext', str(pdf), '-'], text=True)
        # LibreOffice puede partir un guion de título al final de línea y
        # eliminarlo en la capa de texto del PDF.
        flat_title = ' '.join(title.replace('-', '').split())
        flat_pdf = ' '.join(raw.replace('-', '').replace('\u00ad', '').split())
        assert flat_title in flat_pdf, source.name
        paginas += p
        ecuaciones += eq_count
        figuras += fig_count
    print(f'FASCÍCULOS C27 APROBADOS: {len(ORDER)} Word/PDF, '
          f'{figuras} figuras, {ecuaciones} ecuaciones, '
          f'{paginas} páginas acumuladas individuales.')


if __name__ == '__main__':
    main()
