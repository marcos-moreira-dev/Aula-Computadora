#!/usr/bin/env python3
"""Dibuja cuatro esquemas didácticos originales de direcciones y buses.

Son funciones lógicas: no representan temporización o montaje certificado.
"""
from pathlib import Path
import subprocess

from generar_figuras_capitulo_01 import ROOT, STYLE


OUT = ROOT / "libro" / "figuras"


def wrap(title: str, contents: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" '
            f'viewBox="0 0 1000 500"><title>{title}</title>'
            f'<rect width="1000" height="500" fill="white"/>{STYLE}{contents}</svg>')


def block(x, y, w, h, fill="#e6f3fa", radius=13):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="#28465b" stroke-width="3"/>')


FIGS = {}

# 01: el índice elige una sola celda; los ocho bits interiores son contenido.
cells = []
for i, (addr, value) in enumerate((('00', '0x12'), ('01', '0xA5'), ('10', '0x3C'), ('11', '0xFF'))):
    y = 112 + i * 74
    chosen = i == 2
    cells.append(block(647, y, 277, 59, '#d9f4df' if chosen else '#f2f6f9', 9))
    cells.append(f'<text x="665" y="{y+37}" class="small">[{addr}]</text>')
    cells.append(f'<text x="826" y="{y+37}" class="label" text-anchor="middle">{value}</text>')
    cells.append(f'<path class="wire" d="M515,{y+29} H647" stroke="{chr(35)}0b865a"/>')
    cells.append(f'<text x="543" y="{y+19}" class="tiny">SEL{i}</text>')
    if chosen:
        cells.append(f'<circle cx="641" cy="{y+29}" r="8" fill="#20935a"/>')
FIGS["c08_fig01_decodificador_dos_bits"] = wrap('Decodificador de dos bits a cuatro posiciones', '''
<text x="36" y="45" class="label">Una dirección selecciona una posición; el dato vive dentro</text>
<text x="39" y="81" class="small">Dirección 10₂ = posición 2. Su contenido actual: 0x3C.</text>
''' + block(248, 157, 260, 220) + '''
<text x="378" y="222" class="label" text-anchor="middle">Decodificador</text>
<text x="378" y="252" class="small" text-anchor="middle">2 entradas → 4 salidas</text>
<text x="379" y="305" class="small" text-anchor="middle">A1 A0 = 10</text>
<path class="wire" d="M69,229 H248 M69,303 H248"/>
<text x="89" y="210" class="label accent">A1 = 1</text>
<text x="89" y="284" class="label accent">A0 = 0</text>
''' + ''.join(cells) + '''
<text x="501" y="470" class="tiny" text-anchor="middle">SEL activas en alto en este modelo; el chip SN74HC138 real usa salidas activas en bajo.</text>
''')

# 02: grupos físicamente diferentes; flechas con sentido explicativo.
FIGS["c08_fig02_buses_separados"] = wrap('Buses separados de dirección, datos y control', '''
<text x="35" y="44" class="label">Aula-8: dirección, dato y control son grupos distintos</text>
<text x="37" y="82" class="small">Las flechas indican función; los retardos reales todavía no están diseñados.</text>
''' + block(50, 151, 242, 242, '#e6f3fa')
    + block(704, 151, 250, 242, '#e2f3e8') + '''
<text x="171" y="219" class="label" text-anchor="middle">CPU Aula-8</text>
<text x="171" y="261" class="small" text-anchor="middle">solicita dirección</text>
<text x="171" y="292" class="small" text-anchor="middle">lee / escribe</text>
<text x="829" y="219" class="label" text-anchor="middle">Memoria</text>
<text x="829" y="260" class="small" text-anchor="middle">seleccionada</text>
<text x="829" y="292" class="small" text-anchor="middle">guarda bytes</text>
<path class="wire" d="M292,187 H703"/>
<path d="M688,177 l15,10 -15,10" fill="none" stroke="#28465b" stroke-width="3"/>
<text x="500" y="168" text-anchor="middle" class="label accent">A15…A0 (16 líneas)</text>
<path class="wire" d="M292,270 H703"/>
<path d="M307,260 l-15,10 15,10 M688,260 l15,10 -15,10" fill="none" stroke="#28465b" stroke-width="3"/>
<text x="500" y="251" text-anchor="middle" class="label accent">D7…D0 (8 líneas)</text>
<path class="wire" d="M292,351 H703"/>
<path d="M688,341 l15,10 -15,10" fill="none" stroke="#28465b" stroke-width="3"/>
<text x="500" y="335" text-anchor="middle" class="small accent">Selección, lectura, escritura</text>
<text x="500" y="436" class="small" text-anchor="middle">Lectura: memoria → CPU. Escritura: CPU → memoria.</text>
<text x="500" y="469" class="tiny" text-anchor="middle">En el hardware, decodificación y control deciden cuál dispositivo puede conducir.</text>
''')

