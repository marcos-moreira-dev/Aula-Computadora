#!/usr/bin/env python3
"""Genera DOCX C19; usar antes generar_diagramas_tecnicos_aula8.py."""
from pathlib import Path
import generar_capitulo_01 as plantilla

ROOT=Path(__file__).resolve().parents[1]
plantilla.SRC=ROOT/'libro'/'capitulos'/'19_guardar_y_recuperar_programas.md'
plantilla.DOCX=plantilla.SRC.with_suffix('.docx')

if __name__=='__main__':
    plantilla.main()
