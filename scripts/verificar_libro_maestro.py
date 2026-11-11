#!/usr/bin/env python3
"""Auditoría estructural y editorial de C26 y sus actividades seleccionadas."""
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import json
import re
import subprocess
import sys
from xml.etree import ElementTree as ET

from generar_libro_maestro import ROOT, ORDER, OUTPUT, REFERENCES, PAGE_INDEX, parse, selected_activity_blocks

PDF = OUTPUT.with_suffix('.pdf')
WORD_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
MATH_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'


def verify():
    assert OUTPUT.is_file() and OUTPUT.stat().st_size > 1_000_000
    assert PDF.is_file() and PDF.stat().st_size > 100_000
    titles=[]; equations=0; figures=[]; exercises_full=0; exercises_book=0
    for source in ORDER:
        blocks=parse(source.read_text(encoding='utf-8'))
        assert blocks[0][0]=='title',source
        titles.append(blocks[0][1])
        equations+=sum(t=='eq' for t,_ in blocks)
        figures.extend(v[0] for t,v in blocks if t=='fig')
        exercises_full+=sum(t=='paragraph' and v.startswith('**Ejercicio ') for t,v in blocks)
        chosen=selected_activity_blocks(blocks,source)
        exercises_book+=sum(t=='paragraph' and v.startswith('**Ejercicio ') for t,v in chosen)
    assert len(ORDER)==26 and len(titles)==len(set(titles))
    assert exercises_full==312 and exercises_book==110,(exercises_full,exercises_book)
    with ZipFile(OUTPUT) as z:
        assert z.testzip() is None
        xml=z.read('word/document.xml')
        tree=ET.fromstring(xml)
        math_count=len(tree.findall('.//'+MATH_NS+'oMathPara'))
        powers=len(tree.findall('.//'+MATH_NS+'sSup'))
        headings=tree.findall('.//'+WORD_NS+'pStyle')
        headings_1=sum(item.attrib.get(WORD_NS+'val')=='Heading1' for item in headings)
        images={name for name in z.namelist() if name.startswith('word/media/')}
        hyperlinks=z.read('word/_rels/document.xml.rels').decode('utf-8')
        assert math_count==equations,(math_count,equations)
        assert powers>=10,powers
        assert headings_1 >= 26,headings_1
        assert len(images) >= len(set(figures)),(len(images),len(set(figures)))
        assert all(url in hyperlinks for _,_,url in REFERENCES)
    info=subprocess.check_output(['pdfinfo',str(PDF)],text=True)
    pages=int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))
    assert 170 <= pages < 400,pages
    txt=subprocess.check_output(['pdftotext','-layout',str(PDF),'-'],text=True)
    all_pages=txt.split('\f')
    normalized_pages=[' '.join(page.split()) for page in all_pages]
    assert len(all_pages)>=pages
    for title in titles:
        assert title in txt,f'No aparece título {title}'
    assert txt.count('Fuentes y lecturas recomendadas')>=1
    assert 'Referencias y alcance de lo comprobado' not in txt
    assert 'Capítulo 7B.' in txt and 'Capítulo 23B.' in txt
    assert 'Sobre esta edición' in txt and 'Cómo recorrer el libro' in txt
    # Las primeras páginas de cada capítulo deben aparecer tras el sumario.
    headings_with_page=[]
    for title in titles:
        matches=[idx+1 for idx,page in enumerate(normalized_pages[:pages]) if title in page and idx+1>=6]
        assert matches,f'No hay página de capítulo {title}'
        headings_with_page.append(matches[0])
    assert headings_with_page == sorted(headings_with_page),headings_with_page
    index=json.loads(PAGE_INDEX.read_text(encoding='utf-8'))
    assert len(index)==26
    toc=' '.join(' '.join(page.split()) for page in all_pages[2:4])
    for title,page in zip(titles,headings_with_page):
        assert index[title]==page,(title,index[title],page)
        assert re.search(re.escape(title)+r'\.{3,}\s*'+str(page)+r'\b',toc),('TOC',title,page)
    # Páginas vacías no previstas solo entre el índice y las referencias.
    empty=[i+1 for i,page in enumerate(all_pages[:pages]) if len(page.strip())<18]
    assert len(empty)<=2,empty
    print(f'VERIFICACIÓN MAESTRA C27 APROBADA: {len(titles)} capítulos, '
          f'{len(figures)} menciones de figuras, {math_count} ecuaciones OMML, '
          f'{exercises_book} ejercicios esenciales ({exercises_full} en fuentes), '
          f'{len(REFERENCES)} fuentes, {pages} páginas.')
    print(f'Imágenes DOCX: {len(images)}; potencias OMML: {powers}; '
          f'títulos Heading 1: {headings_1}; páginas vacías: {empty}')


if __name__=='__main__':
    try:
        verify()
    except Exception as e:
        print(f'FALLO DE AUDITORÍA MAESTRA: {e}',file=sys.stderr)
        raise
