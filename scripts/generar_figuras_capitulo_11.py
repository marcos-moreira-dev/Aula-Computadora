#!/usr/bin/env python3
"""Cuatro diagramas funcionales, SVG fuente y PNG para el capítulo 11."""
import subprocess
from generar_figuras_capitulo_01 import ROOT, STYLE

OUT = ROOT / 'libro' / 'figuras'


def box(x, y, w, h, fill='#e8f2fa'):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" '
            f'fill="{fill}" stroke="#36556b" stroke-width="2.5"/>')


def text(x, y, value, cls='small', anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" class="{cls}"{a}>{value}</text>'


def page(title, detail, content):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" '
            f'viewBox="0 0 1000 500"><title>{title}</title>'
            '<rect width="1000" height="500" fill="white"/>' + STYLE
            + text(35, 43, title, 'label') + text(35, 76, detail)
            + content + '</svg>')


FIGS = {}

FIGS['c11_fig01_resta_complemento_dos'] = page(
    'Un mismo sumador hace ADD o SUB',
    'SUB=0: sumar A+B.  SUB=1: sumar A+NOT(B)+1.',
    box(54, 185, 170, 116, '#f2f7fa') + box(310, 185, 190, 116, '#e6f2ed')
    + box(594, 185, 187, 116, '#e6f2ed') + box(823, 187, 144, 113, '#fff1d9')
    + text(139, 223, 'B [7:0]', 'label', 'middle')
    + text(139, 258, '8 señales', 'small', 'middle')
    + text(405, 222, 'XOR', 'label', 'middle')
    + text(405, 258, 'B o NOT B', 'small', 'middle')
    + text(688, 222, 'Sumador', 'label', 'middle')
    + text(688, 260, 'A + B\' + Cin', 'small', 'middle')
    + text(894, 224, 'S [7:0]', 'label', 'middle')
    + text(894, 258, 'resultado', 'small', 'middle')
    + '<path class="wire" d="M224,244 H310 M500,244 H594 M781,244 H823"/>'
    + '<path class="wire" d="M688,122 V185"/>'
    + text(702, 143, 'A [7:0]', 'small')
    + '<path class="wire" d="M405,391 V301 M592,391 V301"/>'
    + text(405, 420, 'SUB a XOR', 'small', 'middle')
    + text(605, 420, 'Cin=SUB', 'small', 'middle')
    + '<path class="wire" d="M688,301 V348 H888 V375"/>'
    + text(879, 405, 'Cout interno', 'small', 'middle')
    + text(500, 478, 'En SUB: bandera C de préstamo = 1 - Cout interno.', 'small', 'middle'))


def logic_rows():
    rows = [('A = 0x5A', '01011010'), ('B = 0x3C', '00111100'),
            ('A AND B', '00011000'), ('A OR B', '01111110'),
            ('A XOR B', '01100110'), ('NOT A', '10100101')]
    content = ''
    for i, (name, bits) in enumerate(rows):
        yy = 140 + i * 53
        if i >= 2:
            content += f'<rect x="32" y="{yy-30}" width="932" height="44" rx="9" fill="{("#f3f8fc" if i%2==0 else "#edf6ef")}"/>'
        content += text(65, yy, name, 'label')
        for j, bit in enumerate(bits):
            x = 419 + j * 70
            content += box(x-23, yy-33, 46, 46, '#e1f4e6' if bit == '1' else '#fafafa')
            content += text(x, yy, bit, 'label', 'middle')
    return content


FIGS['c11_fig03_logica_por_bits'] = page(
    'Operaciones lógicas: cada columna es independiente',
    'Los unos se sombrean en verde. Ninguna operación transmite un acarreo al vecino.',
    logic_rows() + text(500, 482, 'NOT se aplica solamente a A; siempre se invierten exactamente ocho bits.', 'small', 'middle'))

FIGS['c11_fig04_comparaciones_banderas'] = page(
    'Un patrón, dos interpretaciones',
    'La resta interna es FF - 01 = FE. Banderas: C préstamo=0, Z=0, N=1, V=0.',
    box(40, 125, 442, 275, '#eaf4fa') + box(518, 125, 442, 275, '#eef7eb')
    + text(261, 171, 'SIN SIGNO', 'label', 'middle')
    + text(261, 222, '0xFF = 255', 'label', 'middle')
    + text(261, 262, '0x01 = 1', 'label', 'middle')
    + text(261, 305, 'C=0 y Z=0', 'small', 'middle')
    + text(261, 356, '255 &gt; 1', 'label', 'middle')
    + text(739, 171, 'CON SIGNO', 'label', 'middle')
    + text(739, 222, '0xFF = -1', 'label', 'middle')
    + text(739, 262, '0x01 = +1', 'label', 'middle')
    + text(739, 305, 'N XOR V = 1', 'small', 'middle')
    + text(739, 356, '-1 &lt; +1', 'label', 'middle')
    + text(500, 451, 'Las entradas, el circuito y las banderas no cambiaron.', 'small', 'middle')
    + text(500, 479, 'Solo cambia la regla con la que el programa compara los patrones.', 'small', 'middle'))

FIGS['c11_fig02_alu_selector'] = page(
    'ALU funcional de ocho bits',
    'Las rutas calculan; un selector elige una sola salida. El registro captura después.',
    box(53, 165, 165, 176, '#f4f7fa')
    + box(301, 137, 230, 104, '#e6f2ed')
    + box(301, 279, 230, 104, '#e6f2ed')
    + box(613, 184, 157, 158, '#fff1d9')
    + box(818, 202, 145, 122, '#e5f3fa')
    + text(135, 209, 'Entradas', 'label', 'middle')
    + text(135, 264, 'A y B', 'label', 'middle')
    + text(416, 175, 'Aritmética', 'label', 'middle')
    + text(416, 208, 'ADD / SUB', 'small', 'middle')
    + text(416, 316, 'Lógica', 'label', 'middle')
    + text(416, 354, 'AND OR XOR NOT', 'small', 'middle')
    + text(691, 241, 'MUX', 'label', 'middle')
    + text(691, 271, 'operación', 'small', 'middle')
    + text(691, 301, 'elegida', 'small', 'middle')
    + text(890, 246, 'S [7:0]', 'label', 'middle')
    + text(890, 279, '8 bits', 'small', 'middle')
    + '<path class="wire" d="M218,216 H258 V191 H301 M258,216 V329 H301"/>'
    + '<path class="wire" d="M531,191 H574 V227 H613 M531,329 H574 V303 H613"/>'
    + '<path class="wire" d="M770,263 H818 M693,113 V184"/>'
    + text(705, 116, 'selector', 'small')
    + text(510, 436, 'Z, N, C y V: lógica de flags separada; política para operaciones lógicas pendiente.', 'small', 'middle')
    + text(510, 476, 'Esquema conceptual: no define conexiones ni reloj reales.', 'tiny', 'middle'))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, source in FIGS.items():
        path = OUT / f'{name}.svg'
        png = OUT / f'{name}.png'
        path.write_text(source, encoding='utf-8')
        subprocess.run(['inkscape', str(path), '--export-type=png',
                        f'--export-filename={png}', '--export-width=2000'], check=True)
        print('Figura', png.relative_to(ROOT))


if __name__ == '__main__':
    main()
