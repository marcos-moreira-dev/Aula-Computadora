#!/usr/bin/env python3
"""Verifica el capítulo 7 y sus ejemplos ideales de registros y buses.

No modela integrados eléctricos, tiempos, niveles de tensión o CPU Aula.
"""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "libro" / "capitulos" / "07_del_bit_al_registro"
FIGURES = (
    "c07_fig01_ocho_flips_un_registro",
    "c07_fig02_multiplexor_y_carga",
    "c07_fig03_almacenamiento_y_triestado",
    "c07_fig04_transferencia_a_b",
)
NS = {
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}


def register_next(previous: int, input_value: int, load: int, edge: bool) -> int:
    """Modelo lógico, entrada y load ya estables cuando llega el flanco."""
    assert previous in range(256) and input_value in range(256)
    assert load in (0, 1)
    return input_value if edge and load else previous


def bus_value(a: int, b: int, a_out: int, b_out: int) -> int | None:
    if a_out and b_out:
        raise ValueError("Los dos registros no deben conducir simultáneamente")
    if a_out:
        return a
    if b_out:
        return b
    return None


def main():
    count = 0

    # Comprobar exhaustivamente cargas y retenciones ideales de un byte.
    for q in range(256):
        for input_value in range(256):
            assert register_next(q, input_value, 0, True) == q
            assert register_next(q, input_value, 1, True) == input_value
            assert register_next(q, input_value, 1, False) == q
            count += 3
    # Peso binario y dos nibbles hexadecimales para los 256 patrones.
    for value in range(256):
        bits = f"{value:08b}"
        weighted = sum(int(bit) * (1 << (7 - index))
                       for index, bit in enumerate(bits))
        assert weighted == value
        assert int(bits[:4], 2) * 16 + int(bits[4:], 2) == value
        assert int(f"{value:02X}", 16) == value
        count += 3
    assert int("10110110", 2) == 182
    assert 11 * 16 + 6 == 182
    assert (1 << 8) == 256
    assert int("00111100", 2) == 0x3C
    assert int("10100101", 2) == 0xA5
    count += 5

    # Un solo conductor posible del bus.
    for a in range(256):
        for enable in (0, 1):
            assert bus_value(a, 165, enable, 0) == (a if enable else None)
            assert bus_value(60, a, 0, enable) == (a if enable else None)
            count += 2
    try:
        bus_value(0, 255, 1, 1)
        raise AssertionError("No se detectó conflicto de dos salidas")
    except ValueError:
        count += 1
    assert bus_value(60, 165, 0, 0) is None
    assert bus_value(60, 165, 1, 0) == 60
    assert bus_value(60, 165, 0, 1) == 165
    count += 3

    # Secuencia editorial de A -> bus -> B. A no se borra.
    a, b = 0x3C, 0xA5
    bus = bus_value(a, b, 1, 0)
    assert (a, b, bus) == (0x3C, 0xA5, 0x3C)
    b = register_next(b, bus, 1, True)
    a = register_next(a, bus, 0, True)
    assert (a, b) == (0x3C, 0x3C)
    assert bus_value(a, b, 0, 1) == 0x3C
    count += 3

    manuscript = BASE.with_suffix(".md").read_text(encoding="utf-8")
    assert manuscript.startswith("# Capítulo 7. Del bit al registro")
    assert "*Parte II" in manuscript
    assert "JavaFX" not in manuscript
    count += 3
    for i in range(1, 13):
        assert f"**Ejercicio {i} " in manuscript
        assert f"**{i}.**" in manuscript
        count += 2
    for token in (
        "b7", "b0", "MSB", "LSB", "byte", "256 patrones", "182",
        "0xB6", "0x3C", "0xA5", "multiplexor", "LOAD", "reloj",
        "flanco ascendente", "alta impedancia", "triestado", "OE_n",
        "A_OUT", "B_OUT", "bus", "conflicto eléctrico", "Z",
        "SN74HC377", "SN74HC245", "CLKEN", "DIR", "no tiene salidas triestado",
        "puente", "semántica", "capítulo 8", "capítulo 9",
    ):
        assert token.lower() in manuscript.lower(), token
        count += 1
    assert manuscript.count("[[EQ:") == 9
    assert manuscript.count("[[FIG:") == 4
    count += 2
    for name in FIGURES:
        for ext, minsize in ((".svg", 1300), (".png", 10000)):
            p = ROOT / "libro" / "figuras" / (name + ext)
            assert p.is_file() and p.stat().st_size > minsize, p
            count += 1
        assert f"[[FIG:{name}|" in manuscript
        count += 1

    with zipfile.ZipFile(BASE.with_suffix(".docx")) as docx:
        assert docx.testzip() is None
        xml = ET.fromstring(docx.read("word/document.xml"))
        equations = xml.findall(".//m:oMath", NS)
        figures = xml.findall(".//wp:inline", NS)
        assert len(equations) == 9, len(equations)
        assert len(figures) == 4, len(figures)
        assert all(img.find("wp:docPr", NS).get("descr") for img in figures)
        headers = [name for name in docx.namelist()
                   if name.startswith("word/header") and name.endswith(".xml")]
        assert headers and any(b"PARTE II" in docx.read(name) for name in headers)
        count += 5

    pdf = BASE.with_suffix(".pdf")
    assert pdf.is_file() and pdf.stat().st_size > 50_000
    info = subprocess.run(["pdfinfo", str(pdf)], text=True,
                          capture_output=True, check=True).stdout
    pages = re.search(r"^Pages:\s*(\d+)", info, re.MULTILINE)
    assert pages and 7 <= int(pages.group(1)) <= 12
    extracted = subprocess.run(["pdftotext", str(pdf), "-"], text=True,
                               capture_output=True, check=True).stdout
    assert len(extracted) > 12_000
    for token in ("Del bit al registro", "Figura 1.", "Figura 2.",
                  "Figura 3.", "Figura 4.", "Solucionario del capítulo 7",
                  "SN74HC377", "SN74HC245", "0xB6", "0x3C"):
        assert token.lower() in extracted.lower(), token
        count += 1
    count += 3
    print(f"Capítulo 7: {count} controles lógicos y documentales correctos, "
          f"{pages.group(1)} páginas, 9 ecuaciones OMML, 4 figuras, 12 ejercicios.")
    print("Sin mediciones eléctricas, CPU, RAM física ni prueba analógica de bus.")


if __name__ == "__main__":
    main()
