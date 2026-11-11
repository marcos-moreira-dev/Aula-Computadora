#!/usr/bin/env python3
"""Produce el DOCX del capítulo 4 con la maqueta editorial del libro."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / "libro" / "capitulos" / "04_construir_funciones_con_compuertas.md"
plantilla.DOCX = plantilla.SRC.with_suffix(".docx")

if __name__ == "__main__":
    plantilla.main()