# 03: two independent and direct transaction illustrations.
FIGS["c08_fig03_lectura_escritura"] = wrap('Lectura y escritura abstractas de memoria', '''
<text x="36" y="44" class="label">Misma clase de memoria, diferente dirección del dato</text>
<text x="38" y="77" class="small">El byte contenido y la dirección elegida se representan por separado.</text>
<rect x="32" y="103" width="936" height="160" rx="13" fill="#f2f8fc"/>
<text x="57" y="133" class="label accent">LECTURA · 0x1200</text>
''' + block(62, 153, 226, 80, '#e6f3fa') + block(705, 153, 228, 80, '#e2f3e8') + '''
<text x="175" y="198" class="label" text-anchor="middle">CPU</text>
<text x="819" y="198" class="label" text-anchor="middle">RAM[0x1200]</text>
<path class="wire" d="M705,194 H288"/>
<path d="M303,184 l-15,10 15,10" fill="none" stroke="#28465b" stroke-width="3"/>
<text x="497" y="177" class="label accent" text-anchor="middle">← 0x41</text>
<text x="497" y="220" class="tiny" text-anchor="middle">Memoria conduce; CPU recibe</text>
<rect x="32" y="279" width="936" height="160" rx="13" fill="#fff6e9"/>
<text x="57" y="309" class="label accent">ESCRITURA · 0x1201</text>
''' + block(62, 329, 226, 80, '#e6f3fa') + block(705, 329, 228, 80, '#e2f3e8') + '''
<text x="175" y="376" class="label" text-anchor="middle">CPU</text>
<text x="819" y="376" class="small" text-anchor="middle">RAM[0x1201]</text>
<path class="wire" d="M288,368 H705"/>
<path d="M690,358 l15,10 -15,10" fill="none" stroke="#28465b" stroke-width="3"/>
<text x="497" y="352" class="label accent" text-anchor="middle">0x53 →</text>
<text x="497" y="399" class="tiny" text-anchor="middle">CPU conduce; memoria recibe</text>
<text x="500" y="478" class="tiny" text-anchor="middle">Las lecturas/escrituras se completan solo si se respetan las señales y tiempos válidos.</text>
''')

# 04: Distinguish address bits, data bus and byte banks in a split panel.
FIGS["c08_fig04_aula8_aula16"] = wrap('Anchos de bus Aula-8 y Aula-16', '''
<text x="38" y="44" class="label">Dos arquitecturas: 16 bits para direcciones, distinto bus de datos</text>
<text x="38" y="78" class="small">Aula-16: direcciones por byte; palabra alineada con dos bancos de 8 bits.</text>
<rect x="38" y="103" width="431" height="341" rx="16" fill="#f1f7fb" stroke="#abc6d7" stroke-width="2"/>
<rect x="531" y="103" width="431" height="341" rx="16" fill="#f4f9f3" stroke="#a6cdb7" stroke-width="2"/>
<text x="252" y="144" class="label" text-anchor="middle">Aula-8</text>
<text x="745" y="144" class="label" text-anchor="middle">Aula-16</text>
''' + block(71, 178, 140, 93) + block(298, 178, 141, 93, '#e2f3e8')
    + block(557, 178, 142, 93) + block(818, 178, 122, 93, '#e2f3e8') + '''
<text x="141" y="229" class="label" text-anchor="middle">CPU</text>
<text x="369" y="229" class="label" text-anchor="middle">Memoria</text>
<path class="wire" d="M211,201 H298 M211,248 H298"/>
<text x="254" y="189" class="tiny" text-anchor="middle">A[15:0]</text>
<text x="254" y="285" class="tiny" text-anchor="middle">D[7:0]</text>
<text x="628" y="228" class="label" text-anchor="middle">CPU</text>
<text x="879" y="229" class="small" text-anchor="middle">Bancos</text>
<path class="wire" d="M699,201 H818 M699,248 H818"/>
<text x="759" y="189" class="tiny" text-anchor="middle">A[15:0]</text>
<text x="759" y="285" class="tiny" text-anchor="middle">D[15:0]</text>
<rect x="83" y="324" width="374" height="76" rx="11" fill="white" stroke="#abc6d7"/>
<text x="269" y="353" class="small" text-anchor="middle">Cada transferencia mueve un byte</text>
<text x="269" y="382" class="tiny" text-anchor="middle">bus de datos externo de 8 bits</text>
<rect x="544" y="315" width="405" height="103" rx="11" fill="white" stroke="#a6cdb7"/>
<text x="748" y="340" class="small" text-anchor="middle">Palabra 0x1234 en 0x2000 (par)</text>
<text x="748" y="369" class="small" text-anchor="middle">banco bajo: [0x2000] = 0x34</text>
<text x="748" y="395" class="small" text-anchor="middle">banco alto: [0x2001] = 0x12</text>
<text x="500" y="480" class="tiny" text-anchor="middle">Esquema conceptual; la selección de bancos y temporización requieren diseño posterior.</text>
''')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, contents in FIGS.items():
        svg = OUT / (name + '.svg')
        png = OUT / (name + '.png')
        svg.write_text(contents, encoding='utf-8')
        subprocess.run(['inkscape', str(svg), '--export-type=png',
                        f'--export-filename={png}', '--export-width=2000'], check=True)
        print('Ilustración:', png.relative_to(ROOT))


if __name__ == '__main__':
    main()
