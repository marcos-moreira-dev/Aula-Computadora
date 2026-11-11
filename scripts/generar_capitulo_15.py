#!/usr/bin/env python3
"""Genera la maqueta Word del capítulo 15 con la plantilla del libro."""

from pathlib import Path
import generar_capitulo_01 as plantilla


ROOT = Path(__file__).resolve().parents[1]
plantilla.SRC = ROOT / 'libro' / 'capitulos' / '15_la_instruccion_en_movimiento.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')


if __name__ == '__main__':
    plantilla.main()
