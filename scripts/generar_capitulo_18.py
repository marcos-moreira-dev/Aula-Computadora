#!/usr/bin/env python3
"""Genera DOCX C18; usar antes generar_diagramas_tecnicos_aula8.py."""
from pathlib import Path
import generar_capitulo_01 as plantilla

ROOT=Path(__file__).resolve().parents[1]
plantilla.SRC=ROOT/'libro'/'capitulos'/'18_hablar_con_la_maquina.md'
plantilla.DOCX=plantilla.SRC.with_suffix('.docx')

if __name__=='__main__':
    plantilla.main()
