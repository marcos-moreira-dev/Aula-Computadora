#!/usr/bin/env python3
"""Genera el capítulo 7 con la maqueta compartida de Aula-Computadora."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / "libro" / "capitulos" / "07_del_bit_al_registro.md"
plantilla.DOCX = plantilla.SRC.with_suffix(".docx")

if __name__ == "__main__":
    plantilla.main()
