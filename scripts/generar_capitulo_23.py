#!/usr/bin/env python3
"""Genera Word C23 con la plantilla editorial y matemáticas OMML."""
from pathlib import Path
import generar_capitulo_01 as plantilla

ROOT = Path(__file__).resolve().parents[1]
plantilla.SRC = ROOT / 'libro' / 'capitulos' / '23_programacion_para_aula_16.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')

if __name__ == '__main__':
    plantilla.main()
