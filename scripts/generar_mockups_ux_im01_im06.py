"""Cinco pantallas UX vectoriales de Aula-Computadora.

IM-02 V1 se conserva como sexto diseño. Son maquetas de producto, no
capturas de una aplicación ejecutable ni circuitos certificados.
"""

from pathlib import Path
import svgwrite

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "ux" / "mockups"
OUT.mkdir(parents=True, exist_ok=True)

C = {
    "navy": "#182738", "ink": "#243648", "muted": "#677a8c",
    "paper": "#f2f5f8", "white": "#ffffff", "line": "#d7e0e9",
    "blue": "#27649b", "teal": "#117f80", "green": "#1f8064",
    "pale": "#e7f1f9", "amber": "#b27a26", "red": "#ba4c4c",
    "stage": "#e4ebf2", "dark": "#182b30",
}


class UI:
    def __init__(self, label):
        self.label = label
        self.d = svgwrite.Drawing(str(OUT / f"{label}_AULA_UX_V1.svg"),
                                  size=(1600, 900), viewBox="0 0 1600 900")
        self.rect(0, 0, 1600, 900, C["paper"])

    def rect(self, x, y, w, h, fill, r=0, border="none", sw=1):
        self.d.add(self.d.rect(insert=(x, y), size=(w, h), rx=r, ry=r,
                               fill=fill, stroke=border, stroke_width=sw))

    def line(self, x1, y1, x2, y2, color=C["line"], w=1.5, dash=None):
        kws = dict(stroke=color, stroke_width=w, stroke_linecap="round")
        if dash:
            kws["stroke_dasharray"] = dash
        self.d.add(self.d.line((x1, y1), (x2, y2), **kws))

    def text(self, x, y, value, size=14, weight="normal", color=C["ink"],
             anchor="start", family="DejaVu Sans, Arial, sans-serif"):
        self.d.add(self.d.text(value, insert=(x, y), font_family=family,
                               font_size=size, font_weight=weight,
                               text_anchor=anchor, fill=color))

    def circle(self, x, y, r, fill, stroke="none", sw=1):
        self.d.add(self.d.circle(center=(x, y), r=r, fill=fill,
                                 stroke=stroke, stroke_width=sw))

    def path(self, path, fill="none", stroke="none", sw=1):
        self.d.add(self.d.path(d=path, fill=fill, stroke=stroke, stroke_width=sw))

    def badge(self, x, y, value, bg="#e6f4f1", fg="#18715b", width=None):
        width = width or max(87, len(value) * 7.3 + 27)
        self.rect(x, y, width, 26, bg, 13)
        self.text(x + width / 2, y + 18, value, 12, "bold", fg, "middle")

    def button(self, x, y, width, value, active=False, disabled=False):
        bg = C["blue"] if active else ("#f3f4f6" if disabled else "#f9fbfd")
        fg = C["white"] if active else ("#9daab6" if disabled else C["ink"])
        self.rect(x, y, width, 34, bg, 5, C["blue"] if active else "#cdd9e4")
        self.text(x + width / 2, y + 22, value, 13,
                  "bold" if active else "normal", fg, "middle")

    def panel_title(self, x, y, title):
        self.text(x, y, title, 13, "bold", C["blue"])

    def shell(self, cpu, mode, toolbar, tabs, active_tab, selected_title="",
              dock_top=767, active_dock=None, no_inspector=False):
        self.rect(0, 0, 1600, 42, C["navy"])
        self.rect(20, 12, 18, 18, C["teal"], 3)
        self.text(29, 26, "A", 12, "bold", C["white"], "middle")
        self.text(52, 26, "Aula-Computadora", 17, "bold", C["white"])
        self.text(215, 26, f"—  {cpu}  /  {mode}", 13, color="#c0cbd6")
        self.badge(1280, 8, "DISEÑO PROPUESTO", "#34495d", "#dce9f5", 160)
        self.text(1542, 27, "─     □     ×", 18, color="#bfcbd6")
        self.rect(0, 42, 1600, 37, C["white"])
        for x, label in [(20, "Archivo"), (102, "Editar"), (175, "Ver"),
                         (229, "Recorrido"), (339, "Simulación"), (470, "Ayuda")]:
            self.text(x, 66, label, 14)
        self.line(0, 79, 1600, 79)
        self.rect(0, 80, 1600, 55, "#f8fafc")
        xx = 22
        for label, width, active, disabled in toolbar:
            self.button(xx, 90, width, label, active, disabled)
            xx += width + 10
        self.line(xx + 5, 89, xx + 5, 124)
        self.text(xx + 22, 112, selected_title, 13, color="#485e72")
        self.line(0, 135, 1600, 135)
        self.rect(0, 136, 270, dock_top - 136, C["white"])
        self.rect(271, 136, (1329 if no_inspector else 993), dock_top - 136, "#ecf1f5")
        self.rect(271, 136, (1329 if no_inspector else 993), 48, "#f9fbfd")
        xx = 295
        for label, width, disabled in tabs:
            self.button(xx, 142, width, label, label == active_tab, disabled)
            xx += width + 9
        if not no_inspector:
            self.rect(1264, 136, 336, dock_top - 136, C["white"])
            self.panel_title(1288, 165, "INSPECTOR")
            self.line(1285, 183, 1578, 183)
        self.rect(0, dock_top, 1600, 858 - dock_top, "#f8fafc")
        self.line(0, dock_top, 1600, dock_top)
        for x, label in [(20, "Problemas"), (140, "Pruebas"),
                         (246, "Señales"), (357, "Salida")]:
            act = label == active_dock
            self.text(x, dock_top + 28, label, 13, "bold" if act else "normal",
                      C["blue"] if act else "#60778a")
            if act:
                self.line(x - 2, dock_top + 37, x + len(label) * 7.4,
                          dock_top + 37, C["blue"], 2.5)
        self.rect(0, 858, 1600, 42, C["stage"])
        self.line(0, 858, 1600, 858, "#ccd8e2")
        self.text(1535, 883, self.label, 11, "bold", "#74889b")

    def side(self, cpu="AULA-8", active="Compuerta NAND", kit=True):
        self.panel_title(20, 165, f"RECORRIDO {cpu}")
        self.line(18, 181, 251, 181)
        self.text(20, 211, "Construcción guiada", 16, "bold")
        stages = (["Electricidad y señales", "Compuerta NAND",
                   "Latch: memoria de 1 bit", "Registro de 8 bits",
                   "Buses y transferencia"] if cpu == "AULA-8" else
                  ["Señales de 16 bits", "Registros y ALU",
                   "Memoria par / impar", "Control e instrucciones",
                   "Programa y pantalla"])
        for i, name in enumerate(stages):
            yy = 246 + i * 39
            if active == name:
                self.rect(10, yy - 24, 251, 36, C["pale"], 4)
                self.rect(10, yy - 24, 4, 36, C["blue"])
            self.text(20, yy, f"{i+1:02d}", 13, "bold", "#678196")
            self.text(57, yy, name, 12, "bold" if name == active else "normal")
        self.line(18, 430, 251, 430)
        self.panel_title(20, 457, "PIEZAS DE ESTA ETAPA" if kit else "EN ESTA VISTA")
        if kit:
            for y, name in [(493, "NAND2 CMOS"), (542, "PMOS didáctico"),
                            (591, "NMOS didáctico")]:
                self.rect(15, y - 14, 240, 40, "#f8fafc", 5, "#e1e8ef")
                self.rect(25, y - 4, 22, 22, "#395a68", 3)
                self.text(60, y + 11, name, 12)
        else:
            for y, name in [(493, "Estado de señales"), (542, "Pruebas de módulo"),
                            (591, "Navegación por niveles")]:
                self.text(25, y, "• " + name, 12, color="#4e6577")

    def canvas(self, width=953, bottom=738, background="#f5f8fa"):
        self.rect(292, 199, width, bottom - 199, background, 7, "#cbd7e2")

    def inspector(self, name, subtitle, lines, values, status=None, compact=False):
        if compact:
            self.rect(1295, 202, 273, 81, "#edf2f5", 5)
            self.text(1431, 254, "◎", 28, "bold", "#397190", "middle")
            self.text(1290, 316, name, 19, "bold")
            self.text(1290, 342, subtitle, 13, "bold", C["blue"])
            for i, ln in enumerate(lines):
                self.text(1290, 372 + 19*i, ln, 12, color="#566a7b")
            self.line(1291, 419, 1577, 419)
            self.panel_title(1290, 447, "DATOS ACTUALES")
            for i, (key, value) in enumerate(values):
                y = 475 + i * 27
                self.text(1290, y, key, 12)
                self.text(1567, y, value, 12, "bold", C["blue"], "end")
            if status:
                self.text(1290, 597, status, 11, color=C["amber"])
            return
        self.rect(1295, 202, 273, 118, "#edf2f5", 5)
        self.rect(1387, 233, 92, 56, "#d2e2eb", 7, "#b4cedd")
        self.text(1433, 268, "◎", 32, "bold", "#397190", "middle")
        self.text(1290, 357, name, 19, "bold")
        self.text(1290, 383, subtitle, 13, "bold", C["blue"])
        for i, ln in enumerate(lines):
            self.text(1290, 419 + 20*i, ln, 12, color="#566a7b")
        top = 457 + len(lines) * 20
        self.line(1291, top, 1577, top)
        self.panel_title(1290, top + 28, "DATOS ACTUALES")
        for i, (key, value) in enumerate(values):
            y = top + 58 + i * 28
            self.text(1290, y, key, 12)
            self.text(1567, y, value, 12, "bold", C["blue"], "end")
        if status:
            self.line(1291, 685, 1577, 685)
            self.text(1290, 712, status, 12, color=C["amber"])

    def status(self, left, middle, right, zoom="100 %"):
        self.text(22, 883, left, 12, color="#43586c")
        self.text(682, 883, middle, 12, color="#43586c")
        self.text(978, 883, right, 12, color="#317c61")
        self.text(1325, 883, f"Zoom: {zoom}", 12, color="#43586c")

    def save(self):
        self.d.save()
        return self.d.filename


