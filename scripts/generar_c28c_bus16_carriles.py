#!/usr/bin/env python3
"""Dibuja y comprueba las 16 líneas de datos de Aula-16 (modelo lógico).

Una línea por bit; no es un esquema de pines ni una placa construida.
"""

import re
import shutil
import subprocess
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'libro' / 'figuras'
STEM = 'c28c_aula16_dieciséis_carriles'


def make_svg():
    elements = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1200" viewBox="0 0 2000 1200">',
        '<title>Los 16 conductores de datos de Aula-16: dos bancos RAM de ocho bits</title>',
        '<rect width="2000" height="1200" fill="#fbfcfd"/>',
        '<text x="75" y="84" fill="#1d3446" font-family="DejaVu Sans" font-size="55" font-weight="bold">Un bus de 16 bits tiene 16 conductores</text>',
        '<text x="75" y="140" fill="#43606d" font-family="DejaVu Sans" font-size="27">Cada línea D15…D0 conecta el dato de CPU con un carril de memoria, no es una sola flecha.</text>',
        '<rect x="65" y="220" width="365" height="815" rx="20" fill="#e5edf5" stroke="#54738a" stroke-width="3"/>',
        '<text x="245" y="267" text-anchor="middle" fill="#1d3446" font-family="DejaVu Sans" font-size="29" font-weight="bold">CPU Aula-16</text>',
        '<text x="245" y="304" text-anchor="middle" fill="#1d3446" font-family="DejaVu Sans" font-size="22">D15…D0 · bidireccional</text>',
        '<rect x="1522" y="250" width="414" height="389" rx="17" fill="#e6f1fc" stroke="#447ca6" stroke-width="3"/>',
        '<rect x="1522" y="645" width="414" height="390" rx="17" fill="#e7f5ee" stroke="#348368" stroke-width="3"/>',
        '<text x="1725" y="303" text-anchor="middle" fill="#1b587e" font-family="DejaVu Sans" font-size="27" font-weight="bold">Banco alto · 8 bits</text>',
        '<text x="1725" y="698" text-anchor="middle" fill="#206b52" font-family="DejaVu Sans" font-size="27" font-weight="bold">Banco bajo · 8 bits</text>',
        '<text x="475" y="205" fill="#46606d" font-family="DejaVu Sans" font-size="23">Cada renglón representa una línea independiente</text>',
    ]

    # El sombreado diferencia carriles sin convertirlos en un cable combinado.
    elements += [
        '<rect x="450" y="328" width="1050" height="298" rx="15" fill="#f1f7fd"/>',
        '<rect x="450" y="724" width="1050" height="297" rx="15" fill="#f1faf5"/>',
    ]

    assignments = []
    for n in range(16):
        high = n >= 8
        rank = 15 - n if high else 7 - n
        # Alto de D15 a D8, bajo de D7 a D0.
        y = (353 if high else 748) + 36 * rank
        color = '#2d7499' if high else '#318264'
        elements.append(
            f'<line id="data-{n}" x1="430" y1="{y}" x2="1522" y2="{y}" '
            f'stroke="{color}" stroke-width="3.2"/>'
        )
        elements.append(f'<circle cx="430" cy="{y}" r="4.5" fill="{color}"/>')
        elements.append(f'<circle cx="1522" cy="{y}" r="4.5" fill="{color}"/>')
        elements.append(
            f'<text x="400" y="{y - 9}" text-anchor="end" fill="{color}" '
            f'font-family="DejaVu Sans Mono" font-size="22" font-weight="bold">D{n}</text>'
        )
        elements.append(
            f'<text x="895" y="{y - 9}" text-anchor="middle" fill="{color}" '
            f'font-family="DejaVu Sans Mono" font-size="22">D{n}</text>'
        )
        elements.append(
            f'<text x="1550" y="{y - 9}" fill="{color}" '
            f'font-family="DejaVu Sans Mono" font-size="20">D{n}</text>'
        )
        assignments.append((n, 'alto' if high else 'bajo', y))

    elements += [
        '<rect x="70" y="1063" width="1860" height="106" rx="14" fill="#e9f0f5"/>',
        '<text x="100" y="1104" fill="#233b4b" font-family="DejaVu Sans" font-size="25" font-weight="bold">RAM de 32 KiB: A14…A1 → fila · A15 → selección de región · A0 → carril de byte</text>',
        '<text x="100" y="1144" fill="#233b4b" font-family="DejaVu Sans" font-size="24">En dirección par, una palabra usa los 16 bits: 0x2000→0x34 (bajo), 0x2001→0x12 (alto) = 0x1234.</text>',
        '</svg>',
    ]
    svg = '\n'.join(elements)
    return svg, assignments


def verify_svg(svg, assignments):
    root = ElementTree.fromstring(svg)
    ns = {'s': 'http://www.w3.org/2000/svg'}
    all_lanes = root.findall(".//s:line", ns)
    assert len(all_lanes) == 16, len(all_lanes)
    assert sorted(int(el.attrib['id'].split('-')[1]) for el in all_lanes) == list(range(16))
    assert len(set(n for n, _, _ in assignments)) == 16
    assert len(set(y for _, _, y in assignments)) == 16
    assert all((n >= 8) == (bank == 'alto') for n, bank, _ in assignments)
    assert all(float(x.attrib['x1']) == 430 and float(x.attrib['x2']) == 1522 for x in all_lanes)
    assert len(re.findall(r'id="data-\d+"', svg)) == 16


def main():
    svg, assignments = make_svg()
    verify_svg(svg, assignments)
    OUT.mkdir(parents=True, exist_ok=True)
    svg_path = OUT / (STEM + '.svg')
    png_path = OUT / (STEM + '.png')
    svg_path.write_text(svg, encoding='utf-8')
    ink = shutil.which('inkscape')
    if ink is None:
        raise SystemExit('Inkscape necesario para exportar PNG; SVG ya generado')
    subprocess.run([ink, str(svg_path), '--export-type=png',
                    f'--export-filename={png_path}', '--export-width=2000'],
                   check=True, capture_output=True, text=True)
    print(f'AULA16 C28-C: {len(assignments)} carriles únicos y asignaciones de banco correctas')
    print(f'SVG: {svg_path}\nPNG: {png_path}')


if __name__ == '__main__':
    main()
