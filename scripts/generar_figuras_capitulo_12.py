#!/usr/bin/env python3
"""Láminas vectoriales de datapath Aula-8: modelos funcionales, no hardware."""
import subprocess
from generar_figuras_capitulo_01 import ROOT
from generar_figuras_capitulo_11 import page, box, text

OUT = ROOT / 'libro' / 'figuras'
FIGS = {}

FIGS['c12_fig01_mapa_cpu_aula8'] = page(
    'Aula-8: bloques y dos anchos diferentes',
    'Dirección externa de 16 bits; dato externo e interno de 8 bits. Ninguna ruta está siempre activa.',
    box(39, 128, 219, 260, '#f1f6fb')
    + text(148, 161, 'Registros', 'label', 'middle')
    + text(148, 202, 'R0  R1  R2  R3', 'small', 'middle')
    + text(148, 241, '4 x 8 bits', 'small', 'middle')
    + text(148, 290, 'PC  SP  X', 'label', 'middle')
    + text(148, 327, '3 x 16 bits', 'small', 'middle')
    + box(330, 127, 215, 119, '#e9f3e8')
    + text(438, 166, 'ALU8 + FLAGS', 'label', 'middle')
    + text(438, 210, 'cálculo de datos', 'small', 'middle')
    + box(330, 286, 215, 101, '#f9f0d8')
    + text(438, 325, 'Bus interno', 'label', 'middle')
    + text(438, 361, '8 bits', 'small', 'middle')
    + box(623, 128, 141, 120, '#e7f5fa')
    + text(694, 170, 'MAR', 'label', 'middle')
    + text(694, 205, '16 bits', 'small', 'middle')
    + box(623, 286, 141, 101, '#e7f5fa')
    + text(694, 329, 'MDR', 'label', 'middle')
    + text(694, 361, '8 bits', 'small', 'middle')
    + box(831, 172, 137, 171, '#f4f7fb')
    + text(899, 207, 'RAM', 'label', 'middle')
    + text(899, 245, 'ROM', 'label', 'middle')
    + text(899, 283, 'E/S', 'label', 'middle')
    + '<path class="wire" d="M258,189 H330 M258,328 H330 M545,333 H623"/>'
    + '<path class="wire" d="M545,188 H585 V335 H623"/>'
    + '<path class="wire" d="M764,187 H831 M764,334 H831"/>'
    + text(796, 159, 'A0..A15', 'tiny', 'middle')
    + text(796, 367, 'D0..D7', 'tiny', 'middle')
    + text(505, 454, 'Control: selecciona fuentes, destinos, ALU, lectura y escritura.', 'small', 'middle')
    + text(505, 480, 'El esquema representa capacidades, no señales de reloj ni cableado físico.', 'tiny', 'middle'))

FIGS['c12_fig02_movimiento_registros'] = page(
    'Una copia controlada: R1 hacia R0',
    'Elegir la fuente no basta: también debe habilitarse la captura del registro destino.',
    box(48, 174, 233, 144, '#e9f4ea')
    + box(383, 174, 218, 144, '#f9f0d8')
    + box(714, 174, 240, 144, '#e8f2fa')
    + text(164, 216, 'R1 · fuente', 'label', 'middle')
    + text(164, 262, '00111100', 'label', 'middle')
    + text(492, 217, 'Bus interno', 'label', 'middle')
    + text(492, 263, '00111100', 'label', 'middle')
    + text(834, 216, 'R0 · destino', 'label', 'middle')
    + text(834, 263, '00111100', 'label', 'middle')
    + '<path class="wire" d="M281,247 H383 M601,247 H714"/>'
    + '<path class="wire" d="M834,110 V174 M164,368 V318"/>'
    + text(842, 113, 'LOAD R0', 'small')
    + text(164, 392, 'SEL=R1', 'small', 'middle')
    + text(502, 436, 'Antes: R0=00000000. Después: R0=00111100.', 'small', 'middle')
    + text(502, 475, 'R1 no se borra: no se activó ninguna escritura en R1.', 'small', 'middle'))

FIGS['c12_fig03_lectura_escritura'] = page(
    'Memoria: el dato cambia de conductor',
    'MAR mantiene 0x6F00 en ambos casos; RD y WR son solicitudes mutuamente excluyentes.',
    box(39, 119, 438, 288, '#e8f3fa')
    + box(523, 119, 438, 288, '#eaf5ea')
    + text(258, 162, 'LECTURA (RD)', 'label', 'middle')
    + text(258, 209, 'RAM entrega byte', 'small', 'middle')
    + text(258, 249, 'RAM  →  D0..D7  →  MDR', 'label', 'middle')
    + text(258, 300, 'CPU NO conduce los datos', 'small', 'middle')
    + text(258, 350, 'MAR = 0x6F00', 'small', 'middle')
    + text(742, 162, 'ESCRITURA (WR)', 'label', 'middle')
    + text(742, 209, 'CPU entrega byte', 'small', 'middle')
    + text(742, 249, 'MDR  →  D0..D7  →  RAM', 'label', 'middle')
    + text(742, 300, 'RAM NO conduce los datos', 'small', 'middle')
    + text(742, 350, 'MAR = 0x6F00; MDR = 0x2A', 'small', 'middle')
    + text(500, 456, 'Nunca dos fuentes incompatibles sobre el mismo bus.', 'small', 'middle')
    + text(500, 481, 'Acciones funcionales; sin polaridad ni tiempos de acceso fijados.', 'tiny', 'middle'))

FIGS['c12_fig04_direccion_dos_pasadas'] = page(
    'X de 16 bits, ALU de 8 bits',
    'Desplazamiento +2 sobre X=0x12FF, conservando FLAGS.C visible.',
    box(43, 115, 913, 92, '#f3f7fb')
    + text(490, 153, 'X inicial = 0x12FF     |     sumar 0x0002', 'label', 'middle')
    + text(490, 185, 'Primero se procesa el byte bajo; después el alto.', 'small', 'middle')
    + box(72, 249, 355, 126, '#e8f3fa')
    + box(576, 249, 355, 126, '#eaf5e9')
    + text(249, 283, 'Paso 1 · byte bajo', 'label', 'middle')
    + text(249, 323, 'FF + 02 = 101 (hex)', 'label', 'middle')
    + text(249, 353, 'Guardar 01 · carry interno 1', 'small', 'middle')
    + text(754, 283, 'Paso 2 · byte alto', 'label', 'middle')
    + text(754, 323, '12 + 00 + 1 = 13 (hex)', 'label', 'middle')
    + text(754, 353, 'Guardar 13 · X=0x1301', 'small', 'middle')
    + '<path class="wire" d="M427,313 H576"/>'
    + text(501, 299, 'ADDR_CARRY', 'tiny', 'middle')
    + text(500, 427, 'La bandera visible FLAGS.C no cambia por este cálculo de dirección.', 'small', 'middle')
    + text(500, 476, 'Este recorrido no implica una ALU general de 16 bits ni tiempos probados.', 'tiny', 'middle'))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, source in FIGS.items():
        svg = OUT / f'{name}.svg'
        png = OUT / f'{name}.png'
        svg.write_text(source, encoding='utf-8')
        subprocess.run(['inkscape', str(svg), '--export-type=png',
                        f'--export-filename={png}', '--export-width=2000'], check=True)
        print('Figura', png.relative_to(ROOT))


if __name__ == '__main__':
    main()
