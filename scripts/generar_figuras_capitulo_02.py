#!/usr/bin/env python3
"""Figuras de terminales y estados de un interruptor NPN de baja tensión."""
from pathlib import Path
import subprocess

from generar_figuras_capitulo_01 import ROOT, STYLE, source, led

OUT = ROOT / "libro" / "figuras"


def wrap(body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 1000 500">
<title>{title}</title><rect width="1000" height="500" fill="white"/>{STYLE}
{body}</svg>'''


FIGURES = {}
FIGURES["c02_fig01_bce_pinout"] = wrap('''
<text x="45" y="42" class="label">Tres terminales, tres funciones eléctricas</text>
<text x="250" y="91" class="small" text-anchor="middle">Vista del encapsulado TO-92</text>
<path d="M 171,203 Q 171,110 250,110 Q 329,110 329,203 L329,260 H171 Z" fill="#eaf2f7" stroke="#283c50" stroke-width="4"/>
<text x="250" y="196" class="label" text-anchor="middle">2N3904</text>
<path class="wire" d="M199,260 V342 M250,260 V342 M301,260 V342"/>
<text x="199" y="369" class="label" text-anchor="middle">1 E</text>
<text x="250" y="369" class="label" text-anchor="middle">2 B</text>
<text x="301" y="369" class="label" text-anchor="middle">3 C</text>
<text x="250" y="395" class="tiny" text-anchor="middle">onsemi 2N3904, según su hoja de datos</text>
<rect x="510" y="108" width="402" height="261" fill="#f3f7fa" rx="16"/>
<text x="710" y="145" class="label" text-anchor="middle">Función de cada terminal</text>
<text x="553" y="195" class="small">C  ·  Colector: rama de la carga</text>
<text x="553" y="249" class="small">B  ·  Base: recibe la señal</text>
<text x="553" y="303" class="small">E  ·  Emisor: retorno común</text>
<rect x="80" y="423" width="840" height="55" fill="#fff1dc" rx="9"/>
<text x="500" y="456" class="small" text-anchor="middle">No aplicar este orden de patas a cualquier NPN: comprobar fabricante y vista.</text>
''', "Patillaje del transistor onsemi 2N3904 en encapsulado TO-92")


def loop(state: bool):
    active = state
    title = "Estado 1: la entrada conecta la base a +5 V" if active else "Estado 0: la entrada conecta la base a GND"
    input_name = "IN = +5 V" if active else "IN = 0 V"
    transistor_state = "SATURACIÓN" if active else "CORTE"
    voltage = "I_C ≈ 8,5 mA" if active else "I_C ≈ 0 mA"
    light = led(662,175,257) if active else '''<rect x="608" y="175" width="108" height="82" rx="13" fill="#e1e8ed" stroke="#596a74" stroke-width="3"/>
<text x="662" y="212" class="label" text-anchor="middle">LED</text>
<text x="662" y="237" class="tiny" text-anchor="middle">apagado</text>
<text x="582" y="180" class="tiny">A (+)</text><text x="582" y="278" class="tiny">K (−)</text>'''
    body = f'''
<text x="37" y="41" class="label">{title}</text>
<path class="wire" d="M120,111 V87 H293 M403,87 H662 V175 M662,257 V289 M662,363 V408 H120 V239"/>
{source(120,160)}
<rect class="block" x="293" y="65" width="110" height="44" rx="7"/>
<text x="348" y="94" class="label" text-anchor="middle">330 Ω</text>
{light}
<rect x="609" y="289" width="106" height="74" rx="13" fill="#e8f3fb" stroke="#273746" stroke-width="3"/>
<text x="662" y="317" class="small" font-weight="bold" text-anchor="middle">Q1 NPN</text>
<text x="662" y="342" class="tiny" text-anchor="middle">{transistor_state}</text>
<text x="729" y="303" class="tiny">C</text><text x="729" y="355" class="tiny">E</text>
<text x="584" y="321" class="tiny">B</text>
<circle cx="183" cy="325" r="7" fill="white" stroke="#273746" stroke-width="3"/>
<text x="165" y="289" class="label accent" text-anchor="middle">{input_name}</text>
<path class="wire" d="M190,325 H341 M481,325 H609"/>
<rect class="block" x="341" y="303" width="140" height="44" rx="7"/>
<text x="411" y="331" class="label" text-anchor="middle">4,7 kΩ</text>
<text x="411" y="373" class="tiny" text-anchor="middle">Resistencia de base</text>
<text x="886" y="206" class="label accent" text-anchor="middle">{voltage}</text>
<text x="886" y="232" class="tiny" text-anchor="middle">estimación, no medida</text>
<rect x="75" y="436" width="863" height="49" rx="8" fill="#eaf3f9"/>
<text x="500" y="467" class="small" text-anchor="middle">IN debe conectarse físicamente al raíl indicado, con GND compartido.</text>
'''
    return wrap(body, title)


FIGURES["c02_fig02_npn_encendido"] = loop(True)
FIGURES["c02_fig03_npn_apagado"] = loop(False)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in FIGURES.items():
        src = OUT / (name + ".svg")
        dst = OUT / (name + ".png")
        src.write_text(svg, encoding="utf-8")
        subprocess.run(["inkscape", str(src), "--export-type=png",
                        f"--export-filename={dst}", "--export-width=2000"],
                       check=True, stdout=subprocess.DEVNULL)
        print(f"Figura nueva: {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
