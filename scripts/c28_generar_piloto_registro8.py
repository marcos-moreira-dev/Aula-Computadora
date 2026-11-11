#!/usr/bin/env python3
"""Genera vistas SVG reproducibles del contrato de registro8 C28-A.

Las vistas proceden del mismo JSON que verifica el modelo. Son esquema de
funciones logicas, no huellas de PCB, patas reales ni netlist de KiCad.
"""
import json
import shutil
import subprocess
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'c28_a' / 'piloto_registro8'

INK = '#203444'
BLUE = '#276486'
ORANGE = '#a76c1a'
GREEN = '#237c59'


class Lienzo:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.partes = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            '<defs><marker id="punta" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" fill="#276486"/></marker></defs>',
            '<style>text{font-family:DejaVu Sans, sans-serif;fill:#203444} .cable{fill:none;stroke:#203444;stroke-width:3;stroke-linejoin:round;stroke-linecap:round} .señal{fill:none;stroke:#276486;stroke-width:3;stroke-linecap:round} .fin{font-size:14px;fill:#576a78} .base{font-size:19px;font-weight:600} .cab{font-size:30px;font-weight:700} .sub{font-size:17px;fill:#506777}</style>',
            '<rect width="100%" height="100%" fill="#ffffff"/>',
        ]

    def rect(self, x, y, w, h, fill='#eaf2f7', stroke=INK, rx=10, sw=2):
        self.partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def line(self, points, color=INK, width=3, arrow=False):
        xy = ' '.join(f'{x},{y}' for x, y in points)
        attr = ' marker-end="url(#punta)"' if arrow else ''
        self.partes.append(f'<polyline points="{xy}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{attr}/>')

    def txt(self, x, y, value, size=18, anchor='middle', color=INK, weight='normal'):
        self.partes.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(str(value))}</text>')

    def polygon(self, points, fill='#f9e8c6', stroke=INK):
        xy = ' '.join(f'{x},{y}' for x, y in points)
        self.partes.append(f'<polygon points="{xy}" fill="{fill}" stroke="{stroke}" stroke-width="3" stroke-linejoin="round"/>')

    def dot(self, x, y):
        self.partes.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{INK}"/>')

    def burbuja_activa_baja(self, x, y):
        self.partes.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#ffffff" stroke="{BLUE}" stroke-width="2.5"/>')

    def guardar(self, path):
        self.partes.append('</svg>')
        path.write_text('\n'.join(self.partes) + '\n', encoding='utf-8')


def celda(contract):
    l = Lienzo(1200, 690)
    l.txt(42, 56, 'Una celda del registro: guardar no es conducir', 30, 'start', weight='bold')
    l.txt(43, 89, 'El diseño de Aula-8 repite esta misma celda ocho veces.', 18, 'start', '#506777')

    # Ruta de datos, esquema de MUX funcional (el cuerpo trapezoidal sigue
    # siendo abstraccion de una red de puertas, no su conexion transistor a transistor).
    l.line([(92, 235), (331, 235)])
    l.txt(94, 213, 'IN_i', 20, 'start', BLUE, 'bold')
    l.polygon([(331, 205), (473, 229), (473, 307), (331, 326)])
    l.txt(401, 261, 'MUX', 22, weight='bold')
    l.txt(401, 287, '2:1', 18)
    l.line([(399, 153), (399, 216)], BLUE)
    l.txt(399, 139, 'LOAD', 18, color=BLUE, weight='bold')
    l.txt(344, 226, '1', 15, 'start')
    l.txt(344, 306, '0', 15, 'start')

    l.line([(473, 269), (600, 269)])
    l.txt(538, 253, 'D_i', 17, color=BLUE)

    # Flip-flop: flanco de subida representado por triangulo de reloj.
    l.rect(600, 215, 190, 135, '#e3f2e9', GREEN, 7, 3)
    l.txt(696, 265, 'FF D', 27, weight='bold')
    l.txt(696, 297, '1 bit', 18)
    l.txt(611, 284, 'D', 17, 'start')
    l.txt(776, 284, 'Q', 17, 'end')
    l.line([(695, 151), (695, 214)], BLUE)
    l.txt(695, 137, 'CLK ↑', 18, color=BLUE, weight='bold')
    l.polygon([(684, 215), (706, 215), (695, 233)], fill='#ffffff', stroke=BLUE)

    # Q no se pierde al inhibir el buffer; tambien alimenta al MUX.
    l.line([(790, 269), (929, 269)])
    l.txt(825, 251, 'Q_i', 18, color=GREEN)
    l.line([(825, 269), (825, 446), (268, 446), (268, 299), (331, 299)])
    l.dot(825, 269)
    l.txt(538, 431, 'Realimentación: LOAD = 0 conserva Q_i', 16, color=GREEN)

    l.polygon([(929, 223), (929, 315), (1014, 269)], fill='#e6eff8', stroke=BLUE)
    l.txt(962, 280, '3E', 18, color=BLUE, weight='bold')
    l.line([(975, 152), (975, 227)], BLUE)
    l.burbuja_activa_baja(975, 234)
    l.txt(975, 139, 'OE_n', 18, color=BLUE, weight='bold')
    l.line([(1014, 269), (1122, 269)], BLUE, 4)
    l.txt(1122, 242, 'BUS_i', 20, 'end', BLUE, 'bold')

    l.rect(50, 505, 1100, 109, '#f4f7f8', '#cbd9df', 13, 1)
    l.txt(80, 540, 'Al flanco ↑: LOAD=1 → Q_i toma IN_i; LOAD=0 → Q_i se conserva.', 19, 'start')
    l.txt(80, 572, 'Entre flancos: Q_i no cambia. OE_n=0 conduce Q_i; OE_n=1 libera el bus (Z).', 19, 'start')
    l.txt(49, 657, 'Modelo lógico; no especifica patas reales, retardo de propagación, voltaje ni estado al encender.', 16, 'start', '#506777')
    l.guardar(OUT / 'c28a_registro8_celda.svg')


