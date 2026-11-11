#!/usr/bin/env python3
"""Produce cuatro figuras vectoriales originales de compuertas combinacionales."""
from pathlib import Path
import subprocess

from generar_figuras_capitulo_01 import ROOT, STYLE


OUT = ROOT / "libro" / "figuras"


def wrap(body: str, title: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 1000 500">
<title>{title}</title><rect width="1000" height="500" fill="white"/>{STYLE}
{body}</svg>'''


def or_gate(x: int, y: int, negate: bool) -> str:
    """Símbolo aproximado de OR, con burbuja de negación opcional."""
    bubble = f'<circle cx="{x + 171}" cy="{y + 56}" r="13" fill="white" stroke="#273746" stroke-width="4"/>' if negate else ""
    end = x + 184 if negate else x + 160
    return f'''<path d="M{x + 53},{y} C{x + 101},{y + 4} {x + 128},{y + 27} {x + 158},{y + 56}
 C{x + 128},{y + 86} {x + 100},{y + 109} {x + 53},{y + 112}
 C{x + 79},{y + 82} {x + 79},{y + 30} {x + 53},{y} Z" fill="#e7f3fa" stroke="#273746" stroke-width="4"/>
<path class="wire" d="M{x},{y + 36} H{x + 66} M{x},{y + 80} H{x + 66} M{end},{y + 56} H{end + 44}"/>{bubble}'''


def nand_block(x: int, y: int, name: str) -> str:
    return f'''<rect x="{x}" y="{y}" width="112" height="82" rx="12" fill="#e7f3fa" stroke="#273746" stroke-width="3"/>
<text x="{x + 56}" y="{y + 33}" text-anchor="middle" class="label">{name}</text>
<text x="{x + 56}" y="{y + 61}" text-anchor="middle" class="small">NAND</text>'''


FIGS: dict[str, str] = {}

FIGS["c04_fig01_or_nor"] = wrap('''
<text x="46" y="43" class="label">OR frente a NOR: el círculo niega la salida</text>
<text x="46" y="79" class="small">OR = al menos una entrada; NOR = ninguna entrada.</text>
''' + or_gate(86, 146, False) + or_gate(86, 306, True) + '''
<text x="49" y="179" class="small">A</text><text x="49" y="222" class="small">B</text>
<text x="49" y="339" class="small">A</text><text x="49" y="382" class="small">B</text>
<text x="301" y="207" class="label accent">OR</text>
<text x="324" y="367" class="label accent">NOR</text>
<rect x="477" y="112" width="477" height="340" rx="15" fill="#f3f8fb"/>
<text x="716" y="151" text-anchor="middle" class="label">Tabla de verdad</text>
<path class="wire" d="M505,173 H926 M505,222 H926 M505,272 H926 M505,322 H926 M505,372 H926"/>
<text x="541" y="207" class="label">A</text><text x="634" y="207" class="label">B</text>
<text x="730" y="207" class="label accent">OR</text>
<text x="848" y="207" class="label accent">NOR</text>
<text x="542" y="257" class="small">0</text><text x="636" y="257" class="small">0</text><text x="735" y="257" class="small">0</text><text x="855" y="257" class="small">1</text>
<text x="542" y="307" class="small">0</text><text x="636" y="307" class="small">1</text><text x="735" y="307" class="small">1</text><text x="855" y="307" class="small">0</text>
<text x="542" y="357" class="small">1</text><text x="636" y="357" class="small">0</text><text x="735" y="357" class="small">1</text><text x="855" y="357" class="small">0</text>
<text x="542" y="407" class="small">1</text><text x="636" y="407" class="small">1</text><text x="735" y="407" class="small">1</text><text x="855" y="407" class="small">0</text>
<text x="716" y="439" text-anchor="middle" class="tiny">NOR = ¬OR en las cuatro combinaciones.</text>
''', "Símbolos lógicos y tablas OR y NOR con salidas complementarias")

FIGS["c04_fig02_xor_discrepancia"] = wrap('''
<text x="46" y="44" class="label">XOR solo vale 1 cuando A y B son diferentes</text>
<text x="46" y="82" class="small">La disyunción exclusiva no se activa en la fila 11.</text>
''' + or_gate(100, 174, False) + '''
<path d="M137,171 C164,207 164,256 137,291" fill="none" stroke="#096b91" stroke-width="4"/>
<text x="65" y="210" class="label accent">A</text><text x="65" y="256" class="label accent">B</text>
<text x="322" y="236" class="label accent">D = A ⊕ B</text>
<rect x="493" y="124" width="455" height="330" rx="15" fill="#f4f8fb"/>
<text x="721" y="160" text-anchor="middle" class="label">Tabla de discrepancia</text>
<path class="wire" d="M519,176 H927 M519,223 H927 M519,274 H927 M519,325 H927 M519,376 H927"/>
<text x="570" y="209" class="label">A</text><text x="695" y="209" class="label">B</text>
<text x="830" y="209" class="label accent">D</text>
<text x="570" y="260" class="small">0</text><text x="695" y="260" class="small">0</text><text x="836" y="260" class="small">0</text>
<rect x="529" y="279" width="389" height="40" rx="5" fill="#e5f4e8"/>
<text x="570" y="310" class="small">0</text><text x="695" y="310" class="small">1</text><text x="836" y="310" class="label accent">1</text>
<rect x="529" y="330" width="389" height="40" rx="5" fill="#e5f4e8"/>
<text x="570" y="361" class="small">1</text><text x="695" y="361" class="small">0</text><text x="836" y="361" class="label accent">1</text>
<text x="570" y="411" class="small">1</text><text x="695" y="411" class="small">1</text><text x="836" y="411" class="small">0</text>
<text x="721" y="442" class="tiny" text-anchor="middle">Filas activas: 01 y 10.</text>
''', "Símbolo XOR y tabla de verdad que destaca las diferencias")

FIGS["c04_fig03_xor_cuatro_nand"] = wrap('''
<text x="40" y="44" class="label">Construir XOR a partir de cuatro NAND</text>
<text x="40" y="79" class="small">Sigue las señales intermedias N1 → N2 y N3 → D.</text>
''' + nand_block(225, 189, "N1") + nand_block(530, 145, "N2") + nand_block(530, 286, "N3") + nand_block(752, 224, "N4") + '''
<path class="wire" d="M89,130 H483 V169 H530 M175,130 V209 H225"/>
<path class="wire" d="M89,386 H485 V342 H530 M203,386 V250 H225"/>
<text x="48" y="136" class="label accent">A</text><text x="48" y="392" class="label accent">B</text>
<path class="wire" d="M337,230 H423 V196 H530 M423,230 V307 H530"/>
<circle cx="423" cy="230" r="6" class="node"/>
<text x="370" y="220" class="tiny accent">N1</text>
<path class="wire" d="M642,186 H695 V251 H752 M642,327 H695 V297 H752"/>
<path class="wire" d="M864,265 H940"/>
<text x="890" y="248" class="label accent">D</text>
<rect x="59" y="427" width="883" height="56" rx="11" fill="#edf6fa"/>
<text x="500" y="449" text-anchor="middle" class="small">N1 = NAND(A,B); N2 = NAND(A,N1); N3 = NAND(B,N1).</text>
<text x="500" y="473" text-anchor="middle" class="small">D = NAND(N2,N3) = A ⊕ B.</text>
''', "Conexiones funcionales de cuatro NAND para realizar XOR")

FIGS["c04_fig04_simplificacion"] = wrap('''
<text x="44" y="43" class="label">Simplificar sin cambiar la tabla de verdad</text>
<text x="44" y="79" class="small">La variable B no cambia la salida si se consideran sus dos posibilidades.</text>
<rect x="62" y="131" width="441" height="232" rx="17" fill="#f2f7fb" stroke="#273746" stroke-width="3"/>
<text x="282" y="174" text-anchor="middle" class="label">Función inicial</text>
<rect x="100" y="215" width="165" height="66" rx="10" fill="#e5edf6" stroke="#273746" stroke-width="2"/>
<text x="183" y="255" text-anchor="middle" class="label">A ∧ B</text>
<rect x="303" y="215" width="165" height="66" rx="10" fill="#e5edf6" stroke="#273746" stroke-width="2"/>
<text x="385" y="255" text-anchor="middle" class="label">A ∧ ¬B</text>
<path class="wire" d="M183,281 V300 H282 M385,281 V300 H282 V320"/>
<text x="282" y="347" text-anchor="middle" class="small">OR entre ambas ramas</text>
<text x="540" y="255" text-anchor="middle" class="label accent">=</text>
<rect x="572" y="131" width="366" height="232" rx="17" fill="#e8f5e9" stroke="#336d4c" stroke-width="3"/>
<text x="755" y="174" text-anchor="middle" class="label">Función simplificada</text>
<text x="755" y="264" text-anchor="middle" style="font-size:76px;font-weight:bold;fill:#096b91">A</text>
<rect x="107" y="389" width="785" height="75" rx="10" fill="#fff1dc"/>
<text x="500" y="419" text-anchor="middle" class="small">F = (A ∧ B) ∨ (A ∧ ¬B) = A</text>
<text x="500" y="445" text-anchor="middle" class="small">Para AB = 00, 01, 10, 11 ambas producen: 0, 0, 1, 1.</text>
''', "Simplificación booleana de dos ramas con variable complementaria")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in FIGS.items():
        source = OUT / f"{name}.svg"
        target = OUT / f"{name}.png"
        source.write_text(svg, encoding="utf-8")
        subprocess.run(["inkscape", str(source), "--export-type=png",
                        f"--export-filename={target}", "--export-width=2000"],
                       check=True)
        print("Figura capítulo 4:", target.relative_to(ROOT))


if __name__ == "__main__":
    main()
