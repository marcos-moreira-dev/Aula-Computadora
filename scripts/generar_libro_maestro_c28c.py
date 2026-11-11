#!/usr/bin/env python3
"""Edición C28-C con nueva lámina de dieciséis conductores de Aula-16."""

import argparse
import json
from pathlib import Path

import generar_libro_maestro_c28b as base


maestro = base.maestro
ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / 'libro' / 'ediciones' / 'C28_C'
maestro.OUTPUT = EDITION / 'Aula_Computadora_C28_C_MAESTRO.docx'
maestro.PAGE_INDEX = EDITION / 'INDICE_C28_C.json'
maestro.ORDER = [
    ROOT / 'libro' / 'revisiones_c28c' / '22_un_bus_externo_de_16_bits_c28c.md'
    if source.name == '22_un_bus_externo_de_16_bits_c28b.md' else source
    for source in maestro.ORDER
]
maestro.ORDER = [
    ROOT / 'libro' / 'revisiones_c28c' / '07_del_bit_al_registro_c28c.md'
    if source.name == '07_del_bit_al_registro_c28b.md' else source
    for source in maestro.ORDER
]


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
