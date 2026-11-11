"""Genera una maqueta SVG original de UI propuesta; no implementa JavaFX ni PCB."""

from pathlib import Path

import svgwrite


OUT = Path(__file__).parent / "IM02_AULA8_PLACA_DIDACTICA_UX_V1.svg"
d = svgwrite.Drawing(str(OUT), size=(1600, 900), viewBox="0 0 1600 900")
PALETTE = {
    "navy": "#182738", "ink": "#243648", "muted": "#677a8c",
    "paper": "#f2f5f8", "panel": "#ffffff", "line": "#d7e0e9",
    "blue": "#27649b", "teal": "#117f80", "green": "#79be8d",
    "chip": "#27383a", "solder": "#d8dabc", "amber": "#d1a345",
}


def rect(x, y, w, h, fill, rx=0, stroke="none", sw=1):
    d.add(d.rect(insert=(x, y), size=(w, h), rx=rx, ry=rx,
                 fill=fill, stroke=stroke, stroke_width=sw))


def text(x, y, value, size=16, weight="normal", fill=None, anchor="start"):
    d.add(d.text(value, insert=(x, y), font_family="DejaVu Sans, Arial, sans-serif",
                 font_size=size, font_weight=weight, text_anchor=anchor,
                 fill=fill or PALETTE["ink"]))


def line(x1, y1, x2, y2, stroke="#bac8d5", sw=1, dash=None):
    opts = dict(stroke=stroke, stroke_width=sw, stroke_linecap="round")
    if dash:
        opts["stroke_dasharray"] = dash
    d.add(d.line((x1, y1), (x2, y2), **opts))


def button(x, y, w, label, selected=False, enabled=True):
    bg = PALETTE["blue"] if selected else ("#f9fbfd" if enabled else "#f3f4f5")
    fg = "#ffffff" if selected else (PALETTE["ink"] if enabled else "#a1adb8")
    rect(x, y, w, 34, bg, 5, "#cdd9e4" if not selected else bg)
    text(x + w / 2, y + 22, label, 13, "bold" if selected else "normal", fg, "middle")


def badge(x, y, value, fill="#e6f4f1", fg="#18715b"):
    w = max(80, len(value) * 7.6 + 25)
    rect(x, y, w, 26, fill, 13)
    text(x + w / 2, y + 18, value, 12, "bold", fg, "middle")


def path(points, fill, stroke="none", sw=1, opacity=1):
    d.add(d.polygon(points, fill=fill, stroke=stroke,
                    stroke_width=sw, opacity=opacity))


d.add(d.rect(insert=(0, 0), size=(1600, 900), fill=PALETTE["paper"]))

# Title and familiar desktop grammar.
rect(0, 0, 1600, 42, PALETTE["navy"])
rect(20, 12, 18, 18, PALETTE["teal"], 3)
text(29, 26, "A", 12, "bold", "#ffffff", "middle")
text(52, 26, "Aula-Computadora", 17, "bold", "#ffffff")
text(215, 26, "—  Aula-8  /  Construir", 13, fill="#bfcbd6")
badge(1283, 8, "DISEÑO PROPUESTO", "#34495d", "#dce9f5")
text(1540, 27, "─     □     ×", 18, fill="#bfcbd6")
rect(0, 42, 1600, 37, "#ffffff")
for x, label in [(20, "Archivo"), (102, "Editar"), (175, "Ver"), (229, "Recorrido"),
                 (339, "Simulación"), (470, "Ayuda")]:
    text(x, 66, label, 14)
line(0, 79, 1600, 79, PALETTE["line"])
rect(0, 80, 1600, 55, "#f8fafc")
for x, w, label, chosen in [
    (22, 92, "Seleccionar", False), (123, 105, "Colocar", True),
    (239, 82, "Quitar", False), (333, 93, "Deshacer", False),
    (437, 78, "Pista", False), (528, 91, "Probar", False)
]:
    button(x, 90, w, label, chosen)
line(641, 89, 641, 125, "#d5dde5")
text(660, 113, "Etapa: montar una NAND", 14, fill="#485e72")
badge(1060, 94, "Montaje sin comprobar", "#fff3df", "#9c6d1d")
line(0, 135, 1600, 135, PALETTE["line"])

