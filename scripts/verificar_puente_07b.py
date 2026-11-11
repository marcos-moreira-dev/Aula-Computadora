#!/usr/bin/env python3
"""Contrasta las interpretaciones numéricas y el interludio 07B.

Comprobaciones conceptuales de anfitrión; no ejecutan CPU ni miden hardware.
"""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "libro" / "capitulos" / "07b_del_bit_al_significado"
FIGURES = (
    "p07b_fig01_del_voltaje_a_la_logica",
    "p07b_fig02_un_byte_varios_significados",
    "p07b_fig03_pesos_con_y_sin_signo",
    "p07b_fig04_escalera_de_significado",
)
NS = {
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}


def weighted_unsigned(bit_string: str) -> int:
    return sum(int(bit) * (1 << (7 - i)) for i, bit in enumerate(bit_string))


def weighted_signed(bit_string: str) -> int:
    return -128 * int(bit_string[0]) + sum(
        int(bit_string[i]) * (1 << (7 - i)) for i in range(1, 8)
    )


def main() -> None:
    checks = 0

    for n in range(256):
        bits = f"{n:08b}"
        signed = n if n < 128 else n - 256
        assert weighted_unsigned(bits) == n
        assert weighted_signed(bits) == signed
        assert int(bits, 2) == int(f"{n:02X}", 16)
        assert set(i for i in range(8) if bits[7 - i] == "1") == {
            i for i in range(8) if n & (1 << i)
        }
        assert -128 <= signed <= 127
        checks += 5

    for a in (0, 1):
        for b in (0, 1):
            assert (not (a and b)) == (a == 0 or b == 0)
            checks += 1
    assert weighted_unsigned("01000001") == 65
    assert weighted_signed("01000001") == 65
    assert weighted_unsigned("11111111") == 255
    assert weighted_signed("11111111") == -1
    assert weighted_signed("10000000") == -128
    assert {i for i in range(8) if 0x41 & (1 << i)} == {0, 6}
    assert "A".encode("utf-8") == bytes.fromhex("41")
    assert "é".encode("utf-8") == bytes.fromhex("C3 A9")
    try:
        bytes.fromhex("FF").decode("utf-8", errors="strict")
        raise AssertionError("Un byte FF no debe aceptarse solo como UTF-8")
    except UnicodeDecodeError:
        pass
    checks += 9

    manuscript = BASE.with_suffix(".md").read_text(encoding="utf-8")
    assert manuscript.startswith("# Capítulo 7B. Del bit al significado")
    assert "*Parte II" in manuscript
    assert "JavaFX" not in manuscript
    assert "capítulo puente" in manuscript.lower()
    checks += 4
    for i in range(1, 13):
        assert f"**Ejercicio {i} " in manuscript
        assert f"**{i}.**" in manuscript
        checks += 2
    for token in (
        "semántica", "hardware", "software", "umbral", "región intermedia",
        "RESET_n", "NAND", "01000001", "0x41", "ASCII", "máscara",
        "b6 y b0", "255", "−1", "−128", "complemento a dos", "UTF-8",
        "0xC3 0xA9", "0x1200", "dirección", "contenido", "ISA",
        "opcode", "tipo", "estructura de datos", "orientada a objetos",
        "MiniC-Aula", "capítulo 8",
    ):
        assert token.lower() in manuscript.lower(), token
        checks += 1
    assert manuscript.count("[[EQ:") == 9
    assert manuscript.count("[[FIG:") == 4
    checks += 2
    for name in FIGURES:
        assert f"[[FIG:{name}|" in manuscript
        for ext, min_bytes in ((".svg", 1300), (".png", 10000)):
            figure = ROOT / "libro" / "figuras" / f"{name}{ext}"
            assert figure.is_file() and figure.stat().st_size > min_bytes, figure
            checks += 1
        checks += 1

    with zipfile.ZipFile(BASE.with_suffix(".docx")) as archive:
        assert archive.testzip() is None
        xml = ET.fromstring(archive.read("word/document.xml"))
        equations = xml.findall(".//m:oMath", NS)
        figures = xml.findall(".//wp:inline", NS)
        assert len(equations) == 9, len(equations)
        assert len(figures) == 4, len(figures)
        assert all(fig.find("wp:docPr", NS).get("descr") for fig in figures)
        checks += 4

    pdf = BASE.with_suffix(".pdf")
    assert pdf.exists() and pdf.stat().st_size > 50_000
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                          check=True, text=True).stdout
    page_count = re.search(r"^Pages:\s*(\d+)", info, flags=re.MULTILINE)
    assert page_count and 7 <= int(page_count.group(1)) <= 11
    extracted = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True,
                               check=True, text=True).stdout
    assert len(extracted) > 15000
    for token in ("Del bit al significado", "Figura 1.", "Figura 2.",
                  "Figura 3.", "Figura 4.", "Solucionario del capítulo 7B",
                  "01000001", "RESET_n", "0x1200", "UTF-8"):
        assert token in extracted, token
        checks += 1
    checks += 3
    print(f"Capítulo 7B: {checks} comprobaciones lógicas y documentales, "
          f"{page_count.group(1)} páginas, 9 ecuaciones OMML, "
          "4 figuras, 12 ejercicios resueltos.")
    print("La CPU, el formato de instrucciones definitivo y los circuitos físicos siguen sin implementar.")


if __name__ == "__main__":
    main()
