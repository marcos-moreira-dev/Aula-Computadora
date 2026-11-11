#!/usr/bin/env python3
"""Produce el DOCX del capítulo 5 con la maqueta editorial del libro."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / "libro" / "capitulos" / "05_la_realimentacion_conserva_informacion.md"
plantilla.DOCX = plantilla.SRC.with_suffix(".docx")

if __name__ == "__main__":
    plantilla.main()
