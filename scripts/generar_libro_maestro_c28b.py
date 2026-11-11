#!/usr/bin/env python3
"""Edición de trabajo C28-B: portada aprobada y láminas de R0.

Conserva intactos el maestro y los capítulos fuente de C27. Los cambios
editoriales de C28-B viven en libro/revisiones_c28b y libro/portadas.
"""

import argparse
import json
import re
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

import generar_libro_maestro as maestro


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / 'libro' / 'ediciones' / 'C28_B'
maestro.OUTPUT = EDITION / 'Aula_Computadora_C28_B_MAESTRO.docx'
maestro.PAGE_INDEX = EDITION / 'INDICE_C28_B.json'
maestro.ORDER = [
    ROOT / 'libro' / 'revisiones_c28b' / '07_del_bit_al_registro_c28b.md'
    if source.name == '07_del_bit_al_registro.md' else source
    for source in maestro.ORDER
]
maestro.ORDER = [
    ROOT / 'libro' / 'revisiones_c28b' / '22_un_bus_externo_de_16_bits_c28b.md'
    if source.name == '22_un_bus_externo_de_16_bits.md' else source
    for source in maestro.ORDER
]


def make_cover_c28b(doc):
    """La imagen aprobada incorpora título, subtítulo y firma gráfica."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    cover = ROOT / 'libro' / 'portadas' / 'Aula_Computadora_Portada_IA_C28_Boceto01.png'
    if not cover.is_file():
        raise FileNotFoundError(cover)
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Equilibra el blanco superior e inferior sin cambiar márgenes del cuerpo.
    paragraph.paragraph_format.space_before = Pt(39)
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 1
    paragraph.add_run().add_picture(str(cover), width=Cm(16.2))


maestro.make_cover = make_cover_c28b


original_equation = maestro.equation


def equation_c28b(document, formula):
    """Protege hexadecimales contra los espacios erráticos del motor de OMML.

    Las potencias de base diez o dieciséis se muestran con superíndices de
    fuente. Ecuaciones sin literales hex conservan su formato OMML estructurado.
    """
    if '0x' not in formula:
        return original_equation(document, formula)
    para = document.add_paragraph(style='Ecuacion')
    para.paragraph_format.keep_together = True
    para.paragraph_format.keep_with_next = True
    segments = re.split(r'(0x[0-9A-Fa-f]+|[⁰¹²³⁴⁵⁶⁷⁸⁹]+)', formula)
    superscript_translation = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')
    for segment in segments:
        if not segment:
            continue
        r = para.add_run(segment.translate(superscript_translation) if segment[0] in '⁰¹²³⁴⁵⁶⁷⁸⁹' else segment)
        if segment.startswith('0x'):
            r.font.name = 'Liberation Mono'
            r.font.size = Pt(10.4)
        elif segment[0] in '⁰¹²³⁴⁵⁶⁷⁸⁹':
            r.font.superscript = True
    return para


maestro.equation = equation_c28b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages-json', type=Path)
    parser.add_argument('--derive-pages', type=Path)
    args = parser.parse_args()
    EDITION.mkdir(parents=True, exist_ok=True)
    if args.derive_pages:
        maestro.derive_page_index(args.derive_pages)
    else:
        pages = json.loads(args.pages_json.read_text(encoding='utf-8')) if args.pages_json else {}
        maestro.build(pages)


if __name__ == '__main__':
    main()
