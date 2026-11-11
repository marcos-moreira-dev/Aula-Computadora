#!/usr/bin/env python3
"""Maqueta el manuscrito fuente del capítulo 1 en Word editable (OMML)."""
from pathlib import Path
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "libro" / "capitulos" / "01_la_corriente_y_sus_caminos.md"
DOCX = SRC.with_suffix(".docx")
FIG_DIR = ROOT / "libro" / "figuras"
ACCENT = RGBColor(16, 86, 121)
INK = RGBColor(32, 43, 54)


def apply_font(style, name, size, bold=False, color=None):
    style.font.name = name
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.color.rgb = color or INK
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    rfonts.set(qn("w:ascii"), name)
    rfonts.set(qn("w:hAnsi"), name)


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tcpr.append(shd)


def add_rich(paragraph, text):
    """Markup editorial mínimo: negritas, cursivas y código en línea."""
    parts = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)", text)
    for piece in parts:
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**"):
            paragraph.add_run(piece[2:-2]).bold = True
        elif piece.startswith("*") and piece.endswith("*"):
            paragraph.add_run(piece[1:-1]).italic = True
        elif piece.startswith("`") and piece.endswith("`"):
            run = paragraph.add_run(piece[1:-1])
            run.font.name = "Liberation Mono"
            run.font.size = Pt(9.3)
        else:
            paragraph.add_run(piece)


def equation(document, formula):
    """Crea OMML editable; los exponentes son estructuras, no glifos elevados.

    Los superíndices Unicode pegados a una cifra se renderizaban mal en
    LibreOffice (por ejemplo, el último cero de 16⁰). Aquí se expresa cada
    potencia con m:sSup, que Word también puede editar como ecuación.
    """
    para = document.add_paragraph(style="Ecuacion")
    # Una ecuación no debe quedar pegada al pie de página ni separarse de la
    # frase que muestra cómo se interpreta su resultado.
    para.paragraph_format.keep_together = True
    para.paragraph_format.keep_with_next = True
    outer = OxmlElement("m:oMathPara")
    inner = OxmlElement("m:oMath")
    def math_run(parent, content):
        run = OxmlElement("m:r")
        props = OxmlElement("m:rPr")
        sty = OxmlElement("m:sty")
        sty.set(qn("m:val"), "p")
        props.append(sty)
        run.append(props)
        t = OxmlElement("m:t")
        t.text = content
        run.append(t)
        parent.append(run)

    elevated = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    regular = "0123456789"
    exponent_pattern = re.compile(r"([0-9A-Za-z)]+)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)")
    cursor = 0
    for match in exponent_pattern.finditer(formula):
        if match.start() > cursor:
            math_run(inner, formula[cursor:match.start()])
        power = OxmlElement("m:sSup")
        base = OxmlElement("m:e")
        math_run(base, match.group(1))
        exp = OxmlElement("m:sup")
        math_run(exp, match.group(2).translate(str.maketrans(elevated, regular)))
        power.append(base)
        power.append(exp)
        inner.append(power)
        cursor = match.end()
    if cursor < len(formula):
        math_run(inner, formula[cursor:])
    outer.append(inner)
    para._p.append(outer)
    return para


def figure(document, figure_id, caption, alt):
    png = FIG_DIR / (figure_id + ".png")
    if not png.is_file():
        raise FileNotFoundError(f"Falta figura: {png}")
    intro = document.add_paragraph(style="Figura")
    intro.paragraph_format.keep_with_next = True
    shape = intro.add_run().add_picture(str(png), width=Cm(15.9))
    inline = shape._inline
    inline.docPr.set("descr", alt)
    inline.docPr.set("title", caption)
    cap = document.add_paragraph(style="Leyenda")
    cap.paragraph_format.keep_together = True
    add_rich(cap, caption)


