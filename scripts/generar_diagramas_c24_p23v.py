#!/usr/bin/env python3
"""Once figuras exactas del interludio P23V y capítulo 24.

Solo describe memoria y comportamiento lógico. SVG originales, PNG por
Inkscape; matrices, direcciones y tamaños son verificables sin una CPU física.
"""
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from generar_diagramas_tecnicos_aula8 import arrow, box, lane, page, resolver_inkscape, t

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'libro' / 'figuras'

# Glifos originales 8x8, bit 7 = columna izquierda; no provienen de una ROM comercial.
GLYPHS = {
    'A': (0x18, 0x24, 0x42, 0x7E, 0x42, 0x42, 0x42, 0x00),
    'H': (0x42, 0x42, 0x42, 0x7E, 0x42, 0x42, 0x42, 0x00),
    'O': (0x3C, 0x42, 0x42, 0x42, 0x42, 0x42, 0x3C, 0x00),
    'L': (0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x7E, 0x00),
}
PALETTE = ('#101820', '#3c9a76', '#dc9245', '#f5f5ed')


def glyph_pixels(letter):
    return [[(row >> (7 - x)) & 1 for x in range(8)] for row in GLYPHS[letter]]


def matrix(letter, left, top, cell, ink='#143d58', bg='#fbfbf6'):
    a = ''
    for y, row in enumerate(glyph_pixels(letter)):
        for x, bit in enumerate(row):
            fill = ink if bit else bg
            a += (f'<rect x="{left+x*cell}" y="{top+y*cell}" width="{cell}" '
                  f'height="{cell}" fill="{fill}" stroke="#94a7b2" stroke-width="0.6"/>')
    return a


def text_grid(left, top, cell=24):
    # 32×16 celdas; HOLA ocupa offset 0..3. La cuadrícula no confunde celda con píxel.
    s = ''
    for y in range(16):
        for x in range(32):
            special = y == 0 and x < 4
            s += (f'<rect x="{left+x*cell}" y="{top+y*cell}" width="{cell}" '
                  f'height="{cell}" fill="{"#e9f4e6" if special else "#f6f8fa"}" '
                  f'stroke="#bdcbd4" stroke-width="0.8"/>')
            if special:
                s += t(left+x*cell+cell/2, top+y*cell+cell*.74, 'HOLA'[x], 'tiny', 'middle')
    return s


