#!/usr/bin/env python3
"""Genera el Word editable del capítulo 9 de Aula-Computadora."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / 'libro' / 'capitulos' / '09_ram_y_rom_reales.md'
plantilla.DOCX = plantilla.SRC.with_suffix('.docx')

if __name__ == '__main__':
    plantilla.main()
