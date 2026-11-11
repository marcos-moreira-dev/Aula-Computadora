#!/usr/bin/env python3
"""Word editable de la ALU (C11), reutilizando el estilo y OMML del libro."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / 'libro' / 'capitulos' / '11_la_unidad_aritmetico_logica.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')

if __name__ == '__main__':
    plantilla.main()
