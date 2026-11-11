#!/usr/bin/env python3
"""Genera Word C22 con la plantilla editorial y matemáticas OMML."""
from pathlib import Path
import generar_capitulo_01 as plantilla

ROOT = Path(__file__).resolve().parents[1]
plantilla.SRC = ROOT / 'libro' / 'capitulos' / '22_un_bus_externo_de_16_bits.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')

if __name__ == '__main__':
    plantilla.main()