def im01():
    u = UI("IM-01")
    u.shell("Inicio", "Seleccionar computadora", [
        ("Continuar", 104, True, False), ("Construir", 100, False, False),
        ("Explorar", 94, False, False)], [("Recorridos", 132, False)],
        "Recorridos", "Dos recorridos independientes", no_inspector=True)
    u.panel_title(20, 165, "TU ESPACIO")
    u.line(18, 181, 251, 181)
    u.text(20, 211, "Computadoras", 16, "bold")
    for yy, name, active in [(246, "Aula-8", True), (292, "Aula-16", False)]:
        if active:
            u.rect(10, yy-25, 251, 39, C["pale"], 5)
            u.rect(10, yy-25, 4, 39, C["blue"])
        u.text(35, yy, name, 15, "bold" if active else "normal")
    u.line(18, 340, 251, 340)
    u.panel_title(20, 368, "CONTINUIDAD")
    for i, s in enumerate(["Se guarda el avance de cada", "computadora por separado.",
                           "No necesitas crear proyectos."]):
        u.text(20, 402 + i*21, s, 12, color=C["muted"])
    u.canvas(width=1287, bottom=739, background="#e8eef4")
    u.text(330, 255, "Elige qué computadora quieres construir", 23, "bold")
    u.text(330, 290, "Aprende por módulos, comprueba las entradas y observa el resultado.", 14, color=C["muted"])
    for x, cpu, kind, badge, task, primary in [
        (330, "AULA-8", "Placa 3D + esquema 2D", "En curso · ejemplo",
         "Último punto: compuerta NAND", "Continuar"),
        (940, "AULA-16", "Esquema 2D", "Sin iniciar",
         "Recomendación: primero Aula-8", "Comenzar")]:
        u.rect(x, 334, 557, 337, C["white"], 9, "#cbd7e2")
        u.rect(x, 334, 557, 7, C["blue"] if cpu == "AULA-8" else C["teal"], 5)
        u.text(x+28, 388, cpu, 21, "bold")
        u.badge(x+323, 362, badge, "#e9f2f9", C["blue"], 198)
        u.text(x+28, 426, kind, 15, "bold", "#48677f")
        # Minimal recognizable board vs circuit illustration.
        if cpu == "AULA-8":
            u.path(f"M{x+65} 481 L{x+310} 470 L{x+359} 567 L{x+105} 586 Z",
                   "#2a725e", "#1b5145", 3)
            for q in range(4):
                u.rect(x+127+q*38, 493+q*3, 26, 35, "#263b3c", 3)
        else:
            for q in range(3):
                xx=x+100+q*105
                u.rect(xx, 483, 75, 65, "#e5f0f6", 5, "#8ab1c6")
                u.text(xx+37, 522, ["REG", "ALU", "RAM"][q], 12, "bold", C["blue"], "middle")
                if q < 2:
                    u.line(xx+75, 515, xx+105, 515, C["blue"], 3)
        u.text(x+29, 617, task, 12, color="#5a7181")
        u.button(x+407, 604, 120, primary, active=True)
    u.text(302, 830, "Explorar abre una computadora de referencia sin alterar tu avance.",
           13, color="#576b7c")
    u.status("Inicio · Sin CPU seleccionada", "Motor: detenido",
             "Progresos independientes", zoom="—")
    return u.save()


