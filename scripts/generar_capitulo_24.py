#!/usr/bin/env python3
"""Regenera el Word del capítulo final con la plantilla común."""
from pathlib import Path
import generar_capitulo_01 as template

root = Path(__file__).resolve().parents[1]
template.SRC = root / 'libro/capitulos/24_una_computadora_que_podemos_explicar.md'
template.DOCX = template.SRC.with_suffix('.docx')

if __name__ == '__main__':
    template.main()
