#!/usr/bin/env python3
"""Genera PDF suplementario y registro trazable de cinco fotos historicas.

Dependencias de desarrollo: reportlab y pillow. No es parte de las pruebas
Windows globales; el PDF generado se entrega en el ZIP global completo.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
PHOTOS = ROOT / "libro" / "figuras_historicas_c28o"
CATALOG = ROOT / "libro" / "FOTOGRAFIAS_HISTORICAS_C28N_MANIFIESTO.json"
EDITION = ROOT / "libro" / "ediciones" / "C28_O"
OUT = EDITION / "Aula_Computadora_Atlas_Historico_C28_O.pdf"
W, H = letter
DARK = colors.HexColor("#10253c")
BLUE = colors.HexColor("#216d8c")
GRAY = colors.HexColor("#505d6a")
PAPER = colors.HexColor("#fbfbf8")


def fonts() -> None:
    base = Path("/usr/share/fonts/truetype/dejavu")
    pdfmetrics.registerFont(TTFont("DejaVu", str(base / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(base / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVuSerif", str(base / "DejaVuSerif.ttf")))
    pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold")


def para(c: canvas.Canvas, text: str, x: float, top: float,
         width: float, size: float = 9.5, leading: float = 15,
         color: colors.Color = DARK, bold: bool = False,
         centered: bool = False) -> float:
    style = ParagraphStyle("custom", fontName="DejaVu-Bold" if bold else "DejaVu",
                           fontSize=size, leading=leading, textColor=color,
                           spaceBefore=0, spaceAfter=0,
                           alignment=TA_CENTER if centered else TA_LEFT)
    p = Paragraph(text, style)
    _, ht = p.wrap(width, 1000)
    p.drawOn(c, x, top - ht)
    return top - ht


def page(c: canvas.Canvas, number: int, group: str) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(46, H-51, 22, 2, fill=1, stroke=0)
    para(c, "AULA COMPUTADORA · ATLAS HISTÓRICO", 75, H-41, 420,
         size=8.3, leading=10, color=GRAY, bold=True)
    c.setStrokeColor(colors.HexColor("#d7dde3"))
    c.line(46, 47, W-46, 47)
    para(c, f"C28-O · {group}", 46, 40, 450, size=7.6, leading=10, color=GRAY)
    para(c, str(number), W-68, 40, 20, size=7.6, leading=10, color=GRAY)


def cover(c: canvas.Canvas) -> None:
    page(c, 1, "introducción")
    para(c, "Atlas histórico", 55, 660, 505, size=28, leading=39,
         color=DARK, bold=True)
    para(c, "Cinco máquinas y piezas reales para entender Aula-8 y Aula-16",
         55, 601, 505, size=14, leading=22, color=BLUE)
    top = 530
    paragraphs = [
        "Una foto de una computadora antigua muestra cómo se materializaron algunas "
        "ideas que estudiamos: direcciones, bits, memorias, interfaces y circuitos integrados.",
        "La foto <b>no demuestra</b> que los circuitos de nuestra Aula estén construidos ni "
        "que un diagrama funcional equivalga a un plano eléctrico. Para comprobar "
        "lógica digital usamos tablas, modelos y simulaciones; para construir usamos "
        "especificaciones eléctricas y pruebas físicas.",
        "Este atlas enlaza cinco dispositivos históricos con preguntas concretas del libro. "
        "Las fotografías están identificadas con autores y licencias Creative Commons.",
    ]
    for entry in paragraphs:
        top = para(c, entry, 57, top, 495, size=11.2, leading=20) - 18
    para(c, "Recorrido", 57, top-13, 480, size=13, leading=20, bold=True)
    top -= 52
    for title in ["1 · Altair 8800 — depositar bytes", "2 · Apple II — chips y buses",
                  "3 · DEC VT100 — texto y terminales", "4 · Intel 8086 — procesador real",
                  "5 · IBM PC 5150 — sistema completo"]:
        top = para(c, title, 65, top, 490, size=10.5, leading=19) - 8
    c.showPage()


PAGES = [
    dict(title="Panel del MITS Altair 8800", chapter="Capítulos 14–17",
         intro="La foto muestra indicadores de dirección y datos, interruptores numerados "
               "y mandos como EXAMINE, DEPOSIT y SINGLE STEP.",
         bridge="En Aula-8 proponemos introducir los bytes de LDI R0,42: "
                "<b>11 00 2A</b> desde la dirección <b>0x6000</b>. En un panel real, "
                "depositar un byte requiere que el procesador no conduzca el bus al mismo tiempo.",
         limit="La foto no valida el arbitraje, las señales de escritura ni la temporización "
               "del panel hipotético de Aula-8.",
         question="Escribe 0x2A en binario y explica por qué DEPOSIT no ejecuta la instrucción."),
    dict(title="Placa madre de un Apple II", chapter="Capítulos 9–12",
         intro="Se distinguen un procesador <b>6502</b>, bancos identificados como ROM y RAM, "
               "ranuras de expansión y pistas del circuito impreso.",
         bridge="Nuestro mapa de memoria necesita traducir una dirección de CPU en la "
                "selección de un chip y una posición interna. La foto permite localizar "
                "físicamente esas clases de componentes y sus conexiones.",
         limit="No podemos identificar todos los pines ni validar una topología de bus "
               "a partir de la apariencia de la placa; hacen falta esquemas y hojas de datos.",
         question="Señala el 6502 y dos zonas de memoria. ¿Por qué un registro no sustituye una RAM?"),
    dict(title="Terminal de texto DEC VT100", chapter="Capítulos 18 y 23B",
         intro="El terminal dispone de teclado y pantalla; se comunicaba con un equipo anfitrión. "
               "Los caracteres visibles no muestran directamente sus señales eléctricas.",
         bridge="Un byte puede representar un número o un carácter según el contexto. "
                "El controlador de la pantalla transforma información codificada en puntos visibles.",
         limit="El VT100 no valida el contrato de video elegido para Aula ni demuestra "
               "un sistema gráfico construido.",
         question="¿Qué diferencia hay entre el valor numérico 0x41 y la letra A codificada en ASCII?"),
    dict(title="Microprocesador Intel 8086", chapter="Capítulo 22",
         intro="Un chip encapsulado concentra una CPU; el Intel 8086 posee un bus de datos externo "
               "de 16 bits. Su silueta no muestra cómo se implementan las microoperaciones.",
         bridge="Aula-16 compara accesos de uno y dos bytes. El ancho del bus de datos "
                "es distinto de la organización de direcciones o del tamaño de los registros.",
         limit="Aula-16 sigue siendo una arquitectura educativa candidata. Esta foto "
               "no certifica una CPU Aula-16 simulada, fabricada ni conectada.",
         question="Distingue bus externo de 16 bits, byte de ocho bits y cantidad de direcciones."),
    dict(title="Computadora IBM PC 5150", chapter="Capítulos 22–24",
         intro="Aparecen unidad central, monitor y teclado de una computadora personal histórica. "
               "El IBM PC 5150 original utilizó un <b>Intel 8088</b> con bus externo de ocho bits.",
         bridge="El sistema necesita combinar procesamiento, memoria, firmware y periféricos. "
                "Una ALU sola no proporciona una máquina con teclado y pantalla.",
         limit="No debemos confundir Intel 8088 (IBM PC 5150) con Intel 8086 (foto anterior), "
               "ni atribuir a Aula capacidades no implementadas.",
         question="Enumera tres piezas o servicios necesarios además de la ALU."),
]


def photo_page(c: canvas.Canvas, entry: dict, data: dict, number: int) -> None:
    page(c, number, entry["chapter"])
    para(c, f"PIEZA HISTÓRICA {number-1:02d} DE 05", 55, 713, 500,
         size=8.3, leading=11, color=BLUE, bold=True)
    para(c, entry["title"], 55, 680, 507, size=19, leading=28,
         bold=True, color=DARK)
    path = PHOTOS / data["archivo"]
    with Image.open(path) as img:
        width, height = img.size
    frame_x, frame_y, frame_w, frame_h = 55, 329, 502, 307
    c.setFillColor(colors.HexColor("#f2f5f5"))
    c.roundRect(frame_x, frame_y, frame_w, frame_h, 7, fill=1, stroke=0)
    scale = min((frame_w - 16) / width, (frame_h - 16) / height)
    disp_w, disp_h = width * scale, height * scale
    c.drawImage(ImageReader(str(path)), frame_x + (frame_w-disp_w)/2,
                frame_y + (frame_h-disp_h)/2, width=disp_w, height=disp_h,
                preserveAspectRatio=True, mask="auto")
    top = 313
    for title, key in [("Observación", "intro"), ("Conexión con Aula", "bridge"),
                       ("Límite de la comparación", "limit"), ("Practica", "question")]:
        text = f"<b>{title}.</b> {entry[key]}"
        top = para(c, text, 57, top, 493, size=9.15, leading=14.3) - 9
    credit = (f"Foto: {data['autor_documentado']}. {data['licencia_esperada']}. "
              "Fuente: Wikimedia Commons. Redimensionada para esta página.")
    para(c, credit, 57, 66, 505, size=7.3, leading=10, color=GRAY)
    c.linkURL(data["pagina_fuente"], (55, 52, 556, 78), relative=0)
    c.showPage()


def credits(c: canvas.Canvas, manifest: list[dict]) -> None:
    page(c, 7, "fuentes y permisos")
    para(c, "Fuentes y créditos fotográficos", 55, 690, 510,
         size=20, leading=30, bold=True)
    top = 630
    for index, data in enumerate(manifest, 1):
        para(c, f"{index}. {data['titulo_commons'].removeprefix('File:')}",
             57, top, 485, size=10.6, leading=16, bold=True)
        top -= 24
        para(c, f"{data['autor_documentado']} · {data['licencia_esperada']}",
             70, top, 480, size=9, leading=13)
        top -= 19
        para(c, data["pagina_fuente"].replace("&", "&amp;"),
             70, top, 480, size=7.4, leading=12, color=BLUE)
        c.linkURL(data["pagina_fuente"], (65, top-18, 545, top+2), relative=0)
        top -= 42
    para(c, "Las licencias requieren atribución. En adaptaciones y recortes también hay que indicar "
         "cambios y revisar la obligación de compartir bajo la misma licencia cuando corresponda.",
         57, top-5, 495, size=9.3, leading=15)
    para(c, "Estas fotografías documentan aparatos históricos, no certifican los circuitos "
         "de Aula-8 o Aula-16. El PDF maestro C28-G no se ha modificado.",
         57, top-63, 495, size=9.3, leading=15)
    c.showPage()


def main() -> None:
    fonts()
    EDITION.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(CATALOG.read_text(encoding="utf-8"))["fotografias"]
    if len(manifest) != len(PAGES):
        raise ValueError("Atlas y manifiesto de imágenes desalineados")
    hashes = {}
    for data in manifest:
        path = PHOTOS / data["archivo"]
        if not path.is_file():
            raise FileNotFoundError(path)
        hashes[data["id"]] = dict(archivo=path.name,
                                 sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                 bytes=path.stat().st_size,
                                 autor=data["autor_documentado"],
                                 licencia=data["licencia_esperada"],
                                 fuente=data["pagina_fuente"])
    pdf = canvas.Canvas(str(OUT), pagesize=letter, pageCompression=1,
                        invariant=1, pdfVersion=(1, 4))
    pdf.setTitle("Aula Computadora Atlas Histórico C28-O")
    pdf.setAuthor("Aula Computadora · Marcos Moreira")
    cover(pdf)
    for idx, (p, data) in enumerate(zip(PAGES, manifest), start=2):
        photo_page(pdf, p, data, idx)
    credits(pdf, manifest)
    pdf.save()
    (EDITION / "ACTIVOS_FOTOGRAFICOS_VERIFICADOS_C28O.json").write_text(
        json.dumps({"edicion":"C28-O","fuentes":hashes,
                    "limite":"Fotografias contextuales, no esquemas ni pruebas HDL"},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PDF generado: {OUT}")


if __name__ == "__main__":
    main()
