#!/usr/bin/env python3
"""Maqueta el capítulo 14 con la plantilla Word editorial acumulativa."""
from pathlib import Path
import generar_capitulo_01 as plantilla


ROOT = Path(__file__).resolve().parents[1]
plantilla.SRC = ROOT / 'libro' / 'capitulos' / '14_de_numeros_a_instrucciones.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')


if __name__ == '__main__':
    plantilla.main()
