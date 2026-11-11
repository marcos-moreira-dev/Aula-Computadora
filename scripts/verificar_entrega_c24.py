#!/usr/bin/env python3
"""Verifica interludio P23V y C24, diagramas y matemáticas del vídeo.

No certifica circuitos físicos, firmware ni ejecución en CPUs Aula.
Solo usa librería estándar, Poppler y los artefactos DOCX/PDF incluidos.
"""
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

from generar_diagramas_c24_p23v import GLYPHS, glyph_pixels, figures, validate_math

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'libro' / 'capitulos'
NS = {
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'svg': 'http://www.w3.org/2000/svg',
}
DOCUMENTS = {
    '23v_de_mapas_de_caracteres_a_escritorio_grafico': (7, 13, 10, 'capítulo 23B'),
    '24_una_computadora_que_podemos_explicar': (4, 13, 9, 'capítulo 24'),
}


def contracts():
    v = json.loads((ROOT / 'simulador-javafx/VIDEO_AULA_V1_CONTRATO.json').read_text(encoding='utf-8'))
    assert v['status'] == 'diseno_logico_congelado_no_implementado'
    for k,expected in (('graphics_width_pixels',256),('graphics_height_pixels',128),
                       ('graphics_bits_per_pixel',2),('graphics_color_count',4),
                       ('text_columns',32),('text_rows',16),('text_buffer_bytes',512),
                       ('graphics_buffer_bytes',8192),('glyph_rom_bytes',2048),
                       ('total_video_ram_bytes',8704),('video_control_reset_value',12)):
        assert v[k] == expected,k
    addrs={int(r['address'],16):r['name'] for r in v['registers']}
    assert addrs == {0xC020:'VIDEO_MODE',0xC022:'VIDEO_STATUS',0xC024:'VRAM_ADDR_LO',
                     0xC026:'VRAM_ADDR_HI',0xC028:'VRAM_DATA',0xC02A:'VIDEO_CTRL'}
    assert v['text_and_graphics_buffers_separate']
    assert not v['physical_video_hardware_implemented']
    assert not v['graphics_instruction_opcodes_added']
    assert not v['video_ram_directly_cpu_mapped']
    assert not v['video_ram_assumed_cleared_on_reset']
    assert not v['font_bitmap_bytes_implemented']
    return 25


def pixels():
    checks=0
    validate_math()
    # Todos los puntos deben estar en la región prevista; las cuatro posiciones
    # de un mismo byte deben usar pares de bits distintos, MSB primero.
    seen_offsets=set()
    for y in range(128):
        for x in range(256):
            loc=y*64+x//4
            shift=6-2*(x%4)
            assert 0 <= loc < 8192
            assert shift in (6,4,2,0)
            assert ((3 << shift) & 0xFF) != 0
            assert ((3 << shift) >> shift) == 3
            assert (loc,shift) not in seen_offsets
            seen_offsets.add((loc,shift))
            checks += 1
    assert len(seen_offsets) == 256*128
    for y in range(128):
        for x in range(256):
            loc=y*32+x//8
            bit=7-x%8
            assert 0 <= loc < 4096 and 0 <= bit <= 7
            checks += 1
    for glyph, rows in GLYPHS.items():
        for y,b in enumerate(rows):
            bits=glyph_pixels(glyph)[y]
            assert sum(bits)==b.bit_count()
            assert b==sum(v << (7-x) for x,v in enumerate(bits))
            checks += 8
    return checks


def diagrams():
    expected=figures()
    assert len(expected)==11
    checks=0
    for name,source in expected.items():
        svg=ROOT / 'libro/figuras' / f'{name}.svg'
        png=svg.with_suffix('.png')
        assert svg.is_file() and png.is_file(),name
        assert png.stat().st_size > 10000
        assert source == svg.read_text(encoding='utf-8'),name
        tree=ET.parse(svg).getroot()
        assert tree.get('viewBox') == '0 0 1000 500'
        checks += 4
    # Las 512 celdas visualizadas tienen coordenadas x/y y color de HOLA.
    tree=ET.parse(ROOT / 'libro/figuras/p23v_fig02_mapa_texto_32x16.svg').getroot()
    rects={(int(float(r.get('x'))),int(float(r.get('y')))) for r in tree.findall('.//svg:rect',NS)
           if r.get('width')=='21' and r.get('height')=='21'}
    assert rects=={(92+x*21,105+y*21) for y in range(16) for x in range(32)}
    checks += 512
    # Figura 1: el cuadro oscuro debe corresponder al bit 1 de cada fila original.
    tree=ET.parse(ROOT / 'libro/figuras/p23v_fig01_codigo_glifo.svg').getroot()
    cells={(int(float(r.get('x'))),int(float(r.get('y')))):r.get('fill')
           for r in tree.findall('.//svg:rect',NS) if r.get('width')=='37'}
    assert len(cells)==64
    for y,row in enumerate(glyph_pixels('A')):
        for x,b in enumerate(row):
            assert cells[(700+37*x,132+37*y)] == ('#143d58' if b else '#fbfbf6')
            checks+=1
    return checks


def document(base, fig_count, eq_count, pages, label):
    source=(BASE/(base+'.md')).read_text(encoding='utf-8')
    assert source.count('[[FIG:')==fig_count
    assert source.count('[[EQ:')==eq_count
    assert len(re.findall(r'^\*\*Ejercicio \d+ ',source,re.M))==12
    assert 'JavaFX' not in source
    for n in range(1,13):
        assert f'**Ejercicio {n} ' in source
        assert f'**{n}.**' in source
    assert source.count('[[PAGEBREAK]]')==2
    assert sum(1 for line in source.splitlines() if line.startswith('| ---')) >= 3
    fig_names=re.findall(r'\[\[FIG:([^|]+)\|',source)
    assert fig_names==[name for name in figures() if name in fig_names] if label=='capítulo 23B' else len(fig_names)==4
    with zipfile.ZipFile(BASE/(base+'.docx')) as z:
        assert z.testzip() is None
        root=ET.fromstring(z.read('word/document.xml'))
        assert len(root.findall('.//m:oMath',NS))==eq_count
        imgs=root.findall('.//wp:inline',NS)
        assert len(imgs)==fig_count
        assert len(root.findall('.//w:tbl',NS))>=3
        assert all(image.find('wp:docPr',NS).get('descr') for image in imgs)
    pdf=BASE/(base+'.pdf')
    assert pdf.is_file() and pdf.stat().st_size>60000
    info=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True,check=True).stdout
    assert re.search(rf'^Pages:\s*{pages}$',info,re.M),f'{label} paginación cambiada'
    txt=subprocess.run(['pdftotext',str(pdf),'-'],capture_output=True,text=True,check=True).stdout
    assert len(txt)>11000,(label,len(txt))
    for i in range(1,fig_count+1):
        assert f'Figura {i}.' in txt
    assert 'Solucionario del' in txt
    assert label.split()[-1] in source
    return 40+12*2+fig_count


def main():
    total=contracts()+pixels()+diagrams()
    for base, params in DOCUMENTS.items():
        total+=document(base,*params)
    print(f'P23V/C24: {total:,} comprobaciones exactas, documentales y matemáticas correctas.')
    print('P23V: 7 SVG + PNG, 13 OMML, 12 ejercicios, Word y PDF de 10 páginas.')
    print('C24: 4 SVG + PNG, 13 OMML, 12 ejercicios, Word y PDF de 9 páginas.')
    print('Aviso: no se ha ejecutado ni certificado hardware Aula.')


if __name__=='__main__':
    main()
