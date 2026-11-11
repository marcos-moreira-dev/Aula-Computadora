#!/usr/bin/env python3
"""Verifica lógica, manuscrito, figuras, Word y PDF del capítulo 3.

No acredita montaje físico, tensiones medidas ni una CPU ejecutable.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path
import math
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "libro" / "capitulos" / "03_de_interruptores_a_logica"
FIGS = ROOT / "libro" / "figuras"
NAMES = ["c03_fig01_serie_ideal", "c03_fig02_nand_simbolo",
         "c03_fig03_pines_74hct00", "c03_fig04_nand_led"]
NS = {"m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"}


def nand(a: int, b: int) -> int:
    return 1 - a * b


def main() -> None:
    checks = 0
    rows = list(product((0, 1), repeat=2))
    assert rows == [(0, 0), (0, 1), (1, 0), (1, 1)]
    checks += 1

    for a, b in rows:
        assert nand(a, b) == 1 - (a & b)
        assert nand(a, b) == int(not (a and b))
        assert nand(nand(a, b), nand(a, b)) == a & b  # AND con NAND
        assert nand(nand(a, a), nand(b, b)) == a | b  # OR con NAND
        checks += 4
    for a in (0, 1):
        assert nand(a, a) == 1 - a  # NOT con NAND
        checks += 1
    assert 2 ** 1 == 2 and 2 ** 2 == 4 and 2 ** 3 == 8
    checks += 1

    vil, vih = 0.8, 2.0
    for voltage, level in [(0.0, "bajo"), (0.5, "bajo"),
                           (0.8, "bajo"), (1.2, "no garantizado"),
                           (2.0, "alto"), (3.0, "alto"), (5.0, "alto")]:
        received = "bajo" if voltage <= vil else ("alto" if voltage >= vih else "no garantizado")
        assert received == level, (voltage, received)
        checks += 1

    voltage_supply, led_drop, output_low, resistance = 5.0, 2.0, 0.3, 1000.0
    voltage_resistor = voltage_supply - led_drop - output_low
    current = voltage_resistor / resistance
    power = current ** 2 * resistance
    assert math.isclose(voltage_resistor, 2.7)
    assert math.isclose(current, 0.0027)
    assert math.isclose(1000 * current, 2.7)
    assert math.isclose(power, 0.00729)
    assert math.isclose(1000 * power, 7.29)
    assert current < 0.004 and power < 0.25
    checks += 6

    manuscript = BASE.with_suffix(".md").read_text(encoding="utf-8")
    assert manuscript.startswith("# Capítulo 3. De interruptores a lógica")
    assert "JavaFX" not in manuscript
    checks += 2
    for idx in range(1, 13):
        assert f"**Ejercicio {idx} " in manuscript, idx
        assert f"**{idx}.**" in manuscript, idx
        checks += 2
    required = ["NAND", "inversor", "2ⁿ", "AND", "OR", "VIL", "VIH", "0,8 V",
                "2,0 V", "SN74HCT00N", "4,5 a 5,5 V", "Texas Instruments",
                "1 kΩ", "100 nF", "2,7 mA", "7,29 mW", "GND", "flotante",
                "pin 14", "pin 7", "pin 3", "no son mediciones",
                "no afirmamos haberlo medido", "salida 1Y"]
    for token in required:
        assert token.lower() in manuscript.lower(), token
        checks += 1
    assert manuscript.count("[[EQ:") >= 9
    assert manuscript.count("[[FIG:") == len(NAMES)
    checks += 2

    for name in NAMES:
        for extension, minimum in ((".svg", 1500), (".png", 20_000)):
            artifact = FIGS / (name + extension)
            assert artifact.is_file() and artifact.stat().st_size > minimum, artifact
            checks += 1
        assert (name + ".png") in manuscript or f"[[FIG:{name}|" in manuscript
        checks += 1

    pinout = (FIGS / (NAMES[2] + ".svg")).read_text(encoding="utf-8")
    for label in ["PDIP-14", "VCC", "GND", "1A", "1B", "1Y"]:
        assert label in pinout
        checks += 1
    led_svg = (FIGS / (NAMES[3] + ".svg")).read_text(encoding="utf-8")
    for label in ["1 kΩ", "100 nF", "pin 14", "pin 7", "pin 3", "LED", "Y = 0"]:
        assert label in led_svg
        checks += 1

    with zipfile.ZipFile(BASE.with_suffix(".docx")) as archive:
        assert archive.testzip() is None
        xml = ET.fromstring(archive.read("word/document.xml"))
        equations = xml.findall(".//m:oMath", NS)
        pictures = xml.findall(".//wp:inline", NS)
        assert len(equations) >= 9, len(equations)
        assert len(pictures) == len(NAMES), len(pictures)
        assert all(pic.find("wp:docPr", NS).get("descr") for pic in pictures)
        checks += 4

    pdf = BASE.with_suffix(".pdf")
    assert pdf.is_file() and pdf.stat().st_size > 50_000
    info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
    match = re.search(r"^Pages:\s*(\d+)", info, re.MULTILINE)
    assert match and 9 <= int(match.group(1)) <= 14
    extracted = subprocess.run(["pdftotext", str(pdf), "-"], check=True,
                               capture_output=True, text=True).stdout
    assert len(extracted) > 16_000, len(extracted)
    for token in ["De interruptores a lógica", "tabla de verdad", "SN74HCT00",
                  "Figura 1.", "Figura 2.", "Figura 3.", "Figura 4.",
                  "Solucionario del capítulo 3", "2,7 mA", "7,29 mW",
                  "100 nF", "1 kΩ", "NAND"]:
        assert token.lower() in extracted.lower(), token
        checks += 1
    checks += 4

    print(f"Capítulo 3: {checks} controles OK. {match.group(1)} páginas, "
          f"{len(equations)} ecuaciones OMML, {len(pictures)} figuras.")
    print("Verificación lógica, aritmética y documental; sin montaje ni mediciones eléctricas.")


if __name__ == "__main__":
    main()
