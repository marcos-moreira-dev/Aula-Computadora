#!/usr/bin/env python3
"""Genera DOCX C20 después de generar los diagramas correspondientes."""
from pathlib import Path
import generar_capitulo_01 as plantilla

ROOT = Path(__file__).resolve().parents[1]
plantilla.SRC = ROOT / 'libro' / 'capitulos' / '20_programar_un_pequeno_sistema.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')

if __name__ == '__main__':
    plantilla.main()
