#!/usr/bin/env python3
"""Verifica tablas de verdad, Word, PDF, ilustraciones y propuesta semántica.

No acredita montaje físico, ni temporización, ni funcionamiento de CPU.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "libro" / "capitulos" / "04_construir_funciones_con_compuertas"
FIGURES = ROOT / "libro" / "figuras"
NAMES = ["c04_fig01_or_nor", "c04_fig02_xor_discrepancia",
         "c04_fig03_xor_cuatro_nand", "c04_fig04_simplificacion"]
NS = {"m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"}


def nand(a: int, b: int) -> int:
    return 1 - (a & b)


def network(a: int, b: int) -> tuple[int, int, int, int]:
    n1 = nand(a, b)
    n2 = nand(a, n1)
    n3 = nand(b, n1)
    return (n1, n2, n3, nand(n2, n3))


def main() -> None:
    checks = 0
    rows = list(product((0, 1), repeat=2))
    assert rows == [(0, 0), (0, 1), (1, 0), (1, 1)]
    checks += 1
    xor_internals = [(1, 1, 1, 0), (1, 1, 0, 1),
                     (1, 0, 1, 1), (0, 1, 1, 0)]
    for idx, (a, b) in enumerate(rows):
        assert (a | b) == int(bool(a or b))
        assert 1 - (a | b) == int(not (a or b))
        assert (a ^ b) == int(a != b)
        assert (a ^ b) == ((1 - a) & b) | (a & (1 - b))
        assert nand(a, b) == int(not (a and b))
        assert network(a, b) == xor_internals[idx]
        assert ((a & b) | (a & (1 - b))) == a
        assert (a & (b | (1 - b))) == a
        checks += 8

    results3 = []
    for a, b, c in product((0, 1), repeat=3):
        y = a & (b | c)
        assert y == int(a == 1 and (b == 1 or c == 1))
        results3.append(y)
        checks += 1
    assert results3 == [0, 0, 0, 0, 0, 1, 1, 1]
    checks += 1
    assert 2 ** 3 == 8
    checks += 1

    manuscript = BASE.with_suffix(".md").read_text(encoding="utf-8")
    assert manuscript.startswith("# Capítulo 4. Construir funciones con compuertas")
    assert "JavaFX" not in manuscript
    assert "Parte II" in manuscript
    checks += 3
    for number in range(1, 13):
        assert f"**Ejercicio {number} " in manuscript, number
        assert f"**{number}.**" in manuscript, number
        checks += 2
    for word in ["OR", "NOR", "XOR", "NAND", "disyunción inclusiva", "discrepancia",
                 "suma de productos", "simplificar", "distributiva", "propagación",
                 "SN74HCT00", "cuatro NAND", "realimentación", "tabla de verdad",
                 "lógica ideal", "capítulo puente", "significado",
                 "N1", "N2", "N3", "retardo", "2³ = 8"]:
        assert word.lower() in manuscript.lower(), word
        checks += 1
    assert manuscript.count("[[EQ:") == 13
    assert manuscript.count("[[FIG:") == len(NAMES)
    checks += 2
    for name in NAMES:
        for extension, minimum in ((".svg", 1400), (".png", 15_000)):
            file = FIGURES / (name + extension)
            assert file.exists() and file.stat().st_size > minimum, file
            checks += 1
        assert f"[[FIG:{name}|" in manuscript, name
        checks += 1

    diagram = (FIGURES / (NAMES[2] + ".svg")).read_text(encoding="utf-8")
    for label in ("N1", "N2", "N3", "N4", "NAND", "XOR"):
        assert label in diagram, label
        checks += 1
    plan = (ROOT / "libro" / "PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md").read_text(encoding="utf-8")
    for label in ("Tras el capítulo 7", "01000001", "11111111", "255",
                  "-1", "ASCII", "complemento a dos", "POO", "sin renumeración",
                  "24 capítulos", "decisión pendiente"):
        assert label.lower() in plan.lower(), label
        checks += 1

    with zipfile.ZipFile(BASE.with_suffix(".docx")) as archive:
        assert archive.testzip() is None
        content = ET.fromstring(archive.read("word/document.xml"))
        formulas = content.findall(".//m:oMath", NS)
        pictures = content.findall(".//wp:inline", NS)
        assert len(formulas) == 13, len(formulas)
        assert len(pictures) == len(NAMES), len(pictures)
        assert all(p.find("wp:docPr", NS).get("descr") for p in pictures)
        headers = [name for name in archive.namelist() if name.startswith("word/header") and name.endswith(".xml")]
        assert headers and any(b"PARTE II" in archive.read(path) for path in headers)
        checks += 5

    pdf = BASE.with_suffix(".pdf")
    assert pdf.is_file() and pdf.stat().st_size > 50_000, pdf
    meta = subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                          check=True, text=True).stdout
    matched = re.search(r"^Pages:\s*(\d+)", meta, re.MULTILINE)
    assert matched and 8 <= int(matched.group(1)) <= 13, meta
    text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True,
                          check=True, text=True).stdout
    assert len(text) > 14_000, len(text)
    for token in ["Construir funciones con compuertas", "PARTE II", "Figura 1.",
                  "Figura 2.", "Figura 3.", "Figura 4.", "Solucionario del capítulo 4",
                  "XOR", "NOR", "NAND", "cuatro NAND", "Tres entradas",
                  "Significado"]:
        assert token.lower() in text.lower(), token
        checks += 1
    checks += 3
    print(f"Capítulo 4: {checks} controles correctos. "
          f"{matched.group(1)} páginas, {len(formulas)} ecuaciones OMML y "
          f"{len(pictures)} figuras; plan del puente semántico registrado.")
    print("Sin montaje físico, medición de retardos ni CPU ejecutada.")


if __name__ == "__main__":
    main()