# Left sidebar.
rect(0, 136, 270, 630, "#ffffff")
text(20, 165, "RECORRIDO AULA-8", 13, "bold", PALETTE["blue"])
line(18, 181, 251, 181, PALETTE["line"])
text(20, 212, "Construcción guiada", 16, "bold")
for y, number, label, state in [
    (245, "01", "Electricidad y señales", "done"),
    (284, "02", "Compuerta NAND", "active"),
    (323, "03", "Latch: memoria de 1 bit", "wait"),
    (362, "04", "Registro de 8 bits", "wait"),
    (401, "05", "Buses y transferencia", "wait"),
]:
    if state == "active":
        rect(10, y - 24, 251, 36, "#e7f1f9", 4)
        rect(10, y - 24, 4, 36, PALETTE["blue"])
    color = "#1e886a" if state == "done" else "#698094"
    text(20, y, "✓" if state == "done" else number, 13, "bold", color)
    text(57, y, label, 12, "bold" if state == "active" else "normal")
line(18, 430, 251, 430, PALETTE["line"])
text(20, 457, "KIT DE ESTA ETAPA", 13, "bold", PALETTE["blue"])
text(20, 485, "Arrastra una pieza a un hueco", 12, fill=PALETTE["muted"])
text(20, 503, "marcado en la placa.", 12, fill=PALETTE["muted"])
for y, label, count in [(528, "PMOS didáctico", "× 2"), (577, "NMOS didáctico", "× 2"),
                        (626, "Alimentación y tierra", "fija")]:
    rect(15, y - 14, 240, 40, "#f8fafc", 5, "#e1e8ef")
    rect(26, y - 5, 24, 22, "#354d59", 3)
    line(32, y + 7, 43, y + 7, "#d5e9da", 2)
    text(62, y + 11, label, 12)
    text(238, y + 11, count, 12, "bold", PALETTE["muted"], "end")

# Workspace tabs.
rect(271, 136, 993, 630, "#ecf1f5")
rect(271, 136, 993, 48, "#f9fbfd")
button(295, 142, 132, "Placa 3D", True)
button(436, 142, 158, "Esquema 2D")
button(603, 142, 141, "Programa", enabled=False)
text(1234, 167, "↗", 18, fill="#7b90a1")
rect(292, 199, 953, 539, "#dce5ec", 7, "#cbd7e2")
text(321, 229, "AULA-8  ›  NAND2  ›  PLACA", 13, "bold", "#43586a")
badge(1006, 208, "3D DIDÁCTICO", "#f8fbfd", "#526d83")

# 3D-style conceptual board, vector geometry rather than fake photorealistic hardware.
d.defs.add(d.linearGradient(id="boardgrad", start=(0, 0), end=(0, 1)))
grad = d.defs.elements[-1]
grad.add_stop_color(0, "#376f5d")
grad.add_stop_color(1, "#214e44")
board = [(402, 340), (951, 302), (1081, 528), (533, 570)]
path([(407, 357), (956, 320), (1081, 541), (534, 585)], "#16372f", "#173a34", 2)
path(board, "url(#boardgrad)", "#1e6553", 3)
path([(425, 357), (939, 321), (1058, 516), (546, 554)], "none", "#7aa38d", 2)

def bxy(u, v):
    return (402 + 549 * u + 131 * v, 340 - 38 * u + 226 * v)


# Printed visual traces; intentionally not asserted to be a validated physical PCB.
for j in range(6):
    u = .12 + .1 * j
    ax, ay = bxy(u, .15)
    bx, by = bxy(u, .85)
    line(ax, ay, bx, by, "#75b09a", 1.4)
for k in range(4):
    v = .23 + .15 * k
    ax, ay = bxy(.09, v)
    bx, by = bxy(.90, v)
    line(ax, ay, bx, by, "#75b09a", 1)

def chip(u, v, label, chosen=False, small=False):
    x, y = bxy(u, v)
    w, h = (112, 44) if not small else (83, 35)
    path([(x, y), (x+w, y-5), (x+w+15, y+h-5), (x+15, y+h)],
         "#243536" if not chosen else "#244d53", "#cce5d3" if chosen else "#162d2b", 2.5)
    path([(x+15, y+h), (x+w+15, y+h-5), (x+w+15, y+h+4), (x+15, y+h+9)], "#142a2c")
    for t in range(3 if small else 5):
        xx = x + (18 + 22 * t if small else 12 + t * (w-18)/5)
        line(xx, y-6, xx+4, y-15, "#cbd4b7", 3)
        if not small:
            line(xx+15, y+h+2, xx+18, y+h+11, "#cbd4b7", 3)
    text(x+w/2+8, y+27, label, 14 if not small else 12, "bold", "#eaf4ec", "middle")


