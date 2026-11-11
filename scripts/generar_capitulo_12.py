#!/usr/bin/env python3
"""Genera Word editable con ecuaciones OMML del capítulo 12."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / 'libro' / 'capitulos' / '12_arquitectura_aula_8.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')

if __name__ == '__main__':
    plantilla.main()
