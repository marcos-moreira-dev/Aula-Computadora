#!/usr/bin/env python3
"""Regenera el Word del interludio P23V sin alterar la numeración 1..24."""
from pathlib import Path
import generar_capitulo_01 as template

root = Path(__file__).resolve().parents[1]
template.SRC = root / 'libro/capitulos/23v_de_mapas_de_caracteres_a_escritorio_grafico.md'
template.DOCX = template.SRC.with_suffix('.docx')

if __name__ == '__main__':
    template.main()
