#!/usr/bin/env python3
"""Genera cuatro figuras originales para explicar latch D y flip-flop D."""
import subprocess

from generar_figuras_capitulo_01 import ROOT, STYLE


OUT = ROOT / "libro" / "figuras"


def wrap(title: str, contents: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" '
            f'viewBox="0 0 1000 500"><title>{title}</title>'
            f'<rect width="1000" height="500" fill="white"/>{STYLE}{contents}</svg>')


def rectangle(x, y, w, h, label, bg="#e6f3fa"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
            f'fill="{bg}" stroke="#28465b" stroke-width="3"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 7}" text-anchor="middle" '
            f'class="label">{label}</text>')


FIGS = {}


FIGS["c06_fig01_desde_sr_hasta_d"] = wrap("Latch D desde NAND y latch SR", '''
<text x="43" y="47" class="label">De una entrada D a un latch con memoria</text>
<text x="43" y="82" class="small">LE = 0 genera HOLD; LE = 1 selecciona SET o RESET mediante D.</text>
''' + rectangle(386, 122, 163, 96, "NAND")
    + rectangle(386, 307, 163, 96, "NAND")
    + rectangle(235, 310, 90, 80, "NOT", "#f2eaf6")
    + rectangle(704, 211, 170, 123, "SR NAND", "#e3f2e8") + '''
<text x="73" y="146" class="label accent">D</text>
<path class="wire" d="M111,142 H386"/>
<path class="wire" d="M166,142 V349 H235"/>
<circle cx="166" cy="142" r="5" class="node"/>
<path class="wire" d="M325,349 H386"/>
<text x="255" y="408" class="tiny">D invertida</text>
<text x="60" y="450" class="label accent">LE</text>
<path class="wire" d="M110,445 H360 V203 H386"/>
<path class="wire" d="M360,385 H386"/>
<circle cx="360" cy="385" r="5" class="node"/>
<!-- Hueco en la vertical LE: el cable de NOT D cruza sin conectarse. -->
<path d="M360,340 V358" stroke="white" stroke-width="11"/>
<path class="wire" d="M325,349 H386"/>
<path class="wire" d="M549,169 H635 V242 H704"/>
<path class="wire" d="M549,351 H635 V302 H704"/>
<text x="579" y="152" class="small accent">S_n</text>
<text x="579" y="374" class="small accent">R_n</text>
<path class="wire" d="M874,269 H960"/>
<text x="917" y="250" class="label accent">Q</text>
<text x="788" y="365" text-anchor="middle" class="tiny">Conserva el bit</text>
<text x="500" y="467" text-anchor="middle" class="tiny">Esquema funcional ideal, no patillaje ni diagrama de montaje.</text>
''')


FIGS["c06_fig02_tabla_latch_d"] = wrap("Tabla del latch D transparente", '''
<text x="45" y="47" class="label">Tabla del latch D sensible a nivel alto</text>
<text x="45" y="81" class="small">Q solo conserva un valor anterior cuando la habilitación está cerrada.</text>
<rect x="55" y="118" width="890" height="317" rx="17" fill="#eef6fb"/>
<text x="133" y="167" class="label">LE</text><text x="317" y="167" class="label">D</text>
<text x="499" y="167" class="label">Q estable</text><text x="751" y="167" class="label">Estado</text>
<path d="M72,187 H930" stroke="#7f9aaa" stroke-width="2"/>
<rect x="75" y="203" width="852" height="63" rx="8" fill="#dbeaf5"/>
<text x="138" y="245" class="label">0</text><text x="296" y="245" class="small">0 o 1</text>
<text x="485" y="245" class="small">Q anterior</text><text x="751" y="245" class="label accent">HOLD</text>
<rect x="75" y="274" width="852" height="63" rx="8" fill="#e0f2e7"/>
<text x="138" y="316" class="label">1</text><text x="323" y="316" class="label">0</text>
<text x="522" y="316" class="label">0</text><text x="748" y="316" class="small">Deja pasar 0</text>
<rect x="75" y="345" width="852" height="63" rx="8" fill="#e0f2e7"/>
<text x="138" y="388" class="label">1</text><text x="323" y="388" class="label">1</text>
<text x="522" y="388" class="label">1</text><text x="748" y="388" class="small">Deja pasar 1</text>
<text x="501" y="467" text-anchor="middle" class="tiny">LE alto: transparente; LE bajo: conserva el último estado válido.</text>
''')


