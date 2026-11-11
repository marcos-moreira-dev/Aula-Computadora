#!/usr/bin/env python3
"""Produce el capítulo 6 en DOCX con la maqueta editorial de Aula."""
import generar_capitulo_01 as plantilla

plantilla.SRC = plantilla.ROOT / "libro" / "capitulos" / "06_memorizar_en_el_tiempo.md"
plantilla.DOCX = plantilla.SRC.with_suffix(".docx")

if __name__ == "__main__":
    plantilla.main()
