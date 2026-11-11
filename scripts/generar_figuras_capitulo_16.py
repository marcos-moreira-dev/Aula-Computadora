#!/usr/bin/env python3
"""Dibuja cuatro figuras originales sobre CALL, RET, pila y bucles."""

import subprocess
from generar_figuras_capitulo_01 import ROOT
from generar_figuras_capitulo_11 import box, page, text

OUT = ROOT / 'libro' / 'figuras'
FIGS = {}


FIGS['c16_fig01_pila_retorno'] = page(
    'La pila desciende y RET no borra la RAM',
    'CALL de 6000 a 6010 conserva el retorno 6003 como bajo 03 y alto 60.',
    box(28, 144, 285, 280, '#e7f1fa')
    + box(357, 144, 285, 280, '#eaf4e6')
    + box(686, 144, 285, 280, '#fff2de')
    + text(170, 184, 'ANTES DE CALL', 'label', 'middle')
    + text(170, 229, 'SP = 8000', 'label', 'middle')
    + text(170, 284, '7FFF: ?    7FFE: ?', 'small', 'middle')
    + text(170, 349, '8000 no es RAM', 'small', 'middle')
    + text(500, 184, 'DESPUÉS DE CALL', 'label', 'middle')
    + text(500, 229, 'SP = 7FFE', 'label', 'middle')
    + text(500, 284, '7FFF: 60    alto', 'small', 'middle')
    + text(500, 320, '7FFE: 03    bajo', 'small', 'middle')
    + text(828, 184, 'DESPUÉS DE RET', 'label', 'middle')
    + text(828, 229, 'SP = 8000', 'label', 'middle')
    + text(828, 284, '7FFF: 60    residuo', 'small', 'middle')
    + text(828, 320, '7FFE: 03    residuo', 'small', 'middle')
    + text(500, 468, 'Liberar pila cambia SP, no borra automáticamente los bytes.', 'small', 'middle'))


def call_flow():
    cards = [
        ('6000: CALL 6010', 'PC tras operandos: 6003', '#e7f1fa'),
        ('PILA: 03 60', 'SP=7FFE; guardar retorno', '#f5eedf'),
        ('6010: LDI R0,2A', 'R0 recibe 42 decimal', '#eaf5e9'),
        ('6013: RET', 'PC vuelve a 6003', '#dfeef8'),
    ]
    out = ''
    for i, (title, note, color) in enumerate(cards):
        x = 22 + i * 250
        out += box(x, 164, 226, 177, color)
        out += text(x + 113, 222, title, 'small', 'middle')
        out += text(x + 113, 274, note, 'tiny', 'middle')
        if i < 3:
            out += f'<path class="wire" d="M{x+226},252 H{x+250}"/>'
    out += box(331, 391, 336, 61, '#fff1dd')
    out += text(499, 430, '6003: HALT, PC=6004', 'label', 'middle')
    out += '<path class="wire" d="M885,341 V370 H500 V391"/>'
    return out


FIGS['c16_fig02_llamar_regresar'] = page(
    'CALL guarda la continuación; RET la recupera',
    'Este recorrido es lógico: no indica cuántos ciclos tarda una CPU real.',
    call_flow())


def stack_rows():
    rows = [('7FFF', '60', 'retorno exterior ALTO'),
            ('7FFE', '03', 'retorno exterior BAJO'),
            ('7FFD', '60', 'retorno interior ALTO'),
            ('7FFC', '13', 'retorno interior BAJO ← SP')]
    out = ''
    for i, (addr, value, note) in enumerate(rows):
        y = 129 + i * 78
        fill = '#e8f2fc' if i < 2 else '#eaf5e7'
        out += box(78, y, 844, 67, fill)
        out += text(174, y + 42, addr, 'label', 'middle')
        out += text(328, y + 42, value, 'label', 'middle')
        out += text(640, y + 42, note, 'small', 'middle')
    out += text(500, 474, 'SP: 8000 → 7FFE → 7FFC → 7FFE → 8000.', 'small', 'middle')
    return out


FIGS['c16_fig03_llamadas_anidadas'] = page(
    'Dos llamadas: dos retornos, uno encima del otro',
    'CALL exterior retorna a 6003; CALL interior retorna a 6013.',
    stack_rows())


def loop_cards():
    states = [('VUELTA 1', 'DEC: 3 → 2', 'Z=0 · salta', '#e6f2fc'),
              ('VUELTA 2', 'DEC: 2 → 1', 'Z=0 · salta', '#eaf4e6'),
              ('VUELTA 3', 'DEC: 1 → 0', 'Z=1 · sigue HALT', '#fff0dc')]
    out = ''
    for i, (title, desc, result, fill) in enumerate(states):
        x = 26 + i * 330
        out += box(x, 147, 289, 244, fill)
        out += text(x + 145, 191, title, 'label', 'middle')
        out += text(x + 145, 249, desc, 'label', 'middle')
        out += text(x + 145, 317, result, 'small', 'middle')
    out += text(500, 461, 'Cada JNZ lee siempre los dos bytes de su destino.', 'small', 'middle')
    return out


FIGS['c16_fig04_bucle_jnz'] = page(
    'Contador de tres: dos saltos y una salida',
    'La propuesta de DEC actualiza Z; JNZ consulta Z sin modificarla.',
    loop_cards())


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
