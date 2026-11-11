#!/usr/bin/env python3
"""Auditoría reproducible del capítulo 2: cuentas, Word, PDF y figuras.

No valida una placa ni el funcionamiento real del 2N3904.
"""
from __future__ import annotations

import math
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "libro" / "capitulos" / "02_el_transistor_como_interruptor"
FIGS = ROOT / "libro" / "figuras"
NAMES = ["c02_fig01_bce_pinout", "c02_fig02_npn_encendido", "c02_fig03_npn_apagado"]
NS = {"m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"}


def close(value: float, expected: float, tolerance: float = 0.000_000_1):
    assert math.isclose(value, expected, rel_tol=0, abs_tol=tolerance), f"{value} != {expected}"


def main():
    checks = 0

    # Dos ramas y las hipótesis que se declaran expresamente en el manuscrito.
    ic = (5.0 - 2.0 - 0.2) / 330.0
    ib = (5.0 - 0.7) / 4700.0
    pairs = [
        (ic, 0.00848484848),
        (ib, 0.00091489361),
        (ic * 1000, 8.48484848),
        (ib * 1000, 0.91489361),
        (ic / ib, 9.274136),
        (ic ** 2 * 330, 0.0237576),
        (ib ** 2 * 4700, 0.003933),
        (0.2 * ic, 0.001697),
        (0.7 * ib, 0.0006404),
        ((0.2 * ic) + (0.7 * ib), 0.002338),
        ((ic + ib) * 1000, 9.39974),
        ((5 - 0.7) / 47_000 * 1000, 0.091489),
        ((5 - 2 - 1) / 330 * 1000, 6.060606),
    ]
    for got, expected in pairs:
        assert math.isclose(got, expected, abs_tol=0.0001), (got, expected)
        checks += 1
    assert ic < 0.010 and ib < 0.001 and ic + ib < 0.015
    checks += 1
    assert ic ** 2 * 330 < 0.25 and ib ** 2 * 4700 < 0.25
    checks += 1

    manuscript = BASE.with_suffix(".md").read_text(encoding="utf-8")
    assert manuscript.startswith("# Capítulo 2. El transistor como interruptor")
    checks += 1
    assert "JavaFX" not in manuscript
    checks += 1
    for idx in range(1, 13):
        assert f"**Ejercicio {idx} " in manuscript, idx
        assert f"**{idx}.**" in manuscript, idx
        checks += 2
    for must_have in ["VCE(sat)", "0,2 V", "8,48 mA", "0,915 mA", "9,27", "GND",
                      "onsemi", "2N3904", "1 = emisor", "2 = base", "3 = colector",
                      "VGS(th)", "RDS(on)"]:
        assert must_have.lower() in manuscript.lower(), must_have
        checks += 1
    assert manuscript.count("[[EQ:") >= 13
    assert manuscript.count("[[FIG:") == 3
    checks += 2

    for name in NAMES:
        for ext in (".svg", ".png"):
            item = FIGS / (name + ext)
            assert item.exists() and item.stat().st_size > (1500 if ext == ".svg" else 20000), item
            checks += 1
    for name in NAMES[1:]:
        svg = (FIGS / (name + ".svg")).read_text(encoding="utf-8")
        assert "330 Ω" in svg and "4,7 kΩ" in svg and "Q1 NPN" in svg
        assert "estimación, no medida" in svg
        checks += 2

    with zipfile.ZipFile(BASE.with_suffix(".docx")) as archive:
        assert archive.testzip() is None
        xml = ET.fromstring(archive.read("word/document.xml"))
        equations = xml.findall(".//m:oMath", NS)
        pictures = xml.findall(".//wp:inline", NS)
        assert len(equations) >= 13, len(equations)
        assert len(pictures) == 3, len(pictures)
        assert all(pic.find("wp:docPr", NS).get("descr") for pic in pictures)
        checks += 4

    pdf = BASE.with_suffix(".pdf")
    assert pdf.is_file() and pdf.stat().st_size > 50000
    info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
    count_match = re.search(r"^Pages:\s*(\d+)", info, flags=re.MULTILINE)
    assert count_match and 9 <= int(count_match.group(1)) <= 13
    extracted = subprocess.run(["pdftotext", str(pdf), "-"], check=True, capture_output=True, text=True).stdout
    assert len(extracted) > 17000, len(extracted)
    for token in ["El transistor como interruptor", "Saturación", "Figura 1.", "Figura 2.",
                  "Figura 3.", "Solucionario del capítulo 2", "330 Ω", "4,7 kΩ",
                  "8,48 mA", "0,915 mA", "2N3904"]:
        assert token.lower() in extracted.lower(), f"Ausente en PDF: {token}"
        checks += 1
    checks += 4
    print(f"Capítulo 2: {checks} controles OK. {count_match.group(1)} páginas, "
          f"{len(equations)} ecuaciones OMML, {len(pictures)} figuras.")
    print("Validación documental y matemática, sin ensayos eléctricos ni componentes físicos.")


if __name__ == "__main__":
    main()