def im03():
    u = UI("IM-03")
    u.shell("Aula-8", "Inspeccionar NAND2",
            [("Volver", 88, False, False), ("Abrir detalle", 120, True, False),
             ("Subir nivel", 104, False, False), ("Centrar", 88, False, False),
             ("Pista", 80, False, False)],
            [("Placa 3D", 132, False), ("Esquema 2D", 158, False),
             ("Programa", 140, True)], "Esquema 2D", "NAND2 › CMOS › Transistores",
            active_dock="Señales")
    u.side(active="Compuerta NAND", kit=True)
    u.canvas()
    u.text(320, 228, "AULA-8  ›  COMPUERTA NAND2  ›  CMOS", 13, "bold", "#43586a")
    u.badge(1030, 210, "ESQUEMA 2D", "#e5f1f7", C["blue"])
    u.text(620, 268, "VDD", 16, "bold", "#275475", "middle")
    u.line(620, 277, 620, 298, "#244e68", 3.5)
    u.line(490, 298, 820, 298, "#244e68", 3.5)
    # CMOS static NAND: parallel PMOS pull-up and series NMOS pull-down.
    for x, label, gate in [(525, "P1 · PMOS", "A"), (785, "P2 · PMOS", "B")]:
        u.line(x, 298, x, 341, "#244e68", 3.5)
        u.rect(x-40, 341, 80, 57, "#e8f2ec", 5, "#75ae93", 2)
        u.text(x, 363, label, 12, "bold", "#2c6050", "middle")
        u.text(x, 382, f"G={gate}", 11, color="#557e6b", anchor="middle")
        u.line(x, 398, x, 440, "#244e68", 3.5)
    u.line(525, 440, 950, 440, "#244e68", 3.5)
    u.circle(650, 440, 5, "#244e68")
    u.text(968, 445, "Y = ¬(A · B)", 17, "bold", C["blue"])
    u.line(650, 440, 650, 475, "#244e68", 3.5)
    for y, label, gate in [(475, "N1 · NMOS", "A"), (580, "N2 · NMOS", "B")]:
        u.rect(610, y, 80, 61, "#e5eff6", 5, "#7ba7c6", 2)
        u.text(650, y+23, label, 12, "bold", C["blue"], "middle")
        u.text(650, y+43, f"G={gate}", 11, color="#557e92", anchor="middle")
        u.line(650, y+61, 650, (580 if y == 475 else 677), "#244e68", 3.5)
    u.line(629, 677, 671, 677, "#244e68", 3)
    u.line(635, 684, 665, 684, "#244e68", 3)
    u.line(644, 690, 656, 690, "#244e68", 3)
    u.text(697, 685, "GND", 13, "bold", "#275475")
    u.text(322, 710, "PMOS en paralelo · NMOS en serie · modelo lógico, no simulación SPICE.",
           12, color=C["muted"])
    u.inspector("N1 · NMOS", "Transistor lógico de canal N",
                ["Parte de la ruta hacia tierra.",
                 "La salida baja si A=1 y B=1."],
                [("Terminal G", "Entrada A"), ("Ruta", "Serie con N2"),
                 ("Estado", "Sin prueba")], "Modelo: representación didáctica")
    u.text(22, 831, "La selección del transistor se conserva al volver a Placa 3D.",
           13, color="#576a79")
    u.status("Aula-8 · Construir · NAND2", "CPU: detenida", "Montaje: en curso")
    return u.save()


