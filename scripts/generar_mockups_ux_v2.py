"""Segunda revisión de UX: diez pantallas, toolbar con iconos SVG.

Reutiliza los planos V1 sin alterarlos. Las nuevas escenas siguen siendo
maquetas deterministas de producto, no ejecuciones de una CPU real.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "ux" / "mockups"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

spec = importlib.util.spec_from_file_location(
    "aula_ux_v1", Path(__file__).with_name("generar_mockups_ux_im01_im06.py")
)
base = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(base)
UI = base.UI
C = base.C


TOOLBARS = {
    "IM-01": ([
        ("Continuar", "play", True, False),
        ("Construir", "tool", False, False),
        ("Explorar", "eye", False, False),
    ], "Dos recorridos independientes", None),
    "IM-02": ([
        ("Seleccionar", "cursor", False, False),
        ("Colocar", "plus", True, False),
        ("Quitar", "trash", False, False),
        ("Deshacer", "undo", False, False),
        ("Pista", "bulb", False, False),
        ("Probar", "check", False, False),
    ], "Etapa: montar una NAND", "Montaje sin comprobar"),
    "IM-03": ([
        ("Volver", "back", False, False),
        ("Abrir detalle", "zoom", True, False),
        ("Subir nivel", "up", False, False),
        ("Centrar", "target", False, False),
        ("Pista", "bulb", False, False),
    ], "NAND2 › CMOS › Transistores", None),
    "IM-04": ([
        ("Probar", "check", True, False),
        ("Cambiar entradas", "switch", False, False),
        ("Abrir resultados", "list", False, False),
        ("Volver", "back", False, False),
    ], "Caso: A=1, B=1", None),
    "IM-05": ([
        ("Traducir", "code", False, True),
        ("Cargar", "upload", False, True),
        ("Ejecutar", "play", False, True),
        ("Detener", "stop", False, True),
    ], "Código conceptual · herramientas aún no implementadas", None),
    "IM-06": ([
        ("Inspeccionar", "zoom", True, False),
        ("Mostrar señales", "activity", False, False),
        ("Un pulso", "step", False, True),
        ("Ejecutar", "play", False, True),
    ], "Palabra alineada · lectura conceptual", None),
    "IM-07": ([
        ("Volver a construir", "back", False, False),
        ("Inspeccionar", "zoom", True, False),
        ("Pausar", "pause", False, True),
        ("Un pulso", "step", False, True),
        ("Señales", "activity", False, False),
    ], "Referencia completa · no modifica el progreso", "Exploración de referencia"),
    "IM-08": ([
        ("Subir nivel", "up", False, False),
        ("Abrir detalle", "zoom", True, False),
        ("Centrar", "target", False, False),
        ("Pista", "bulb", False, False),
    ], "Aula-8 › Registro A › Bit 0", None),
    "IM-09": ([
        ("Continuar", "play", True, False),
        ("Construir", "tool", False, False),
        ("Explorar", "eye", False, False),
    ], "Preferencias de la aplicación", None),
    "IM-10": ([
        ("Mostrar paneles", "panels", False, False),
        ("Centrar", "target", False, False),
        ("Zoom −", "minus", False, False),
        ("Zoom +", "plus", False, False),
        ("Salir de concentración", "panels", True, False),
    ], "Modo concentración", None),
}


def elem(parent, name, **attrs):
    return ET.SubElement(parent, f"{{{NS}}}{name}", {k.replace("_", "-"): str(v)
                                                  for k, v in attrs.items()})


# Trazos iconográficos vectoriales originales, sin tipografía de iconos externa.
ICON_PATHS = {
    "play": ["M8 5 L19 12 L8 19 Z"],
    "pause": ["M8 5 V19", "M16 5 V19"],
    "stop": ["M6 6 H18 V18 H6 Z"],
    "cursor": ["M5 3 L5 21 L10 16 L14 22 L17 20 L13 14 L21 12 Z"],
    "plus": ["M12 5 V19", "M5 12 H19"],
    "minus": ["M5 12 H19"],
    "trash": ["M5 7 H19", "M9 7 V5 H15 V7", "M7 7 L8 20 H16 L17 7",
              "M10 10 V17", "M14 10 V17"],
    "undo": ["M9 7 L4 12 L9 17", "M4 12 H15 Q21 12 20 19"],
    "back": ["M13 5 L6 12 L13 19", "M6 12 H20"],
    "up": ["M5 13 L12 6 L19 13", "M12 6 V20"],
    "zoom": ["M11 5 A6 6 0 1 0 11 17 A6 6 0 1 0 11 5",
             "M16 16 L21 21"],
    "target": ["M12 3 A9 9 0 1 0 12 21 A9 9 0 1 0 12 3",
               "M12 8 A4 4 0 1 0 12 16 A4 4 0 1 0 12 8"],
    "bulb": ["M7 10 A5 5 0 1 1 17 10 Q17 14 14 16 V18 H10 V16 Q7 14 7 10",
             "M10 21 H14"],
    "check": ["M5 12 L10 17 L20 6", "M4 4 H20 V20 H4 Z"],
    "tool": ["M5 19 L16 8", "M14 5 L19 10", "M4 18 L7 21"],
    "eye": ["M2 12 Q12 1 22 12 Q12 23 2 12 Z",
             "M12 9 A3 3 0 1 0 12 15 A3 3 0 1 0 12 9"],
    "switch": ["M4 8 H20", "M16 4 L20 8 L16 12",
               "M20 16 H4", "M8 12 L4 16 L8 20"],
    "list": ["M8 6 H21", "M8 12 H21", "M8 18 H21",
             "M3 6 H4", "M3 12 H4", "M3 18 H4"],
    "code": ["M9 6 L3 12 L9 18", "M15 6 L21 12 L15 18"],
    "upload": ["M12 18 V4", "M6 10 L12 4 L18 10", "M4 17 V21 H20 V17"],
    "activity": ["M2 13 H7 L10 6 L14 18 L17 11 H22"],
    "step": ["M5 5 L15 12 L5 19 Z", "M19 5 V19"],
    "panels": ["M4 4 H20 V20 H4 Z", "M9 4 V20", "M4 10 H20"],
}


def icon(group, x, y, name, color):
    ico = elem(group, "g", transform=f"translate({x},{y}) scale(0.70)")
    for p in ICON_PATHS[name]:
        elem(ico, "path", d=p, fill="none", stroke=color,
             stroke_width="1.9", stroke_linecap="round",
             stroke_linejoin="round")


def enhance_toolbar(source: Path, destination: Path, scene: str):
    t = ET.parse(source)
    root = t.getroot()
    g = elem(root, "g", id="toolbar_icons_v2")
    elem(g, "rect", x=0, y=80, width=1600, height=55, fill="#f8fafc")
    actions, status, badge = TOOLBARS[scene]
    x = 20
    for label, glyph, active, disabled in actions:
        width = max(88, int(len(label) * 7.1 + 54))
        fill = C["blue"] if active else ("#f1f3f5" if disabled else "#ffffff")
        stroke = C["blue"] if active else "#cdd9e4"
        fg = "#ffffff" if active else ("#a6b3c0" if disabled else C["ink"])
        elem(g, "rect", x=x, y=90, width=width, height=34, rx=4,
             fill=fill, stroke=stroke, stroke_width=1)
        icon(g, x+9, 98, glyph, fg)
        elem(g, "text", x=x+36, y=112.5, fill=fg,
             font_size=12.3, font_family="DejaVu Sans, sans-serif",
             font_weight="bold" if active else "normal").text = label
        x += width + 9
    elem(g, "line", x1=x+4, y1=89, x2=x+4, y2=124,
         stroke="#d5dde5", stroke_width=1)
    elem(g, "text", x=x+19, y=112.5, fill="#485e72",
         font_size=12.5, font_family="DejaVu Sans, sans-serif").text = status
    if badge:
        elem(g, "rect", x=1345, y=94, width=227, height=26, rx=13,
             fill="#fff3df", stroke="none")
        elem(g, "text", x=1458, y=111.5, text_anchor="middle",
             fill="#9c6d1d", font_size=11.6,
             font_family="DejaVu Sans, sans-serif",
             font_weight="bold").text = badge
    elem(g, "line", x1=0, y1=135, x2=1600, y2=135,
         stroke="#d7e0e9", stroke_width=1)
    # Native menus appear above the toolbar, including its icon overlay.
    for child in list(root):
        if child.get("id") == "menu_ver_abierto":
            root.remove(child)
            root.append(child)
    t.write(destination, encoding="utf-8", xml_declaration=True)


def save_v2(u: UI):
    path = OUT / f"{u.label}_AULA_UX_V1.svg"
    u.d.saveas(str(path))
    return path


def scene07():
    u = UI("IM-07")
    u.shell("Aula-8", "Explorar referencia",
            [("Volver a construir", 169, False, False),
             ("Inspeccionar", 114, True, False), ("Pausar", 82, False, True),
             ("Un pulso", 88, False, True), ("Señales", 86, False, False)],
            [("Placa 3D", 132, False), ("Esquema 2D", 158, False),
             ("Programa", 140, True)],
            "Esquema 2D", "Referencia completa · no modifica el progreso",
            active_dock="Señales")
    u.panel_title(20, 165, "EXPLORAR AULA-8")
    u.line(18, 181, 251, 181)
    u.text(20, 210, "Computadora de referencia", 15, "bold")
    u.badge(20, 225, "Solo lectura", "#e9f2f9", C["blue"], 117)
    for i, label in enumerate(["CPU y registros", "ALU y banderas", "Control",
                               "RAM y ROM", "Monitor y E/S"]):
        y=290 + i*47
        if i==1:
            u.rect(10, y-23, 250, 36, C["pale"], 4)
            u.rect(10, y-23, 4, 36, C["blue"])
        u.text(28, y, label, 13, "bold" if i==1 else "normal")
    u.line(18, 544, 251, 544)
    u.panel_title(20, 575, "SIN CAMBIAR EL AVANCE")
    for i, s in enumerate(["La máquina se puede observar", "desde el primer momento.",
                           "Aquí no se colocan piezas."]):
        u.text(20, 604 + 22*i, s, 12, color=C["muted"])
    u.canvas()
    u.text(323, 229, "AULA-8  ›  CPU  ›  RUTA DE DATOS",
           13, "bold", "#43586a")
    u.badge(1033, 209, "ESQUEMA FUNCIONAL", "#e5f1f7", C["blue"], 170)
    # Blocks and schematic grouping; arrows denote functional transfers only.
    blocks = [(351, 325, 160, 86, "PC", "Dirección"),
              (569, 325, 160, 86, "MAR", "Dirección"),
              (790, 325, 184, 86, "RAM / ROM", "Memoria"),
              (351, 520, 160, 86, "Registro A", "8 bits"),
              (569, 520, 160, 86, "ALU", "8 bits"),
              (790, 520, 184, 86, "Registro B", "8 bits")]
    for x,y,w,h,title,sub in blocks:
        u.rect(x,y,w,h,"#e5f0f7",7,"#a1c1d6",2)
        u.text(x+w/2,y+34,title,17,"bold",C["blue"],"middle")
        u.text(x+w/2,y+60,sub,12,color=C["muted"],anchor="middle")
    for x1,y1,x2,y2,col in [(511,367,569,367,C["blue"]),
                             (729,367,790,367,C["blue"]),
                             (511,563,569,563,C["green"]),
                             (729,563,790,563,C["green"])]:
        u.line(x1,y1,x2,y2,col,4)
        u.path(f"M{x2-9} {y2-5} L{x2} {y2} L{x2-9} {y2+5}",
               "none",col,2)
    u.line(882,411,882,520,C["blue"],3,"7 5")
    u.line(432,411,432,520,C["blue"],3,"7 5")
    u.text(355,288,"Buses agrupados para lectura; ampliar un módulo abre sus bits.",12,color=C["muted"])
    u.text(348,662,"BUS[7:0] (ejemplo visual)",13,"bold",C["blue"])
    for i,val in enumerate("00101010"):
        u.rect(575+i*43,634,34,41,("#bfe7d5" if val=="1" else "#e1e8ee"),
               4,"#aebfcb")
        u.text(592+i*43,661,val,16,"bold",
               "#216d58" if val=="1" else "#627789","middle")
    u.inspector("ALU de Aula-8", "Bloque funcional",
                ["Muestra una operación lógica.",
                 "Abre el detalle para ver un bit."],
                [("Ancho", "8 bits"), ("Vista", "Referencia"),
                 ("Edición", "Bloqueada")],
                "No es una CPU ejecutada")
    u.text(21,831,"Valores ilustrativos de una futura simulación; no proceden de un motor real.",
           13,color="#576a79")
    u.status("Aula-8 · Explorar referencia", "Motor: demostración visual",
             "Progreso: sin cambios")
    return save_v2(u)


def scene08():
    u=UI("IM-08")
    u.shell("Aula-8","Detalle de registro",
            [("Subir nivel",110,False,False),("Abrir detalle",127,True,False),
             ("Centrar",92,False,False),("Pista",78,False,False)],
            [("Placa 3D",132,False),("Esquema 2D",158,False),
             ("Programa",140,True)],
            "Esquema 2D", "Aula-8 › Registro A › Bit 0",active_dock="Pruebas")
    u.panel_title(20,165,"JERARQUÍA DEL CIRCUITO")
    u.line(18,181,251,181)
    for y,label,level in [(215,"Aula-8",0),(258,"CPU",1),
                           (301,"Registro A",2),(344,"Celda del bit 0",3)]:
        if level==3:
            u.rect(10,y-25,251,38,C["pale"],4)
            u.rect(10,y-25,4,38,C["blue"])
        u.text(20+level*11,y,("▸ " if level!=3 else "• ")+label,13,
               "bold" if level==3 else "normal")
    u.line(18,389,251,389)
    u.panel_title(20,420,"VISTAS DEL MISMO ELEMENTO")
    u.button(16,442,116,"Símbolo",True)
    u.button(139,442,115,"Transistores",False,True)
    for i,s in enumerate(["El registro tiene ocho celdas.",
                          "Aquí inspeccionas una sola.",
                          "El despiece físico depende del",
                          "circuito aprobado de esa celda."]):
        u.text(20,522+i*23,s,12,color=C["muted"])
    u.canvas()
    u.text(320,228,"CPU  ›  REGISTRO A  ›  CELDA DEL BIT 0",13,"bold","#43586a")
    u.badge(1030,210,"NIVEL LÓGICO","#e5f1f7",C["blue"])
    u.text(320,282,"REGISTRO DE 8 BITS",16,"bold",C["blue"])
    for i in range(8):
        x=324+i*108
        active=i==0
        u.rect(x,302,92,68,"#d5ebe3" if active else "#e5edf3",
               5,C["green"] if active else "#aebfcc",2.5 if active else 1)
        u.text(x+46,328,f"BIT {i}",12,"bold",C["blue"],"middle")
        u.text(x+46,350,"1" if active else "0",16,"bold",
               "#216d58" if active else "#64798a","middle")
    u.line(370,371,370,426,C["green"],2.5,"6 4")
    u.text(321,437,"AMPLIACIÓN · CELDA DEL BIT 0",14,"bold",C["blue"])
    u.rect(373,464,770,207,"#ffffff",8,"#cbd8e4")
    u.rect(641,508,235,106,"#e8f1f8",7,"#83aac4",2)
    u.text(759,547,"CELDA DE MEMORIA",16,"bold",C["blue"],"middle")
    u.text(759,578,"D  ·  CLK  ·  Q",13,color="#516e83",anchor="middle")
    u.line(448,541,641,541,C["blue"],4)
    u.text(440,532,"D = 1",14,"bold",C["blue"],"end")
    u.line(536,601,641,601,C["amber"],4)
    u.text(528,622,"CLK",13,"bold",C["amber"],"end")
    u.line(876,556,1050,556,C["green"],4)
    u.text(1065,562,"Q = 1",15,"bold",C["green"])
    u.text(399,654,"Vista funcional; la topología transistor a transistor se consulta en el módulo validado.",
           11,color=C["muted"])
    u.inspector("Celda · bit 0","Memoria de un bit",
                ["Conserva un estado lógico.",
                 "Forma parte del registro A."],
                [("Entrada D","1"),("Salida Q","1"),
                 ("Reloj","Sin pulso")],"Vista: símbolo funcional")
    u.text(20,831,"Seleccionar una celda cambia el foco; subir nivel conserva el estado del montaje.",
           13,color="#576a79")
    u.status("Aula-8 · Registro A · Bit 0","Motor: detenido",
             "Selección: celda A0")
    return save_v2(u)


def scene09():
    # A modal window reuses the start screenshot under a translucent scrim.
    src=OUT/"IM-01_AULA_UX_V1.svg"
    out=OUT/"IM-09_AULA_UX_V1.svg"
    tree=ET.parse(src)
    root=tree.getroot()
    g=elem(root,"g",id="preferencias_modal_v1")
    elem(g,"rect",x=0,y=136,width=1600,height=722,fill="#102238",
         opacity=".24")
    elem(g,"rect",x=452,y=174,width=695,height=515,rx=6,
         fill="#ffffff",stroke="#9caebe",stroke_width=2)
    elem(g,"rect",x=452,y=174,width=695,height=52,rx=6,fill="#f0f5f9")
    elem(g,"text",x=479,y=207,fill=C["ink"],font_size=18,
         font_weight="bold",font_family="DejaVu Sans, sans-serif").text="Preferencias"
    elem(g,"text",x=1112,y=207,fill="#6b7d90",
         font_size=21,font_family="DejaVu Sans, sans-serif").text="×"
    elem(g,"rect",x=453,y=226,width=186,height=394,fill="#f7f9fc")
    for i,label in enumerate(["Apariencia","Interacción","Accesibilidad","Guardado"]):
        y=270+i*56
        if i==1:
            elem(g,"rect",x=461,y=y-28,width=171,height=42,
                 rx=4,fill="#e1edf6")
            elem(g,"rect",x=461,y=y-28,width=4,height=42,fill=C["blue"])
        elem(g,"text",x=482,y=y,fill=C["blue"] if i==1 else C["ink"],
             font_size=13,font_weight="bold" if i==1 else "normal",
             font_family="DejaVu Sans, sans-serif").text=label
    elem(g,"text",x=673,y=270,fill=C["ink"],font_size=17,font_weight="bold",
         font_family="DejaVu Sans, sans-serif").text="Interacción y navegación"
    settings=[("Mostrar ayudas breves al pasar el ratón",True),
              ("Resaltar el elemento seleccionado",True),
              ("Mantener inspector visible al cambiar de pestaña",True),
              ("Reducir animaciones de cámara",False)]
    for i,(label,on) in enumerate(settings):
        y=326+i*56
        elem(g,"rect",x=679,y=y-19,width=19,height=19,rx=2,
             fill="#e6f2ee" if on else "#ffffff",
             stroke="#8ea9ba")
        if on:
            elem(g,"path",d=f"M684 {y-10} L688 {y-5} L695 {y-15}",
                 fill="none",stroke=C["green"],stroke_width=2.2)
        elem(g,"text",x=716,y=y-3,fill=C["ink"],font_size=12.5,
             font_family="DejaVu Sans, sans-serif").text=label
    elem(g,"text",x=677,y=550,fill=C["muted"],font_size=12,
         font_family="DejaVu Sans, sans-serif").text=(
         "El avance se guarda automáticamente; no existe gestor de proyectos.")
    elem(g,"line",x1=453,y1=620,x2=1146,y2=620,
         stroke="#d7e0e9",stroke_width=1)
    for x,w,label,primary in [(677,120,"Restaurar",False),
                               (873,104,"Cancelar",False),
                               (990,121,"Aplicar",True)]:
        elem(g,"rect",x=x,y=639,width=w,height=34,rx=4,
             fill=C["blue"] if primary else "#f9fbfd",
             stroke=C["blue"] if primary else "#cbd7e1")
        elem(g,"text",x=x+w/2,y=660,text_anchor="middle",font_size=12.5,
             font_family="DejaVu Sans, sans-serif",
             font_weight="bold" if primary else "normal",
             fill="#ffffff" if primary else C["ink"]).text=label
    tree.write(out,encoding="utf-8",xml_declaration=True)
    return out


def scene10():
    u=UI("IM-10")
    u.shell("Aula-8","Concentración",
            [("Mostrar paneles",132,False,False),("Centrar",88,False,False),
             ("Zoom −",80,False,False),("Zoom +",80,False,False),
             ("Salir de concentración",197,True,False)],
            [("Esquema 2D",158,False),("Programa",141,True)],
            "Esquema 2D","Modo concentración",no_inspector=True,
            active_dock=None)
    u.rect(0,136,57,630,"#f6f9fc")
    u.line(56,136,56,766)
    for y,label in [(191,"≡"),(248,"⌂"),(305,"＋"),(362,"−"),(419,"◎")]:
        u.text(28,y,label,22,"bold",C["blue"],"middle")
    u.rect(57,136,1543,48,"#f9fbfd")
    u.button(79,143,158,"Esquema 2D",True)
    u.button(245,143,144,"Programa",disabled=True)
    u.rect(81,199,1494,539,"#f5f8fa",7,"#cbd7e2")
    u.text(103,228,"ESQUEMA 2D AMPLIADO  ›  NAND2",14,"bold",C["blue"])
    u.badge(1375,209,"ZOOM 160 %","#e5f1f7",C["blue"],165)
    # Expanded logic-gate diagram. Wires stand for signals, not arbitrary pinouts.
    u.line(334,395,656,395,C["blue"],5)
    u.line(334,531,656,531,C["blue"],5)
    u.text(314,402,"A",23,"bold",C["blue"],"end")
    u.text(314,538,"B",23,"bold",C["blue"],"end")
    u.path("M656 320 L824 320 A145 145 0 0 1 824 606 L656 606 Z",
           "#e3eff7","#517f9d",5)
    u.circle(956,463,17,C["white"],"#517f9d",5)
    u.line(973,463,1299,463,C["green"],5)
    u.text(1312,470,"Y",23,"bold",C["green"])
    u.text(190,685,"Los paneles se ocultan; el circuito conserva selección, zoom y estado.",
           14,color=C["muted"])
    # Concentration mode also hides the bottom dock; the statusbar stays.
    u.rect(0,767,1600,91,"#ecf1f5")
    u.rect(81,738,1494,108,"#f5f8fa")
    u.line(81,846,1575,846,"#cbd7e2")
    u.text(190,821,"Paneles ocultos · pulsa «Salir de concentración» para recuperarlos.",
           13,color="#576a79")
    u.status("Aula-8 · Concentración","Motor: detenido",
             "Paneles: ocultos",zoom="160 %")
    out=save_v2(u)
    # Open the actual Ver menu on top of the focus-mode scene.
    tree=ET.parse(out)
    root=tree.getroot()
    menu=elem(root,"g",id="menu_ver_abierto")
    elem(menu,"rect",x=166,y=76,width=282,height=289,rx=4,
         fill="#ffffff",stroke="#a8b8c6",stroke_width=1.5)
    choices=[("Ajustar a ventana","Ctrl+0"),
             ("Centrar selección","F"),
             ("Zoom +","Ctrl++"),
             ("Zoom −","Ctrl+−"),
             ("Mostrar/ocultar paneles","Tab"),
             ("Modo concentración","F11")]
    for i,(label,shortcut) in enumerate(choices):
        y=108+i*41
        if i==5:
            elem(menu,"rect",x=174,y=y-25,width=266,height=34,
                 fill="#e1edf6",rx=3)
            elem(menu,"text",x=184,y=y-3,fill=C["green"],font_size=16,
                 font_family="DejaVu Sans, sans-serif").text="✓"
        elem(menu,"text",x=201,y=y-3,fill=C["ink"],
             font_size=12.4,font_family="DejaVu Sans, sans-serif").text=label
        elem(menu,"text",x=426,y=y-3,fill=C["muted"],text_anchor="end",
             font_size=11.5,font_family="DejaVu Sans, sans-serif").text=shortcut
    tree.write(out,encoding="utf-8",xml_declaration=True)
    return out


def main():
    for scene in ("IM-01","IM-02","IM-03","IM-04","IM-05","IM-06"):
        old=OUT/f"{scene}_AULA_UX_V1.svg"
        enhance_toolbar(old,OUT/f"{scene}_AULA_UX_V2.svg",scene)
    for generator in (scene07,scene08,scene09,scene10):
        path=generator()
        enhance_toolbar(path,OUT/f"{path.stem.replace('_V1', '_V2')}.svg",path.stem[:5])
        # The intermediate V1 for new scenes is useful only as input to V2.
        # Keep it as a source alternative; no V1 PNG is produced.
    print("10 escenas SVG V2 generadas en",OUT)


if __name__=="__main__":
    main()
