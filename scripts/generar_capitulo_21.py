#!/usr/bin/env python3
"""Genera DOCX C21 después de generar los diagramas correspondientes."""
from pathlib import Path
import generar_capitulo_01 as plantilla

ROOT = Path(__file__).resolve().parents[1]
plantilla.SRC = ROOT / 'libro' / 'capitulos' / '21_que_implica_ampliar_la_palabra.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')

if __name__ == '__main__':
    plantilla.main()
