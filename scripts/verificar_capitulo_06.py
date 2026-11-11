#!/usr/bin/env python3
"""Verifica el modelo lógico del latch D, flip-flop D y entrega editorial C06.

No modela setup/hold, metastabilidad ni componentes eléctricos reales.
"""
from itertools import product
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "libro" / "capitulos" / "06_memorizar_en_el_tiempo"
FIGURES = (
    "c06_fig01_desde_sr_hasta_d",
    "c06_fig02_tabla_latch_d",
    "c06_fig03_flancos_y_capturas",
    "c06_fig04_latch_versus_flipflop",
)
NS = {
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}


def nand(a: int, b: int) -> int:
    return 1 - (a & b)


def sr_controls(d: int, le: int) -> tuple[int, int]:
    return nand(d, le), nand(1 - d, le)


def latch_next(q: int, d: int, le: int) -> int:
    return d if le else q


def flipflop_next(q: int, d: int, previous_clock: int, clock: int,
                  clear_n: int = 1, preset_n: int = 1) -> int:
    if (clear_n, preset_n) == (0, 0):
        raise ValueError("Preset y clear simultáneos no admitidos")
    if clear_n == 0:
        return 0
    if preset_n == 0:
        return 1
    return d if previous_clock == 0 and clock == 1 else q


def main() -> None:
    checks = 0
    for d, le in product((0, 1), repeat=2):
        expected_controls = (1, 1) if le == 0 else ((0, 1) if d else (1, 0))
        assert sr_controls(d, le) == expected_controls
        assert sr_controls(d, le) != (0, 0)
        checks += 2
        for previous_q in (0, 1):
            assert latch_next(previous_q, d, le) == (d if le else previous_q)
            checks += 1
    assert sr_controls(1, 0) == (1, 1)
    assert sr_controls(1, 1) == (0, 1)
    assert sr_controls(0, 1) == (1, 0)
    checks += 3

    state = 0
    latch_seq = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 1)]
    latch_results = []
    for le, d in latch_seq:
        state = latch_next(state, d, le)
        latch_results.append(state)
        checks += 1
    assert latch_results == [0, 0, 1, 0, 0]
    checks += 1

    state, previous_clock = 0, 0
    clocks = [0, 0, 1, 1, 0, 1, 1]
    data = [0, 1, 1, 0, 0, 0, 1]
    ff_results = []
    for clock, d in zip(clocks, data):
        state = flipflop_next(state, d, previous_clock, clock)
        previous_clock = clock
        ff_results.append(state)
        checks += 1
    assert ff_results == [0, 0, 1, 1, 1, 0, 0]
    checks += 1
    for q, d, previous_clock, clock in product((0, 1), repeat=4):
        assert flipflop_next(q, d, previous_clock, clock) == (
            d if previous_clock == 0 and clock == 1 else q)
        assert flipflop_next(q, d, previous_clock, clock, clear_n=0) == 0
        assert flipflop_next(q, d, previous_clock, clock, preset_n=0) == 1
        checks += 3
    try:
        flipflop_next(0, 0, 0, 0, clear_n=0, preset_n=0)
        raise AssertionError("Combinación simultánea no rechazada")
    except ValueError:
        checks += 1
    assert 1 / 0.001 == 1000
    assert 1 / 0.002 == 500
    checks += 2

    manuscript = BASE.with_suffix(".md").read_text(encoding="utf-8")
    assert manuscript.startswith("# Capítulo 6. Memorizar en el tiempo")
    assert "*Parte II" in manuscript
    assert "JavaFX" not in manuscript
    checks += 3
    for number in range(1, 13):
        assert f"**Ejercicio {number} " in manuscript, number
        assert f"**{number}.**" in manuscript, number
        checks += 2
    for token in (
        "latch D", "flip-flop D", "transparente", "S_n", "R_n", "NAND",
        "LE = 0", "LE = 1", "setup", "hold", "flanco ascendente",
        "flanco descendente", "asíncrono", "reset", "preset", "CLR_n",
        "PRE_n", "SN74HC373", "SN74HC74", "metastabilidad", "clock-to-Q",
        "último valor válido", "semántica lógica", "capítulo 7",
        "no hemos conectado", "no hemos construido",
    ):
        assert token.lower() in manuscript.lower(), token
        checks += 1
    assert manuscript.count("[[EQ:") == 9
    assert manuscript.count("[[FIG:") == len(FIGURES)
    checks += 2
    for name in FIGURES:
        for extension, threshold in ((".svg", 1400), (".png", 15000)):
            artifact = ROOT / "libro" / "figuras" / (name + extension)
            assert artifact.is_file() and artifact.stat().st_size > threshold, artifact
            checks += 1
        assert f"[[FIG:{name}|" in manuscript
        checks += 1

    with zipfile.ZipFile(BASE.with_suffix(".docx")) as docx:
        assert docx.testzip() is None
        xml = ET.fromstring(docx.read("word/document.xml"))
        equations = xml.findall(".//m:oMath", NS)
        images = xml.findall(".//wp:inline", NS)
        assert len(equations) == 9, len(equations)
        assert len(images) == 4, len(images)
        assert all(pic.find("wp:docPr", NS).get("descr") for pic in images)
        headers = [name for name in docx.namelist()
                   if name.startswith("word/header") and name.endswith(".xml")]
        assert headers and any(b"PARTE II" in docx.read(name) for name in headers)
        checks += 5

    pdf = BASE.with_suffix(".pdf")
    assert pdf.is_file() and pdf.stat().st_size > 50_000
    info = subprocess.run(["pdfinfo", str(pdf)], text=True, capture_output=True,
                          check=True).stdout
    match = re.search(r"^Pages:\s*(\d+)", info, flags=re.MULTILINE)
    assert match and 7 <= int(match.group(1)) <= 12, info
    content = subprocess.run(["pdftotext", str(pdf), "-"], text=True,
                             capture_output=True, check=True).stdout
    assert len(content) > 13_000, len(content)
    for token in ("Memorizar en el tiempo", "PARTE II", "Figura 1.", "Figura 2.",
                  "Figura 3.", "Figura 4.", "Solucionario del capítulo 6",
                  "SN74HC74", "SN74HC373", "setup", "hold", "reset"):
        assert token.lower() in content.lower(), token
        checks += 1
    checks += 3
    print(f"Capítulo 6: {checks} controles correctos, {match.group(1)} páginas, "
          f"{len(equations)} ecuaciones OMML, {len(images)} figuras y 12 ejercicios.")
    print("Comprobación lógica y documental, sin medición física ni análisis temporal analógico.")


if __name__ == "__main__":
    main()
