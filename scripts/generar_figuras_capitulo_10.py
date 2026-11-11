#!/usr/bin/env python3
"""Genera cuatro láminas técnicas vectoriales para el capítulo 10."""
import subprocess

from generar_figuras_capitulo_01 import ROOT, STYLE

OUT = ROOT / 'libro' / 'figuras'


def wrap(title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" '
            f'viewBox="0 0 1000 500"><title>{title}</title>'
            f'<rect width="1000" height="500" fill="white"/>{STYLE}{body}</svg>')


def rect(x, y, w, h, color='#e6f3fa'):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" '
            f'fill="{color}" stroke="#28465b" stroke-width="3"/>')


FIGS = {}

FIGS['c10_fig01_medio_sumador'] = wrap('Medio sumador: XOR y AND', '''
<text x="37" y="46" class="label">Un medio sumador produce una suma y un acarreo</text>
<text x="38" y="79" class="small">Dos bits entran en paralelo a dos funciones lógicas; no hay Cin.</text>
''' + rect(62, 177, 197, 131, '#f4f7fa') + '''
<text x="160" y="219" class="label" text-anchor="middle">Entradas</text>
<text x="160" y="258" class="small" text-anchor="middle">A y B</text>
''' + rect(379, 137, 252, 111, '#e3f1e7') + rect(379, 295, 252, 111, '#fff2d9') + '''
<path class="wire" d="M259,214 H315 V192 H379"/>
<path class="wire" d="M259,270 H315 V351 H379"/>
<text x="328" y="179" class="tiny" text-anchor="middle">A, B</text>
<text x="328" y="372" class="tiny" text-anchor="middle">A, B</text>
<text x="505" y="183" class="label" text-anchor="middle">XOR</text>
<text x="505" y="215" class="small" text-anchor="middle">distintos → 1</text>
<text x="505" y="341" class="label" text-anchor="middle">AND</text>
<text x="505" y="373" class="small" text-anchor="middle">ambos 1 → 1</text>
<path class="wire" d="M631,192 H792 M631,350 H792"/>
<text x="804" y="201" class="label accent">S = A ⊕ B</text>
<text x="804" y="359" class="label accent">C = A ∧ B</text>
<text x="499" y="462" class="small" text-anchor="middle">Con A=B=1: S=0 y C=1, es decir, 1 + 1 = 10 en binario.</text>
<text x="500" y="486" class="tiny" text-anchor="middle">Las líneas marcadas A, B representan dos señales separadas, no un cortocircuito.</text>
''')

FIGS['c10_fig02_sumador_completo'] = wrap('Sumador completo con dos medios sumadores y OR', '''
<text x="37" y="46" class="label">El sumador completo recibe también el acarreo anterior</text>
<text x="38" y="81" class="small">Dos medios sumadores más una OR: P es la suma parcial; G y H son acarreos parciales.</text>
''' + rect(184, 157, 228, 111, '#e3f1e7') + rect(534, 157, 228, 111, '#e3f1e7') + rect(534, 352, 228, 83, '#fff2d9') + '''
<text x="297" y="205" class="label" text-anchor="middle">Medio sumador 1</text>
<text x="297" y="237" class="small" text-anchor="middle">P = A XOR B</text>
<text x="647" y="205" class="label" text-anchor="middle">Medio sumador 2</text>
<text x="647" y="237" class="small" text-anchor="middle">S = P XOR Cin</text>
<text x="647" y="401" class="label" text-anchor="middle">OR de G y H</text>
<path class="wire" d="M76,190 H184 M76,238 H184"/>
<text x="61" y="195" class="label accent">A</text>
<text x="61" y="243" class="label accent">B</text>
<path class="wire" d="M412,190 H534"/>
<text x="470" y="177" class="label accent" text-anchor="middle">P</text>
<path class="wire" d="M647,107 V157"/>
<text x="666" y="128" class="label accent">Cin</text>
<path class="wire" d="M762,193 H892"/>
<text x="904" y="201" class="label accent">S</text>
<path class="wire" d="M296,268 V393 H534"/>
<text x="317" y="329" class="label accent">G</text>
<path class="wire" d="M650,268 V352"/>
<text x="669" y="324" class="label accent">H</text>
<path class="wire" d="M762,394 H864"/>
<text x="875" y="401" class="label accent">Cout</text>
<text x="500" y="479" class="tiny" text-anchor="middle">Cout = (A AND B) OR (Cin AND (A XOR B)); el dibujo es funcional.</text>
''')


