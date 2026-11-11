#!/usr/bin/env python3
"""Dibuja C18/C19 como contratos verificables, NO como netlists ni oscilogramas.

Uso: python3 scripts/generar_diagramas_tecnicos_aula8.py
Produce ocho SVG editables de 1000x500 y ocho PNG a 2000 px de ancho.
Requiere Inkscape; no necesita hardware, servicios remotos ni datos aleatorios.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

from generar_figuras_capitulo_01 import ROOT
from generar_figuras_capitulo_11 import box, page, text as original_text

OUT = ROOT / 'libro' / 'figuras'


def t(x, y, string, style='small', anchor=None):
    return original_text(x, y, escape(str(string)), style, anchor)


def lane(x, y, w, h, fill, title, body=None):
    result = box(x, y, w, h, fill) + t(x + w/2, y + 48, title, 'label', 'middle')
    if body is not None:
        result += t(x + w/2, y + 94, body, 'small', 'middle')
    return result


def arrow(x1, y1, x2, y2, color='#244d68', marker=True):
    # Líneas de flujo FUNCIONAL; no representan pistas eléctricas.
    line = f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="4"/>'
    if marker:
        dx, dy = x2 - x1, y2 - y1
        scale = max(1.0, (dx*dx + dy*dy) ** 0.5)
        ux, uy = dx/scale, dy/scale
        lx, ly = x2 - ux*17, y2 - uy*17
        px, py = -uy*9, ux*9
        line += (f'<path d="M{x2},{y2} L{lx+px},{ly+py} L{lx-px},{ly-py} Z" '
                 f'fill="{color}"/>')
    return line


def check_contracts():
    rom = json.loads((ROOT / 'simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.json')
                     .read_text(encoding='utf-8'))
    storage = json.loads((ROOT / 'simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.json')
                         .read_text(encoding='utf-8'))
    assert rom['status'] == storage['status'] == 'propuesta_no_aprobada'
    assert not rom['firmware_implemented'] and not storage['controller_hardware_implemented']
    assert rom['terminal']['memory_mapped_data'] == 'C000'
    assert rom['terminal']['memory_mapped_status'] == 'C002'
    services = {row['name']: row['slot'] for row in rom['public_services']}
    assert services == {'FW_PUTC': 'FF00', 'FW_GETC': 'FF04',
                        'FW_PUTS': 'FF08', 'FW_STATUS': 'FF0C'}
    regs = {row['name']: row['address'] for row in storage['mmio']['registers']}
    assert regs == {'COMMAND': 'C010', 'STATUS': 'C012', 'BLOCK_LO': 'C014',
                    'BLOCK_HI': 'C016', 'DATA': 'C018', 'ERROR': 'C01A',
                    'COUNT_LO': 'C01C', 'COUNT_HI': 'C01E'}
    assert storage['transfer']['block_bytes'] == 256
    assert storage['nominal_status'] == {'idle': '00', 'transfer': '03',
                                          'done': '04', 'error': '08'}
    return rom, storage, services, regs


def resolver_inkscape():
    """Localiza Inkscape tanto en GNU/Linux como en Windows común."""
    candidate = shutil.which('inkscape') or shutil.which('inkscape.com')
    if candidate:
        return candidate
    if os.name == 'nt':
        locations = [Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'Inkscape/bin/inkscape.com',
                     Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'Inkscape/bin/inkscape.exe']
        locations.extend(Path(os.environ.get('ProgramFiles(x86)', 'C:/Program Files (x86)'))
                         / ('Inkscape/bin/' + filename) for filename in ('inkscape.com', 'inkscape.exe'))
        for path in locations:
            if path.is_file():
                return str(path)
    raise SystemExit('Inkscape no está instalado o disponible; instala Inkscape para generar los PNG.')


def make_figures():
    rom, storage, svc, reg = check_contracts()
    figures = {}

    a = lane(27, 153, 222, 178, '#e7f1fb', 'TERMINAL', 'teclas / pantalla')
    a += lane(389, 153, 238, 178, '#f9eedc', 'CONTROLADOR', 'RX / TX; por definir')
    a += lane(767, 153, 205, 178, '#e9f4e6', 'AULA-8', 'CPU y firmware')
    a += arrow(249, 203, 389, 203) + t(316, 190, 'RX byte', 'tiny', 'middle')
    a += arrow(389, 278, 249, 278) + t(317, 310, 'TX byte', 'tiny', 'middle')
    a += arrow(767, 206, 627, 206) + arrow(627, 239, 767, 239)
    a += t(699, 187, 'DATA RD/WR', 'tiny', 'middle')
    a += arrow(627, 280, 767, 280) + t(700, 312, 'STATUS', 'tiny', 'middle')
    a += t(500, 408, f'MMIO DATA {rom["terminal"]["memory_mapped_data"]}  |  STATUS {rom["terminal"]["memory_mapped_status"]}', 'small', 'middle')
    a += t(500, 445, 'Sin UART ni polaridad de señales eléctricas definidos.', 'tiny', 'middle')
    figures['c18_fig01_terminal_y_mmio'] = page('Terminal: caminos funcionales RX y TX',
        'Flechas conceptuales, no oscilograma ni diagrama de cableado.', a)

    a = lane(25, 154, 245, 164, '#e7f1fb', 'PROGRAMA', '6003: CALL FF00')
    a += lane(373, 154, 255, 164, '#f9eedc', 'RANURA FF00', '30 00 E1 00')
    a += lane(730, 154, 245, 164, '#e9f4e6', 'DESTINO FICTICIO', 'E100: rutina PUTC')
    a += arrow(270, 230, 373, 230) + arrow(628, 230, 730, 230)
    a += t(320, 209, 'CALL', 'tiny', 'middle') + t(677, 209, 'JMP', 'tiny', 'middle')
    a += arrow(842, 318, 842, 393) + arrow(842, 393, 157, 393)
    a += t(500, 378, 'RET usa la dirección 6006 guardada por CALL', 'small', 'middle')
    a += t(500, 448, 'El NOP final de la ranura no se ejecuta en la ruta normal.', 'tiny', 'middle')
    figures['c18_fig02_llamada_publica_rom'] = page('Dirección pública de un servicio de ROM',
        f'{svc["FW_PUTC"]}: ranura de cuatro bytes; E100 todavía no contiene firmware.', a)

    phases = [('6000', 'CALL GETC', '35 04 FF', '#e7f1fb'),
              ('6003', 'ST 6F00', '13 00 00 6F', '#f9eedc'),
              ('6007', 'CALL PUTC', '35 00 FF', '#e9f4e6'),
              ('600A', 'RET', '02', '#e7f1fb')]
    a = ''
    for i,(addr,title,code,color) in enumerate(phases):
        x=22 + i*246
        a += lane(x, 154, 216, 169, color, title, code)
        a += t(x+108, 293, 'PC '+addr, 'tiny', 'middle')
        if i<3: a += arrow(x+216, 240, x+246, 240)
    a += lane(256, 372, 486, 79, '#eef7ef', 'RAM[6F00] = 42', None)
    a += t(500, 470, 'Ejemplo: GETC recibe B (0x42), ST guarda, PUTC transmite.', 'tiny', 'middle')
    figures['c18_fig03_eco_con_variable'] = page('Una entrada, una variable, una salida',
        'El byte se guarda en RAM antes de transmitir; valores hipotéticos.', a)

    chars=[('6100','48','H'),('6101','4F','O'),('6102','4C','L'),('6103','41','A'),('6104','00','FIN')]
    a = ''
    for i,(addr,byte,ch) in enumerate(chars):
        x=23+i*197
        a += box(x, 170, 168, 166, '#e9f5e9' if i==4 else '#e7f1fb')
        a += t(x+84,210,addr,'small','middle')
        a += t(x+84,264,byte,'label','middle')
        a += t(x+84,310,ch,'small','middle')
    a += t(500, 390, 'X = 6100  |  FW_PUTS recorre hasta el byte 00 (sin imprimirlo).', 'small', 'middle')
    a += t(500, 432, 'Pantalla esperada: HOLA', 'label', 'middle')
    figures['c18_fig04_cadena_terminada'] = page('Cadena terminada en cero',
        'Cinco posiciones de memoria para cuatro caracteres ASCII.', a)

    a = ''
    for i in range(4):
        x=23+i*244
        fill='#e6f4e7' if i==2 else '#e7f1fb'
        a += lane(x, 164, 220, 174, fill, f'BLOQUE {i:04X}', f'Offset {i*256:04X}')
        a += t(x+110, 314, f'{i*256:04X}–{i*256+255:04X}', 'tiny', 'middle')
        if i<3: a += arrow(x+220, 257, x+244, 257)
    a += t(500, 393, 'BLOQUE 0002 = bytes 0200–02FF de la imagen.', 'small', 'middle')
    a += t(500, 435, 'El número de bloque no es el nombre de un archivo.', 'tiny', 'middle')
    figures['c19_fig01_bloques_y_offsets'] = page('Imagen dividida en unidades exactas de 256 bytes',
        'Los offsets se calculan como número de bloque × 256.', a)

    a=''
    names=list(reg.items())
    for i,(name, addr) in enumerate(names):
        col=i%2; row=i//2
        x=36 + col*492; y=126 + row*86
        a += box(x, y, 445, 71, '#e7f1fb' if name!='DATA' else '#f9eedc')
        a += t(x+75, y+45, addr, 'label', 'middle')
        a += t(x+251, y+44, name, 'label', 'middle')
    a += t(500, 487, 'Solo direcciones PARES; cada registro representa un byte.', 'tiny', 'middle')
    figures['c19_fig02_registros_controlador'] = page('Registros de un controlador de bloques candidato',
        'C010–C01F: ocho registros de 8 bits y direcciones impares reservadas.', a)

    status=storage['nominal_status']
    a=lane(29, 153, 220, 160, '#e7f1fb', f'REPOSO  {status["idle"]}', 'COUNT 0000')
    a+=lane(375, 153, 250, 160, '#f9eedc', f'ACTIVO  {status["transfer"]}', 'BUSY + DRQ')
    a+=lane(751, 153, 220, 160, '#e9f4e6', f'DONE  {status["done"]}', 'COUNT 0100')
    a+=arrow(249, 226, 375, 226)+arrow(625, 226, 751, 226)
    a+=t(310, 204, 'READ/WRITE', 'tiny', 'middle')+t(693, 205, '256 B', 'tiny', 'middle')
    a+=box(377, 356, 245, 91, '#fae5e1')
    a+=t(500, 394, f'ERROR  {status["error"]}', 'label','middle')
    a+=t(500, 426, 'bloque/comando inválido', 'tiny','middle')
    a+=arrow(500, 313, 500, 356, '#af4d39')
    a+=t(500, 477, 'RESET cancela y vuelve a REPOSO', 'tiny','middle')
    figures['c19_fig03_estados_transferencia'] = page('Estados y conteo de una transferencia de bloques',
        'La transición representa acceso lógico, no tiempo de reloj.', a)

    a=lane(27, 155, 448, 188, '#e7f1fb', 'LOAD crudo (futuro)', '256 bytes de bloque')
    a+=lane(526, 155, 448, 188, '#e9f4e6', 'LOADX AEX1 (futuro)', '32 cab. + 7 código + 217 relleno')
    a+=box(52, 364, 396, 85, '#f9eedc')
    a+=t(250, 398, 'RAM: 256 bytes', 'label','middle')
    a+=t(250, 429, 'incluye 249 bytes extra', 'tiny','middle')
    a+=box(552, 364, 396, 85, '#f9eedc')
    a+=t(750, 398, 'RAM: solo 7 útiles', 'label','middle')
    a+=t(750, 429, 'sin copiar la cabecera', 'tiny','middle')
    a+=arrow(251,343,251,364) + arrow(750,343,750,364)
    figures['c19_fig04_carga_cruda_y_aex1'] = page('Guardar bytes no equivale a cargar un ejecutable',
        'Ambos comandos son propuestas: ninguno funciona aún en ROM.', a)

    return figures


def main():
    inkscape=resolver_inkscape()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg_content in make_figures().items():
        svg=OUT/(name+'.svg')
        png=OUT/(name+'.png')
        svg.write_text(svg_content,encoding='utf-8')
        ET.parse(svg)  # Detectar XML roto ANTES de lanzar Inkscape.
        subprocess.run([inkscape,str(svg),'--export-type=png',
                        f'--export-filename={png}','--export-width=2000'],check=True)
        assert png.is_file() and png.stat().st_size>10000
        print('FIGURA VALIDADA:',svg.relative_to(ROOT),png.relative_to(ROOT))


if __name__=='__main__':
    main()
