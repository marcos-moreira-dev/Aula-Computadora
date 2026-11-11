#!/usr/bin/env python3
"""C28-S: inspección automática local del PDF maestro sin modificarlo.

Requiere PyMuPDF y Pillow en el entorno EDITORIAL. No forma parte de la
prueba Windows estándar porque Marcos no debe instalar dependencias nuevas.
Genera evidencia de geometría y ocho hojas de contacto a baja resolución.
No sustituye la lectura humana a escala normal ni certifica figuras/circuitos.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "libro/ediciones/C28_G/Aula_Computadora_C28_G_MAESTRO.pdf"
OUTPUT = ROOT / "c28_s/revision_pdf"
SHEET = OUTPUT / "hojas_contacto"
EXPECTED_PAGES = 248


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    doc = fitz.open(PDF)
    assert doc.page_count == EXPECTED_PAGES
    assert not doc.is_encrypted
    OUTPUT.mkdir(parents=True, exist_ok=True)
    SHEET.mkdir(parents=True, exist_ok=True)
    problems = []
    pages = []
    total_spans = total_images = 0
    replacements = 0
    headings = []
    footer_numbers = 0

    cols, rows_per_sheet = 4, 8
    tile_w, tile_h = 330, 475
    sheet = None
    paint = None
    font = ImageFont.load_default()
    sheet_filenames = []

    for index, page in enumerate(doc):
        if index % (cols * rows_per_sheet) == 0:
            sheet = Image.new("RGB", (cols * tile_w, rows_per_sheet * tile_h), "#dce5ed")
            paint = ImageDraw.Draw(sheet)
        blocks = page.get_text("dict")["blocks"]
        spans = [(s["text"], s["bbox"]) for block in blocks if "lines" in block
                 for line in block["lines"] for s in line["spans"] if s["text"].strip()]
        images = [block for block in blocks if block.get("type") == 1]
        total_spans += len(spans)
        total_images += len(images)
        replacement = sum(s.count("\ufffd") for s, _ in spans)
        replacements += replacement
        text = page.get_text("text")
        if not spans and not images:
            problems.append({"pagina": index + 1, "tipo": "pagina_sin_texto_ni_imagen"})
        bad_boxes = []
        for s, box in spans:
            if box[0] < -1 or box[1] < -1 or box[2] > page.rect.width+1 or box[3] > page.rect.height+1:
                bad_boxes.append({"texto": s[:55], "caja": [round(v, 2) for v in box]})
        for block in images:
            box = block["bbox"]
            if box[0] < -1 or box[1] < -1 or box[2] > page.rect.width+1 or box[3] > page.rect.height+1:
                bad_boxes.append({"tipo": "imagen", "caja": [round(v, 2) for v in box]})
        if bad_boxes:
            problems.append({"pagina": index + 1, "tipo": "elementos_fuera_pagina", "elementos": bad_boxes})
        lines = text.splitlines()
        for paragraph in lines:
            if paragraph.startswith("Capítulo ") and "....." not in paragraph:
                headings.append({"pagina": index+1, "titulo": paragraph[:100]})
                break
        if index > 0:
            assert re.search(r"Aula Computadora\s+·\s+" + str(index+1) + r"\b", text), index+1
            footer_numbers += 1
        pages.append({"numero": index+1, "fragmentos_texto": len(spans),
                      "imagenes": len(images), "caracteres": len(text),
                      "caracteres_reemplazo": replacement,
                      "cajas_fuera_de_pagina": len(bad_boxes)})

        # Miniatura: revisión de composición, NO legibilidad del texto.
        pix = page.get_pixmap(matrix=fitz.Matrix(0.49, 0.49), alpha=False)
        thumb = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        thumb.thumbnail((tile_w - 18, tile_h - 41), Image.Resampling.LANCZOS)
        cell = index % (cols * rows_per_sheet)
        x = (cell % cols) * tile_w + (tile_w - thumb.width) // 2
        y = (cell // cols) * tile_h + 24
        sheet.paste(thumb, (x, y))
        paint.text((x, y-18), f"PÁGINA {index+1:03d}", fill="#223344", font=font)

        if cell == cols * rows_per_sheet - 1 or index == len(doc) - 1:
            name = f"C28_S_CONTACTO_{index // (cols*rows_per_sheet)+1:02d}.jpg"
            sheet.save(SHEET / name, "JPEG", quality=78, optimize=True)
            sheet_filenames.append(str(Path("hojas_contacto") / name))
            sheet.close()

    toc_lines = (doc[2].get_text("text") + "\n" + doc[3].get_text("text")).splitlines()
    toc = []
    for line in toc_lines:
        match = re.fullmatch(r"Capítulo (\d+B?)\. (.+?)\.{5,}(\d+)", line)
        if match:
            toc.append({"id": match.group(1), "titulo": match.group(2).strip(),
                        "pagina": int(match.group(3))})
    expected_ids = [str(i) for i in range(1, 25)]
    expected_ids.insert(7, "7B")
    expected_ids.insert(expected_ids.index("23")+1, "23B")
    assert [item["id"] for item in toc] == expected_ids, [item["id"] for item in toc]
    assert len(headings) == len(toc) == 26
    for table_entry, actual in zip(toc, headings):
        match = re.match(r"Capítulo (\d+B?)\. (.+)", actual["titulo"])
        assert match
        assert (table_entry["id"], table_entry["pagina"]) == (match.group(1), actual["pagina"])
        assert table_entry["titulo"].startswith(match.group(2).strip()), table_entry
    assert footer_numbers == 247
    assert replacements == 0, f"Caracteres ilegibles U+FFFD: {replacements}"
    assert not problems, f"Hallazgos que requieren revisión: {len(problems)}"
    report = {
        "etapa": "C28-S / auditoria geometrica y contacto visual del maestro PDF",
        "maestro_pdf": str(PDF.relative_to(ROOT)),
        "sha256_maestro": digest(PDF),
        "paginas": len(doc),
        "formato": "A4",
        "fragmentos_texto": total_spans,
        "bloques_imagen": total_images,
        "caracteres_reemplazo": replacements,
        "entradas_indice_verificadas": len(toc),
        "pies_de_pagina_con_numero": footer_numbers,
        "indice_coincide_con_capitulos": True,
        "indice": toc,
        "alertas_cajas_o_paginas": problems,
        "paginas_detalle": pages,
        "titulos_detectados_por_extraccion": headings,
        "hojas_contacto": sheet_filenames,
        "limitaciones": [
            "La geometria de texto/imagen no detecta una ecuacion semanticamente errada",
            "Los montajes reducidos no demuestran legibilidad, orden de lectura ni ausencia de superposiciones finas",
            "La revision visual de 248 paginas a resolucion final permanece pendiente",
            "No se altero el Word/PDF maestro ni se verifica fisicamente ningun circuito",
        ],
    }
    (OUTPUT / "C28_S_REPORTE_PAGINAS.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"C28-S: {len(doc)} páginas, {total_spans} fragmentos, {total_images} imágenes")
    print(f"C28-S: cero cajas fuera de página y cero caracteres de sustitución; {len(sheet_filenames)} hojas de contacto")
    print(f"C28-S: {len(toc)} capítulos coinciden con el índice; {footer_numbers} folios correctos")
    print("C28-S: inspección visual humana al 100% todavía PENDIENTE")


if __name__ == "__main__":
    main()
