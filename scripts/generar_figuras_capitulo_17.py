#!/usr/bin/env python3
"""Cuatro esquemas didácticos de reset, mapa, ROM pública y monitor."""

import subprocess
from generar_figuras_capitulo_01 import ROOT
from generar_figuras_capitulo_11 import box, page, text

OUT = ROOT / 'libro' / 'figuras'
FIGS = {}


def reset_cards():
    cards = [('RESET', 'estado definido', '#e8f2fa'),
             ('ROM FFFC', 'byte bajo: 00', '#f8f0dc'),
             ('ROM FFFD', 'byte alto: E0', '#f8f0dc'),
             ('PC = E000', 'inicio firmware', '#e9f5e9')]
    out = ''
    for i, (title, note, fill) in enumerate(cards):
        x = 22 + i * 251
        out += box(x, 171, 224, 168, fill)
        out += text(x + 112, 228, title, 'label', 'middle')
        out += text(x + 112, 286, note, 'small', 'middle')
        if i < 3:
            out += f'<path class="wire" d="M{x+224},254 H{x+251}"/>'
    out += text(500, 420, 'Vector en ROM de firmware ≠ micro-ROM de la unidad de control.',
                'small', 'middle')
    return out


FIGS['c17_fig01_vector_reset'] = page(
    'Reset no ejecuta bytes aleatorios de RAM',
    'La dirección E000 depende de un vector 00 E0 grabado previamente.',
    reset_cards())


def map_rows():
    ranges = [('E000–FFFF', 'EEPROM 8 KiB', '#e4f2e6'),
              ('C000–DFFF', 'E/S y zonas por definir', '#fff0dc'),
              ('8000–BFFF', 'Sin RAM inicial asignada', '#f6f2ec'),
              ('0000–7FFF', 'RAM 32 KiB', '#e7f2fa')]
    out = ''
    for i, (addr, label, fill) in enumerate(ranges):
        y = 120 + i * 82
        out += box(95, y, 810, 71, fill)
        out += text(252, y + 43, addr, 'label', 'middle')
        out += text(648, y + 43, label, 'small', 'middle')
    out += text(500, 472, 'RAM[6000–6FFF] es parte de la RAM; FFFC/FFFD está en ROM.',
                'small', 'middle')
    return out


FIGS['c17_fig02_mapa_memoria'] = page(
    'Mapa funcional, no lista de chips instalados',
    'El bus tiene 16 bits de dirección; 64 KiB direccionables no son 64 KiB de RAM.',
    map_rows())


FIGS['c17_fig03_ranuras_rom'] = page(
    'Una dirección pública no revela la rutina interna',
    'Las direcciones E100 y FF00 son ejemplos aún sin firmware ejecutable.',
    box(27, 163, 279, 200, '#e6f1f9')
    + box(361, 163, 279, 200, '#f8f0dc')
    + box(695, 163, 279, 200, '#e8f5e8')
    + text(166, 203, 'PROGRAMA', 'label', 'middle')
    + text(166, 264, 'CALL FF00', 'label', 'middle')
    + text(500, 203, 'RANURA FF00', 'label', 'middle')
    + text(500, 253, '30 00 E1 00', 'label', 'middle')
    + text(500, 305, 'JMP E100', 'small', 'middle')
    + text(834, 203, 'RUTINA FICTICIA', 'label', 'middle')
    + text(834, 260, 'E100 → RET', 'label', 'middle')
    + '<path class="wire" d="M306,260 H361 M640,260 H695"/>'
    + text(500, 434, 'RET recuperaría el retorno que guardó CALL.', 'small', 'middle'))


FIGS['c17_fig04_run_dos_ret'] = page(
    'RUN y PUTC: hay dos niveles de retorno',
    'HALT no equivale a RET ni provoca un prompt por sí solo.',
    box(30, 166, 221, 192, '#e8f1fa')
    + box(271, 166, 221, 192, '#f8efdc')
    + box(511, 166, 221, 192, '#e9f5e8')
    + box(751, 166, 221, 192, '#e8f1fa')
    + text(140, 211, 'MONITOR', 'label', 'middle')
    + text(140, 275, 'CALL 6000', 'small', 'middle')
    + text(381, 211, 'PROGRAMA', 'label', 'middle')
    + text(381, 271, 'CALL FF00', 'small', 'middle')
    + text(622, 211, 'SERVICIO ROM', 'label', 'middle')
    + text(622, 275, 'RET → 6006', 'small', 'middle')
    + text(862, 211, 'PROGRAMA', 'label', 'middle')
    + text(862, 271, 'RET → monitor', 'small', 'middle')
    + '<path class="wire" d="M251,258 H271 M492,258 H511 M732,258 H751"/>'
    + text(500, 426, 'Si el programa termina en HALT, no retorna al monitor.', 'small', 'middle'))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg_content in FIGS.items():
        svg = OUT / f'{name}.svg'
        png = OUT / f'{name}.png'
        svg.write_text(svg_content, encoding='utf-8')
        subprocess.run(['inkscape', str(svg), '--export-type=png',
                        f'--export-filename={png}', '--export-width=2000'], check=True)
        print('Figura', png.relative_to(ROOT))


if __name__ == '__main__':
    main()
