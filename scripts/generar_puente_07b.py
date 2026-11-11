#!/usr/bin/env python3
"""Maqueta el interludio Del bit al significado con la plantilla común."""
import generar_capitulo_01 as plantilla


plantilla.SRC = plantilla.ROOT / "libro" / "capitulos" / "07b_del_bit_al_significado.md"
plantilla.DOCX = plantilla.SRC.with_suffix(".docx")


if __name__ == "__main__":
    plantilla.main()