def im04():
    u = UI("IM-04")
    u.shell("Aula-8", "Prueba de compuerta",
            [("Probar", 94, True, False), ("Cambiar entradas", 157, False, False),
             ("Abrir resultados", 152, False, False), ("Volver", 88, False, False)],
            [("Placa 3D", 132, False), ("Esquema 2D", 158, False),
             ("Programa", 140, True)], "Esquema 2D",
            "Caso: A=1, B=1", dock_top=615, active_dock="Problemas")
    u.side(active="Compuerta NAND", kit=False)
    u.canvas(bottom=592)
    u.text(320, 228, "PRUEBA DE NAND2", 15, "bold")
    u.badge(986, 209, "1 discrepancia", "#fce8e7", C["red"], 175)
    # Abstract gate, not undocumented pin-level schematic.
    u.line(390, 374, 568, 374, "#557d95", 4)
    u.line(390, 458, 568, 458, "#557d95", 4)
    u.text(372, 379, "A = 1", 16, "bold", C["blue"], "end")
    u.text(372, 463, "B = 1", 16, "bold", C["blue"], "end")
    u.path("M568 326 L670 326 A90 90 0 0 1 670 505 L568 505 Z",
           "#e9f2f9", "#517f9d", 4)
    u.circle(769, 415, 12, C["white"], "#517f9d", 4)
    u.line(781, 415, 938, 415, C["red"], 4)
    u.text(955, 407, "Y observada: 1", 18, "bold", C["red"])
    u.text(955, 438, "Y esperada: 0", 15, "bold", C["blue"])
    u.rect(338, 530, 842, 39, "#fff1ed", 5, "#f0c4bf")
    u.text(356, 555, "La salida no coincide con la tabla NAND. La causa aún no se ha determinado.",
           13, color="#9a4f49")
    u.inspector("NAND2", "Prueba de verdad",
                ["Compara entradas y salida.",
                 "No supone una falla física."],
                [("Entrada A", "1"), ("Entrada B", "1"),
                 ("Esperado", "0"), ("Observado", "1")],
                "Resultado: no superado", compact=True)
    u.text(20, 682, "PROBLEMA · PR-004", 13, "bold", C["red"])
    u.text(20, 713, "Para A=1 y B=1 se observó 1, pero NAND2 debe producir 0.",
           14, color=C["ink"])
    u.text(20, 745, "Revisa el circuito y vuelve a probar. No hay evidencia suficiente para señalar una pieza.",
           12, color=C["muted"])
    u.line(0, 773, 1600, 773)
    u.text(20, 801, "Vectores: 00→1   ✓     01→1   ✓     10→1   ✓     11→1   ✕  (esperado 0)",
           13, "bold", C["blue"])
    u.status("Aula-8 · Probar módulo", "CPU: detenida", "Pruebas: 3 de 4")
    return u.save()


