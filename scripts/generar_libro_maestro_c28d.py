#!/usr/bin/env python3
"""Edición incremental C28-D: RAM contigua con bifurcación y selector JNZ NAND."""

import argparse
import json
from pathlib import Path

import generar_libro_maestro_c28c as base

maestro = base.maestro
ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "libro" / "ediciones" / "C28_D"
maestro.OUTPUT = EDITION / "Aula_Computadora_C28_D_MAESTRO.docx"
maestro.PAGE_INDEX = EDITION / "INDICE_C28_D.json"
changes = {
    "14_de_numeros_a_instrucciones.md": "14_de_numeros_a_instrucciones_c28d.md",
    "15_la_instruccion_en_movimiento.md": "15_la_instruccion_en_movimiento_c28d.md",
}
maestro.ORDER = [
    ROOT / "libro" / "revisiones_c28d" / changes[source.name]
    if source.name in changes else source
    for source in maestro.ORDER
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pages-json", type=Path)
    p.add_argument("--derive-pages", type=Path)
    args = p.parse_args()
    EDITION.mkdir(parents=True, exist_ok=True)
    if args.derive_pages:
        maestro.derive_page_index(args.derive_pages)
    else:
        pages = json.loads(args.pages_json.read_text(encoding="utf-8")) if args.pages_json else {}
        maestro.build(pages)


if __name__ == "__main__":
    main()
