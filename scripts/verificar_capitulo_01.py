#!/usr/bin/env python3
"""Controles reproducibles de cálculo, integración DOCX y PDF del capítulo 1."""
from __future__ import annotations

from pathlib import Path
import math
import re
import subprocess
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "libro" / "capitulos" / "01_la_corriente_y_sus_caminos"
FIG = ROOT / "libro" / "figuras"
NS = {"m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"}


def eq(actual: float, expected: float, tol: float = 1e-10):
    assert math.isclose(actual, expected, abs_tol=tol), f"{actual!r} != {expected!r}"


def main():
    checks = 0
    current = (5.0 - 2.0) / 330.0
    eq(current, 1 / 110)
    checks += 1
    eq(current * current * 330, 3 / 110)
    checks += 1
    eq(2 * current, 1 / 55)
    checks += 1
    eq(5 * current, (3 + 2) / 110)
    checks += 1
    eq((4.5 - 2) / 330, 1 / 132)
    checks += 1
    eq(5 * 5 / 330, 5 / 66)
    checks += 1
    eq((5 - 2) / 0.010, 300)
    checks += 1
    eq(0.010 ** 2 * 330, 0.033)
    checks += 1
    eq(5 / 1000, 0.005)
    checks += 1
    assert 0.0273 < 0.25 and 0.0758 < 0.25
    checks += 1

    manuscript = BASE.with_suffix(".md").read_text(encoding="utf-8")
    for idx in range(1, 13):
        assert f"**Ejercicio {idx} " in manuscript
        assert f"**{idx}.**" in manuscript
        checks += 2
    assert "JavaFX" not in manuscript
    checks += 1
    assert "no medido" in manuscript and "montaje físico" in manuscript
    checks += 1
    assert manuscript.count("[[FIG:") == 4
    checks += 1

    with zipfile.ZipFile(BASE.with_suffix(".docx")) as archive:
        assert archive.testzip() is None
        content = archive.read("word/document.xml")
        doc = ET.fromstring(content)
        equations = doc.findall(".//m:oMath", NS)
        images = doc.findall(".//wp:inline", NS)
        assert len(equations) >= 10, f"Solo hay {len(equations)} ecuaciones OMML"
        assert len(images) == 4
        assert all(elem.find("wp:docPr", NS).get("descr") for elem in images)
        checks += 4

    for i in range(1, 5):
        name = ["c01_fig01_lazo_serie", "c01_fig02_medir_tension", "c01_fig03_medir_corriente", "c01_fig04_protoboard_conexiones"][i - 1]
        svg, png = FIG / f"{name}.svg", FIG / f"{name}.png"
        assert svg.is_file() and png.is_file()
        assert png.stat().st_size > 20_000
        checks += 2

    pdf = BASE.with_suffix(".pdf")
    assert pdf.is_file() and pdf.stat().st_size > 60_000
    page_info = subprocess.run(["pdfinfo", str(pdf)], text=True, capture_output=True, check=True)
    match = re.search(r"^Pages:\s*(\d+)", page_info.stdout, re.MULTILINE)
    assert match and 8 <= int(match.group(1)) <= 13
    extraction = subprocess.run(["pdftotext", str(pdf), "-"], text=True, capture_output=True, check=True).stdout
    assert len(extraction) > 12_000
    for token in ["Ley de Ohm", "Figura 1.", "Figura 2.", "Figura 3.", "Figura 4.", "Solucionario", "330 Ω", "9,09 mA"]:
        assert token in extraction, f"Ausente en PDF: {token}"
        checks += 1
    checks += 3
    print(f"Capítulo 1: {checks} controles OK. {match.group(1)} páginas, {len(equations)} ecuaciones OMML, 4 figuras.")
    print("Validación documental/cálculo; no valida físicamente un circuito.")


if __name__ == "__main__":
    main()
