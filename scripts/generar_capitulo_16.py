#!/usr/bin/env python3
"""Genera Word editable del capítulo 16 con la plantilla compartida."""

from pathlib import Path
import generar_capitulo_01 as plantilla

ROOT = Path(__file__).resolve().parents[1]
plantilla.SRC = ROOT / 'libro' / 'capitulos' / '16_subrutinas_y_pila.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')

if __name__ == '__main__':
    plantilla.main()
