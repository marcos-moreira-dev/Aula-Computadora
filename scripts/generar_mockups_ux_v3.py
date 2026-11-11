"""Tercera revisión semántica UX de Aula-Computadora: 16 escenas vectoriales.

Las capturas son escenarios de diseño. No demuestran un CPU ejecutado,
un circuito físico, una ISA aprobada ni interacción JavaFX implementada.
Conserva V1 y V2, sin sobrescribir sus SVG/PNG.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "ux" / "mockups"
spec = importlib.util.spec_from_file_location(
    "aula_ux_v2", Path(__file__).with_name("generar_mockups_ux_v2.py")
)
v2 = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(v2)
UI, C, elem = v2.UI, v2.C, v2.elem


v2.TOOLBARS.update({
    "IM-11": ([
        ("Seleccionar", "cursor", False, False),
        ("Colocar", "plus", True, False),
        ("Cancelar", "back", False, False),
        ("Pista", "bulb", False, False),
        ("Probar", "check", False, True),
    ], "Arrastra PMOS a la posición P2", "Arrastre activo"),
    "IM-12": ([
        ("Ver pruebas", "check", True, False),
        ("Inspeccionar", "zoom", False, False),
        ("Siguiente etapa", "step", False, False),
    ], "NAND2 validada · módulo reutilizable", "Verificado lógicamente"),
    "IM-13": ([
        ("Iniciar", "play", False, False),
        ("Reanudar", "play", True, False),
        ("Detener", "stop", False, False),
        ("Un pulso", "step", False, False),
        ("Una instrucción", "step", False, False),
        ("Reiniciar", "undo", False, False),
    ], "Instantánea hipotética tras un pulso", "CPU pausada"),
    "IM-14": ([
        ("Examinar", "eye", False, False),
        ("Depositar", "upload", True, False),
        ("Siguiente", "step", False, False),
        ("Ejecutar", "play", False, True),
        ("Detener", "stop", False, True),
    ], "Panel manual · propiedad exclusiva del bus", "CPU detenida"),
    "IM-15": ([
        ("Explorar Aula-8", "eye", False, False),
        ("Volver al recorrido", "back", False, False),
        ("Comenzar Aula-16", "step", True, False),
    ], "Aula-8 completada · progreso conservado", "Recorrido finalizado"),
    "IM-16": ([
        ("Traducir", "code", False, True),
        ("Cargar", "upload", False, True),
        ("Ejecutar", "play", False, True),
        ("Detener", "stop", False, True),
    ], "Una pantalla · modo gráfico exclusivo", "Vídeo: 256 × 128 · 2 bpp"),
})


def svg_rect(parent, x, y, width, height, fill, radius=0, stroke="none", sw=1, **kw):
    return elem(parent, "rect", x=x, y=y, width=width, height=height,
                rx=radius, fill=fill, stroke=stroke, stroke_width=sw, **kw)


def svg_text(parent, x, y, label, size=13, color=None, bold=False, anchor="start"):
    el = elem(parent, "text", x=x, y=y, font_size=size, fill=color or C["ink"],
              text_anchor=anchor, font_family="DejaVu Sans, sans-serif",
              font_weight="bold" if bold else "normal")
    el.text = label
    return el


def svg_line(parent, x1, y1, x2, y2, color=None, width=2, dash=None):
    attrs = dict(x1=x1, y1=y1, x2=x2, y2=y2,
                 stroke=color or C["blue"], stroke_width=width)
    if dash:
        attrs["stroke_dasharray"] = dash
    elem(parent, "line", **attrs)


def replace_text(path: Path, replacements: dict[str, str]):
    tree = ET.parse(path)
    for el in tree.getroot().iter():
        if el.tag.endswith("}text") and el.text:
            for before, after in replacements.items():
                el.text = el.text.replace(before, after)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def add_scene_03_objective(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()
    g = elem(root, "g", id="separar_objetivo_y_piezas_v3")
    svg_rect(g, 0, 429, 270, 338, "#ffffff")
    svg_text(g, 20, 460, "OBJETIVO DE LA ETAPA", 13, C["blue"], True)
    svg_rect(g, 15, 476, 240, 49, "#eaf2f9", 4, "#bfceda")
    svg_text(g, 29, 496, "NAND2 CMOS", 13, C["ink"], True)
    svg_text(g, 29, 515, "Construir y comprobar", 11, C["muted"])
    svg_text(g, 20, 552, "PIEZAS DISPONIBLES", 13, C["blue"], True)
    for yy, title, count in [(568, "PMOS didáctico", "× 2"),
                             (624, "NMOS didáctico", "× 2")]:
        svg_rect(g, 15, yy, 240, 44, "#f7fafc", 4, "#d8e2ea")
        svg_rect(g, 26, yy+12, 20, 20, "#385766", 3)
        svg_text(g, 58, yy+27, title, 12)
        svg_text(g, 240, yy+27, count, 12, C["muted"], True, "end")
    svg_text(g, 20, 709, "La NAND aparece como módulo", 11, C["muted"])
    svg_text(g, 20, 728, "solo tras superar la prueba.", 11, C["muted"])
    tree.write(path, encoding="utf-8", xml_declaration=True)


def correct_scene_07(path: Path):
    """Arquitectura fiel a R0–R3/PC/SP/X sin inventar una topología de bus."""
    tree = ET.parse(path)
    root = tree.getroot()
    g = elem(root, "g", id="arquitectura_aula8_v3")
    svg_rect(g, 292, 199, 953, 539, "#f5f8fa", 7, "#cbd8e4")
    svg_text(g, 320, 228, "AULA-8  ›  CPU  ›  MAPA ARQUITECTÓNICO", 13, "#43586a", True)
    svg_rect(g, 1000, 209, 216, 26, "#e5f1f7", 13)
    svg_text(g, 1108, 227, "NO ES UN NETLIST", 11, C["blue"], True, "middle")
    svg_text(g, 328, 267, "Registros y módulos establecidos; las líneas indican relación funcional.",
             12, C["muted"])
    def block(x, y, w, h, title, subtitle, fill="#e4f0f7"):
        svg_rect(g, x, y, w, h, fill, 6, "#a0c0d5", 1.5)
        svg_text(g, x+w/2, y+27, title, 15, C["blue"], True, "middle")
        svg_text(g, x+w/2, y+49, subtitle, 11, C["muted"], False, "middle")
    for x, title, subtitle in [(326,"PC","16 bits"), (518,"SP","16 bits"),
                               (710,"X","16 bits")]:
        block(x, 304, 156, 65, title, subtitle)
    block(902, 304, 300, 65, "Control / µROM", "Control interno · definición pendiente")
    for x, title in [(326,"R0"),(485,"R1"),(644,"R2"),(803,"R3")]:
        block(x, 407, 132, 67, title, "8 bits", "#e6f1f9")
    block(973, 407, 229, 67, "ALU + Z/C/N/V", "8 bits · indicadores", "#e4f2ea")
    svg_line(g, 338, 499, 1189, 499, C["blue"], 5)
    svg_text(g, 762, 520, "BUS DE DATOS · 8 BITS", 12, C["blue"], True, "middle")
    block(326, 551, 254, 66, "RAM", "Capacidad instalada: por validar")
    block(610, 551, 254, 66, "ROM", "Firmware separado de µROM")
    block(894, 551, 308, 66, "E/S Y PANTALLA", "Periféricos mapeados")
    svg_line(g, 338, 643, 1189, 643, C["blue"], 3)
    svg_text(g, 762, 665, "BUS DE DIRECCIONES · 16 BITS", 12,
             C["blue"], True, "middle")
    svg_text(g, 322, 710, "Vista de bloques didácticos; la conectividad real se deriva del modelo validado.",
             11, C["muted"])
    tree.write(path, encoding="utf-8", xml_declaration=True)


def generate_foundation():
    for i in range(1, 11):
        scene = f"IM-{i:02d}"
        src = OUT / f"{scene}_AULA_UX_V2.svg"
        dst = OUT / f"{scene}_AULA_UX_V3.svg"
        shutil.copyfile(src, dst)
    replace_text(OUT / "IM-02_AULA_UX_V3.svg", {
        "Montaje sin comprobar": "Piezas colocadas · sin probar",
    })
    add_scene_03_objective(OUT / "IM-03_AULA_UX_V3.svg")
    replace_text(OUT / "IM-05_AULA_UX_V3.svg", {
        "Editor · pseudocódigo": "Editor anfitrión · ejemplo",
        "Monitor de texto · 32 × 16": "Pantalla Aula · texto 32 × 16",
        "Una única pantalla conectada.": "Pantalla de la CPU simulada.",
    })
    correct_scene_07(OUT / "IM-07_AULA_UX_V3.svg")
    replace_text(OUT / "IM-08_AULA_UX_V3.svg", {
        "Registro A": "R0", "REGISTRO A": "R0", "registro A": "R0",
        "registro de 8 bits": "R0 de 8 bits", "celda A0": "celda R0.0",
    })


def side_stage(u, stage, title="RECORRIDO AULA-8", kit=None):
    u.panel_title(20, 165, title)
    u.line(18, 181, 251, 181)
    u.text(20, 211, "Construcción guiada", 16, "bold")
    steps = ["Electricidad y señales", "Compuerta NAND", "Latch: memoria de 1 bit",
             "Registro de 8 bits", "Buses y transferencia", "CPU y programa"]
    for i, label in enumerate(steps):
        y = 246 + i*37
        if i == stage:
            u.rect(10,y-24,251,35,C["pale"],4)
            u.rect(10,y-24,4,35,C["blue"])
        mark = "✓" if i < stage else f"{i+1:02d}"
        u.text(20,y,mark,12,"bold",C["green"] if i < stage else "#678196")
        u.text(57,y,label,11.3,"bold" if i == stage else "normal")
    u.line(18,481,251,481)
    u.panel_title(20,508,"KIT DE ESTA ETAPA" if kit else "EN ESTA VISTA")
    if kit:
        for i,(name, count) in enumerate(kit):
            y=526+i*50
            u.rect(15,y,240,40,"#f8fafc",4,"#d9e3eb")
            u.rect(24,y+12,20,20,"#385766",3)
            u.text(56,y+26,name,11.8)
            u.text(245,y+26,count,11,"bold",C["muted"],"end")
    else:
        for i,msg in enumerate(["Selecciona un elemento", "para inspeccionar su estado."]):
            u.text(20,544+i*24,msg,12,color=C["muted"])


def scene11():
    u=UI("IM-11")
    u.shell("Aula-8", "Colocar transistor", [],
            [("Placa 3D",132,False),("Esquema 2D",158,False),
             ("Programa",140,True)], "Placa 3D", "Arrastrar y encajar",
            active_dock="Pruebas")
    side_stage(u,1,kit=[("PMOS didáctico","1 disp."),
                        ("NMOS didáctico","2 disp."),
                        ("Alimentación y tierra","fija")])
    u.text(20,720,"Solo se admiten posiciones",11,color=C["muted"])
    u.text(20,739,"previstas para este circuito.",11,color=C["muted"])
    u.canvas(background="#dce6ee")
    u.text(319,229,"AULA-8  ›  NAND2  ›  COLOCACIÓN GUIADA",13,"bold",C["blue"])
    u.badge(1056,209,"3D DIDÁCTICO","#edf7f8",C["blue"],157)
    u.path("M388 331 L968 289 L1137 641 L519 694 Z", "#276c58", "#164b40",4)
    u.path("M420 361 L952 324 L1095 615 L536 654 Z", "none", "#80ada3",2)
    for x,y,label,done in [(554,380,"P1",True),(783,369,"P2",False),
                            (630,495,"N1",False),(868,493,"N2",False)]:
        fill="#263b42" if done else "none"
        color="#d8efe7" if done else "#abd0c1"
        u.rect(x,y,118,62,fill,4,color,2)
        u.text(x+59,y+35,label,15,"bold",C["white"] if done else "#f0faf4","middle")
    # Ghost placement is deliberately aligned to P2; wiring is predesigned.
    u.rect(778,364,128,72,"#69ba96",5,"#9bf3c4",3)
    u.rect(790,374,105,50,"#e1f4e8",4,"#087552",2)
    u.text(843,403,"PMOS",14,"bold","#0a5a46","middle")
    u.path("M911 400 L928 414 L922 416 L926 427 L920 429 L916 417 L909 422 Z",
           "#ffffff","#253f4a",2)
    u.badge(804,444,"Encaje válido","#dff6e8",C["green"],145)
    u.text(340,714,"Suelta la pieza en P2. La prueba se habilita cuando el montaje esté completo.",
           12,color="#506879")
    u.inspector("PMOS didáctico","Pieza seleccionada",
                ["Conduce hacia la alimentación", "cuando su compuerta está a 0.",
                 "Se coloca en una zona prevista."],
                [("Terminal G","Entrada lógica"),("Terminal D","Salida / nodo"),
                 ("Terminal S","Alimentación")],"Sin prueba lógica")
    u.text(20,831,"Arrastre en curso; una zona inadmisible no debe aceptar la pieza.",
           13,color=C["muted"])
    u.status("Aula-8 · NAND2 · Colocar PMOS","CPU: detenida","Montaje: incompleto",zoom="85 %")
    return u.save()


def scene12():
    u=UI("IM-12")
    u.shell("Aula-8","NAND2 verificada",[],
            [("Placa 3D",132,False),("Esquema 2D",158,False),
             ("Programa",140,True)], "Esquema 2D", "Pruebas NAND",
            active_dock="Pruebas")
    side_stage(u,2,kit=[("NAND2 reutilizable","× 1"),
                        ("Componentes del latch","bloqueados")])
    u.text(20,712,"Se agrupan circuitos ya",11,color=C["muted"])
    u.text(20,733,"comprobados, no miles de piezas.",11,color=C["muted"])
    u.canvas()
    u.text(319,228,"AULA-8  ›  NAND2  ›  RESULTADO",13,"bold",C["blue"])
    u.badge(1024,210,"EJEMPLO DE ÉXITO","#e2f5ed",C["green"],184)
    u.text(340,284,"Circuito aprobado por su prueba didáctica",16,"bold")
    u.line(397,398,533,398,C["blue"],4)
    u.line(397,495,533,495,C["blue"],4)
    u.text(385,404,"A",16,"bold",C["blue"],"end")
    u.text(385,501,"B",16,"bold",C["blue"],"end")
    u.path("M532 355 L602 355 A94 94 0 0 1 602 538 L532 538 Z",
           "#e5f1f8","#5e88a8",4)
    u.circle(699,446,10,"#ffffff","#5e88a8",3)
    u.line(709,446,774,446,C["green"],4)
    u.text(785,451,"Y",17,"bold",C["green"])
    u.rect(839,302,351,283,"#ffffff",6,"#bfcfdb")
    u.text(864,334,"TABLA DE VERDAD",14,"bold",C["blue"])
    for x,h in [(877,"A"),(955,"B"),(1033,"Esperado"),(1144,"Obtenido")]:
        u.text(x,368,h,11,"bold",anchor="middle")
    for i,(a,b,y) in enumerate([(0,0,1),(0,1,1),(1,0,1),(1,1,0)]):
        yy=405+i*42
        u.rect(850,yy-23,326,33,"#f5faf7" if i%2==0 else "#ffffff",3)
        for x,s in [(877,a),(955,b),(1033,y),(1144,y)]:
            u.text(x,yy,str(s),13,"bold",anchor="middle")
        u.text(1170,yy,"✓",13,"bold",C["green"])
    u.rect(343,618,842,81,"#e7f5ee",6,"#a5d0b9")
    u.text(365,650,"MÓDULO NAND2 CREADO",14,"bold",C["green"])
    u.text(365,679,"Ya puede utilizarse como una unidad en los siguientes montajes.",12)
    u.inspector("NAND2 · módulo","Verificación didáctica",
                ["Produce 0 únicamente si", "A=1 y B=1."],
                [("Vectores","4 de 4"),("Estructura","Conforme al objetivo"),
                 ("Estado","Reutilizable")],"No es validación eléctrica")
    u.text(20,831,"Ejemplo de interfaz: no se han ejecutado todavía pruebas dentro de JavaFX.",
           12,color=C["muted"])
    u.status("Aula-8 · NAND2 terminada","CPU: detenida", "Módulo: disponible")
    return u.save()


def scene13():
    u=UI("IM-13")
    u.shell("Aula-8","Señales por pulso",[],
            [("Placa 3D",132,False),("Esquema 2D",158,False),
             ("Programa",140,False)], "Esquema 2D", "Pausada tras un pulso",
            active_dock="Señales")
    u.panel_title(20,165,"EXPLORAR AULA-8")
    u.line(18,181,251,181)
    u.text(20,210,"CPU de referencia",15,"bold")
    u.badge(20,224,"Solo lectura","#e7f1f9",C["blue"],123)
    for i,t in enumerate(["Resumen", "Registros", "Buses y señales", "Memoria", "Monitor"]):
        yy=300+i*49
        if i==2:
            u.rect(10,yy-25,250,35,C["pale"],4)
            u.rect(10,yy-25,4,35,C["blue"])
        u.text(28,yy,t,13,"bold" if i==2 else "normal")
    u.line(18,575,251,575)
    u.panel_title(20,602,"LEYENDA DE SEÑALES")
    for i,(value,color,label) in enumerate([("1",C["green"],"Alto"),
                                             ("0","#607889","Bajo"),
                                             ("X",C["amber"],"Desconocido")]):
        yy=633+i*35
        u.badge(20,yy-19,value,color,C["white"],31)
        u.text(64,yy,label,12)
    u.canvas()
    u.text(322,229,"CPU  ›  PULSO HIPOTÉTICO 42",13,"bold",C["blue"])
    u.badge(1015,208,"MAQUETA · SIN MOTOR","#fcebd6",C["amber"],198)
    u.text(339,286,"Registro de datos",14,"bold")
    for i,(name,bits) in enumerate([("R0","00101010"),("R1","00000101"),
                                    ("R2","00000000"),("R3","00000000")]):
        yy=309+i*68
        u.rect(338,yy,242,55,"#e9f1f6",5,"#bfd1df")
        u.text(357,yy+22,name,13,"bold",C["blue"])
        u.text(560,yy+35,bits,16,"bold",anchor="end")
    u.rect(627,309,207,122,"#e5f0f7",6,"#9fc1d7",2)
    u.text(730,343,"ALU · 8 BITS",15,"bold",C["blue"],"middle")
    u.text(730,373,"Z=0  C=0",14,anchor="middle")
    u.text(730,401,"N=0  V=0",14,anchor="middle")
    u.rect(881,310,311,121,"#e5f1f8",6,"#b9cfdf")
    u.text(1036,343,"RAM / ROM",15,"bold",C["blue"],"middle")
    u.text(1036,375,"Datos y direcciones",12,anchor="middle")
    u.text(1036,401,"Buses: 8 / 16 bits",12,"bold",anchor="middle")
    u.line(580,355,627,355,C["green"],4)
    u.line(834,365,881,365,"#68829c",4)
    u.text(628,476,"BUS[7:0] · vector de ejemplo",13,"bold",C["blue"])
    for i,v in enumerate("00101010"):
        x=628+i*70
        u.rect(x,492,53,62,"#d0ece0" if v=="1" else "#e1e8ed",4,"#afc3d1")
        u.text(x+27,532,v,21,"bold",C["green"] if v=="1" else "#576f83","middle")
    u.rect(342,593,848,91,"#fff",5,"#c4d6e2")
    u.text(360,624,"PC",12,"bold",C["blue"])
    u.text(399,624,"0x6000",13,"bold")
    u.text(555,624,"SP",12,"bold",C["blue"])
    u.text(595,624,"0x8000",13,"bold")
    u.text(748,624,"X",12,"bold",C["blue"])
    u.text(781,624,"0x6F00",13,"bold")
    u.text(363,661,"Los valores y las rutas son ilustrativos; no implican CPU ejecutada.",11,color=C["muted"])
    u.inspector("R0 · registro de 8 bits","Estado seleccionado",
                ["Muestra el valor retenido", "después de un pulso lógico."],
                [("Binario","00101010"),("Hexadecimal","0x2A"),
                 ("Reloj","Pausado")],"Instantánea hipotética")
    u.text(20,831,"Señales: 1 alto · 0 bajo · X desconocido. El color no es el único indicador.",
           12,color=C["muted"])
    u.status("Aula-8 · Explorar · Pulso 42","Motor: ejemplo visual", "Pausa hipotética")
    return u.save()


def scene14():
    u=UI("IM-14")
    u.shell("Aula-8","Panel de depósito",[],
            [("Placa 3D",132,False),("Esquema 2D",158,False),
             ("Programa",140,False)], "Programa", "Programar desde cero",
            active_dock="Salida")
    side_stage(u,5,kit=None)
    u.canvas()
    u.text(320,229,"PROGRAMA  ›  DEPÓSITO MANUAL",13,"bold",C["blue"])
    u.badge(1033,209,"EJEMPLO DIDÁCTICO","#fff3df",C["amber"],181)
    for x,w,label,active in [(311,201,"Panel manual",True),
                             (520,188,"Monitor ROM",False),
                             (716,208,"Editor de Aula",False),
                             (933,282,"Herramientas externas",False)]:
        u.button(x,253,w,label,active)
    u.rect(320,311,572,300,"#ffffff",6,"#bdd0de")
    u.text(342,345,"CPU DETENIDA · BUS BAJO CONTROL DEL PANEL",13,"bold",C["blue"])
    u.text(342,389,"Dirección · 16 bits",12,"bold")
    u.text(343,419,"0x6000",19,"bold")
    for i,b in enumerate("0110000000000000"):
        x=342+i*31.5
        u.rect(x,445,25,30,"#cce8dd" if b=="1" else "#e4ebf0",3,"#b9cbd7")
        u.text(x+12.5,466,b,13,"bold",anchor="middle")
    u.text(342,511,"Dato · 8 bits",12,"bold")
    u.text(342,539,"0x41",18,"bold")
    for i,b in enumerate("01000001"):
        x=462+i*48
        u.rect(x,513,38,39,"#cce8dd" if b=="1" else "#e4ebf0",3,"#b9cbd7")
        u.text(x+19,539,b,15,"bold",anchor="middle")
    u.text(343,580,"Byte ilustrativo: no se afirma que sea una instrucción válida.",11,color=C["muted"])
    u.rect(911,311,291,300,"#eaf3f8",6,"#bad0df")
    u.text(934,347,"DESPUÉS DEL DEPÓSITO",13,"bold",C["blue"])
    for i,(n,s) in enumerate([("1","Arrancar ROM"),("2","Monitor de comandos"),
                               ("3","Editor/ASM nativos")]):
        y=388+i*65
        u.badge(936,y-20,n,"#d6e9f6",C["blue"],34)
        u.text(981,y,s,12)
    u.rect(322,638,880,73,"#edf2f6",4)
    u.text(342,665,"HERRAMIENTAS EXTERNAS ≠ PROGRAMAS EJECUTADOS POR AULA",12,"bold",C["blue"])
    u.text(342,691,"Un editor Java o compilador cruzado debe identificarse como función del anfitrión.",11)
    u.inspector("Depósito en RAM","Panel de entrada manual",
                ["Escribe un byte en RAM", "con la CPU detenida."],
                [("Dirección","0x6000"),("Dato","0x41"),
                 ("Control del bus","Panel")],"No se ha depositado")
    u.text(20,831,"No cargar en ROM; ejecutar solo después de validar código y propiedad del bus.",
           12,color=C["muted"])
    u.status("Aula-8 · Panel manual","CPU: detenida", "Depósito: pendiente")
    return u.save()


def scene15():
    u=UI("IM-15")
    u.shell("Aula-8","Recorrido completado",[],
            [("Resumen",130,False)],"Resumen", "Final de recorrido",
            no_inspector=True,active_dock=None)
    u.panel_title(20,165,"TU ESPACIO")
    u.line(18,181,251,181)
    u.text(20,211,"Recorridos",15,"bold")
    for yy,name,state,active in [(258,"Aula-8","Completado",True),
                                  (319,"Aula-16","Sin iniciar",False)]:
        if active:
            u.rect(10,yy-30,251,49,C["pale"],4)
            u.rect(10,yy-30,4,49,C["blue"])
        u.text(29,yy-4,name,14,"bold")
        u.text(29,yy+14,state,11,color=C["green"] if active else C["muted"])
    u.line(18,393,251,393)
    u.panel_title(20,422,"GUARDADO")
    u.text(20,456,"El recorrido queda disponible",12,color=C["muted"])
    u.text(20,479,"para explorar y repasar.",12,color=C["muted"])
    u.canvas(width=1287,bottom=740,background="#e9f0f5")
    u.rect(318,221,1211,490,"#ffffff",8,"#c5d8e3")
    u.badge(353,256,"RECORRIDO COMPLETADO","#dff3e9",C["green"],252)
    u.text(355,338,"Has construido Aula-8",27,"bold")
    u.text(356,374,"Puedes explorar sus componentes, revisar señales y seguir aprendiendo con Aula-16.",
           14,color=C["muted"])
    checks=["Puertas y memoria", "Registros y ALU", "Control y CPU",
            "RAM, ROM y E/S", "Programa observable"]
    for i,label in enumerate(checks):
        x=353+(i%3)*366
        y=420+(i//3)*78
        u.rect(x,y,324,60,"#f3faf6",5,"#b7d7c6")
        u.badge(x+12,y+17,"✓","#d2eddf",C["green"],31)
        u.text(x+56,y+38,label,12.5,"bold")
    u.text(355,627,"Cada recorrido guarda su progreso por separado.",12,color=C["muted"])
    u.button(1191,645,258,"Comenzar Aula-16",True)
    u.text(309,828,"Duración objetivo: hasta cinco horas por CPU. Aún requiere validación con estudiantes.",
           13,color=C["muted"])
    u.status("Aula-8 · Completada","Motor: detenido","Guardado: correcto",zoom="—")
    return u.save()


def scene16():
    u=UI("IM-16")
    u.shell("Aula-8","Pantalla gráfica",[],
            [("Placa 3D",132,False),("Esquema 2D",158,False),
             ("Programa",140,False)], "Programa", "Modo gráfico de vídeo",
            active_dock="Salida")
    side_stage(u,5,kit=None)
    u.canvas()
    u.text(320,229,"PROGRAMA  ›  UNA PANTALLA  ›  MODO GRÁFICO",13,"bold",C["blue"])
    u.badge(1014,209,"VÍDEO V1 CONGELADO","#e5f1f7",C["blue"],198)
    u.rect(325,257,284,412,"#ffffff",5,"#c5d7e2")
    u.text(344,290,"PANTALLA VIRTUAL",14,"bold",C["blue"])
    u.text(344,322,"Modo visible",12)
    u.badge(344,337,"Gráficos · 2 bpp","#e2eff8",C["blue"],195)
    for i,(label,value) in enumerate([("Resolución","256 × 128"),
                                      ("Colores","4 índices"),
                                      ("VRAM gráfica","8192 B"),
                                      ("Búfer texto","512 B"),
                                      ("Glifos ROM","2048 B")]):
        yy=412+i*44
        u.text(344,yy,label,12)
        u.text(586,yy,value,12,"bold",C["blue"],"end")
    u.rect(629,257,585,412,"#ffffff",5,"#bfd1dc")
    u.text(650,288,"Monitor integrado · cuatro colores",13,"bold",C["blue"])
    u.rect(648,311,545,332,"#192a31",4)
    # A schematic raster test pattern, not a screenshot of emulated video.
    pal=["#132e40","#3d7392","#80ada5","#e7e5c5"]
    cellw=14
    for row in range(16):
        for col in range(32):
            value=(col//5 + row//4 + ((col-row)//9))%4
            x=672+col*cellw
            y=344+row*17
            u.rect(x,y,cellw,17,pal[value])
    u.text(665,625,"Patrón geométrico ilustrativo · no es VRAM ejecutada",11,color="#cfd9de")
    u.inspector("Vídeo Aula V1","Un solo monitor",
                ["Texto y gráficos son", "modos exclusivos.",
                 "Los búferes se conservan."],
                [("Modo","Gráfico"),("VRAM","Indirecta"),
                 ("CPU","Sin ejecutar")],"Sin GPU ni VGA")
    u.text(20,831,"La pantalla es única: el cambio de modo no borra el otro búfer.",
           13,color=C["muted"])
    u.status("Aula-8 · Vídeo V1","Motor: no implementado","Modo ilustrativo")
    return u.save()


def main():
    # El generador V2 sigue siendo fuente reproducible de las primeras diez.
    v2.main()
    generate_foundation()
    for scene in (scene11,scene12,scene13,scene14,scene15,scene16):
        source=Path(scene())
        name=source.stem[:5]
        v2.enhance_toolbar(source, OUT / f"{name}_AULA_UX_V3.svg", name)
    print("16 escenas SVG V3 generadas en",OUT)


if __name__ == "__main__":
    main()