def im05():
    u = UI("IM-05")
    u.shell("Aula-8", "Programa y monitor",
            [("Traducir", 98, False, True), ("Cargar", 87, False, True),
             ("Ejecutar", 94, False, True), ("Detener", 94, False, True)],
            [("Placa 3D", 132, False), ("Esquema 2D", 158, False),
             ("Programa", 140, False)], "Programa",
            "Código conceptual · herramientas aún no implementadas",
            active_dock="Salida")
    u.side(active="Buses y transferencia", kit=False)
    u.canvas(background="#e6edf3")
    u.text(320, 229, "PROGRAMA  ›  EDITOR + PANTALLA", 13, "bold", "#43586a")
    u.badge(974, 210, "EJEMPLO CONCEPTUAL", "#fff3df", C["amber"], 219)
    u.rect(312, 256, 438, 400, "#ffffff", 6, "#cbd7e2")
    u.rect(312, 256, 438, 38, "#f0f5f9", 6)
    u.text(331, 281, "Editor · pseudocódigo", 13, "bold", C["blue"])
    u.line(346, 312, 346, 627, "#e1e8ee")
    source = [
        "; Ejemplo didáctico, no ISA aprobada",
        "INICIO:",
        "  A ← 65            ; letra 'A'",
        "  MONITOR ← A",
        "  DETENER",
        "",
        "; El ensamblador real queda",
        "; pendiente de implementación."
    ]
    for i, s in enumerate(source):
        y = 329 + i*32
        u.text(329, y, str(i+1), 11, color="#92a3b1", anchor="end",
               family="DejaVu Sans Mono, monospace")
        u.text(361, y, s, 12, color=("#537c69" if s.startswith(";") else "#274c68"),
               family="DejaVu Sans Mono, monospace")
    u.rect(765, 256, 450, 400, "#ffffff", 6, "#cbd7e2")
    u.rect(765, 256, 450, 38, "#f0f5f9", 6)
    u.text(785, 281, "Monitor de texto · 32 × 16", 13, "bold", C["blue"])
    u.rect(792, 316, 397, 287, "#0f2220", 5, "#355b52", 2)
    # 16 rows of 32 cells are shown as a subtle virtual grid, not a second screen.
    for i in range(1, 32):
        x=792 + 397*i/32
        u.line(x, 316, x, 603, "#16332e", .65)
    for j in range(1,16):
        y=316 + 287*j/16
        u.line(792, y, 1189, y, "#16332e", .65)
    u.text(811, 349, "AULA-8", 18, "bold", "#94d8b7",
           family="DejaVu Sans Mono, monospace")
    u.text(811, 377, "> A", 17, "bold", "#94d8b7",
           family="DejaVu Sans Mono, monospace")
    u.text(800, 629, "Salida ilustrativa; no corresponde a una CPU ejecutada.",
           11, color=C["muted"])
    u.inspector("Monitor", "Salida de texto virtual",
                ["Una única pantalla conectada.",
                 "No hay terminal separado."],
                [("Columnas", "32"), ("Filas", "16"),
                 ("Glifo", "8 × 8 píxeles"),
                 ("Modo", "Texto")], "Estado: vista de diseño")
    u.text(21, 832, "Sin ejecución real: los botones permanecerán deshabilitados hasta disponer del motor.",
           13, color="#576a79")
    u.status("Aula-8 · Programa", "Motor: no disponible", "Archivo: sin traducir")
    return u.save()


