#!/usr/bin/env python3
"""Cuatro diagramas originales del interludio sobre semántica de bits."""
import subprocess

from generar_figuras_capitulo_01 import ROOT, STYLE


OUT = ROOT / "libro" / "figuras"


def wrap(title: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" '
            f'viewBox="0 0 1000 500"><title>{title}</title>'
            f'<rect width="1000" height="500" fill="#ffffff"/>{STYLE}{body}</svg>')


def box(x, y, w, h, label, fill="#edf5fb", size="label"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" '
            f'fill="{fill}" stroke="#28465b" stroke-width="2"/>'
            f'<text x="{x+w/2}" y="{y+h/2+7}" class="{size}" '
            f'text-anchor="middle">{label}</text>')


FIGS = {}

FIGS["p07b_fig01_del_voltaje_a_la_logica"] = wrap("Del voltaje al significado de una señal", '''
<text x="40" y="43" class="label">El circuito reconoce estados, no voltajes universales</text>
<text x="40" y="72" class="small">Los umbrales dependen de la tecnología y de su hoja de datos.</text>
<rect x="45" y="116" width="333" height="207" rx="15" fill="#f6f9fc" stroke="#aabccb" stroke-width="2"/>
<text x="67" y="146" class="small">Tensión de entrada</text>
<rect x="80" y="167" width="265" height="45" fill="#d8ecff"/>
<text x="212" y="196" class="small" text-anchor="middle">Región reconocida ALTA</text>
<rect x="80" y="212" width="265" height="41" fill="#fff0d6"/>
<text x="212" y="238" class="tiny" text-anchor="middle">Región NO GARANTIZADA</text>
<rect x="80" y="253" width="265" height="45" fill="#e2f2e5"/>
<text x="212" y="281" class="small" text-anchor="middle">Región reconocida BAJA</text>
<path class="wire" d="M379,218 H456"/>
<path class="wire" d="M444,209 l12,9 -12,9"/>
'''+box(460, 169, 202, 103, "Lógica 0 o 1", "#e8f2ff")+'''
<path class="wire" d="M663,218 H732"/>
<path class="wire" d="M720,209 l12,9 -12,9"/>
'''+box(738, 169, 213, 103, "Función de señal", "#e2f3e8", "small")+'''
<rect x="55" y="362" width="892" height="87" rx="15" fill="#f0f6fb"/>
<text x="78" y="395" class="small">Ejemplo: RESET_n = 0 solicita reset (señal activa en bajo).</text>
<text x="78" y="423" class="small">RESET_n = 1 deja de solicitarlo. El nombre/polaridad forman parte del contrato.</text>
''')

FIGS["p07b_fig02_un_byte_varios_significados"] = wrap("Tres interpretaciones de un byte", '''
<text x="40" y="44" class="label">Los bits se conservan; cambia la regla que los lee</text>
<text x="40" y="74" class="small">El patrón central no incluye una etiqueta de tipo.</text>
'''+box(315, 111, 371, 91, "01000001", "#fff0da")+'''
<path class="wire" d="M500,202 V238 H168 V275 M500,238 V275 M500,238 H827 V275"/>
<circle class="node" cx="500" cy="238" r="5"/>
'''+box(47, 275, 245, 106, "Número: 65", "#e8f2ff", "small")
   +box(374, 275, 251, 106, "ASCII: A", "#e2f3e8", "small")
   +box(707, 275, 245, 106, "Máscara: b6 y b0", "#e8f2ff", "small")+'''
<rect x="77" y="419" width="844" height="48" rx="10" fill="#f5f7f9"/>
<text x="500" y="448" class="small" text-anchor="middle">¿Instrucción? Solo una ISA definida puede responder.</text>
''')

FIGS["p07b_fig03_pesos_con_y_sin_signo"] = wrap("Pesos de 11111111 según la convención", '''
<text x="36" y="43" class="label">Un byte de unos, dos resultados numéricos distintos</text>
<text x="36" y="75" class="small">En complemento a dos de ocho bits, b7 pesa -128; sin signo pesa +128.</text>
<text x="46" y="153" class="small">Bits</text>
'''+''.join(
    f'<rect x="{175+i*94}" y="113" width="79" height="63" rx="9" fill="#fff0d8" '
    'stroke="#b68c42" stroke-width="2"/>'
    f'<text x="{214+i*94}" y="151" class="label" text-anchor="middle">1</text>'
    f'<text x="{214+i*94}" y="190" class="tiny" text-anchor="middle">b{7-i}</text>'
    for i in range(8)
)+'''
<text x="44" y="261" class="small">Sin signo</text>
'''+''.join(
    f'<text x="{214+i*94}" y="261" class="small" text-anchor="middle">{2**(7-i)}</text>'
    for i in range(8)
)+'''
<text x="44" y="330" class="small">Con signo</text>
'''+''.join(
    f'<text x="{214+i*94}" y="330" class="small" text-anchor="middle">{-(2**7) if i == 0 else 2**(7-i)}</text>'
    for i in range(8)
)+'''
<path class="wire" d="M160,278 H937"/>
<rect x="60" y="385" width="425" height="66" rx="14" fill="#e8f2ff"/>
<text x="273" y="426" class="label" text-anchor="middle">Sin signo = 255</text>
<rect x="515" y="385" width="425" height="66" rx="14" fill="#e2f3e8"/>
<text x="728" y="426" class="label" text-anchor="middle">Con signo = -1</text>
''')

FIGS["p07b_fig04_escalera_de_significado"] = wrap("Del estado del hardware al programa", '''
<text x="38" y="43" class="label">Cada interpretación necesita una regla conocida</text>
<text x="38" y="72" class="small">Es un recorrido conceptual; no son componentes físicos obligatorios.</text>
'''+box(45, 122, 265, 95, "Señal lógica", "#e8f2ff", "small")
   +box(369, 122, 265, 95, "Patrón de bits", "#e8f2ff", "small")
   +box(693, 122, 265, 95, "Valor codificado", "#fff0d8", "small")+'''
<path class="wire" d="M310,169 H367 M634,169 H691"/>
<path class="wire" d="M356,160 l11,9 -11,9 M680,160 l11,9 -11,9"/>
<path class="wire" d="M826,217 V268"/>
<path class="wire" d="M817,257 l9,11 9,-11"/>
'''+box(693, 270, 265, 96, "Tipo y estructura", "#e2f3e8", "small")
   +box(369, 270, 265, 96, "Operación de programa", "#e2f3e8", "small")
   +box(45, 270, 265, 96, "Significado humano", "#fff0d8", "small")+'''
<path class="wire" d="M693,318 H636 M369,318 H312"/>
<path class="wire" d="M646,309 l-10,9 10,9 M322,309 l-10,9 10,9"/>
<rect x="55" y="405" width="887" height="59" rx="12" fill="#f3f6f8"/>
<text x="498" y="431" class="small" text-anchor="middle">POO: una opción posterior para agrupar estado y comportamiento.</text>
<text x="498" y="453" class="tiny" text-anchor="middle">No corresponde a un circuito ni es requisito de MiniC-Aula.</text>
''')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg_code in FIGS.items():
        svg_path = OUT / f"{name}.svg"
        png_path = OUT / f"{name}.png"
        svg_path.write_text(svg_code, encoding="utf-8")
        subprocess.run(["inkscape", str(svg_path), "--export-type=png",
                        f"--export-filename={png_path}", "--export-width=2000"],
                       check=True, stdout=subprocess.DEVNULL)
        print(f"Figura creada: {png_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
