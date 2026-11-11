#!/usr/bin/env python3
"""Edición incremental C28-E: PC16 sin aprobar microarquitectura real."""

import argparse
import json
from pathlib import Path

import generar_libro_maestro_c28d as base

maestro = base.maestro
ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "libro" / "ediciones" / "C28_E"
maestro.OUTPUT = EDITION / "Aula_Computadora_C28_E_MAESTRO.docx"
maestro.PAGE_INDEX = EDITION / "INDICE_C28_E.json"
maestro.ORDER = [
    ROOT / "libro" / "revisiones_c28e" / "15_la_instruccion_en_movimiento_c28e.md"
    if source.name == "15_la_instruccion_en_movimiento_c28d.md" else source
    for source in maestro.ORDER
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages-json", type=Path)
    parser.add_argument("--derive-pages", type=Path)
    args = parser.parse_args()
    EDITION.mkdir(parents=True, exist_ok=True)
    if args.derive_pages:
        maestro.derive_page_index(args.derive_pages)
    else:
        pages = json.loads(args.pages_json.read_text(encoding="utf-8")) if args.pages_json else {}
        maestro.build(pages)


if __name__ == "__main__":
    main()
