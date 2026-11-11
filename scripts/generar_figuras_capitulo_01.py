#!/usr/bin/env python3
"""Produce cuatro diagramas eléctricos originales, en SVG editable y PNG."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "libro" / "figuras"

STYLE = '''
<style>
  text {font-family: 'DejaVu Sans', Arial, sans-serif; fill:#1b2a38}
  .wire {stroke:#273746;stroke-width:4;fill:none;stroke-linejoin:round;stroke-linecap:round}
  .node {fill:#273746}
  .block {fill:#f0f6fb;stroke:#273746;stroke-width:3}
  .label {font-size:22px;font-weight:bold}
  .small {font-size:17px}
  .tiny {font-size:15px}
  .accent {fill:#096b91}
  .light {fill:#fbe2aa;stroke:#ad7200;stroke-width:3}
  .red {stroke:#b64a30;fill:none;stroke-width:3}
</style>'''

def wrap(children, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="490" viewBox="0 0 1000 490">
<title>{title}</title><rect width="1000" height="490" fill="white"/>{STYLE}
{children}</svg>'''

def source(x=110, y=160):
    return f'''<rect class="block" x="{x-61}" y="{y-49}" width="122" height="128" rx="12"/>
<text x="{x}" y="{y-15}" class="label" text-anchor="middle">5 V</text>
<text x="{x}" y="{y+14}" class="small" text-anchor="middle">CC</text>
<text x="{x}" y="{y+41}" class="tiny" text-anchor="middle">regulada</text>
<text x="{x-19}" y="{y-70}" class="label" text-anchor="middle">+</text>
<text x="{x-19}" y="{y+102}" class="label" text-anchor="middle">−</text>'''

def led(cx, top, bottom):
    cy = (top + bottom)/2
    return f'''<rect x="{cx-54}" y="{top}" width="108" height="{bottom-top}" rx="14" class="light"/>
<text x="{cx}" y="{cy+2}" class="label" text-anchor="middle">LED</text>
<text x="{cx}" y="{cy+29}" class="tiny" text-anchor="middle">rojo</text>
<text x="{cx-77}" y="{top+7}" class="tiny">A (+)</text>
<text x="{cx-77}" y="{bottom+17}" class="tiny">K (−)</text>
<path class="red" d="M {cx+61},{cy-21} l 22,-22 m -8,0 l 8,0 l 0,8 M {cx+70},{cy-3} l 22,-22 m -8,0 l 8,0 l 0,8"/>'''

FIGS = {}
FIGS["c01_fig01_lazo_serie"] = wrap('''
<text x="37" y="39" class="label">Un circuito cerrado: una sola ruta para la corriente</text>
<path class="wire" d="M110,111 V87 H276 M390,87 H620 V173 M620,255 V340 H110 V239"/>
''' + source(110,160) + '''
<rect class="block" x="276" y="65" width="114" height="44" rx="7"/>
<text x="333" y="94" class="label" text-anchor="middle">330 Ω</text>
''' + led(620,173,255) + '''
<path d="M432,70 h91 l-17,-12 m17,12 l-17,12" class="wire"/>
<text x="475" y="125" class="small accent" text-anchor="middle">I (convencional)</text>
<text x="333" y="129" class="small" text-anchor="middle">Resistencia R</text>
<text x="620" y="373" class="small" text-anchor="middle">Retorno a la fuente</text>
<rect x="64" y="403" width="872" height="54" rx="10" fill="#ecf5fb"/>
<text x="500" y="438" class="small" text-anchor="middle">La resistencia y el LED están en serie: comparten la misma corriente.</text>
''', "Circuito en serie con fuente de 5 V, resistencia de 330 ohmios y LED rojo")

FIGS["c01_fig02_medir_tension"] = wrap('''
<text x="37" y="39" class="label">Para medir tensión, conectar el voltímetro en paralelo</text>
<path class="wire" d="M110,111 V87 H278 M390,87 H570 V173 M570,257 V341 H110 V239"/>
''' + source(110,160) + '''
<rect class="block" x="278" y="65" width="112" height="44" rx="7"/>
<text x="334" y="94" class="label" text-anchor="middle">330 Ω</text>
''' + led(570,173,257) + '''
<path class="wire" d="M570,156 V128 H772 V181 M772,237 V289 H570 V257"/>
<circle class="block" cx="772" cy="209" r="30"/>
<text x="772" y="217" class="label" text-anchor="middle">V</text>
<circle class="node" cx="570" cy="156" r="6"/>
<circle class="node" cx="570" cy="289" r="6"/>
<text x="830" y="202" class="small">Multímetro</text>
<text x="830" y="224" class="tiny">modo V CC</text>
<text x="686" y="113" class="tiny">Punta roja</text>
<text x="686" y="315" class="tiny">Punta negra</text>
<rect x="64" y="394" width="872" height="68" rx="10" fill="#ecf5fb"/>
<text x="500" y="422" class="small" text-anchor="middle">El medidor compara la tensión entre dos nodos del LED.</text>
<text x="500" y="449" class="tiny" text-anchor="middle">Conexión conceptual; antes de usar el instrumento, verificar bornes y rango.</text>
''', "Voltímetro conectado en paralelo a los extremos del LED")

FIGS["c01_fig03_medir_corriente"] = wrap('''
<text x="37" y="39" class="label">Para medir corriente, intercalar el amperímetro en serie</text>
<path class="wire" d="M110,111 V87 H263 M375,87 H478 M544,87 H674 V173 M674,257 V341 H110 V239"/>
''' + source(110,160) + '''
<rect class="block" x="263" y="65" width="112" height="44" rx="7"/>
<text x="319" y="94" class="label" text-anchor="middle">330 Ω</text>
<circle class="block" cx="511" cy="87" r="33"/>
<text x="511" y="96" class="label" text-anchor="middle">A</text>
''' + led(674,173,257) + '''
<text x="511" y="144" class="tiny" text-anchor="middle">Multímetro en A CC</text>
<text x="511" y="165" class="tiny" text-anchor="middle">(borne mA/A según rango)</text>
<rect x="64" y="392" width="872" height="71" rx="10" fill="#fff2e8"/>
<text x="500" y="418" class="small" text-anchor="middle">No unir los bornes del amperímetro entre +5 V y GND:</text>
<text x="500" y="445" class="small" text-anchor="middle">se produciría un cortocircuito potencialmente peligroso.</text>
''', "Amperímetro instalado en serie; advertencia contra cortocircuito")

FIGS["c01_fig04_protoboard_conexiones"] = wrap('''
<text x="35" y="38" class="label">El mismo circuito, ahora en las conexiones de una protoboard</text>
<rect x="80" y="65" width="840" height="348" rx="17" fill="#f7f9fa" stroke="#aabac3" stroke-width="2"/>
<text x="110" y="111" class="small" fill="#b64a30">+ 5 V</text>
<rect x="208" y="92" width="635" height="34" rx="10" fill="#fce5dd"/>
<path d="M240,110 H819" stroke="#b64a30" stroke-width="5"/>
<text x="112" y="383" class="small">− GND</text>
<rect x="208" y="360" width="635" height="36" rx="10" fill="#e7f1fb"/>
<path d="M240,379 H819" stroke="#296a9b" stroke-width="5"/>
<text x="171" y="229" class="small">fila 3</text>
<text x="171" y="305" class="small">fila 8</text>
<rect x="252" y="201" width="244" height="42" rx="9" fill="#e1f1e6" stroke="#9ac7a9"/>
<rect x="252" y="278" width="244" height="42" rx="9" fill="#e1f1e6" stroke="#9ac7a9"/>
<g fill="white" stroke="#495a66" stroke-width="2">
<circle cx="271" cy="222" r="8"/><circle cx="321" cy="222" r="8"/>
<circle cx="371" cy="222" r="8"/><circle cx="421" cy="222" r="8"/>
<circle cx="471" cy="222" r="8"/>
<circle cx="271" cy="299" r="8"/><circle cx="321" cy="299" r="8"/>
<circle cx="371" cy="299" r="8"/><circle cx="421" cy="299" r="8"/>
<circle cx="471" cy="299" r="8"/>
</g>
<path d="M371,110 V149 M371,193 V222" class="wire"/>
<rect x="354" y="149" width="34" height="44" rx="6" fill="#f1d0a6" stroke="#77583a" stroke-width="2"/>
<text x="408" y="171" class="tiny">330 Ω</text>
<path d="M421,222 V246 M421,282 V299" class="wire"/>
<rect x="404" y="246" width="34" height="36" rx="9" fill="#ffdda0" stroke="#ad7200" stroke-width="2"/>
<text x="506" y="263" class="tiny">LED</text>
<text x="506" y="283" class="tiny">A (+)</text>
<text x="548" y="331" class="tiny">K (−)</text>
<path d="M471,299 H521 V379" class="wire"/>
<text x="635" y="208" class="small">Los cinco orificios de</text>
<text x="635" y="233" class="small">una fila se conectan</text>
<text x="635" y="258" class="small">por dentro de la placa.</text>
<text x="635" y="300" class="tiny">Fila 3 ≠ fila 8.</text>
<text x="635" y="329" class="tiny">Los rieles son independientes.</text>
<rect x="75" y="424" width="850" height="47" rx="9" fill="#ecf5fb"/>
<text x="500" y="452" class="tiny" text-anchor="middle">Vista didáctica: comprobar la continuidad real de rieles y grupos en cada protoboard.</text>
''', "Protoboard didáctica: resistor, LED y conexión interna de hileras")

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in FIGS.items():
        svg_path = OUT / (name + ".svg")
        png_path = OUT / (name + ".png")
        svg_path.write_text(svg, encoding="utf-8")
        subprocess.run(["inkscape", str(svg_path), "--export-type=png",
                        f"--export-filename={png_path}", "--export-width=2000"],
                       check=True, stdout=subprocess.DEVNULL)
        print(f"Figura lista: {png_path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
