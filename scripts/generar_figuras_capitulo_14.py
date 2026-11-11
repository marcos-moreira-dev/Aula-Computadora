#!/usr/bin/env python3
"""Cuatro diagramas originales: codificación y carga manual (no cableado)."""
import subprocess

from generar_figuras_capitulo_01 import ROOT
from generar_figuras_capitulo_11 import page, box, text


OUT = ROOT / 'libro' / 'figuras'
FIGURES = {}


FIGURES['c14_fig01_un_byte_tres_lecturas'] = page(
    'Un byte: la forma no dicta su significado',
    'Los mismos ocho bits se pueden representar en tres bases.',
    box(115, 143, 355, 112, '#e7f3fa')
    + box(530, 143, 355, 112, '#e7f3fa')
    + text(290, 182, '0010', 'label', 'middle')
    + text(707, 182, '1010', 'label', 'middle')
    + text(290, 225, 'nibble alto = 2', 'small', 'middle')
    + text(707, 225, 'nibble bajo = A', 'small', 'middle')
    + '<path class="wire" d="M290,255 V293 H492 V312 M707,255 V293 H492"/>'
    + box(350, 312, 295, 84, '#eaf4e9')
    + text(492, 347, '0x2A', 'label', 'middle')
    + text(492, 377, '2 × 16 + 10 = 42', 'small', 'middle')
    + text(500, 459, 'Patrón guardado ≠ significado automático de opcode.', 'small', 'middle'))


def program_map():
    code = [
        ('6000', '11', '#d9e9f5'), ('6001', '00', '#e6f4e8'),
        ('6002', '2A', '#f9eed2'), ('6003', '13', '#d9e9f5'),
        ('6004', '00', '#e6f4e8'), ('6005', '00', '#f9eed2'),
        ('6006', '6F', '#f9eed2'), ('6007', '01', '#d9e9f5'),
    ]
    s = ''
    for i, (addr, val, color) in enumerate(code):
        x = 33 + i * 120
        s += box(x, 158, 98, 122, color)
        s += text(x + 49, 196, addr, 'small', 'middle')
        s += text(x + 49, 248, val, 'label', 'middle')
    s += '<path class="wire" d="M36,318 V333 H369 V318 M394,318 V333 H847 V318 M873,318 V333 H968 V318"/>'
    s += text(198, 363, 'LDI: 3 bytes', 'label', 'middle')
    s += text(622, 363, 'ST: 4 bytes', 'label', 'middle')
    s += text(920, 363, 'HALT', 'small', 'middle')
    s += text(510, 420, 'RAM[6F00] es el DESTINO de ST, fuera de estas ocho posiciones.', 'small', 'middle')
    s += text(510, 465, 'Azul: opcode   ·   Verde: selector   ·   Crema: dato o dirección.', 'small', 'middle')
    return s


FIGURES['c14_fig02_mapa_programa'] = page(
    'Código almacenado de 6000 a 6007',
    'Un opcode de un byte no impide instrucciones de longitud variable.',
    program_map())


FIGURES['c14_fig03_modos_direccion'] = page(
    'Los operandos deciden la dirección',
    'Tres codificaciones de LD; todos los valores son provisionales.',
    box(32, 144, 293, 247, '#e7f3fa')
    + box(352, 144, 293, 247, '#eaf4e9')
    + box(672, 144, 293, 247, '#f9f0d8')
    + text(179, 180, 'ABSOLUTO', 'label', 'middle')
    + text(179, 221, 'LD R0,[6F00]', 'small', 'middle')
    + text(179, 269, '12 00 00 6F', 'label', 'middle')
    + text(179, 319, '00 6F → 6F00', 'small', 'middle')
    + text(179, 360, '4 bytes', 'small', 'middle')
    + text(498, 180, 'POR X', 'label', 'middle')
    + text(498, 221, 'LD R1,[X-1]', 'small', 'middle')
    + text(498, 269, '12 05 FF', 'label', 'middle')
    + text(498, 319, '05 = modo 1, R1', 'small', 'middle')
    + text(498, 360, 'FF = -1', 'small', 'middle')
    + text(818, 180, 'POR SP', 'label', 'middle')
    + text(818, 221, 'LD R2,[SP+6]', 'small', 'middle')
    + text(818, 269, '12 0A 06', 'label', 'middle')
    + text(818, 319, '0A = modo 2, R2', 'small', 'middle')
    + text(818, 360, '06 = +6', 'small', 'middle')
    + text(500, 467, 'Los desplazamientos requieren cálculo; no implican ALU16.', 'small', 'middle'))


FIGURES['c14_fig04_panel_seguro'] = page(
    'Depositar un byte: el bus tiene dueño',
    'Panel manual posible, solo con la CPU detenida y aislada.',
    box(30, 165, 214, 155, '#fcece9')
    + box(274, 165, 214, 155, '#e7f3fa')
    + box(518, 165, 214, 155, '#f9f0d8')
    + box(762, 165, 208, 155, '#eaf4e9')
    + text(137, 211, '1. PARAR', 'label', 'middle')
    + text(137, 251, 'CPU no conduce', 'small', 'middle')
    + text(137, 282, 'bus concedido', 'small', 'middle')
    + text(381, 211, '2. ELEGIR', 'label', 'middle')
    + text(381, 251, 'dirección: 16 bits', 'small', 'middle')
    + text(381, 282, 'dato: 8 bits', 'small', 'middle')
    + text(625, 211, '3. DEPOSIT', 'label', 'middle')
    + text(625, 251, 'escribir RAM', 'small', 'middle')
    + text(625, 282, 'EXAMINE y verificar', 'small', 'middle')
    + text(866, 211, '4. SOLTAR', 'label', 'middle')
    + text(866, 251, 'liberar bus', 'small', 'middle')
    + text(866, 282, 'arranque explícito', 'small', 'middle')
    + '<path class="wire" d="M244,242 H274 M488,242 H518 M732,242 H762"/>'
    + text(500, 381, 'RESET no coloca automáticamente PC en 6000.', 'small', 'middle')
    + text(500, 447, 'Faltan arbitraje, temporización, controles y esquema eléctrico real.', 'small', 'middle'))


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
