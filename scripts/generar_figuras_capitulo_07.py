#!/usr/bin/env python3
"""Cuatro diagramas didácticos de registro de 8 bits y bus compartido."""
import subprocess

from generar_figuras_capitulo_01 import ROOT, STYLE


OUT = ROOT / "libro" / "figuras"


def wrap(title: str, contents: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" '
            f'viewBox="0 0 1000 500"><title>{title}</title>'
            f'<rect width="1000" height="500" fill="white"/>{STYLE}{contents}</svg>')


def rect(x, y, w, h, label, bg="#e6f3fa", font="label"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
            f'fill="{bg}" stroke="#28465b" stroke-width="3"/>'
            f'<text x="{x+w/2}" y="{y+h/2+7}" text-anchor="middle" '
            f'class="{font}">{label}</text>')


FIGS = {}

pieces = [
    f'<rect x="{45+i*115}" y="162" width="100" height="142" rx="11" '
    'fill="#e8f4fb" stroke="#28465b" stroke-width="2"/>'
    f'<text x="{95+i*115}" y="193" class="small" text-anchor="middle">b{7-i}</text>'
    f'<text x="{95+i*115}" y="246" class="label" text-anchor="middle">D → Q</text>'
    f'<path class="wire" d="M{95+i*115},304 V359"/>'
    f'<circle class="node" cx="{95+i*115}" cy="359" r="4"/>'
    for i in range(8)
]
FIGS["c07_fig01_ocho_flips_un_registro"] = wrap("Registro de ocho flip-flops D", '''
<text x="42" y="46" class="label">Ocho memorias de un bit, un reloj compartido</text>
<text x="42" y="80" class="small">D7…D0 son entradas independientes; Q7…Q0 forman un dato de ocho bits.</text>
<rect x="34" y="115" width="934" height="284" rx="20" fill="#f6f9fc" stroke="#a8bfcb" stroke-width="2"/>
''' + ''.join(pieces) + '''
<path class="wire" d="M64,359 H939"/>
<path class="wire" d="M64,359 V428"/>
<text x="84" y="445" class="label accent">CLK ↑</text>
<text x="500" y="466" class="tiny" text-anchor="middle">Todos capturan en el mismo flanco lógico; las salidas físicas tienen retardo.</text>
''')


FIGS["c07_fig02_multiplexor_y_carga"] = wrap("Carga y retención por multiplexor", '''
<text x="40" y="47" class="label">Una posición del registro: elegir cargar o conservar</text>
<text x="40" y="84" class="small">El multiplexor selecciona un dato antes de que llegue el próximo flanco.</text>
''' + rect(342, 207, 154, 130, "MUX 2:1", "#e6f3fa")
    + rect(625, 197, 148, 139, "FF D", "#e1f3e8") + '''
<text x="55" y="228" class="label accent">IN_i</text>
<path class="wire" d="M111,225 H342"/>
<path class="wire" d="M496,266 H625"/>
<text x="534" y="248" class="small accent">D_i</text>
<path class="wire" d="M773,266 H921"/>
<text x="862" y="248" class="label accent">Q_i</text>
<path class="wire" d="M861,266 V393 H238 V302 H342"/>
<circle class="node" cx="861" cy="266" r="5"/>
<text x="110" y="390" class="small">Realimentación</text>
<path class="wire" d="M420,129 V207"/>
<text x="385" y="119" class="label accent">LOAD</text>
<path class="wire" d="M701,336 V422"/>
<text x="660" y="447" class="label accent">CLK ↑</text>
<text x="500" y="482" class="tiny" text-anchor="middle">LOAD = 0 selecciona Q_i; LOAD = 1 selecciona IN_i.</text>
''')


FIGS["c07_fig03_almacenamiento_y_triestado"] = wrap("Almacenamiento y salida triestado", '''
<text x="44" y="47" class="label">Guardar un byte no equivale a conducirlo al bus</text>
<text x="44" y="82" class="small">LOAD y OE_n controlan bloques diferentes.</text>
''' + rect(106, 186, 273, 155, "Registro de 8 bits")
    + rect(538, 198, 199, 131, "Búfer 3 estados", "#e2f3e8", "small") + '''
<text x="54" y="230" class="small accent">IN[7:0]</text>
<path class="wire" d="M80,244 H106"/>
<path class="wire" d="M379,264 H538"/>
<text x="439" y="245" class="small accent">Q[7:0]</text>
<path class="wire" d="M737,264 H928"/>
<text x="793" y="246" class="label accent">BUS[7:0]</text>
<path class="wire" d="M239,127 V186"/>
<text x="199" y="117" class="small accent">LOAD + CLK</text>
<path class="wire" d="M629,129 V198"/>
<text x="607" y="116" class="label accent">OE_n</text>
<rect x="126" y="382" width="741" height="69" rx="12" fill="#f0f5f9"/>
<text x="500" y="409" class="small" text-anchor="middle">OE_n = 0: BUS recibe Q.  OE_n = 1: salida Z.</text>
<text x="500" y="437" class="tiny" text-anchor="middle">Z no borra Q y no debe confundirse con 0 lógico.</text>
''')


FIGS["c07_fig04_transferencia_a_b"] = wrap("Transferencia A hacia B con bus", '''
<text x="42" y="44" class="label">Copiar 0x3C: el registro A no pierde su valor</text>
<text x="42" y="76" class="small">Primero se conduce el bus; luego B captura el dato en un flanco.</text>
''' + rect(60, 122, 210, 136, "A: 0x3C", "#e6f3fa")
    + rect(404, 131, 189, 120, "BUS: 0x3C", "#fff3dc", "small")
    + rect(732, 122, 210, 136, "B: 0xA5 → 0x3C", "#e2f3e8", "small") + '''
<path class="wire" d="M270,190 H404 M593,190 H732"/>
<path d="M392,181 l12,9 -12,9 M720,181 l12,9 -12,9" fill="none" stroke="#273746" stroke-width="3"/>
<text x="303" y="173" class="small accent">A_OUT</text>
<text x="625" y="172" class="small accent">B_LOAD ↑</text>
<rect x="53" y="310" width="894" height="127" rx="15" fill="#f0f6fb"/>
<text x="100" y="344" class="small">1. A_OUT = 1, B_OUT = 0 → A conduce 0x3C.</text>
<text x="100" y="379" class="small">2. B_LOAD = 1 y CLK ↑ → B captura 0x3C.</text>
<text x="100" y="413" class="small">3. Se deshabilita A antes de habilitar B_OUT.</text>
<text x="500" y="471" text-anchor="middle" class="tiny">El cambio de origen debe evitar dos salidas activas simultáneamente.</text>
''')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, contents in FIGS.items():
        svg = OUT / (name + ".svg")
        png = OUT / (name + ".png")
        svg.write_text(contents, encoding="utf-8")
        subprocess.run(["inkscape", str(svg), "--export-type=png",
                        f"--export-filename={png}", "--export-width=2000"], check=True)
        print(f"Ilustración: {png.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