def ocho_carriles(contract):
    l = Lienzo(1200, 765)
    l.txt(42, 55, 'Registro R0 de Aula-8: ocho caminos de un bit', 30, 'start', weight='bold')
    l.txt(42, 87, 'Cada camino ejecuta la misma lógica; el conjunto forma un byte.', 18, 'start', '#506777')
    l.rect(45, 108, 1110, 51, '#f3f7f8', '#d2dfe5', 9, 1)
    l.txt(66, 140, 'Señales compartidas:', 17, 'start', weight='bold')
    l.txt(464, 140, 'LOAD (selección)', 16, color=ORANGE)
    l.txt(729, 140, 'CLK ↑ (captura)', 16, color=GREEN)
    l.txt(1005, 140, 'OE_n (triestado)', 16, color=BLUE)
    for linea, bit in enumerate(range(7, -1, -1)):
        y = 199 + linea * 59
        if linea % 2:
            l.rect(43, y - 23, 1104, 48, '#f8fafb', '#f8fafb', 2, 0)
        l.txt(64, y + 7, f'b{bit}', 18, 'start', weight='bold')
        l.txt(126, y + 7, f'IN{bit}', 16, color=BLUE)
        l.line([(159, y), (248, y)])
        l.polygon([(248, y-19), (349, y-12), (349, y+13), (248, y+20)], fill='#faedd9', stroke=ORANGE)
        l.txt(299, y+6, 'MUX', 14, color=ORANGE, weight='bold')
        l.line([(349, y), (434, y)])
        l.rect(434, y-22, 122, 44, '#e5f3ea', GREEN, 6, 2)
        l.txt(495, y + 6, 'DFF ↑', 16, color=GREEN, weight='bold')
        l.line([(556, y), (718, y)])
        l.polygon([(718, y-21), (718, y+21), (768, y)], fill='#e6eff8', stroke=BLUE)
        l.txt(736, y+5, '3E', 12, color=BLUE, weight='bold')
        l.line([(768, y), (1000, y)], BLUE, 3)
        l.txt(1032, y+7, f'BUS{bit}', 16, color=BLUE)
    l.line([(1098, 177), (1118, 177), (1118, 642), (1098, 642)], BLUE, 4)
    l.txt(1124, 661, '8 líneas', 17, 'end', BLUE, 'bold')
    l.rect(48, 678, 1096, 58, '#f3f7f9', '#d3e0e8', 8, 1)
    l.txt(68, 704, 'MUX recibe IN_i y el retorno Q_i; CLK, LOAD y OE_n se distribuyen a las ocho celdas.', 16, 'start')
    l.txt(68, 725, 'Los nombres representan conexiones eléctricas lógicas: aún faltan circuitos de interfaz y arbitraje de bus.', 13, 'start', '#506777')
    l.guardar(OUT / 'c28a_registro8_ocho_carriles.svg')


def main():
    c = json.loads((OUT / 'registro8_contrato.json').read_text(encoding='utf-8'))
    assert c['anchura_bits'] == c['celdas'] == 8
    assert [e['tipo'] for e in c['elementos_por_celda']] == [
        'multiplexor_2_a_1', 'flip_flop_D', 'buffer_tres_estados']
    celda(c)
    ocho_carriles(c)
    if not shutil.which('inkscape'):
        print('SVG guardados; PNG no generados (Inkscape no disponible).')
        return
    for svg in sorted(OUT.glob('c28a_registro8_*.svg')):
        png = svg.with_suffix('.png')
        subprocess.run(['inkscape', str(svg), '--export-type=png',
                        f'--export-filename={png}', '--export-width=1800'],
                       check=True, capture_output=True)
        print(f'Generado {png.name}')


if __name__ == '__main__':
    main()
