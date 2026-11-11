#!/usr/bin/env python3
"""Edición maestra reproducible C26 desde las 26 fuentes Markdown originales.

El índice se resuelve en dos pasadas: --pages-json recibe las páginas de inicio
medidas en el PDF de prueba, y reimprime el índice sin cambiar su altura.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from generar_capitulo_01 import add_rich, create_styles, equation, figure, parse, table, apply_font

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / 'libro' / 'capitulos'
OUTPUT = ROOT / 'libro' / 'Aula_Computadora_C26_0_1_MAESTRO.docx'
PAGE_INDEX = ROOT / 'libro' / 'INDICE_C26_0_1.json'
ORDER = sorted(CAP.glob('[0-9][0-9]_*.md'))
ORDER.insert(7, CAP / '07b_del_bit_al_significado.md')
ORDER.insert(-1, CAP / '23v_de_mapas_de_caracteres_a_escritorio_grafico.md')
assert len(ORDER) == 26, len(ORDER)

REFERENCES = [
    ('NIST', 'Guide for the Use of the International System of Units, SP 811', 'https://physics.nist.gov/cuu/pdf/sp811.pdf'),
    ('onsemi', '2N3904 NPN General-Purpose Amplifier', 'https://www.onsemi.com/pdf/datasheet/2n3904-d.pdf'),
    ('Texas Instruments', 'SN74HCT00, cuatro puertas NAND', 'https://www.ti.com/lit/ds/symlink/sn74hct00.pdf'),
    ('Texas Instruments', 'SN74HC74, flip-flops D', 'https://www.ti.com/lit/ds/symlink/sn74hc74.pdf'),
    ('Texas Instruments', 'SN74HC373, latches de ocho bits', 'https://www.ti.com/lit/ds/symlink/sn74hc373.pdf'),
    ('Texas Instruments', 'SN74HC377, registros con habilitación', 'https://www.ti.com/lit/ds/symlink/sn74hc377.pdf'),
    ('Texas Instruments', 'SN74HC138, decodificador 3 a 8', 'https://www.ti.com/lit/ds/symlink/sn74hc138.pdf'),
    ('Texas Instruments', 'CD74HC283, sumador de cuatro bits', 'https://www.ti.com/lit/ds/symlink/cd74hc283.pdf'),
    ('Texas Instruments', 'SN74HC86, puertas XOR', 'https://www.ti.com/lit/ds/symlink/sn74hc86.pdf'),
    ('Texas Instruments', 'SN74HC157, multiplexores 2 a 1', 'https://www.ti.com/lit/ds/symlink/sn74hc157.pdf'),
    ('Alliance Memory', 'AS6C62256, SRAM asíncrona 32 K × 8', 'https://www.alliancememory.com/as6c62256/'),
    ('Microchip', 'AT28C64B, EEPROM 8 K × 8', 'https://www.microchip.com/en-us/product/AT28C64B'),
    ('MITS', 'Altair 8800 Operators Manual', 'https://vtda.org/docs/computing/MITS/MITS_Altari8800OperatorsManual_1975.pdf'),
    ('Apple Computer', 'Apple-1 Operation Manual', 'https://device.report/m/52627e26d76bf7b0639394eca3b3471d97580b7e6f2e743a079ccd4fede03833'),
    ('MOS Technology', 'KIM-1 User Manual', 'https://www.kim-1.com/docs/usrman.htm'),
    ('Intel', 'The 8086 Family User’s Manual (1979)', 'https://bitsavers.org/components/intel/8086/9800722-03_The_8086_Family_Users_Manual_Oct79.pdf'),
    ('GNU Binutils', 'GNU assembler manual', 'https://sourceware.org/binutils/docs/as/'),
    ('IETF', 'RFC 3629, UTF-8', 'https://www.rfc-editor.org/rfc/rfc3629.html'),
    ('Unicode Consortium', 'Unicode Character Encoding Model (UTR 17)', 'https://www.unicode.org/reports/tr17/'),
    ('Commodore', 'C64 Programmer’s Reference Guide, gráficos', 'https://www.commodore.ca/manuals/c64_programmers_reference/c64-programmers_reference_guide-03-programming_graphics.pdf'),
    ('Texas Instruments', 'TMS9918A Video Display Processors Data Manual', 'https://computers.baffa.tec.br/pages/datasheet/TMS9918A_TMS9928A_TMS9929A_Video_Display_Processors_Data_Manual_Nov82.pdf'),
    ('W3C', 'SVG 2, Paths', 'https://www.w3.org/TR/SVG/paths.html'),
    ('Microsoft', 'Introducción a DirectWrite', 'https://learn.microsoft.com/en-us/windows/win32/directwrite/introducing-directwrite'),
    ('Microsoft', 'Desktop Window Manager, Overview', 'https://learn.microsoft.com/en-us/windows/win32/dwm/dwm-overview'),
]


def link(paragraph, label, url):
    part = paragraph.part
    rel_id = part.relate_to(url,
                            'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
                            is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), rel_id)
    run = OxmlElement('w:r')
    props = OxmlElement('w:rPr')
    col = OxmlElement('w:color'); col.set(qn('w:val'), '105679'); props.append(col)
    under = OxmlElement('w:u'); under.set(qn('w:val'), 'single'); props.append(under)
    run.append(props)
    t = OxmlElement('w:t'); t.text = label; run.append(t)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def heading_on_new_page(doc, value, *, level=1):
    p = doc.add_heading(value, level=level)
    p.paragraph_format.page_break_before = True
    return p


def get_titles():
    titles=[]
    for source in ORDER:
        blocks=parse(source.read_text(encoding='utf-8'))
        titles.append(next(val for typ,val in blocks if typ=='title'))
    return titles


def make_cover(doc):
    p=doc.add_paragraph(style='Title')
    p.paragraph_format.space_before=Pt(22)
    p.paragraph_format.space_after=Pt(7)
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.add_run('Aula Computadora')
    p=doc.add_paragraph()
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run('De la electricidad a una computadora que podemos explicar')
    r.font.name='Liberation Sans'; r.font.size=Pt(16)
    p.paragraph_format.space_after=Pt(14)
    # Ilustración histórica original: arte conceptual, nunca una foto de la CPU
    # candidata ni sustituto de un diagrama eléctrico verificable.
    p=doc.add_paragraph()
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(ROOT/'libro'/'figuras'/'portada_conceptual_c27.png'), width=Cm(12.5))
    p=doc.add_paragraph()
    p.paragraph_format.space_before=Pt(6)
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run('Edición C27 de estudio · 26 capítulos, incluidos 7B y 23B')
    r.font.size=Pt(10)
    p=doc.add_paragraph()
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.add_run('Marcos Moreira · Noviembre de 2026').italic=True


def make_credits(doc):
    heading_on_new_page(doc,'Sobre esta edición')
    p=doc.add_paragraph()
    add_rich(p,'**Aula Computadora** es un recorrido desde corriente, transistores y puertas lógicas hasta memoria, CPU, lenguaje de máquina, firmware, programación y salida visual. El hilo conductor son dos arquitecturas didácticas, **Aula-8** y **Aula-16**. No se presupone que el lector tenga que construir una placa antes de comprender el comportamiento del sistema.')
    p=doc.add_paragraph()
    add_rich(p,'Los **capítulos 7B y 23B** conectan temas que merecen su propia explicación: cómo los bits adquieren significado y cómo un sistema muestra caracteres y píxeles. Las cifras y los circuitos se acompañan de los supuestos necesarios para comprenderlos. Cuando aparece una arquitectura Aula se estudia su funcionamiento lógico; su eventual implementación física es un problema de ingeniería adicional.')
    p=doc.add_paragraph()
    add_rich(p,'La ilustración de portada presenta una **microcomputadora ficticia** de inspiración histórica. No representa una placa construida ni un esquema eléctrico operativo. Los dibujos de circuitos que acompañan al texto se identifican por su nivel —funcional, lógico o montaje de ejemplo— y no sustituyen la hoja de datos de componentes reales.')


def make_toc(doc, titles, numbers):
    for part in range(2):
        heading_on_new_page(doc,'Índice de contenidos' if part==0 else 'Índice de contenidos (continuación)')
        note=doc.add_paragraph()
        note.paragraph_format.space_after=Pt(12)
        note.add_run('Recorrido por la materia y las actividades de cada capítulo.').italic=True
        start,end=part*13,(part+1)*13
        for idx in range(start,end):
            p=doc.add_paragraph(style='EntradaIndice')
            p.paragraph_format.keep_together=True
            p.paragraph_format.tab_stops.add_tab_stop(Cm(15.65), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
            r=p.add_run(titles[idx]); r.bold=True
            p.add_run('\t')
            r=p.add_run(str(numbers.get(titles[idx], '000'))); r.bold=True


def make_reading_guide(doc):
    heading_on_new_page(doc,'Cómo recorrer el libro')
    for title,body in [
        ('Empezar por la intuición física','Los primeros capítulos distinguen corriente, tensión, lógica combinacional y memoria. Cada figura se interpreta como un modelo, y cada relación cuantitativa explicita sus supuestos.'),
        ('Seguir el dato','Los registros, buses y memorias permiten reconstruir qué sucede desde que una CPU solicita una dirección hasta que obtiene un byte o escribe un resultado.'),
        ('Programar sin magia','Las instrucciones de Aula-8 y Aula-16 enlazan operaciones binarias, control, pila y firmware. El libro separa rigurosamente el programa ilustrativo de una CPU ejecutada en hardware.'),
        ('Ver caracteres y píxeles','El capítulo 23B distingue ROM de caracteres, mapa de texto, mapa de píxeles, color, controlador de vídeo y subrutinas. El equipo didáctico elige un modo mediante registros; no necesita una GPU comercial.'),
        ('Repasar con intención','Al final de cada capítulo encontrarás ejercicios con soluciones. Puedes seleccionar los que comprueben las ideas que más te cuesta aplicar; lo importante es poder explicar y reconstruir cada recorrido.'),
    ]:
        doc.add_heading(title,level=2)
        doc.add_paragraph(body)
    p=doc.add_paragraph()
    add_rich(p,'**Convenciones de lectura:** `0x` introduce hexadecimal, los corchetes indican posiciones de memoria, y los diagramas separan las señales lógicas de sus hipotéticas implementaciones electrónicas.')


def selected_activity_blocks(blocks, source):
    """Actividades esenciales variables por capítulo en la edición C27.

    Las doce originales y sus doce soluciones quedan íntegramente en cada
    manuscrito Markdown y en la edición individual de los capítulos. El libro
    integral selecciona menos ejercicios donde la explicación necesita espacio.
    Los números visibles se renumeran consecutivamente junto a su solución.
    """
    core = {
        '01_la_corriente_y_sus_caminos.md',
        '05_la_realimentacion_conserva_informacion.md',
        '07_del_bit_al_registro.md',
        '08_direcciones_y_buses.md',
        '12_arquitectura_aula_8.md',
        '14_de_numeros_a_instrucciones.md',
        '16_subrutinas_y_pila.md',
        '22_un_bus_externo_de_16_bits.md',
    }
    selected = {
        '01_la_corriente_y_sus_caminos.md': (1, 3, 6, 7, 12),
        '08_direcciones_y_buses.md': (1, 3, 5, 7, 12),
        '22_un_bus_externo_de_16_bits.md': (2, 5, 8, 10, 11),
        '07b_del_bit_al_significado.md': (1, 6, 12),
        '23v_de_mapas_de_caracteres_a_escritorio_grafico.md': (1, 6, 12),
    }
    chosen = selected.get(source.name, (1, 3, 5, 9, 12) if source.name in core else (1, 5, 9, 12))
    renumber = {old: idx for idx, old in enumerate(chosen, 1)}
    phase = None
    result = []
    seen = {'exercise': set(), 'solution': set()}
    for kind, value in blocks:
        if kind == 'h1':
            if 'Ejercicios' in value:
                phase = 'exercise'
            elif value.startswith('Solucionario'):
                phase = 'solution'
            else:
                phase = None
        if phase == 'exercise' and kind == 'paragraph':
            match = re.match(r'^\*\*Ejercicio (\d+)\b', value)
            if match:
                old = int(match.group(1))
                if old not in renumber:
                    continue
                seen['exercise'].add(old)
                value = value.replace(f'**Ejercicio {old}', f'**Ejercicio {renumber[old]}', 1)
        if phase == 'solution' and kind == 'paragraph':
            match = re.match(r'^\*\*(\d+)\.\*\*', value)
            if match:
                old = int(match.group(1))
                if old not in renumber:
                    continue
                seen['solution'].add(old)
                value = value.replace(f'**{old}.**', f'**{renumber[old]}.**', 1)
        result.append((kind, value))
    if seen['exercise'] != set(chosen) or seen['solution'] != set(chosen):
        raise ValueError(f'Actividades y soluciones incompletas en {source}: {seen}')
    return result


def make_body(doc):
    for source in ORDER:
        blocks=selected_activity_blocks(parse(source.read_text(encoding='utf-8')), source)
        for i,(typ,val) in enumerate(blocks):
            if typ=='title':
                p=heading_on_new_page(doc,val)
                p.paragraph_format.space_before=Pt(20)
                p.paragraph_format.space_after=Pt(10)
            elif typ=='subtitle':
                p=doc.add_paragraph(style='SubtituloCapitulo')
                p.add_run(val)
            elif typ=='h1':
                h=doc.add_heading(val,level=2)
                if val.startswith('Solucionario') or (i>0 and blocks[i-1][0]=='pagebreak'):
                    h.paragraph_format.page_break_before=True
            elif typ=='pagebreak':
                continue
            elif typ=='h2':
                doc.add_heading(val,level=3)
            elif typ=='eq':
                p=equation(doc,val)
                if i+1<len(blocks) and blocks[i+1][0]=='table':
                    p.paragraph_format.keep_with_next=True
            elif typ=='fig':
                try:
                    figure(doc,*val)
                except Exception as exc:
                    raise RuntimeError(f'Figura inválida {val[0]} en {source.name}') from exc
            elif typ=='table':
                table(doc,val)
            elif typ=='number':
                p=doc.add_paragraph(style='Ejercicio')
                p.paragraph_format.left_indent=Cm(.55)
                p.paragraph_format.first_line_indent=Cm(-.55)
                add_rich(p,val)
            else:
                p=doc.add_paragraph(style='Ejercicio' if val.startswith('**Ejercicio ') else 'Normal')
                if i+1<len(blocks) and blocks[i+1][0] in {'table','eq'}:
                    p.paragraph_format.keep_with_next=True
                add_rich(p,val)


def make_bibliography(doc):
    heading_on_new_page(doc,'Fuentes y lecturas recomendadas')
    p=doc.add_paragraph()
    p.add_run('Una selección de manuales, normas y documentos históricos para profundizar. ').bold=True
    p.add_run('La lista ampliada está en FUENTES_CONSULTADAS.txt del repositorio.')
    for idx,(owner,title,url) in enumerate(REFERENCES,1):
        p=doc.add_paragraph(style='Referencia')
        p.add_run(f'{idx}. {owner}. ').bold=True
        p.add_run(f'{title}. ')
        link(p,'Fuente original',url)
    doc.add_heading('Materiales de contexto',level=2)
    doc.add_paragraph('J. Clark Scott, But How Do It Know? The Basic Principles of Computers for Everyone. Referencia didáctica externa, no reproducida ni traducida en este volumen.')
    doc.add_paragraph('Fernando Sandoval Galárraga y Marcos Alejandro Moreira Merino, Una Historia en 8 Bits. Manuscrito previo de coautoría usado como antecedente conceptual, sin incorporación automática de figuras o pasajes.')
    doc.add_paragraph('Los contratos de microarquitectura, ISA y vídeo de Aula-8 y Aula-16 son originales del repositorio y no se atribuyen a las CPU históricas consultadas.')


def build(pages):
    doc=Document()
    create_styles(doc,running_title='Aula Computadora',part='I–VI')
    for name,size,before,after in [('Heading 1',20,20,9),('Heading 2',14.2,16,7),('Heading 3',11.7,11,5)]:
        s=doc.styles[name]
        apply_font(s,'Liberation Sans',size,bold=True,color=RGBColor(17,71,101))
        s.paragraph_format.space_before=Pt(before)
        s.paragraph_format.space_after=Pt(after)
        s.paragraph_format.keep_with_next=True
    doc.styles['Title'].font.name='Liberation Sans'
    doc.styles['Title'].font.size=Pt(38)
    doc.styles['Title'].font.bold=True
    doc.styles['Title'].font.color.rgb=RGBColor(0,0,0)
    # Word/LibreOffice pueden insertar una regla azul heredada bajo Title.
    title_props=doc.styles['Title'].element.get_or_add_pPr()
    rule=title_props.find(qn('w:pBdr'))
    if rule is not None:
        title_props.remove(rule)
    for name,sz,sp in [('EntradaIndice',10.6,10),('Referencia',9.3,7),('SubtituloCapitulo',10.1,19)]:
        style=doc.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
        style.base_style=doc.styles['Normal']
        apply_font(style,'Liberation Serif' if name!='SubtituloCapitulo' else 'Liberation Sans',sz,color=RGBColor(38,53,65))
        style.paragraph_format.space_after=Pt(sp)
    doc.styles['SubtituloCapitulo'].font.italic=True
    doc.styles['SubtituloCapitulo'].paragraph_format.keep_with_next=True
    doc.core_properties.title='Aula Computadora'
    doc.core_properties.subject='Libro didáctico de electrónica digital, arquitectura, CPU y vídeo'
    doc.core_properties.author='Marcos Moreira'
    make_cover(doc)
    make_credits(doc)
    make_toc(doc,get_titles(),pages)
    make_reading_guide(doc)
    make_body(doc)
    make_bibliography(doc)
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    doc.save(OUTPUT)
    print(f'WORD MAESTRO: {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)')
    print(f'Capítulos: {len(ORDER)}; bibliografía: {len(REFERENCES)} fuentes')


def derive_page_index(pdf):
    text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
    pages=[' '.join(page.split()) for page in text.split('\f')]
    numbering={}
    for title in get_titles():
        found=[idx+1 for idx,page in enumerate(pages) if idx>=5 and title in page]
        if not found:
            raise ValueError(f'No se encontró encabezado en PDF: {title}')
        numbering[title]=found[0]
    vals=list(numbering.values())
    if vals!=sorted(vals):
        raise ValueError(f'Orden inconsistente en PDF: {vals}')
    PAGE_INDEX.write_text(json.dumps(numbering,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'ÍNDICE PAGINADO: {PAGE_INDEX}; capítulos: {vals}')


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--pages-json',type=Path)
    ap.add_argument('--derive-pages',type=Path)
    args=ap.parse_args()
    if args.derive_pages:
        derive_page_index(args.derive_pages)
    else:
        build(json.loads(args.pages_json.read_text(encoding='utf-8')) if args.pages_json else {})
