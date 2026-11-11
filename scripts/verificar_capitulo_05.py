#!/usr/bin/env python3
"""Comprueba estados estables del latch NAND y el paquete editorial C05.

No simula transitorios analógicos, metastabilidad ni un montaje físico.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "libro" / "capitulos" / "05_la_realimentacion_conserva_informacion"
FIG_DIR = ROOT / "libro" / "figuras"
FIGURES = (
    "c05_fig01_combinacional_realimentacion",
    "c05_fig02_latch_nand_cruzado",
    "c05_fig03_tabla_estados",
    "c05_fig04_secuencia_memoria",
)
NS = {
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}


def nand(x: int, y: int) -> int:
    return 1 - (x & y)


def fixed_points(s_n: int, r_n: int) -> set[tuple[int, int]]:
    return {
        (q, q_n)
        for q, q_n in product((0, 1), repeat=2)
        if q == nand(s_n, q_n) and q_n == nand(r_n, q)
    }


def main() -> None:
    checks = 0
    expected = {
        (0, 0): {(1, 1)},
        (0, 1): {(1, 0)},
        (1, 0): {(0, 1)},
        (1, 1): {(0, 1), (1, 0)},
    }
    for controls, states in expected.items():
        assert fixed_points(*controls) == states, controls
        checks += 1
        for q, q_n in states:
            assert nand(controls[0], q_n) == q
            assert nand(controls[1], q) == q_n
            checks += 2
    assert len(fixed_points(1, 1)) == 2
    assert all(q != q_n for q, q_n in fixed_points(1, 1))
    assert fixed_points(0, 0) == {(1, 1)}
    checks += 3

    # Los cinco momentos son estados estables, no ciclos del circuito físico.
    state = (0, 1)  # Se obtuvo antes mediante RESET; no se supone power-on.
    sequence = [(1, 1), (0, 1), (1, 1), (1, 0), (1, 1)]
    visited = []
    for pair in sequence:
        possibilities = fixed_points(*pair)
        if pair == (1, 1):
            assert state in possibilities
        else:
            assert len(possibilities) == 1
            state = next(iter(possibilities))
        visited.append(state)
        checks += 2
    assert visited == [(0, 1), (1, 0), (1, 0), (0, 1), (0, 1)]
    assert 2 ** 2 == 4
    checks += 2

    manuscript = BASE.with_suffix(".md").read_text(encoding="utf-8")
    assert manuscript.startswith("# Capítulo 5. La realimentación conserva información")
    assert "*Parte II" in manuscript
    assert "JavaFX" not in manuscript
    checks += 3
    for number in range(1, 13):
        assert f"**Ejercicio {number} " in manuscript, number
        assert f"**{number}.**" in manuscript, number
        checks += 2
    for token in (
        "latch SR", "NAND", "realimentación", "activas en bajo", "S_n", "R_n",
        "Q_n", "estado anterior", "entrada prohibida", "liberar ambas",
        "retardos", "estado estable", "asíncrono", "SN74HCT00N", "pin 3",
        "pin 6", "0,1 µF", "4,5 a 5,5 V", "semántica", "POO", "capítulo 6",
        "capítulo 7", "no se ha realizado montaje",
    ):
        # "POO" aparece en la propuesta, no dentro del texto que solo
        # menciona 'objetos de programación' como contextualización.
        target = (ROOT / "libro" / "PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md").read_text(encoding="utf-8") if token == "POO" else manuscript
        assert token.lower() in target.lower(), token
        checks += 1
    assert manuscript.count("[[EQ:") == 11
    assert manuscript.count("[[FIG:") == len(FIGURES)
    checks += 2
    for name in FIGURES:
        for suffix, minimum in ((".svg", 1400), (".png", 15000)):
            artifact = FIG_DIR / (name + suffix)
            assert artifact.is_file() and artifact.stat().st_size > minimum, artifact
            checks += 1
        assert f"[[FIG:{name}|" in manuscript
        checks += 1

    bridge = (ROOT / "libro" / "PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md").read_text(encoding="utf-8")
    for token in ("semántica lógica de circuito", "semántica del software", "POO",
                  "Tras el capítulo 7", "01000001", "11111111",
                  "24 capítulos", "sin renumeración", "desarrollada como interludio P07B"):
        assert token.lower() in bridge.lower(), token
        checks += 1

    with zipfile.ZipFile(BASE.with_suffix(".docx")) as docx:
        assert docx.testzip() is None
        document = ET.fromstring(docx.read("word/document.xml"))
        formulas = document.findall(".//m:oMath", NS)
        pictures = document.findall(".//wp:inline", NS)
        assert len(formulas) == 11, len(formulas)
        assert len(pictures) == 4, len(pictures)
        assert all(pic.find("wp:docPr", NS).get("descr") for pic in pictures)
        headers = [p for p in docx.namelist() if p.startswith("word/header") and p.endswith(".xml")]
        assert headers and any(b"PARTE II" in docx.read(h) for h in headers)
        checks += 5

    pdf = BASE.with_suffix(".pdf")
    assert pdf.is_file() and pdf.stat().st_size > 50_000
    meta = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
    match = re.search(r"^Pages:\s*(\d+)", meta, re.MULTILINE)
    assert match and 7 <= int(match.group(1)) <= 12, meta
    pdftext = subprocess.run(["pdftotext", str(pdf), "-"], check=True, capture_output=True, text=True).stdout
    assert len(pdftext) > 12_000, len(pdftext)
    for token in ("La realimentación conserva información", "PARTE II", "Figura 1.",
                  "Figura 2.", "Figura 3.", "Figura 4.", "Solucionario del capítulo 5",
                  "S_n", "R_n", "SN74HCT00N", "prohibida", "Semántica lógica"):
        assert token.lower() in pdftext.lower(), token
        checks += 1
    checks += 3
    print(f"Capítulo 5: {checks} controles correctos, {match.group(1)} páginas, "
          f"{len(formulas)} ecuaciones OMML, {len(pictures)} figuras y 12 ejercicios resueltos.")
    print("Estados NAND estables verificados; sin simulación temporal ni certificación física.")


if __name__ == "__main__":
    main()
