#!/usr/bin/env python3
"""Genera el capítulo 13 desde Markdown con Word/OMML editables."""
import generar_capitulo_01 as plantilla


plantilla.SRC = (plantilla.ROOT / 'libro' / 'capitulos'
                 / '13_la_unidad_de_control.md')
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')


if __name__ == '__main__':
    plantilla.main()
