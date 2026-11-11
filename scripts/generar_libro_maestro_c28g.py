#!/usr/bin/env python3
"""Edición C28-G incremental desde C28-F, ISA y tiempos aún candidatos."""

import argparse
import json
from pathlib import Path

import generar_libro_maestro_c28f as base

maestro = base.maestro
ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "libro" / "ediciones" / "C28_G"
maestro.OUTPUT = EDITION / "Aula_Computadora_C28_G_MAESTRO.docx"
maestro.PAGE_INDEX = EDITION / "INDICE_C28_G.json"
maestro.ORDER = [
    ROOT / "libro" / "revisiones_c28g" / "15_la_instruccion_en_movimiento_c28g.md"
    if source.name == "15_la_instruccion_en_movimiento_c28f.md" else source
    for source in maestro.ORDER
]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--pages-json", type=Path)
    p.add_argument("--derive-pages", type=Path)
    args = p.parse_args()
    EDITION.mkdir(parents=True,exist_ok=True)
    if args.derive_pages:
        maestro.derive_page_index(args.derive_pages)
    else:
        pages = json.loads(args.pages_json.read_text(encoding="utf-8")) if args.pages_json else {}
        maestro.build(pages)


if __name__=="__main__":
    main()
