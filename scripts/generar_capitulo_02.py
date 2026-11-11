#!/usr/bin/env python3
"""Regenera la maqueta Word del capítulo 2 con la plantilla del capítulo 1."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / "libro" / "capitulos" / "02_el_transistor_como_interruptor.md"
plantilla.DOCX = plantilla.SRC.with_suffix(".docx")

if __name__ == "__main__":
    plantilla.main()
