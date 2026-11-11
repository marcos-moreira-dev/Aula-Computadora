#!/usr/bin/env python3
"""Cuatro diagramas funcionales originales C15; no son netlists eléctricos."""

import subprocess

from generar_figuras_capitulo_01 import ROOT
from generar_figuras_capitulo_11 import box, page, text


OUT = ROOT / 'libro' / 'figuras'
FIGURES = {}


def fetch_path():
    stages = [
        ('PC', '0x6000', '#dfeefa'),
        ('MAR', '0x6000', '#e9f1f8'),
        ('RAM', '[6000]=11', '#f6f0dc'),
        ('MDR', '0x11', '#e8f4e9'),
        ('IR', '0x11', '#dfeefa'),
    ]
    content = ''
    for i, (name, value, color) in enumerate(stages):
        xx = 35 + i * 198
        content += box(xx, 164, 170, 112, color)
        content += text(xx + 85, 206, name, 'label', 'middle')
        content += text(xx + 85, 250, value, 'small', 'middle')
        if i != 4:
            content += f'<path class="wire" d="M{xx+170},220 H{xx+198}"/>'
    content += '<path class="wire" d="M912,276 V324 H520 V349"/>'
    content += box(359, 349, 321, 73, '#f8ebd4')
    content += text(520, 383, 'DECODE → ruta LDI', 'label', 'middle')
    content += text(500, 472, 'Una lectura lógica puede requerir varias acciones físicas.', 'small', 'middle')
    return content


FIGURES['c15_fig01_camino_fetch'] = page(
    'Buscar: de PC a IR sin perder el opcode',
    'Las flechas son dependencias funcionales, no pulsos medidos.',
    fetch_path())


FIGURES['c15_fig02_direccion_st'] = page(
    'ST conserva la dirección mientras lee bytes',
    'MDR cambia con cada lectura; ADDR_LO y ADDR_HI recuerdan el destino.',
    box(26, 148, 301, 249, '#e8f2fc')
    + box(349, 148, 301, 249, '#edf4e8')
    + box(672, 148, 301, 249, '#fcf0db')
    + text(176, 184, 'LEER BAJO', 'label', 'middle')
    + text(176, 230, 'RAM[6005] = 00', 'small', 'middle')
    + text(176, 272, 'ADDR_LO = 00', 'label', 'middle')
    + text(176, 328, 'PC pasa a 6006', 'small', 'middle')
    + text(500, 184, 'LEER ALTO', 'label', 'middle')
    + text(500, 230, 'RAM[6006] = 6F', 'small', 'middle')
    + text(500, 272, 'ADDR_HI = 6F', 'label', 'middle')
    + text(500, 328, 'PC pasa a 6007', 'small', 'middle')
    + text(822, 184, 'RECOMPONER', 'label', 'middle')
    + text(822, 230, 'alto : bajo', 'small', 'middle')
    + text(822, 273, 'MAR = 6F00', 'label', 'middle')
    + text(822, 330, 'dirección de datos', 'small', 'middle')
    + text(500, 459, 'Si el byte bajo solo viviera en MDR, se perdería al leer 6F.', 'small', 'middle'))


FIGURES['c15_fig03_preparar_escritura'] = page(
    'Escribir no es reutilizar el último byte leído',
    'Después de leer el alto 6F, ST_STAGE_DATA prepara el 2A antes de WR.',
    box(31, 150, 292, 247, '#fae9e7')
    + box(353, 150, 292, 247, '#f8f0dc')
    + box(675, 150, 292, 247, '#e5f4e7')
    + text(176, 187, 'RIESGO', 'label', 'middle')
    + text(176, 234, 'MAR = 6F00', 'small', 'middle')
    + text(176, 280, 'MDR = 6F', 'label', 'middle')
    + text(176, 339, 'Aún no escribir', 'small', 'middle')
    + text(499, 187, 'PREPARAR', 'label', 'middle')
    + text(499, 234, 'R0 = 2A', 'small', 'middle')
    + text(499, 280, 'MDR ← 2A', 'label', 'middle')
    + text(499, 339, 'ST_STAGE_DATA', 'small', 'middle')
    + text(821, 187, 'ESCRIBIR', 'label', 'middle')
    + text(821, 234, 'MAR = 6F00', 'small', 'middle')
    + text(821, 280, 'RAM[6F00] = 2A', 'label', 'middle')
    + text(821, 339, 'WR solo si el bus es seguro', 'small', 'middle')
    + text(500, 462, 'No hay un circuito ni temporización eléctrica certificados.', 'small', 'middle'))


def operations_grid():
    lines = [
        [('1  R  6000:11', '#e6f2fa'), ('2  R  6001:00', '#e6f2fa'),
         ('3  R  6002:2A', '#e6f2fa')],
        [('4  R  6003:13', '#eaf3e9'), ('5  R  6004:00', '#eaf3e9'),
         ('6  R  6005:00', '#eaf3e9')],
        [('7  R  6006:6F', '#eaf3e9'), ('8  W  6F00:2A', '#f8e3cf'),
         ('9  R  6007:01', '#e5eff9')],
    ]
    content = ''
    for row, cells in enumerate(lines):
        for col, (label, fill) in enumerate(cells):
            x, y = 37 + 321 * col, 137 + row * 112
            content += box(x, y, 288, 82, fill)
            content += text(x + 144, y + 49, label, 'label', 'middle')
    content += text(500, 480, 'R: lectura de RAM   ·   W: escritura de RAM   ·   no son ciclos.',
                    'small', 'middle')
    return content


FIGURES['c15_fig04_transacciones'] = page(
    'Nueve transacciones externas, tres instrucciones',
    'LDI: 3 lecturas.  ST: 4 lecturas y 1 escritura.  HALT: 1 lectura.',
    operations_grid())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in FIGURES.items():
        svg = OUT / f'{name}.svg'
        png = OUT / f'{name}.png'
        svg.write_text(src, encoding='utf-8')
        subprocess.run(['inkscape', str(svg), '--export-type=png',
                        f'--export-filename={png}', '--export-width=2000'], check=True)
        print('Figura', png.relative_to(ROOT))


if __name__ == '__main__':
    main()