def im06():
    u = UI("IM-06")
    u.shell("Aula-16", "Memoria en dos bancos",
            [("Inspeccionar", 115, True, False), ("Mostrar señales", 137, False, False),
             ("Un pulso", 94, False, True), ("Ejecutar", 95, False, True)],
            [("Esquema 2D", 158, False), ("Programa", 141, True)],
            "Esquema 2D", "Palabra alineada · lectura conceptual",
            active_dock="Señales")
    u.side(cpu="AULA-16", active="Memoria par / impar", kit=False)
    u.canvas(background="#f5f8fa")
    u.text(320, 228, "AULA-16  ›  RAM  ›  DOS BANCOS DE 8 BITS",
           13, "bold", "#43586a")
    u.badge(1007, 209, "2D · SIN 3D", "#e5f1f7", C["blue"], 162)
    u.rect(333, 345, 188, 197, "#e1f0f6", 8, "#83b3cd", 2)
    u.text(427, 380, "CPU AULA-16", 17, "bold", "#285977", "middle")
    for y,label in [(423,"A[15:0]"),(462,"D[15:0]"),(501,"Lectura / escritura")]:
        u.text(427, y, label, 13, color="#406a82", anchor="middle")
    for x,title,low,byte,bg in [(747,"Banco PAR","D[7:0]","0x34","#e7f2e9"),
                                 (983,"Banco IMPAR","D[15:8]","0x12","#f1e8f5")]:
        u.rect(x, 331, 203, 222, bg, 8, "#a8becd", 2)
        u.text(x+101, 370, title, 15, "bold", C["ink"], "middle")
        u.text(x+101, 405, "8 bits", 13, color="#527080", anchor="middle")
        u.text(x+101, 444, low, 13, "bold", C["blue"], "middle")
        u.rect(x+52, 470, 100, 43, "#ffffff", 5, "#bfccd6")
        u.text(x+102, 497, byte, 19, "bold", C["blue"], "middle")
    # Abstract bus connections, not pin-to-pin / electrical claim.
    u.line(521, 408, 711, 408, C["blue"], 6)
    u.line(711, 408, 711, 292, C["blue"], 6)
    u.line(711, 292, 1084, 292, C["blue"], 6)
    u.line(848, 292, 848, 331, C["blue"], 6)
    u.line(1084, 292, 1084, 331, C["blue"], 6)
    u.text(727, 279, "Dirección A[15:1] · 15 líneas", 13, "bold", C["blue"])
    u.line(521, 472, 679, 472, "#299177", 5)
    u.line(679, 472, 679, 580, "#299177", 5)
    u.line(679, 580, 848, 580, "#299177", 5)
    u.line(848, 580, 848, 553, "#299177", 5)
    u.line(521, 486, 653, 486, "#9a72ba", 5)
    u.line(653, 486, 653, 614, "#9a72ba", 5)
    u.line(653, 614, 1084, 614, "#9a72ba", 5)
    u.line(1084, 614, 1084, 553, "#9a72ba", 5)
    u.text(770, 603, "Byte bajo", 12, "bold", "#247b64")
    u.text(932, 634, "Byte alto", 12, "bold", "#9161b1")
    u.rect(351, 649, 820, 57, "#e9eff6", 5, "#bfcfdd")
    u.text(370, 671, "Dirección 0x6000 (par)     0x6000 → 0x34     0x6001 → 0x12",
           13, "bold", "#2a506b")
    u.text(370, 691, "Palabra reconstruida: 0x1234  ·  little-endian  ·  capacidad instalada sin fijar",
           12, color="#5c7385")
    u.inspector("Lectura de palabra", "Organización candidata",
                ["Dos bancos de 8 bits.",
                 "Una palabra usa dos bytes."],
                [("Dirección", "0x6000"),
                 ("Byte bajo", "0x34"),
                 ("Byte alto", "0x12"),
                 ("Resultado", "0x1234")], "Sin temporización física validada")
    u.text(21, 831, "Ejemplo de acceso alineado; no implica 64 KiB de RAM físicamente instalada.",
           13, color="#576a79")
    u.status("Aula-16 · Construir · Memoria", "Motor: detenido",
             "Diseño de interfaz propuesto")
    return u.save()


if __name__ == "__main__":
    for generator in (im01, im03, im04, im05, im06):
        print(generator())