def bit_columns():
    bits_a = '00001101'
    bits_b = '00001001'
    bits_cin = '00010010'  # C7 ... C0: bit 4 y bit 1 reciben acarreo.
    bits_s = '00010110'
    columns = ''
    for j in range(8):
        x = 301 + 79 * j
        i = 7 - j
        columns += f'<text x="{x}" y="157" class="tiny" text-anchor="middle">i={i}</text>'
        if bits_cin[j] == '1':
            columns += f'<rect x="{x-24}" y="177" width="48" height="38" rx="9" fill="#ffe6ad"/>'
        if bits_s[j] == '1':
            columns += f'<rect x="{x-24}" y="350" width="48" height="38" rx="9" fill="#dbf2df"/>'
        for y, val in ((205, bits_cin[j]), (266, bits_a[j]), (322, bits_b[j]), (378, bits_s[j])):
            columns += f'<text x="{x}" y="{y}" class="label" text-anchor="middle">{val}</text>'
    return columns


FIGS['c10_fig03_suma_trece_mas_nueve'] = wrap('Suma manual con acarreos 13 más 9', '''
<text x="37" y="46" class="label">13 + 9: leer los acarreos de derecha a izquierda</text>
<text x="38" y="81" class="small">Cada columna usa su A, B y el acarreo que llegó desde la columna de menor peso.</text>
<rect x="60" y="115" width="889" height="309" rx="16" fill="#f5f8fa" stroke="#c1d3de"/>
<text x="90" y="205" class="small">Cin</text>
<text x="90" y="266" class="small">A = 13</text>
<text x="90" y="322" class="small">B = 9</text>
<text x="90" y="378" class="small accent">S = 22</text>
<path class="wire" d="M242,337 H920"/>
''' + bit_columns() + '''
<text x="500" y="453" class="small" text-anchor="middle">C1 = 1 y C4 = 1; los demás acarreos de entrada valen cero.</text>
<text x="500" y="483" class="tiny" text-anchor="middle">S = 00010110₂ = 16 + 4 + 2 = 22₁₀. Las columnas se rotulan i=7…0.</text>
''')


def ripple_boxes():
    result = ''
    for i in range(8):
        x = 71 + 109 * i
        result += rect(x, 163, 82, 88, '#e4f3e9')
        result += (f'<text x="{x+41}" y="198" class="label" text-anchor="middle">FA{i}</text>'
                   f'<text x="{x+41}" y="228" class="tiny" text-anchor="middle">S{i}</text>'
                   f'<path class="wire" d="M{x+41},119 V163"/>'
                   f'<text x="{x+41}" y="107" class="tiny" text-anchor="middle">A{i},B{i}</text>')
        if i != 7:
            result += (f'<path class="wire" d="M{x+82},206 H{x+109}"/>'
                       f'<text x="{x+95}" y="193" class="tiny" text-anchor="middle">C{i+1}</text>')
    return result


FIGS['c10_fig04_cadena_y_dos_bytes'] = wrap('Acarreo propagado en 8 bits y dos bytes', '''
<text x="37" y="46" class="label">El acarreo conecta cada etapa con la siguiente</text>
<text x="38" y="80" class="small">La etapa FA0 trabaja con el bit de menor peso; FA7 recibe el último acarreo interno.</text>
''' + ripple_boxes() + '''
<path class="wire" d="M35,206 H71 M916,206 H968"/>
<text x="33" y="192" class="tiny">C0=0</text>
<text x="929" y="190" class="tiny">C8</text>
<text x="500" y="287" class="small" text-anchor="middle">Ocho sumadores completos: las salidas S0...S7 forman un byte.</text>
''' + rect(71, 323, 389, 115, '#eef6fc') + rect(541, 323, 389, 115, '#f1f8ec') + '''
<text x="265" y="353" class="label" text-anchor="middle">Primera pasada: byte bajo</text>
<text x="265" y="391" class="small" text-anchor="middle">FF + 01 + 0 = 100 (hex)</text>
<text x="265" y="420" class="tiny" text-anchor="middle">Sale 00, pasa acarreo 1</text>
<text x="736" y="353" class="label" text-anchor="middle">Segunda pasada: byte alto</text>
<text x="736" y="391" class="small" text-anchor="middle">01 + 00 + 1 = 02 (hex)</text>
<text x="736" y="420" class="tiny" text-anchor="middle">Resultado global 0x0200</text>
<path class="wire" d="M460,388 H541"/>
<text x="501" y="376" class="tiny accent" text-anchor="middle">carry</text>
<text x="500" y="485" class="tiny" text-anchor="middle">El ejemplo de dos bytes usa una ALU de 8 bits en dos pasos; no es un diagrama temporal ni un plano eléctrico.</text>
''')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, content in FIGS.items():
        svg = OUT / f'{name}.svg'
        png = OUT / f'{name}.png'
        svg.write_text(content, encoding='utf-8')
        subprocess.run(['inkscape', str(svg), '--export-type=png',
                        f'--export-filename={png}', '--export-width=2000'], check=True)
        print('Figura:', png.relative_to(ROOT))


if __name__ == '__main__':
    main()
