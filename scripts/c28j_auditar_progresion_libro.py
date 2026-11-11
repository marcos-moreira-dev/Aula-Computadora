#!/usr/bin/env python3
"""C28-J: inventario reproducible de la progresión editorial de 26 capítulos.

Solo analiza fuentes y activos; NO certifica corrección lógica, electrónica,
estilo literario ni la correspondencia semántica entre dibujos y circuitos.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "libro" / "capitulos"
FIGURES = ROOT / "libro" / "figuras"
REPORT = ROOT / "libro" / "AUDITORIA_PROGRESION_C28J.md"
JSON_REPORT = ROOT / "libro" / "AUDITORIA_PROGRESION_C28J.json"

# Etiquetas editoriales para orientar la revisión, NO módulos ya certificados.
CONTRIBUTIONS = {
    "01": "corriente, resistencia y alimentación de una práctica",
    "02": "transistor usado como interruptor controlado",
    "03": "tabla de verdad, NAND y señal de habilitación",
    "04": "funciones combinacionales y XOR con NAND",
    "05": "realimentación y almacenamiento de un bit",
    "06": "biestable D y control de carga mediante reloj",
    "07": "ocho biestables forman el registro R0 de Aula-8",
    "07b": "significado de un byte, números, texto e instrucciones",
    "08": "buses de 16 direcciones y 8 datos; acceso a memoria",
    "09": "transferencias entre registros, RAM y ROM",
    "10": "sumador y cambio del estado aritmético",
    "11": "selección de operaciones de una ALU de 8 bits",
    "12": "integración del datapath de Aula-8",
    "13": "señales que coordinan las microacciones",
    "14": "bytes de programa y flujo de lectura del panel",
    "15": "trayecto PC/MAR/MDR/IR y acceso a instrucciones",
    "16": "pila, SP, saltos, CALL y RET",
    "17": "vector de reset y arranque desde ROM",
    "18": "terminal y periféricos en mapa de memoria",
    "19": "bloques de almacenamiento y recuperación de programas",
    "20": "programas y ensamblado en el anfitrión",
    "21": "operaciones de 16 bits sin alterar 16 bits de dirección",
    "22": "bus externo Aula-16 de 16 bits y bancos bajo/alto",
    "23": "algoritmos Aula-16 con ISA aún candidata",
    "23v": "periférico de vídeo V1 en texto y gráficos",
    "24": "integración didáctica y límites del prototipo",
}

FIGURE_REF = re.compile(r"\[\[FIG:([^|\]\s]+)\|", re.MULTILINE)
FORMULA_REF = re.compile(r"\[\[EQ:[^\]]+\]\]")
CONSTRUCTION = re.compile(r"^## Construimos Aula-", re.MULTILINE)
CHAPTER_TITLE = re.compile(r"^# (Capítulo [^\n]+)", re.MULTILINE)
TABLE_HEADER = re.compile(r"^\|\s*[-:| ]{3,}\|?\s*$", re.MULTILINE)


def chapter_key(filename: str) -> str:
    return filename.partition("_")[0]


def public_key(key: str) -> str:
    """Conservar el nombre editorial 23B aunque la fuente se llame 23v."""
    return "23B" if key == "23v" else key.upper()


def assess(path: Path) -> dict:
    source = path.read_text(encoding="utf-8")
    key = chapter_key(path.name)
    title = CHAPTER_TITLE.search(source)
    figures = list(FIGURE_REF.findall(source))
    issues: list[str] = []

    for ext in (".docx", ".pdf"):
        if not path.with_suffix(ext).is_file():
            issues.append(f"No existe fascículo {ext}")
    for name in figures:
        png = FIGURES / (name + ".png")
        svg = FIGURES / (name + ".svg")
        if not png.is_file() or png.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            issues.append(f"PNG ausente o cabecera incorrecta: {name}")
        if not svg.is_file():
            issues.append(f"SVG ausente: {name}")
        else:
            try:
                ET.parse(svg)
            except ET.ParseError:
                issues.append(f"SVG no válido como XML: {name}")

    if not title:
        issues.append("No se reconoce el título")
    if "## Solucionario" not in source:
        issues.append("No aparece encabezado de solucionario")
    if not figures:
        issues.append("No hay referencias a figuras")
    if key not in CONTRIBUTIONS:
        issues.append("Falta etiqueta editorial de aporte")

    return {
        "id": key,
        "id_editorial": public_key(key),
        "archivo": path.name,
        "titulo": title.group(1) if title else path.stem,
        "aporte_educativo": CONTRIBUTIONS.get(key, "revisar"),
        "seccion_construimos_explicita": bool(CONSTRUCTION.search(source)),
        "figuras_referenciadas": len(figures),
        "identificadores_figuras": figures,
        "formulas": len(FORMULA_REF.findall(source)),
        "tablas_aproximadas": len(TABLE_HEADER.findall(source)),
        "tiene_solucionario": "## Solucionario" in source,
        "problemas_estructurales": issues,
    }


def run() -> dict:
    chapters = [assess(p) for p in sorted(CHAPTERS.glob("*.md"))]
    keys = [x["id"] for x in chapters]
    missing_keys = sorted(set(CONTRIBUTIONS) - set(keys))
    issues = sum(len(ch["problemas_estructurales"]) for ch in chapters)
    explicit = sum(ch["seccion_construimos_explicita"] for ch in chapters)
    result = {
        "version": "C28-J / diagnóstico de progresión del LIBRO",
        "capitulos": len(chapters),
        "secciones_construimos_explicitas": explicit,
        "capitulos_sin_ese_encabezado": [ch["id"] for ch in chapters
                                         if not ch["seccion_construimos_explicita"]],
        "referencias_figuras": sum(ch["figuras_referenciadas"] for ch in chapters),
        "svg_suplementarios_sin_referencia": sorted(
            {p.stem for p in FIGURES.glob("*.svg")} -
            {name for ch in chapters for name in ch["identificadores_figuras"]}),
        "problemas_estructurales": issues,
        "faltantes_en_matriz": missing_keys,
        "limites": ["No evalúa calidad didáctica o redacción completa",
                    "Una tabla o figura correcta en formato puede ser conceptualmente incorrecta",
                    "No ejecuta testbenches ni pruebas eléctricas"],
        "detalle": chapters,
    }

    lines = [
        "# Auditoría de progresión editorial C28-J — 26 capítulos",
        "",
        "**Método:** inventario automático de fuentes Markdown, fascículos",
        "Word/PDF, referencias a PNG/SVG, ecuaciones y encabezados de",
        "construcción. **No** constituye lectura semántica certificada.",
        "",
        f"- Capítulos: **{len(chapters)}** (objetivo: 26).",
        f"- Bloques explícitos «Construimos Aula…»: **{explicit}**.",
        f"- Referencias a ilustraciones: **{result['referencias_figuras']}**.",
        f"- Diagramas SVG adicionales de pilotos fuera de los 26 capítulos: **{len(result['svg_suplementarios_sin_referencia'])}**.",
        f"- Problemas estructurales detectados: **{issues}**.",
        "",
        "| Cap. | Qué aporta a la computadora | «Construimos» | Figuras | Fórmulas | Estructura |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for chapter in chapters:
        status = "REVISAR" if chapter["problemas_estructurales"] else "OK"
        lines.append(
            f"| {chapter['id_editorial']} | {chapter['aporte_educativo']} | "
            f"{'Sí' if chapter['seccion_construimos_explicita'] else 'No (revisar narrativa)'} | "
            f"{chapter['figuras_referenciadas']} | {chapter['formulas']} | {status} |"
        )

    lines += [
        "",
        "## Capítulos sin encabezado «Construimos»",
        "",
        ", ".join(f"**{public_key(key)}**" for key in result["capitulos_sin_ese_encabezado"]),
        "",
        "**Interpretación:** la ausencia de ese título NO significa que falte",
        "una explicación constructiva. Revisar especialmente el salto de",
        "conceptos a piezas en C04 y 07B, el carácter provisional de C23",
        "y la síntesis final de C24. C01/C02 incluyen prácticas propias y",
        "tampoco requieren una sección con ese nombre para ser correctos.",
        "",
        "## Próximos controles manuales (todavía no certificados)",
        "",
        "1. Leer todos los cierres y aperturas de capítulo como una secuencia continua.",
        "2. Comprobar que diagramas 2D, tablas y nombres de señales coinciden con su modelo.",
        "3. Añadir un anclaje de construcción solo cuando mejore la comprensión.",
        "4. Distinguir pruebas digitales de documentación y de montajes físicos.",
        "5. Integrar el suplemento C28-H únicamente tras revisar el capítulo 15 y la política del PC.",
        "6. Revisar cuáles diagramas adicionales de los pilotos merecen entrar en una futura edición maestra.",
        "",
        "El progreso editorial global previo (77 %) **no se modifica solo por",
        "pasar esta auditoría estructural**. Su objetivo es localizar el trabajo",
        "real, no producir un porcentaje artificial.",
    ]
    if missing_keys:
        lines += ["", "**Faltan identificadores de capítulos:** " + ", ".join(missing_keys)]
    for chapter in chapters:
        if chapter["problemas_estructurales"]:
            lines += ["", f"**{chapter['id_editorial']}:** " + "; ".join(chapter["problemas_estructurales"])]

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    JSON_REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(f"C28-J: {len(chapters)} capítulos, {explicit} bloques Construimos, "
          f"{result['referencias_figuras']} figuras referenciadas; "
          f"{issues} problemas estructurales.")
    print("Informe:", REPORT)
    return result


if __name__ == "__main__":
    audit = run()
    if audit["capitulos"] != 26 or audit["faltantes_en_matriz"] or audit["problemas_estructurales"]:
        raise SystemExit(1)
