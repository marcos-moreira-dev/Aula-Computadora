#!/usr/bin/env python3
"""Cuatro dibujos SVG+PNG originales del capítulo 9, todos conceptuales."""
import subprocess

from generar_figuras_capitulo_01 import ROOT, STYLE


OUT = ROOT / 'libro' / 'figuras'


def wrap(title, contents):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" '
            f'viewBox="0 0 1000 500"><title>{title}</title>'
            f'<rect width="1000" height="500" fill="white"/>{STYLE}{contents}</svg>')


def rect(x, y, w, h, color='#e6f3fa'):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" '
            f'fill="{color}" stroke="#28465b" stroke-width="3"/>')


FIGS = {}

FIGS['c09_fig01_celda_sram_conceptual'] = wrap('Celda SRAM de seis transistores, abstracción lógica', '''
<text x="37" y="46" class="label">SRAM: conservar un bit y habilitar su acceso</text>
<text x="39" y="80" class="small">Dos inversores se realimentan; WL gobierna dos accesos hacia las líneas de bit.</text>
<rect x="40" y="116" width="922" height="319" rx="17" fill="#f5f8fa" stroke="#bbccd7"/>
''' + rect(335, 218, 142, 79, '#e2f3e8') + rect(547, 218, 142, 79, '#e2f3e8') + '''
<text x="406" y="263" class="label" text-anchor="middle">INV 1</text>
<text x="618" y="263" class="label" text-anchor="middle">INV 2</text>
<path class="wire" d="M335,258 H299 V329 H726 V258 H689"/>
<path class="wire" d="M477,258 H547"/>
<text x="506" y="284" class="tiny" text-anchor="middle">Q̅</text>
<text x="516" y="346" class="tiny" text-anchor="middle">Q</text>
''' + rect(201, 206, 87, 66, '#fff3dc') + rect(740, 206, 87, 66, '#fff3dc') + '''
<text x="245" y="247" class="small" text-anchor="middle">Acceso</text>
<text x="784" y="247" class="small" text-anchor="middle">Acceso</text>
<path class="wire" d="M112,240 H201 M827,240 H916"/>
<text x="111" y="213" class="label accent">BL</text>
<text x="883" y="213" class="label accent">BL̅</text>
<path class="wire" d="M245,150 V206 M784,150 V206 M245,150 H784"/>
<text x="493" y="138" class="label accent" text-anchor="middle">WL: línea de palabra</text>
<path class="wire" d="M288,240 H335 M512,258 V184 H740 V240"/>
<text x="500" y="403" class="small" text-anchor="middle">Núcleo lógico de realimentación + dos transistores de acceso</text>
<text x="500" y="473" class="tiny" text-anchor="middle">Bloques funcionales; no es un esquema 6T de transistores ni incluye prelectura y amplificador.</text>
''')

FIGS['c09_fig02_sram_pines'] = wrap('Interfaz funcional SRAM 32K por 8', '''
<text x="37" y="45" class="label">AS6C62256: el chip lleva dentro la matriz y sus decodificadores</text>
<text x="40" y="83" class="small">Las etiquetas son nombres de señal, no números físicos de patilla.</text>
''' + rect(332, 141, 346, 277, '#e2f3e8') + '''
<text x="505" y="193" class="label" text-anchor="middle">SRAM AS6C62256</text>
<text x="505" y="228" class="small" text-anchor="middle">32K posiciones × 8 bits</text>
<text x="505" y="278" class="small" text-anchor="middle">Decodificador + matriz</text>
<text x="505" y="315" class="small" text-anchor="middle">Lectura + escritura</text>
<path class="wire" d="M67,212 H332"/>
<path d="M317,202 l15,10 -15,10" fill="none" stroke="#28465b" stroke-width="3"/>
<text x="75" y="193" class="label accent">A0…A14 (15)</text>
<path class="wire" d="M678,212 H939"/>
<path d="M693,202 l-15,10 15,10 M924,202 l15,10 -15,10" fill="none" stroke="#28465b" stroke-width="3"/>
<text x="712" y="189" class="label accent">DQ0…DQ7 (8)</text>
<path class="wire" d="M174,364 H332"/>
<text x="73" y="351" class="small accent">CE#, OE#, WE#</text>
<path class="wire" d="M504,113 V141 M504,418 V454"/>
<text x="521" y="130" class="tiny">VCC</text>
<text x="520" y="446" class="tiny">VSS</text>
<text x="500" y="482" text-anchor="middle" class="tiny">Los detalles de alimentación y tiempos dependen de la hoja de datos del modelo y encapsulado exactos.</text>
''')