chip(.20, .25, "PMOS 01", small=True)
chip(.47, .24, "PMOS 02", small=True)
chip(.23, .52, "NMOS 01", selected := True, small=True)
chip(.54, .53, "NMOS 02", small=True)

bx, by = bxy(.24, .52)
d.add(d.ellipse(center=(bx+45, by+23), r=(64, 29), fill="none", stroke="#78d9e2",
                stroke_width=2.3, stroke_dasharray="8 5"))
line(bx+69, by+45, bx+105, by+82, "#eaf7f3", 1.6)
rect(bx+100, by+65, 186, 47, "#ffffff", 6, "#9db6c4")
text(bx+111, by+85, "NMOS 01 seleccionado", 12, "bold")
text(bx+111, by+101, "Inspeccionar  ›", 11, fill="#437491")

for u, v in [(0.04, 0.06), (0.94, 0.06), (0.06, 0.89), (0.93, 0.87)]:
    x, y = bxy(u, v)
    d.add(d.circle(center=(x, y), r=5, fill="#b4bca7", stroke="#1d4437", stroke_width=2))

text(332, 703, "Ilustración conceptual — no representa una PCB de fabricación", 12,
     fill="#687e90")
button(960, 687, 49, "−")
button(1017, 687, 86, "85 %")
button(1112, 687, 49, "+")
button(1170, 687, 56, "↔")

# Inspector.
rect(1264, 136, 336, 630, "#ffffff")
text(1288, 165, "INSPECTOR", 13, "bold", PALETTE["blue"])
line(1285, 183, 1578, 183, PALETTE["line"])
rect(1295, 202, 273, 156, "#edf2f5", 5)
# Schematic icon illustration, not a precise pinout.
line(1359, 283, 1410, 283, "#557f80", 3)
rect(1408, 241, 52, 85, "#303d48", 7)
line(1461, 283, 1504, 283, "#557f80", 3)
for px in (1415, 1440, 1450):
    line(px, 239, px, 222, "#cad5d6", 4)
text(1435, 289, "N", 20, "bold", "#f8fafc", "middle")
text(1431, 344, "Modelo didáctico · vista física", 11, fill="#607887", anchor="middle")
text(1290, 389, "NMOS 01", 20, "bold")
badge(1291, 404, "Seleccionado")
text(1290, 458, "Transistor MOS de canal N", 14, "bold")
for y, s in [(487, "Conduce entre drenador y fuente"),
             (507, "cuando la compuerta se activa en el"),
             (527, "modelo didáctico. No es SPICE.")]:
    text(1290, y, s, 12, fill="#516577")
line(1291, 548, 1577, 548, PALETTE["line"])
text(1290, 577, "TERMINALES", 13, "bold", PALETTE["blue"])
for y, label, value in [(609, "G · Compuerta", "Entrada"),
                         (637, "D · Drenador", "Red D1"),
                         (665, "S · Fuente", "Red S1")]:
    text(1290, y, label, 12)
    text(1567, y, value, 12, fill=PALETTE["muted"], anchor="end")
line(1290, 683, 1567, 683, PALETTE["line"])
text(1290, 709, "Estado: sin comprobar", 12, fill="#a27637")

# Bottom utility dock and status bar.
rect(0, 767, 1600, 91, "#f8fafc")
line(0, 767, 1600, 767, PALETTE["line"])
for x, label in [(20, "Problemas"), (140, "Pruebas"), (246, "Señales"), (357, "Salida")]:
    text(x, 796, label, 13, "bold" if label == "Pruebas" else "normal",
         PALETTE["blue"] if label == "Pruebas" else "#5e7489")
line(138, 805, 216, 805, PALETTE["blue"], 2.5)
text(21, 831, "Aún no se ha ejecutado la prueba. Usa «Probar» para evaluar las conexiones.",
     13, fill="#576a79")
rect(0, 858, 1600, 42, "#e4ebf2")
line(0, 858, 1600, 858, "#cfdce5")
text(22, 883, "Aula-8    ·    Construir    ·    Etapa: NAND2", 12, fill="#43586c")
text(678, 883, "CPU: detenida", 12, fill="#43586c")
text(947, 883, "Guardado: correcto", 12, fill="#317c61")
text(1285, 883, "Zoom: 85 %", 12, fill="#43586c")
text(1536, 883, "IM-02", 11, "bold", "#7e91a2")

OUT.parent.mkdir(parents=True, exist_ok=True)
d.save()
print(OUT)