def table(document, parsed_rows):
    column_count = len(parsed_rows[0])
    if column_count == 4:
        widths = [3.3, 1.65, 2.0, 8.5]
    elif column_count == 3:
        widths = [5, 5, 5]
    else:
        # Los sumadores requieren tablas de verdad de 5 columnas y una
        # bitácora de acarreo de 7, sin desbordar el ancho útil A4.
        widths = [15.5 / column_count] * column_count
    tb = document.add_table(rows=0, cols=len(parsed_rows[0]))
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    tb.style = "Table Grid"
    for idx, row in enumerate(parsed_rows):
        cells = tb.add_row().cells
        trpr = tb.rows[idx]._tr.get_or_add_trPr()
        trpr.append(OxmlElement("w:cantSplit"))
        for col, raw in enumerate(row):
            cell = cells[col]
            cell.width = Cm(widths[col])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            # Conservar juntas todas las filas de tablas breves, evitando
            # que una tabla diagnóstica se parta entre dos páginas.
            if idx != len(parsed_rows) - 1:
                p.paragraph_format.keep_with_next = True
            add_rich(p, raw)
            for r in p.runs:
                r.font.size = Pt(8.4)
                if idx == 0:
                    r.font.bold = True
            if idx == 0:
                shade(cell, "DBEAF2")
            elif idx % 2 == 0:
                shade(cell, "F6F9FB")
        if idx == 0:
            tb.rows[idx]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    document.add_paragraph().paragraph_format.space_after = Pt(0)


