#!/usr/bin/env python3
"""Genera Word editable del capítulo 10, con ecuaciones nativas OMML."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / 'libro' / 'capitulos' / '10_el_circuito_que_suma.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')

if __name__ == '__main__':
    plantilla.main()
