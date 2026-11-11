#!/usr/bin/env python3
"""Genera cuatro figuras originales sobre realimentación y latch SR NAND."""
from pathlib import Path
import subprocess

from generar_figuras_capitulo_01 import ROOT, STYLE


OUT = ROOT / "libro" / "figuras"


def wrap(title: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 1000 500">
<title>{title}</title><rect width="1000" height="500" fill="white"/>{STYLE}
{body}</svg>'''


def block(x: int, y: int, name: str, fill: str = "#e7f3fa") -> str:
    return f'''<rect x="{x}" y="{y}" width="176" height="96" rx="15" fill="{fill}" stroke="#283a4b" stroke-width="3"/>
<text x="{x + 88}" y="{y + 43}" text-anchor="middle" class="label">{name}</text>
<text x="{x + 88}" y="{y + 70}" text-anchor="middle" class="small">NAND</text>'''


FIGS = {}

FIGS["c05_fig01_combinacional_realimentacion"] = wrap("Comparación entre función combinacional y realimentación", '''
<text x="45" y="47" class="label">Del resultado inmediato al estado que persiste</text>
<text x="45" y="85" class="small">No toda realimentación crea memoria; aquí estudiaremos una pareja estable.</text>
<rect x="48" y="126" width="429" height="314" rx="17" fill="#f2f7fb" stroke="#aecbd9" stroke-width="2"/>
<text x="263" y="169" text-anchor="middle" class="label">Red combinacional</text>
<text x="263" y="201" text-anchor="middle" class="small">Sin estado almacenado</text>
''' + block(190, 249, "1 compuerta") + '''
<text x="66" y="281" class="small accent">A</text><text x="66" y="320" class="small accent">B</text>
<path class="wire" d="M88,273 H190 M88,315 H190 M366,297 H443"/>
<text x="383" y="279" class="small accent">Y</text>
<text x="263" y="407" text-anchor="middle" class="tiny">Y depende de A y B actuales</text>
<rect x="518" y="126" width="433" height="314" rx="17" fill="#f1f7f0" stroke="#8dbb9a" stroke-width="2"/>
<text x="735" y="169" text-anchor="middle" class="label">Red realimentada</text>
<text x="735" y="201" text-anchor="middle" class="small">Un estado puede persistir</text>
<rect x="660" y="247" width="177" height="91" rx="15" fill="#d9efe0" stroke="#336d4c" stroke-width="3"/>
<text x="748" y="279" text-anchor="middle" class="label">2 NAND</text>
<text x="748" y="311" text-anchor="middle" class="small">cruzadas</text>
<path class="wire" d="M552,267 H660 M837,291 H917"/>
<text x="541" y="251" class="tiny accent">S_n, R_n</text>
<text x="857" y="274" class="small accent">Q</text>
<path d="M900,291 V385 H616 V314 H660" fill="none" stroke="#28805a" stroke-width="4"/>
<path d="M647,307 L658,314 L647,321" fill="none" stroke="#28805a" stroke-width="3"/>
<text x="745" y="414" text-anchor="middle" class="tiny">La salida influye en entradas internas</text>
''')

FIGS["c05_fig02_latch_nand_cruzado"] = wrap("Conexiones cruzadas sin cortocircuitos del latch SR", '''
<text x="45" y="45" class="label">Latch SR: dos NAND unidas por realimentación</text>
<text x="45" y="78" class="small">S_n y R_n se activan con 0. Q_n complementa Q solo en estados válidos.</text>
''' + block(330, 150, "NAND 1") + block(670, 280, "NAND 2") + '''
<path class="wire" d="M140,185 H330"/>
<text x="72" y="192" class="label accent">S_n</text>
<text x="193" y="172" class="tiny">SET</text>
<path class="wire" d="M506,205 H617 V316 H670"/>
<circle cx="588" cy="205" r="5" class="node"/>
<path class="wire" d="M506,205 H888"/>
<text x="897" y="210" class="label accent">Q</text>
<path class="wire" d="M532,353 H670"/>
<text x="462" y="361" class="label accent">R_n</text>
<text x="536" y="339" class="tiny">RESET</text>
<path class="wire" d="M846,329 H943"/>
<text x="948" y="336" class="label accent">Q_n</text>
<path d="M903,329 V456 H234 V230 H330" fill="none" stroke="#28805a" stroke-width="4" stroke-linejoin="round"/>
<circle cx="903" cy="329" r="6" fill="#28805a"/>
<text x="490" y="440" text-anchor="middle" class="small" style="fill:#28805a">Realimentación de Q_n hacia NAND 1</text>
<text x="591" y="291" text-anchor="middle" class="tiny accent">Q hacia NAND 2</text>
<text x="303" y="217" class="tiny">Q_n</text>
''')


FIGS["c05_fig03_tabla_estados"] = wrap("Tabla de estados del latch SR NAND activo en bajo", '''
<text x="45" y="47" class="label">Tabla de estados: las entradas no bastan para HOLD</text>
<text x="45" y="81" class="small">Las salidas indicadas corresponden a estados estables ideales.</text>
<rect x="59" y="123" width="880" height="333" rx="16" fill="#f2f8fb"/>
<text x="121" y="168" class="label">S_n R_n</text>
<text x="369" y="168" class="label">Q</text>
<text x="518" y="168" class="label">Q_n</text>
<text x="683" y="168" class="label">Lectura</text>
<path class="wire" d="M79,187 H916"/>
<rect x="79" y="199" width="837" height="47" rx="7" fill="#e5f3e9"/>
<text x="150" y="233" class="label">0 1</text><text x="381" y="233" class="label">1</text><text x="531" y="233" class="label">0</text><text x="695" y="233" class="label">SET</text>
<rect x="79" y="254" width="837" height="47" rx="7" fill="#e5f3e9"/>
<text x="150" y="288" class="label">1 0</text><text x="381" y="288" class="label">0</text><text x="531" y="288" class="label">1</text><text x="695" y="288" class="label">RESET</text>
<rect x="79" y="309" width="837" height="47" rx="7" fill="#e5eff8"/>
<text x="150" y="343" class="label">1 1</text><text x="353" y="343" class="small">anterior</text><text x="494" y="343" class="small">anterior</text><text x="695" y="343" class="label accent">HOLD</text>
<rect x="79" y="364" width="837" height="47" rx="7" fill="#ffebe7"/>
<text x="150" y="398" class="label">0 0</text><text x="381" y="398" class="label">1</text><text x="531" y="398" class="label">1</text><text x="695" y="398" class="small">PROHIBIDA</text>
<text x="501" y="440" text-anchor="middle" class="tiny">Con 00, Q = Q_n = 1; al liberar ambas órdenes, el futuro estado no está garantizado.</text>
''')


cards = []
step_data = [
    ("t0", "11", "Inicio", "0", "#e5eff8"),
    ("t1", "01", "SET", "1", "#e2f3e7"),
    ("t2", "11", "HOLD", "1", "#e2f3e7"),
    ("t3", "10", "RESET", "0", "#e5eff8"),
    ("t4", "11", "HOLD", "0", "#e5eff8"),
]
for idx, (moment, inputs, order, q, color) in enumerate(step_data):
    x = 39 + 191 * idx
    cards.append(f'''
<rect x="{x}" y="161" width="174" height="251" rx="14" fill="{color}" stroke="#a4b9c8" stroke-width="2"/>
<text x="{x + 87}" y="203" text-anchor="middle" class="label">{moment}</text>
<text x="{x + 87}" y="249" text-anchor="middle" class="small">S_n R_n: {inputs}</text>
<text x="{x + 87}" y="292" text-anchor="middle" class="small accent">{order}</text>
<text x="{x + 87}" y="368" text-anchor="middle" style="font-size:63px;font-weight:bold;fill:#17384b">{q}</text>
''')
    if idx < len(step_data) - 1:
        cards.append(f'<path d="M{x + 177},282 H{x + 189}" stroke="#176d92" stroke-width="3" fill="none"/>')
FIGS["c05_fig04_secuencia_memoria"] = wrap("Secuencia de cinco momentos de un latch SR", '''
<text x="38" y="49" class="label">Guardar 1, conservarlo, borrar y volver a conservar 0</text>
<text x="38" y="87" class="small">Mismo control 11 en t0, t2 y t4; diferente Q porque cambia la historia.</text>
<text x="40" y="143" class="small">Paso de estado estable a estado estable, no tiempo de reloj medido</text>
''' + "\n".join(cards) + '''
<text x="502" y="464" text-anchor="middle" class="tiny">En cada tarjeta, el número grande es Q después de asentarse.</text>
''')


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in FIGS.items():
        target_svg = OUT / f"{name}.svg"
        target_png = OUT / f"{name}.png"
        target_svg.write_text(svg, encoding="utf-8")
        subprocess.run(["inkscape", str(target_svg), "--export-type=png",
                        f"--export-filename={target_png}", "--export-width=2000"],
                       check=True)
        print("Figura capítulo 5:", target_png.relative_to(ROOT))


if __name__ == "__main__":
    main()