FIGS['c09_fig03_mapa_64k_ejemplo'] = wrap('Mapa de memoria ilustrativo 64 KiB', '''
<text x="37" y="46" class="label">Un espacio de 64 KiB no implica 64 KiB de RAM instalada</text>
<text x="38" y="81" class="small">Ejemplo de reparto: capacidad física, ventanas de dirección y regiones sin asignación.</text>
<rect x="181" y="116" width="230" height="320" fill="none" stroke="#28465b" stroke-width="3"/>
<rect x="184" y="119" width="224" height="154" fill="#cfe9f5"/>
<rect x="184" y="276" width="224" height="114" fill="#eeeef1"/>
<rect x="184" y="393" width="224" height="40" fill="#ddf0df"/>
<path class="wire" d="M182,275 H410 M182,392 H410"/>
<text x="88" y="127" class="small">0x0000</text>
<text x="88" y="286" class="small">0x8000</text>
<text x="88" y="404" class="small">0xE000</text>
<text x="88" y="443" class="small">0xFFFF</text>
<path class="wire" d="M412,187 H499 M412,338 H499 M412,412 H499"/>
<text x="520" y="182" class="label accent">SRAM · 32 KiB</text>
<text x="521" y="209" class="small">0x0000 – 0x7FFF</text>
<text x="521" y="237" class="tiny">A15 = 0; dirección interna A14…A0</text>
<text x="520" y="325" class="label">Sin asignación · 24 KiB</text>
<text x="521" y="352" class="small">0x8000 – 0xDFFF</text>
<text x="520" y="395" class="label accent">EEPROM · 8 KiB</text>
<text x="521" y="425" class="small">0xE000 – 0xFFFF</text>
<text x="521" y="449" class="tiny">A15:A13 = 111; A12…A0 internos</text>
<text x="500" y="487" class="tiny" text-anchor="middle">Mapa únicamente ilustrativo; no establece el reparto final de memoria o E/S de Aula.</text>
''')

FIGS['c09_fig04_expansion_profundidad_anchura'] = wrap('Expandir profundidad frente a anchura de una memoria', '''
<text x="36" y="43" class="label">Dos chips iguales pueden ampliar posiciones o ampliar bits por posición</text>
<text x="37" y="78" class="small">Las dos opciones almacenan 64 KiB de datos, pero sus accesos son distintos.</text>
<rect x="37" y="102" width="445" height="347" rx="16" fill="#f0f7fb" stroke="#b4d0de" stroke-width="2"/>
<rect x="518" y="102" width="445" height="347" rx="16" fill="#f3f8f0" stroke="#aacbaa" stroke-width="2"/>
<text x="260" y="138" class="label" text-anchor="middle">Profundidad</text>
<text x="741" y="138" class="label" text-anchor="middle">Anchura</text>
''' + rect(92, 203, 156, 67) + rect(282, 203, 156, 67) + '''
<text x="170" y="242" class="small" text-anchor="middle">32K × 8</text>
<text x="360" y="242" class="small" text-anchor="middle">32K × 8</text>
<path class="wire" d="M170,186 V203 M360,186 V203"/>
<text x="264" y="161" class="tiny" text-anchor="middle">A15 decide qué CE# se activa</text>
<text x="170" y="181" class="tiny" text-anchor="middle">CE0#</text>
<text x="360" y="181" class="tiny" text-anchor="middle">CE1#</text>
<text x="260" y="302" class="small" text-anchor="middle">Comparten A14…A0 y D7…D0</text>
<rect x="85" y="335" width="370" height="65" rx="12" fill="white" stroke="#b4d0de"/>
<text x="270" y="374" class="label accent" text-anchor="middle">64K × 8 bits</text>
''' + rect(568, 203, 158, 67, '#e2f3e8') + rect(757, 203, 158, 67, '#e2f3e8') + '''
<text x="647" y="242" class="small" text-anchor="middle">32K × 8</text>
<text x="836" y="242" class="small" text-anchor="middle">32K × 8</text>
<text x="741" y="163" class="tiny" text-anchor="middle">Ambos responden a la misma dirección</text>
<path class="wire" d="M741,175 H647 V203 M741,175 H836 V203"/>
<text x="647" y="297" class="tiny" text-anchor="middle">D7…D0</text>
<text x="838" y="297" class="tiny" text-anchor="middle">D15…D8</text>
<rect x="550" y="335" width="386" height="65" rx="12" fill="white" stroke="#aacbaa"/>
<text x="743" y="374" class="label accent" text-anchor="middle">32K × 16 bits</text>
<text x="500" y="484" class="tiny" text-anchor="middle">Ambas son demostraciones de organización; no reemplazan el mapa ni los bancos de Aula-16.</text>
''')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg_content in FIGS.items():
        path_svg = OUT / f'{name}.svg'
        path_png = OUT / f'{name}.png'
        path_svg.write_text(svg_content, encoding='utf-8')
        subprocess.run(['inkscape', str(path_svg), '--export-type=png',
                        f'--export-filename={path_png}', '--export-width=2000'], check=True)
        print('Ilustración:', path_png.relative_to(ROOT))


if __name__ == '__main__':
    main()
