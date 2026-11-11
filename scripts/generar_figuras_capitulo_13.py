#!/usr/bin/env python3
"""Cuatro láminas originales de control microprogramado: modelos, no cableado."""
import subprocess
from generar_figuras_capitulo_01 import ROOT
from generar_figuras_capitulo_11 import page, box, text


OUT = ROOT / 'libro' / 'figuras'
FIGURES = {}

FIGURES['c13_fig01_unidad_control'] = page(
    'Dos recorridos: programa y microcontrol',
    'PC identifica bytes de programa; microPC selecciona acciones internas.',
    box(54, 146, 193, 103, '#e7f3fa')
    + box(300, 146, 245, 103, '#e7f3fa')
    + box(598, 146, 334, 103, '#e7f3fa')
    + text(150, 185, 'PC · 16 bits', 'label', 'middle')
    + text(150, 220, 'dirección programa', 'small', 'middle')
    + text(422, 185, 'RAM / ROM', 'label', 'middle')
    + text(422, 220, 'bytes de instrucciones', 'small', 'middle')
    + text(765, 185, 'IR · opcode', 'label', 'middle')
    + text(765, 220, 'selección de ruta', 'small', 'middle')
    + '<path class="wire" d="M247,194 H300 M545,194 H598"/>'
    + box(52, 314, 183, 105, '#f9f0d8')
    + box(285, 314, 255, 105, '#f9f0d8')
    + box(592, 314, 339, 105, '#eaf4eb')
    + text(143, 358, 'microPC', 'label', 'middle')
    + text(143, 389, 'estado interno', 'small', 'middle')
    + text(413, 358, 'ROM de control', 'label', 'middle')
    + text(413, 389, 'sin tamaño fijado', 'small', 'middle')
    + text(763, 355, 'Señales para datapath', 'label', 'middle')
    + text(763, 390, 'cargas · buses · RD/WR', 'small', 'middle')
    + '<path class="wire" d="M235,370 H285 M540,370 H592"/>'
    + '<path class="wire" d="M765,249 V275 H143 V314"/>'
    + text(519, 303, 'despacho y condiciones', 'tiny', 'middle')
    + text(495, 470, 'ROM de control y ROM de firmware son memorias distintas.', 'small', 'middle'))

FIGURES['c13_fig02_macro_lectura'] = page(
    'Leer un opcode exige varias dependencias',
    'READ_PC_TO_IR es una macro lógica, no cuatro ciclos de reloj.',
    box(28, 171, 213, 142, '#e7f3fa')
    + box(276, 171, 210, 142, '#edf4e8')
    + box(519, 171, 210, 142, '#f9f0d8')
    + box(762, 171, 210, 142, '#e7f3fa')
    + text(134, 208, '1. Preparar', 'label', 'middle')
    + text(134, 250, 'MAR recibe PC', 'small', 'middle')
    + text(381, 208, '2. Pedir lectura', 'label', 'middle')
    + text(381, 250, 'RD y dato válido', 'small', 'middle')
    + text(624, 208, '3. Retener', 'label', 'middle')
    + text(624, 250, 'MDR guarda byte', 'small', 'middle')
    + text(866, 208, '4. Usar', 'label', 'middle')
    + text(866, 250, 'IR recibe byte', 'small', 'middle')
    + text(866, 278, 'PC avanza', 'small', 'middle')
    + '<path class="wire" d="M241,240 H276 M486,240 H519 M729,240 H762"/>'
    + text(500, 369, 'La memoria debe entregar datos estables antes de capturarlos.', 'small', 'middle')
    + text(500, 418, 'No se asignaron flancos, retardo, READY ni frecuencia.', 'small', 'middle')
    + text(500, 466, 'La CPU no conduce datos externos mientras la memoria responde a RD.', 'tiny', 'middle'))

FIGURES['c13_fig03_despacho'] = page(
    'El despacho no equivale a ejecutar una instrucción',
    'IR selecciona una ruta; solo tres rutas están descritas en el borrador.',
    box(30, 149, 228, 100, '#e7f3fa')
    + box(336, 149, 318, 100, '#f9f0d8')
    + text(144, 189, 'FETCH_OPCODE', 'label', 'middle')
    + text(144, 225, 'leer y conservar IR', 'small', 'middle')
    + text(495, 189, 'DECODE', 'label', 'middle')
    + text(495, 225, 'seleccionar microsecuencia', 'small', 'middle')
    + '<path class="wire" d="M258,197 H336"/>'
    + box(702, 122, 273, 66, '#e8f4e9')
    + box(702, 209, 273, 66, '#e8f4e9')
    + box(702, 296, 273, 66, '#e8f4e9')
    + text(837, 162, '11 → LDI_SELECTOR', 'small', 'middle')
    + text(837, 249, '13 → ST_SELECTOR', 'small', 'middle')
    + text(837, 336, '01 → HALT_ENTER', 'small', 'middle')
    + '<path class="wire" d="M654,198 H680 V155 H702 M680,241 H702 M680,329 H702"/>'
    + box(45, 311, 285, 101, '#fdebe8')
    + box(366, 311, 287, 101, '#f4f1dc')
    + text(187, 354, 'FAULT', 'label', 'middle')
    + text(187, 385, 'opcode inexistente', 'small', 'middle')
    + text(510, 354, 'PENDING_ROUTE', 'label', 'middle')
    + text(510, 385, 'conocido sin ruta escrita', 'small', 'middle')
    + text(501, 473, 'Ni el número de estados ni sus direcciones internas están fijados.', 'tiny', 'middle'))

FIGURES['c13_fig04_escritura_segura'] = page(
    'ST: conservar dirección y preparar dato',
    'Los bytes de dirección sobreviven aunque MDR se reutilice.',
    box(30, 145, 285, 222, '#e7f3fa')
    + box(358, 145, 285, 222, '#f9f0d8')
    + box(686, 145, 285, 222, '#eaf4e9')
    + text(173, 185, '1. Retener dirección', 'label', 'middle')
    + text(173, 232, 'ADDR_LO = 00', 'small', 'middle')
    + text(173, 273, 'ADDR_HI = 6F', 'small', 'middle')
    + text(173, 327, 'MDR puede cambiar', 'small', 'middle')
    + text(501, 185, '2. Preparar salida', 'label', 'middle')
    + text(501, 232, 'MAR = 0x6F00', 'small', 'middle')
    + text(501, 273, 'R0 = 0x2A', 'small', 'middle')
    + text(501, 327, 'MDR recibe 2A', 'small', 'middle')
    + text(828, 185, '3. Escribir RAM', 'label', 'middle')
    + text(828, 232, 'WR habilitado', 'small', 'middle')
    + text(828, 273, 'CPU conduce datos', 'small', 'middle')
    + text(828, 327, 'RAM guarda 0x2A', 'small', 'middle')
    + '<path class="wire" d="M315,255 H358 M643,255 H686"/>'
    + text(500, 417, 'Activar WR cuando MDR aún contiene 6F escribiría el byte equivocado.', 'small', 'middle')
    + text(500, 471, 'Secuencia propuesta: sin tiempo, reloj ni circuitería comprobados.', 'tiny', 'middle'))


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
