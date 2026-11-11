#!/usr/bin/env python3
"""Ocho figuras originales reproducibles de C22 y C23.

Cada figura describe un contrato lógico, no pistas de PCB ni ciclos medidos.
Las constantes se comprueban contra la arquitectura ya documentada.
"""
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from generar_diagramas_tecnicos_aula8 import arrow, box, lane, page, resolver_inkscape, t

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'libro' / 'figuras'


def contract():
    state = json.loads((ROOT / 'ESTADO_PORTABLE.json').read_text(encoding='utf-8'))
    sixteen = state['architecture']['aula16']
    assert state['architecture']['address_bus_bits'] == 16
    assert state['architecture']['addressable_bytes'] == 65536
    assert sixteen['external_data_bus_bits'] == 16
    assert sixteen['memory_banks_of_8_bits'] == 2
    assert sixteen['word_alignment_bytes'] == 2
    assert sixteen['byte_addressable'] and sixteen['little_endian']
    assert 0x2000 >> 1 == 0x1000
    assert (0x2200 + 4) % 2 == 0


def figures():
    figs = {}
    # No basta con dos rectángulos y una raya: se muestran los dos octetos
    # físicos, el decodificador y la selección de paridad de la dirección.
    a = lane(26, 194, 225, 230, '#f0f4fb', 'CPU AULA-16', 'A15..A0 / RD / WR')
    a += lane(369, 106, 252, 112, '#f9eedc', 'DECODIFICADOR', 'A15 y A0 / ancho')
    a += lane(715, 190, 252, 123, '#e9f4e6', 'BANCO BAJO', '0x2000 contiene 34')
    a += lane(715, 336, 252, 123, '#e7f1fb', 'BANCO ALTO', '0x2001 contiene 12')
    a += '<path d="M213,194 V163 H369" stroke="#244d68" stroke-width="4" fill="none"/>'
    a += t(294, 147, 'A[15:0]', 'tiny', 'middle')
    a += '<path d="M251,269 H715" stroke="#388a63" stroke-width="9" fill="none"/>'
    a += '<path d="M251,414 H715" stroke="#4380ab" stroke-width="9" fill="none"/>'
    a += t(488, 250, 'D7..D0  (8 hilos)', 'small', 'middle')
    a += t(488, 395, 'D15..D8  (8 hilos)', 'small', 'middle')
    a += t(486, 305, 'A14..A1: 14 bits de fila dentro de cada banco RAM.', 'tiny', 'middle')
    a += t(486, 332, 'A0 y el ancho de acceso habilitan uno o ambos.', 'tiny', 'middle')
    a += t(500, 483, 'Palabra par: 34 en carril bajo + 12 en carril alto = 0x1234 (little-endian).', 'tiny', 'middle')
    figs['c22_fig01_bancos_y_carriles'] = page('Dos bancos para una memoria byte a byte',
        'Ejemplo con bus de datos externo de 16 bits, separado en dos carriles de 8.', a)

    a = lane(308, 120, 388, 112, '#f9eedc', 'REGISTRO R0', '0x1234')
    a += lane(35, 314, 420, 120, '#e9f4e6', 'RAM[2000]  ·  BANCO BAJO', '0x34')
    a += lane(544, 314, 420, 120, '#e7f1fb', 'RAM[2001]  ·  BANCO ALTO', '0x12')
    a += arrow(397, 234, 248, 310) + arrow(607, 234, 754, 310)
    a += t(500, 475, 'Lectura: 34 + (12 × 256) = 0x1234.', 'small', 'middle')
    figs['c22_fig02_palabra_y_little_endian'] = page('Little-endian desde un registro hacia dos bytes',
        'La posición de los bytes cambia, no los bits de cada byte.', a)

    items = [
        ('BYTE PAR', 'Solo D7..D0', '#e9f4e6'),
        ('BYTE IMPAR', 'Solo D15..D8', '#e7f1fb'),
        ('PALABRA PAR', 'Ambos carriles', '#f9eedc'),
        ('PALABRA IMPAR', 'Error de V1', '#fce8e8'),
    ]
    a = ''
    for i, (name, detail, color) in enumerate(items):
        x = 27 + (i % 2) * 498
        y = 142 + (i // 2) * 178
        a += box(x, y, 448, 145, color)
        a += t(x + 224, y + 49, name, 'label', 'middle')
        a += t(x + 224, y + 105, detail, 'small', 'middle')
    a += t(500, 487, 'Lectura y escritura usan la misma selección lógica de carril.', 'tiny', 'middle')
    figs['c22_fig03_matriz_operaciones'] = page('Selección de bancos por anchura y paridad',
        'La palabra impar se rechaza sin intentar un acceso dividido.', a)

    failures = [
        ('BYTE SWAP', '1234 → 3412', '#f9eedc'),
        ('CARRIL CRUZADO', 'STB altera vecino', '#fce8e8'),
        ('IMPAR', 'LDW 2001 admitida', '#fce8e8'),
        ('MMIO', 'C020 leído como word', '#f9eedc'),
    ]
    a = ''
    for i, (name, detail, color) in enumerate(failures):
        x = 28 + (i % 2) * 495
        y = 143 + (i // 2) * 177
        a += box(x, y, 448, 143, color)
        a += t(x + 224, y + 50, name, 'label', 'middle')
        a += t(x + 224, y + 106, detail, 'small', 'middle')
    a += t(500, 484, 'Los cuatro síntomas tienen causas y pruebas diferentes.', 'tiny', 'middle')
    figs['c22_fig04_casos_fallo_bus'] = page('Diagnosticar un bus de dos carriles',
        'Síntomas lógicos para el modelo; no mediciones de osciloscopio.', a)

    a = ''
    stages = [
        ('PROBLEMA', 'Sumar 3 palabras', '#e9f4e6'),
        ('FUENTE', 'Pseudocódigo', '#e7f1fb'),
        ('HERRAMIENTAS', 'ISA/ABI futuras', '#f9eedc'),
        ('CPU AULA-16', 'No implementada', '#fce8e8'),
    ]
    for i, (name, detail, color) in enumerate(stages):
        x = 24 + i * 246
        a += lane(x, 159, 216, 168, color, name, detail)
        if i < 3:
            a += arrow(x + 216, 246, x + 246, 246)
    a += t(500, 415, 'Hoy sí podemos comprobar la referencia matemática en anfitrión.', 'small', 'middle')
    a += t(500, 454, 'No existe binario Aula-16 generado ni ejecutado.', 'tiny', 'middle')
    figs['c23_fig01_niveles_de_programa'] = page('De una idea a una computadora ejecutando',
        'Cada herramienta debe existir y pasar pruebas antes de la siguiente.', a)

    a = ''
    entries = [('2200', 'FF 01', '01FF'), ('2202', '01 00', '0001'), ('2204', '02 00', '0002')]
    for i, (addr, bytes_, word) in enumerate(entries):
        x = 25 + i * 325
        a += lane(x, 136, 300, 171, '#e7f1fb', f'RAM {addr}', bytes_)
        a += t(x + 150, 279, f'Valor {word}', 'small', 'middle')
        if i < 2:
            a += arrow(x + 300, 215, x + 325, 215)
    a += lane(291, 361, 420, 110, '#e9f4e6', 'RESULTADO EN 2210', '02 02  =  0x0202')
    figs['c23_fig02_sumar_arreglo'] = page('Recorrido de tres palabras alineadas',
        'El puntero sube de dos en dos; suma matemática 511+1+2=514.', a)

    steps = [('48, 18', 'inicio'), ('30, 18', 'a−b'), ('12, 18', 'a−b'),
             ('12, 6', 'b−a'), ('6, 6', 'fin')]
    a = ''
    for i, (state, detail) in enumerate(steps):
        x = 18 + 196 * i
        a += lane(x, 164, 176, 165, '#e9f4e6' if i == 4 else '#e7f1fb', state, detail)
        if i < 4:
            a += arrow(x + 176, 249, x + 196, 249)
    a += t(500, 405, 'MCD = 6: los estados esperados son idénticos en ambas máquinas.', 'small', 'middle')
    a += t(500, 451, 'Los opcodes y el ancho natural de los datos NO son idénticos.', 'tiny', 'middle')
    figs['c23_fig03_euclides_dos_maquinas'] = page('Euclides es portable como algoritmo, no como bytes',
        'Una secuencia de enteros positivos comprobable sin hardware Aula-16.', a)

    a = lane(28, 158, 280, 180, '#e9f4e6', 'MODELO HOY', 'Python · matemáticas')
    a += lane(362, 158, 280, 180, '#f9eedc', 'HERRAMIENTAS', 'ISA y ABI pendientes')
    a += lane(696, 158, 280, 180, '#fce8e8', 'EJECUCIÓN AULA', 'CPU pendiente')
    a += arrow(308, 250, 362, 250) + arrow(642, 250, 696, 250)
    a += t(500, 413, 'El modelo verifica valores y memoria, no instrucciones ni señales.', 'small', 'middle')
    a += t(500, 451, 'La compilación cruzada requiere codificación y cargador definidos.', 'tiny', 'middle')
    figs['c23_fig04_compilacion_y_pruebas'] = page('Qué puede verificarse hoy y qué todavía no',
        'Diferencia entre referencia anfitriona, herramientas y ejecución real.', a)
    return figs


def main():
    contract()
    OUT.mkdir(parents=True, exist_ok=True)
    inkscape = resolver_inkscape()
    for name, svg in figures().items():
        src, png = OUT / f'{name}.svg', OUT / f'{name}.png'
        ET.fromstring(svg)
        src.write_text(svg, encoding='utf-8')
        subprocess.run([inkscape, str(src), '--export-type=png',
                        f'--export-filename={png}', '--export-width=2000'],
                       check=True, capture_output=True, text=True)
        assert png.is_file() and png.stat().st_size > 10000
        print(name, src.stat().st_size, png.stat().st_size)


if __name__ == '__main__':
    main()
