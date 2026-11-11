#!/usr/bin/env python3
"""Regenera la edición C27 sin sobrescribir los archivos maestros C26."""

import argparse
import json
from pathlib import Path

import generar_libro_maestro as maestro


maestro.OUTPUT = maestro.ROOT / 'libro' / 'Aula_Computadora_C27_0_1_MAESTRO.docx'
maestro.PAGE_INDEX = maestro.ROOT / 'libro' / 'INDICE_C27_0_1.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages-json', type=Path)
    parser.add_argument('--derive-pages', type=Path)
    args = parser.parse_args()
    if args.derive_pages:
        maestro.derive_page_index(args.derive_pages)
        return
    pages = json.loads(args.pages_json.read_text(encoding='utf-8')) if args.pages_json else {}
    maestro.build(pages)


if __name__ == '__main__':
    main()