def wave(data, y0, y1, boundaries, ink="#176d92"):
    """Dibuja estados lógicos sobre tramos discretos, sin escala temporal física."""
    values = [y1 if value else y0 for value in data]
    path = f"M{boundaries[0]},{values[0]}"
    for idx, new_y in enumerate(values):
        path += f" H{boundaries[idx + 1]}"
        if idx + 1 < len(values) and values[idx + 1] != new_y:
            path += f" V{values[idx + 1]}"
    return f'<path d="{path}" fill="none" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>'


steps = [96, 206, 326, 446, 566, 686, 806, 925]
clk = [0, 0, 1, 1, 0, 1, 1]
data = [0, 1, 1, 0, 0, 0, 1]
q = [0, 0, 1, 1, 1, 0, 0]
FIGS["c06_fig03_flancos_y_capturas"] = wrap("Captura por flancos ascendentes", '''
<text x="42" y="43" class="label">Flip-flop D: dos flancos ascendentes, dos capturas</text>
<text x="42" y="76" class="small">t0 a t6 describen estados estables; las líneas no representan nanosegundos medidos.</text>
<rect x="58" y="105" width="893" height="325" rx="14" fill="#f3f8fb"/>
''' + ''.join(f'<text x="{x + 26}" y="132" class="small">t{idx}</text>' for idx, x in enumerate(steps[:7])) + '''
<text x="73" y="192" class="small accent">CLK</text><text x="73" y="282" class="small accent">D</text>
<text x="73" y="370" class="small accent">Q</text>
<path d="M326,143 V414 M686,143 V414" stroke="#60a584" stroke-width="2" stroke-dasharray="7,6"/>
''' + wave(clk, 209, 159, steps) + wave(data, 304, 253, steps, "#864b91")
    + wave(q, 397, 346, steps, "#268254") + '''
<text x="332" y="445" class="tiny" style="fill:#268254">Captura 1</text>
<text x="677" y="445" class="tiny" style="fill:#268254">Captura 0</text>
<text x="500" y="477" text-anchor="middle" class="tiny">Q dibujada como estado lógico asentado; físicamente hay retardo de CLK a Q.</text>
''')


FIGS["c06_fig04_latch_versus_flipflop"] = wrap("Comparación entre latch y flip-flop", '''
<text x="41" y="46" class="label">Dos memorias de un bit que aceptan datos de forma diferente</text>
<text x="41" y="82" class="small">El circuito y el nombre de la señal determinan cuándo puede cambiar Q.</text>
<rect x="39" y="115" width="447" height="311" rx="16" fill="#eff6fb" stroke="#9bbbd0" stroke-width="2"/>
<text x="263" y="164" text-anchor="middle" class="label">Latch D</text>
<text x="263" y="199" text-anchor="middle" class="small">LE = 1 abre una ventana</text>
<rect x="85" y="225" width="355" height="82" rx="12" fill="#dbeef7"/>
<text x="263" y="259" text-anchor="middle" class="label">D: 0 → 1 → 0</text>
<text x="263" y="288" text-anchor="middle" class="small">Q sigue 0 → 1 → 0</text>
<text x="263" y="349" text-anchor="middle" class="small">Sigue D durante todo el nivel alto</text>
<text x="263" y="384" text-anchor="middle" class="tiny">Al cerrar LE, conserva el último valor válido.</text>
<rect x="514" y="115" width="447" height="311" rx="16" fill="#eef7f0" stroke="#9bbcaa" stroke-width="2"/>
<text x="738" y="164" text-anchor="middle" class="label">Flip-flop D</text>
<text x="738" y="199" text-anchor="middle" class="small">CLK ↑ marca una captura</text>
<rect x="560" y="225" width="355" height="82" rx="12" fill="#dff0e3"/>
<text x="738" y="259" text-anchor="middle" class="label">D cambia con CLK alto</text>
<text x="738" y="288" text-anchor="middle" class="small">Q conserva el dato capturado</text>
<text x="738" y="349" text-anchor="middle" class="small">Necesita otro flanco ascendente</text>
<text x="738" y="384" text-anchor="middle" class="tiny">Reset asíncrono es una excepción explícita.</text>
<text x="500" y="466" text-anchor="middle" class="tiny">Comparación de contratos lógicos, no una medición de señales eléctricas.</text>
''')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, contents in FIGS.items():
        path_svg = OUT / f"{name}.svg"
        path_png = OUT / f"{name}.png"
        path_svg.write_text(contents, encoding="utf-8")
        subprocess.run(["inkscape", str(path_svg), "--export-type=png",
                        f"--export-filename={path_png}", "--export-width=2000"], check=True)
        print(f"Figura capítulo 6: {path_png.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
