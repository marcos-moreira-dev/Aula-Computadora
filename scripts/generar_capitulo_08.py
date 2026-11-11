#!/usr/bin/env python3
"""Genera el capítulo 8 con la plantilla Word editorial común."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / "libro" / "capitulos" / "08_direcciones_y_buses.md"
plantilla.DOCX = plantilla.SRC.with_suffix(".docx")

if __name__ == "__main__":
    plantilla.main()
