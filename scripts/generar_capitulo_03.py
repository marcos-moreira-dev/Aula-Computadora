#!/usr/bin/env python3
"""Produce el DOCX del capítulo 3 usando la maqueta verificada del libro."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / "libro" / "capitulos" / "03_de_interruptores_a_logica.md"
plantilla.DOCX = plantilla.SRC.with_suffix(".docx")

if __name__ == "__main__":
    plantilla.main()