def figures():
    d = {}
    a = lane(29, 146, 225, 145, '#e7f1fb', 'CÓDIGO 0x41', 'carácter A')
    a += arrow(254, 217, 315, 217)
    a += lane(315, 146, 276, 145, '#f9eedc', 'ROM DE GLIFOS', '8 filas × 8 bits')
    a += arrow(591, 217, 672, 217)
    a += matrix('A', 700, 132, 37)
    a += t(165, 365, 'Filas hex de A:', 'small', 'middle')
    a += t(165, 407, '18 24 42 7E 42 42 42 00', 'small', 'middle')
    a += t(500, 474, 'El código identifica el glifo; no codifica los píxeles de su dibujo.', 'small', 'middle')
    d['p23v_fig01_codigo_glifo'] = page('De un byte a ocho filas de puntos',
        'Glifo A original; los cuadros oscuros corresponden exactamente a bits 1.', a)

    a = text_grid(92, 105, 21)
    a += t(868, 164, 'Fila 0,', 'small', 'middle') + t(868, 195, 'cols. 0..3', 'small', 'middle')
    a += t(868, 245, 'H O L A', 'label', 'middle')
    a += t(868, 293, 'bytes 0..3', 'small', 'middle')
    a += t(868, 349, '32 × 16', 'label', 'middle')
    a += t(868, 383, '= 512 B', 'small', 'middle')
    a += t(500, 472, 'Cada celda contiene un CÓDIGO, no un bloque de 64 bytes.', 'small', 'middle')
    d['p23v_fig02_mapa_texto_32x16'] = page('La RAM de texto es un mapa de 512 celdas',
        'Los cuatro primeros códigos de la fila cero forman HOLA; el glifo se consulta aparte.', a)

    a = lane(36, 136, 438, 151, '#e7f1fb', '1 bpp · SOLO COMPARACIÓN', '256×128 = 4096 bytes')
    a += lane(527, 136, 438, 151, '#e9f4e6', '2 bpp · V1 REAL', '256×128 = 8192 bytes')
    a += t(251, 338, 'x=7 → byte 0, bit 0', 'small', 'middle')
    a += t(251, 380, 'x=8 → byte 1, bit 7', 'small', 'middle')
    a += t(251, 422, '(255,127) → byte 4095, bit 0', 'small', 'middle')
    a += t(746, 338, '(8,0) → byte 2, bits 7–6', 'small', 'middle')
    a += t(746, 380, 'índice 2 → byte 80 en hex', 'small', 'middle')
    a += t(746, 422, '(255,127) → byte 8191, bits 1–0', 'small', 'middle')
    d['p23v_fig03_pixeles_y_offsets'] = page('Dos convenios distintos para ubicar un píxel',
        'El monocromo es hipotético; el dispositivo V1 usa 2 bits por píxel.', a)

    a = lane(20, 151, 214, 164, '#e7f1fb', 'CPU', 'LD/ST · dirección')
    a += lane(272, 151, 214, 164, '#f9eedc', 'FIRMWARE ROM', 'rutina en software')
    a += lane(524, 151, 214, 164, '#e9f4e6', 'CONTROLADOR', 'búfer y escaneo')
    a += lane(775, 151, 205, 164, '#e7f1fb', 'PANTALLA', 'caracteres o píxeles')
    a += arrow(234, 228, 272, 228) + arrow(486, 228, 524, 228) + arrow(738, 228, 775, 228)
    a += t(500, 385, 'ROM de glifos (2 KiB) → consultada por el controlador de texto.', 'small', 'middle')
    a += t(500, 425, 'Micro-ROM de control (si la hubiera) ≠ firmware ≠ ROM de caracteres.', 'small', 'middle')
    a += t(500, 468, 'El modelo lógico NO especifica reloj, conector ni placa física.', 'tiny', 'middle')
    d['p23v_fig04_rom_controlador'] = page('Cuatro responsabilidades que no son intercambiables',
        'La rutina PLOT sería software; la presentación del píxel corresponde al controlador.', a)

    a = lane(21, 145, 232, 147, '#e7f1fb', 'CPU / ISA', 'escritura absoluta')
    a += lane(295, 145, 209, 147, '#f9eedc', 'DECODIFICADOR', 'EA = C020')
    a += lane(549, 145, 209, 147, '#e9f4e6', 'REGISTROS', 'C024/C026/C028')
    a += lane(805, 145, 174, 147, '#e7f1fb', 'VRAM', 'offset 0002')
    a += arrow(253, 217, 295, 217) + arrow(504, 217, 549, 217) + arrow(758, 217, 805, 217)
    a += t(500, 350, '1) C020 ← 01 (ver gráficos)    2) C02A ← 0E (acceder bitmap)', 'small', 'middle')
    a += t(500, 399, '3) C024 ← 02, C026 ← 00    4) C028 ← 80', 'small', 'middle')
    a += t(500, 466, 'Dirección de CPU C028 ≠ puntero interno 0002 de la VRAM.', 'label', 'middle')
    d['p23v_fig05_tres_direcciones'] = page('La CPU no tiene que conocer el píxel como opcode',
        'Secuencia de ejemplo con registros ya especificados; sintaxis de ISA aún candidata.', a)

    a = ''
    patterns = [(1,2,'4096 B',('#171d25','#f7f7f4')),
                (2,4,'8192 B',PALETTE),
                (4,16,'16384 B',('#101820','#264e5d','#3c9a76','#dc9245')),
                (8,256,'32768 B',('#101820','#264e5d','#3c9a76','#dc9245'))]
    for i,(bpp, n, size, colors) in enumerate(patterns):
        x = 24 + i*247
        a += box(x, 143, 220, 278, '#f7f9fc')
        a += t(x+110, 189, f'{bpp} bpp', 'label', 'middle')
        a += t(x+110, 226, f'{n} índices', 'small', 'middle')
        for y in range(8):
            for xx in range(8):
                idx = ((xx//2) + (y//2)) % len(colors)
                color = colors[idx]
                a += f'<rect x="{x+48+xx*16}" y="{243+y*16}" width="16" height="16" fill="{color}"/>'
        a += t(x+110, 400, size, 'small', 'middle')
    a += t(500, 472, 'El patrón es orientativo; 4/8 bpp NO están implementados en V1.', 'tiny', 'middle')
    d['p23v_fig06_profundidad_color'] = page('El coste de representar una imagen',
        'Todos los tamaños suponen 256×128 píxeles empaquetados, sin relleno ni cabecera.', a)

    a = matrix('A', 55, 159, 29)
    a += t(171, 428, 'Matriz 8×8', 'small', 'middle')
    a += box(370, 141, 259, 279, '#f7f9fc')
    a += '<path d="M427 361 L496 193 L564 361 M452 294 H540" fill="none" stroke="#17627c" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>'
    a += '<path d="M439 337 C446 308,461 270,476 226" fill="none" stroke="#e6a341" stroke-width="3" stroke-dasharray="8 8"/>'
    a += t(500, 445, 'Contorno vectorial original', 'small', 'middle')
    a += box(682, 141, 279, 279, '#f7f9fc')
    a += '<path d="M739 361 L807 193 L875 361 M765 294 H850" fill="none" stroke="#17627c" stroke-width="17" stroke-linejoin="round"/>'
    a += t(824, 445, 'Contorno rasterizado', 'small', 'middle')
    d['p23v_fig07_tipografia_y_contornos'] = page('Del glifo cuadriculado al contorno escalable',
        'Comparación conceptual; los tres diseños son originales, sin fuente comercial.', a)

    a = lane(22, 145, 290, 215, '#e7f1fb', 'EXPLICADO', 'bits, registros, memoria')
    a += lane(356, 145, 290, 215, '#e9f4e6', 'MODELO COMPROBADO', 'Python, diagramas, PDF')
    a += lane(689, 145, 289, 215, '#fce8e8', 'PENDIENTE', 'CPU, ROM, hardware')
    a += arrow(312, 252, 356, 252) + arrow(646, 252, 689, 252)
    a += t(500, 452, 'Un manuscrito completo no equivale a una microcomputadora construida.', 'small', 'middle')
    d['c24_fig01_alcances_y_evidencias'] = page('Tres formas de decir «funciona»',
        'Teoría, simulación de referencia y verificación física producen evidencias diferentes.', a)

    a = ''
    areas = [('0000–7FFF', 'RAM CPU · 32 KiB', '#e9f4e6'),
             ('8000–BFFF', 'Expansión reservada', '#f9eedc'),
             ('C000–C0FF', 'MMIO · terminal y controladores', '#e7f1fb'),
             ('C100–DFFF', 'Reservado', '#f9eedc'),
             ('E000–FFFF', 'ROM firmware CPU · 8 KiB', '#e9f4e6')]
    for i,(addr,desc,color) in enumerate(areas):
        y = 113 + i*66
        a += box(48,y,905,55,color)
        a += t(169,y+37,addr,'label','middle')
        a += t(640,y+37,desc,'small','middle')
    a += t(500, 484, 'Vídeo: C020–C02F es MMIO; sus 8704 B de VRAM son internos.', 'small', 'middle')
    d['c24_fig02_mapa_final'] = page('Mapa de 65536 direcciones de byte',
        'Contrato lógico; un rango reservado no se convierte mágicamente en memoria.', a)

    a = ''
    steps = [('1. SEMÁNTICA', 'ejemplos exactos'), ('2. HERRAMIENTAS', 'assembler / test'),
             ('3. SIMULACIÓN', 'ciclos y buses'), ('4. PROTOTIPO', 'medición real')]
    for i,(h,body) in enumerate(steps):
        x = 19 + i*247
        a += lane(x, 162, 226, 184, '#e9f4e6' if i==0 else '#e7f1fb', h, body)
        if i<3: a += arrow(x+226,249,x+247,249)
    a += t(500, 432, 'Cada etapa añade pruebas; ninguna puede omitirse por confianza.', 'small', 'middle')
    d['c24_fig04_escalera_verificacion'] = page('La evidencia crece junto con la máquina',
        'La primera etapa usa modelos anfitriones; las demás requieren nuevos artefactos.', a)

    a = lane(30, 137, 443, 135, '#e9f4e6', 'AULA-8', 'bus 8 bits; natural 8 bits')
    a += lane(526, 137, 443, 135, '#e7f1fb', 'AULA-16', 'bus 16 bits; natural 16 bits')
    a += lane(260, 341, 483, 112, '#f9eedc', 'MISMO PROBLEMA', 'almacenar → sumar → Euclides → Fibonacci')
    a += arrow(260,272,400,341) + arrow(750,272,601,341)
    a += t(500, 492, 'Algoritmos compartidos; ISA, ABI y binarios NO compartidos.', 'tiny', 'middle')
    d['c24_fig03_dos_arquitecturas_un_metodo'] = page('Dos máquinas: una disciplina de razonamiento',
        'Comparar resultados y modelos no significa prometer compatibilidad binaria.', a)
    return d


def validate_math():
    assert len(GLYPHS) == 4 and all(len(v)==8 for v in GLYPHS.values())
    assert glyph_pixels('A')[0] == [0,0,0,1,1,0,0,0]
    assert [ord(c) for c in 'HOLA'] == [0x48,0x4f,0x4c,0x41]
    assert 32*16 == 512
    assert [256*128*b//8 for b in (1,2,4,8)] == [4096,8192,16384,32768]
    assert (0*256+7)//8 == 0 and (0*256+8)//8 == 1
    assert (127*256+255)//8 == 4095
    assert 0*64+8//4 == 2 and 127*64+255//4 == 8191
    assert (2 << (6-2*(8%4))) == 0x80


def main():
    validate_math()
    OUT.mkdir(parents=True,exist_ok=True)
    inkscape=resolver_inkscape()
    fs=figures()
    assert len(fs)==11
    for name,svg in fs.items():
        target=OUT / f'{name}.svg'
        image=OUT / f'{name}.png'
        ET.fromstring(svg)
        target.write_text(svg, encoding='utf-8')
        subprocess.run([inkscape,str(target),'--export-type=png',f'--export-filename={image}',
                        '--export-width=2000'],check=True,capture_output=True,text=True)
        assert image.stat().st_size > 10000
        print(name,image.stat().st_size)


if __name__=='__main__':
    main()
