#!/usr/bin/env python3
"""Figuras didácticas originales de interruptores ideales y lógica NAND real."""
from pathlib import Path
import subprocess

from generar_figuras_capitulo_01 import ROOT, STYLE

OUT = ROOT / "libro" / "figuras"


def wrap(body: str, title: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 1000 500">
<title>{title}</title><rect width="1000" height="500" fill="white"/>{STYLE}
{body}</svg>'''


FIGURES = {}

FIGURES["c03_fig01_serie_ideal"] = wrap('''
<text x="50" y="45" class="label">Dos permisos en serie: A Y B</text>
<text x="50" y="81" class="small">Modelo de interruptores ideales; representa AND, no un montaje NPN.</text>
<rect class="block" x="77" y="169" width="144" height="110" rx="12"/>
<text x="149" y="213" text-anchor="middle" class="label">Inicio</text>
<text x="149" y="246" text-anchor="middle" class="small">de la ruta</text>
<path class="wire" d="M221,224 H296 M443,224 H548 M695,224 H776"/>
<rect x="296" y="161" width="147" height="128" rx="12" fill="#e8f5e9" stroke="#336d4c" stroke-width="3"/>
<text x="369" y="204" text-anchor="middle" class="label">A = 1</text>
<text x="369" y="242" text-anchor="middle" class="small">cerrado</text>
<rect x="548" y="161" width="147" height="128" rx="12" fill="#e8f5e9" stroke="#336d4c" stroke-width="3"/>
<text x="622" y="204" text-anchor="middle" class="label">B = 1</text>
<text x="622" y="242" text-anchor="middle" class="small">cerrado</text>
<rect class="block" x="776" y="169" width="150" height="110" rx="12"/>
<text x="851" y="213" text-anchor="middle" class="label">Ruta</text>
<text x="851" y="246" text-anchor="middle" class="small">completa</text>
<path d="M448,326 H551" stroke="#096b91" stroke-width="2" stroke-dasharray="7 7"/>
<text x="500" y="355" text-anchor="middle" class="label accent">Z = A ∧ B = 1</text>
<rect x="75" y="404" width="850" height="72" rx="10" fill="#fff1dc"/>
<text x="500" y="432" text-anchor="middle" class="small">Si A = 0 o B = 0, uno de los interruptores se abre</text>
<text x="500" y="459" text-anchor="middle" class="small">y se interrumpe la ruta: Z = 0.</text>
''', "Modelo ideal de dos permisos AND con interruptores en serie")

FIGURES["c03_fig02_nand_simbolo"] = wrap('''
<text x="51" y="42" class="label">La negación de AND: una puerta NAND</text>
<text x="51" y="77" class="small">El círculo de salida indica que negamos el resultado de AND.</text>
<path class="wire" d="M82,204 H256 M82,293 H256"/>
<text x="115" y="183" class="label accent">A</text>
<text x="115" y="321" class="label accent">B</text>
<path d="M256,157 H349 A90,90 0 0 1 349,337 H256 Z" fill="#e8f3fb" stroke="#283c50" stroke-width="4"/>
<circle cx="456" cy="248" r="16" fill="white" stroke="#283c50" stroke-width="4"/>
<path class="wire" d="M472,248 H545"/>
<text x="515" y="225" class="label accent">Y</text>
<text x="289" y="382" class="small">Y = ¬(A ∧ B)</text>
<rect x="619" y="122" width="330" height="288" rx="12" fill="#f4f8fb"/>
<text x="784" y="158" text-anchor="middle" class="label">Tabla de verdad</text>
<path class="wire" d="M647,185 H920 M647,233 H920 M647,282 H920 M647,331 H920 M647,381 H920"/>
<text x="678" y="218" class="label">A</text>
<text x="777" y="218" class="label">B</text>
<text x="876" y="218" class="label accent">Y</text>
<text x="677" y="267" class="small">0</text><text x="777" y="267" class="small">0</text><text x="875" y="267" class="small">1</text>
<text x="677" y="316" class="small">0</text><text x="777" y="316" class="small">1</text><text x="875" y="316" class="small">1</text>
<text x="677" y="365" class="small">1</text><text x="777" y="365" class="small">0</text><text x="875" y="365" class="small">1</text>
<text x="677" y="402" class="small">1</text><text x="777" y="402" class="small">1</text><text x="875" y="402" class="small">0</text>
''', "Símbolo lógico de NAND y tabla completa")


def pin_label(x: int, y: int, number: int, name: str, left: bool) -> str:
    outside = x - 185 if left else x + 185
    label_x = x - 27 if left else x + 27
    anchor = "end" if left else "start"
    return f'''<path class="wire" d="M{x},{y} H{outside}"/>
<text x="{label_x}" y="{y-9}" text-anchor="{anchor}" class="tiny">{number}</text>
<text x="{outside + (-10 if left else 10)}" y="{y+6}" text-anchor="{anchor}" class="small">{name}</text>'''


FIGURES["c03_fig03_pines_74hct00"] = wrap('''
<text x="48" y="42" class="label">SN74HCT00N: encapsulado PDIP-14</text>
<text x="48" y="77" class="small">Vista superior, muesca orientada arriba (referencia TI).</text>
<rect x="400" y="97" width="200" height="347" rx="18" fill="#eaf2f7" stroke="#283c50" stroke-width="4"/>
<path d="M465,97 A35,35 0 0 0 535,97" stroke="#283c50" stroke-width="4" fill="white"/>
<text x="500" y="255" text-anchor="middle" class="label">74HCT00</text>
<text x="500" y="283" text-anchor="middle" class="small">4 compuertas</text>
<text x="500" y="309" text-anchor="middle" class="small">NAND de 2</text>
<text x="500" y="336" text-anchor="middle" class="small">entradas</text>
''' + "\n".join(pin_label(400, 142 + i * 44, i + 1,
                      ["1A", "1B", "1Y", "2A", "2B", "2Y", "GND"][i], True)
           for i in range(7)) + "\n" + "\n".join(pin_label(600, 142 + i * 44,
                      14 - i, ["VCC", "4B", "4A", "4Y", "3B", "3A", "3Y"][i], False)
           for i in range(7)) + '''
<rect x="82" y="452" width="837" height="36" rx="9" fill="#fff1dc"/>
<text x="500" y="476" class="tiny" text-anchor="middle">Primera NAND: 1A = pin 1, 1B = pin 2, 1Y = pin 3. VCC = 14. GND = 7.</text>
''', "Distribución de terminales del SN74HCT00N PDIP-14, vista superior")

FIGURES["c03_fig04_nand_led"] = wrap('''
<text x="47" y="41" class="label">Una NAND real, un LED activo en nivel bajo</text>
<text x="47" y="72" class="small">Conectar IN A y IN B a +5 V o GND mediante selectores externos.</text>
<path class="wire" d="M130,94 H875"/>
<text x="130" y="115" class="label accent">+5 V CC</text>
<rect x="365" y="186" width="221" height="202" rx="15" fill="#eaf2f7" stroke="#273746" stroke-width="4"/>
<text x="475" y="220" text-anchor="middle" class="label">SN74HCT00</text>
<text x="475" y="253" text-anchor="middle" class="small">Primera NAND</text>
<text x="475" y="291" text-anchor="middle" class="label">Y = ¬(A ∧ B)</text>
<path class="wire" d="M475,94 V186 M475,388 V429 H875"/>
<text x="489" y="160" class="tiny">pin 14 VCC</text>
<text x="490" y="413" class="tiny">pin 7 GND</text>
<text x="877" y="440" text-anchor="end" class="small">GND / 0 V</text>
<path class="wire" d="M133,272 H365 M133,338 H365 M586,338 H726 V282"/>
<text x="133" y="255" class="label accent">IN A</text>
<text x="133" y="323" class="label accent">IN B</text>
<text x="317" y="265" class="tiny">pin 1</text>
<text x="317" y="330" class="tiny">pin 2</text>
<text x="601" y="322" class="tiny">1Y / pin 3</text>
<path class="wire" d="M726,94 V122 M726,167 V200 M726,279 V282"/>
<rect class="block" x="679" y="122" width="94" height="45" rx="8"/>
<text x="726" y="150" text-anchor="middle" class="label">1 kΩ</text>
<rect x="681" y="200" width="90" height="79" rx="13" fill="#fbe2aa" stroke="#ad7200" stroke-width="3"/>
<text x="726" y="228" text-anchor="middle" class="label">LED</text>
<text x="726" y="254" text-anchor="middle" class="tiny">rojo</text>
<text x="781" y="204" class="tiny">A +</text>
<text x="781" y="279" class="tiny">K −</text>
<path class="wire" d="M875,94 V183 M875,211 V429"/>
<path d="M848,183 H902 M848,211 H902" stroke="#283c50" stroke-width="4"/>
<text x="914" y="202" class="tiny">100 nF</text>
<rect x="91" y="449" width="818" height="41" rx="10" fill="#edf6fa"/>
<text x="500" y="475" text-anchor="middle" class="tiny">Y = 0 → LED encendido; Y = 1 → LED apagado. Otras entradas del chip a nivel definido.</text>
''', "Circuito didáctico NAND 74HCT00 con salida LED activa en bajo")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in FIGURES.items():
        src = OUT / (name + ".svg")
        dst = OUT / (name + ".png")
        src.write_text(svg, encoding="utf-8")
        subprocess.run(["inkscape", str(src), "--export-type=png",
                        f"--export-filename={dst}", "--export-width=2000"],
                       check=True, stdout=subprocess.DEVNULL)
        print(f"Figura 3 nueva: {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
