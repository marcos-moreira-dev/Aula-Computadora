#!/usr/bin/env python3
"""Genera Word editable del capítulo 17 con la plantilla compartida."""

from pathlib import Path
import generar_capitulo_01 as plantilla

ROOT = Path(__file__).resolve().parents[1]
plantilla.SRC = ROOT / 'libro' / 'capitulos' / '17_encender_una_computadora.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')

if __name__ == '__main__':
    plantilla.main()