def create_styles(doc, running_title="La corriente y sus caminos", part="I"):
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21)
    sec.top_margin = Cm(2.15)
    sec.bottom_margin = Cm(2.15)
    sec.left_margin = Cm(2.4)
    sec.right_margin = Cm(2.35)
    sec.header_distance = Cm(.85)
    sec.footer_distance = Cm(.85)

    normal = doc.styles["Normal"]
    apply_font(normal, "Liberation Serif", 10.6)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.20
    for name, size, before, after in [("Heading 1", 15, 15, 7), ("Heading 2", 12.2, 12, 5)]:
        style = doc.styles[name]
        apply_font(style, "Liberation Sans", size, bold=True, color=ACCENT)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True
    for name, base, size in [("Ecuacion", "Normal", 11.8), ("Figura", "Normal", 10),
                             ("Leyenda", "Normal", 9.1), ("Ejercicio", "Normal", 10.5)]:
        if name not in doc.styles:
            from docx.enum.style import WD_STYLE_TYPE
            style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        else:
            style = doc.styles[name]
        style.base_style = doc.styles[base]
        apply_font(style, "Liberation Serif", size, color=INK)
    doc.styles["Ecuacion"].paragraph_format.space_before = Pt(1)
    doc.styles["Ecuacion"].paragraph_format.space_after = Pt(7)
    doc.styles["Ecuacion"].paragraph_format.left_indent = Cm(.8)
    doc.styles["Figura"].paragraph_format.space_before = Pt(9)
    doc.styles["Figura"].paragraph_format.space_after = Pt(1)
    doc.styles["Figura"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.styles["Leyenda"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.styles["Leyenda"].paragraph_format.space_after = Pt(10)
    doc.styles["Ejercicio"].paragraph_format.space_after = Pt(10)

    header = sec.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = header.add_run(f"AULA-COMPUTADORA  ·  PARTE {part}")
    run.bold = True
    run.font.name = "Liberation Sans"
    run.font.size = Pt(7.8)
    run.font.color.rgb = ACCENT

    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run(running_title + "    ·    ")
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    footer._p.append(fld)
    for r in footer.runs:
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(88, 101, 116)


def parse(source):
    blocks = []
    pending = []
    def flush():
        if pending:
            blocks.append(("paragraph", " ".join(pending)))
            pending.clear()
    for raw in source.splitlines():
        s = raw.strip()
        if not s:
            flush()
            continue
        if s == "[[PAGEBREAK]]":
            flush(); blocks.append(("pagebreak", ""))
        elif s.startswith("# "):
            flush(); blocks.append(("title", s[2:]))
        elif s.startswith("## "):
            flush(); blocks.append(("h1", s[3:]))
        elif s.startswith("### "):
            flush(); blocks.append(("h2", s[4:]))
        elif s.startswith("[[EQ:") and s.endswith("]]"):
            flush(); blocks.append(("eq", s[5:-2]))
        elif s.startswith("[[FIG:") and s.endswith("]]"):
            flush(); blocks.append(("fig", s[6:-2].split("|", 2)))
        elif s.startswith("|"):
            flush(); blocks.append(("table_line", s))
        elif re.match(r"^\d+\.\s", s):
            flush(); blocks.append(("number", s))
        elif s.startswith("*Parte "):
            flush(); blocks.append(("subtitle", s.strip("*")))
        else:
            pending.append(s)
    flush()
    # Reagrupar líneas de tablas; saltar separador Markdown.
    packed = []
    tlines = []
    for typ, val in blocks:
        if typ == "table_line":
            cells = [c.strip() for c in val.strip("|").split("|")]
            if not all(re.fullmatch(r"[-: ]+", c or "") for c in cells):
                tlines.append(cells)
        else:
            if tlines:
                packed.append(("table", tlines))
                tlines = []
            packed.append((typ, val))
    if tlines:
        packed.append(("table", tlines))
    return packed


def main():
    doc = Document()
    blocks = parse(SRC.read_text(encoding="utf-8"))
    title = next(v for t, v in blocks if t == "title")
    subtitle = next((v for t, v in blocks if t == "subtitle"), "Parte I")
    part_match = re.search(r"Parte\s+([IVX]+)", subtitle)
    create_styles(doc, title.split(". ", 1)[-1],
                  part=part_match.group(1) if part_match else "I")
    for index, (typ, value) in enumerate(blocks):
        if typ == "title":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(24)
            p.paragraph_format.space_after = Pt(9)
            r = p.add_run(value)
            r.bold = True; r.font.name = "Liberation Sans"
            r.font.size = Pt(25); r.font.color.rgb = ACCENT
        elif typ == "subtitle":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(18)
            r = p.add_run(value)
            r.italic = True; r.font.size = Pt(10); r.font.color.rgb = ACCENT
        elif typ == "h1":
            heading = doc.add_heading(value, level=1)
            if value.startswith("Solucionario") or (index > 0 and blocks[index - 1][0] == "pagebreak"):
                # El salto pertenece al encabezado: un párrafo de salto
                # independiente puede producir una página vacía si cae al final.
                heading.paragraph_format.page_break_before = True
        elif typ == "pagebreak":
            # El siguiente encabezado trae el salto; no insertar párrafo vacío.
            continue
        elif typ == "h2":
            doc.add_heading(value, level=2)
        elif typ == "eq":
            p = equation(doc, value)
            if index + 1 < len(blocks) and blocks[index + 1][0] == "table":
                p.paragraph_format.keep_with_next = True
        elif typ == "fig":
            figure(doc, *value)
        elif typ == "table":
            table(doc, value)
        elif typ == "number":
            p = doc.add_paragraph(style="Ejercicio")
            p.paragraph_format.left_indent = Cm(.55)
            p.paragraph_format.first_line_indent = Cm(-.55)
            add_rich(p, value)
        else:
            p = doc.add_paragraph(style="Ejercicio" if value.startswith("**Ejercicio ") else "Normal")
            # Si la siguiente pieza es una tabla, conservar su explicación
            # inmediata con ella; evita tablas solitarias al inicio de página.
            if index + 1 < len(blocks) and blocks[index + 1][0] in {"table", "eq"}:
                p.paragraph_format.keep_with_next = True
            add_rich(p, value)
    DOCX.parent.mkdir(parents=True, exist_ok=True)
    doc.save(DOCX)
    print(f"WORD GENERADO: {DOCX}")
    print(f"BLOQUES: {len(parse(SRC.read_text(encoding='utf-8')))}")


if __name__ == "__main__":
    main()
