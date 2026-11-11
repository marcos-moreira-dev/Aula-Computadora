#!/usr/bin/env python3
"""C27: figuras SVG/PNG didácticas reproducibles a partir de datos Aula.

Los dibujos son de lógica y transferencia de datos; no son netlists ni prueban
que una CPU haya ejecutado las instrucciones. El ejemplo ISA es candidato.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "libro" / "figuras"
ISA = ROOT / "simulador-javafx" / "ISA_AULA8_CANDIDATA.json"

INK = "#223442"
BLUE = "#275e72"
AMBER = "#a95d28"
LIGHT = "#e5eff3"
MINT = "#e7f1e6"
GRAY = "#eff0ef"


def el(x, y, value, *, size=21, color=INK, weight="normal", anchor="start", mono=False):
    face = "DejaVu Sans Mono,monospace" if mono else "DejaVu Sans,Arial,sans-serif"
    return (f'<text x="{x}" y="{y}" font-family="{face}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>')


def rect(x, y, w, h, fill=LIGHT, stroke="#8ba8b5", r=9):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')


def line(x1, y1, x2, y2, *, color=BLUE, width=4, arrow=False, dashed=False):
    marker = ' marker-end="url(#arrow)"' if arrow else ""
    dash = ' stroke-dasharray="9 6"' if dashed else ""
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{width}" '
            f'fill="none"{marker}{dash}/>' )


def route(points, *, color=AMBER, width=4, marker=True, dashed=False):
    d = " ".join(("M" if i == 0 else "L") + f"{x} {y}" for i, (x, y) in enumerate(points))
    dash = ' stroke-dasharray="8 6"' if dashed else ""
    end = ' marker-end="url(#arrowAmber)"' if marker else ""
    return f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none"{end}{dash}/>'


def paper(title, subtitle, body, height=560):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}"
      viewBox="0 0 1000 {height}" role="img">
    <defs>
      <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
        <path d="M1 1 L9 5 L1 9" fill="none" stroke="{BLUE}" stroke-width="2.4"/>
      </marker>
      <marker id="arrowAmber" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
        <path d="M1 1 L9 5 L1 9" fill="none" stroke="{AMBER}" stroke-width="2.4"/>
      </marker>
    </defs>
    <rect width="1000" height="{height}" fill="#fbfaf7"/>
    <rect width="1000" height="9" fill="{BLUE}"/>
    {el(38, 61, title, size=31, weight='bold')}
    {el(39, 94, subtitle, size=17, color='#536c7a')}
    {body}
    </svg>'''


def validate_isa():
    source = json.loads(ISA.read_text(encoding="utf-8"))
    assert source["architecture"] == "Aula-8" and source["status"] == "propuesta_no_aprobada"
    assert source["encoding"]["external_data_bus_bits"] == 8
    assert source["encoding"]["address_bits"] == 16
    assert source["encoding"]["immediate_word_byte_order"] == "little_endian"
    op = {row["mnemonic"]: int(row["opcode"], 16) for row in source["instructions"]}
    assert [op[k] for k in ("LDI", "ST", "JMP", "JNZ", "CALL", "RET", "DEC", "HALT")] == [
        0x11, 0x13, 0x30, 0x32, 0x35, 0x02, 0x2A, 0x01]
    original = next(row for row in source["examples"] if row["name"] == "depositar_42")
    loop = next(row for row in source["examples"] if row["name"] == "bucle_de_tres")
    assert original["bytes_hex"] == "11 00 2A 13 00 00 6F 01"
    assert loop["bytes_hex"] == "11 00 03 2A 00 32 03 60 01"
    return op, original, loop


def fig_register():
    s = rect(110, 146, 790, 255, '#f3f6f8')
    s += el(500, 175, "PRIMER REGISTRO GENERAL  R0", size=24, weight="bold", anchor="middle")
    for i in range(8):
        x = 149 + i * 89
        bit = 7 - i
        s += rect(x, 214, 69, 114, MINT)
        s += el(x+34, 240, f"D{bit}", size=17, mono=True, anchor="middle")
        s += el(x+34, 281, "DFF", size=18, weight="bold", anchor="middle")
        s += el(x+34, 312, f"Q{bit}", size=17, mono=True, anchor="middle")
    s += line(168, 355, 833, 355, width=5)
    s += el(500, 389, "CLK de flanco activo; LOAD gobierna la captura (contrato lógico)", size=16, anchor="middle")
    s += el(500, 450, "Bus de entrada D[7:0] → 8 biestables → bus de salida Q[7:0]", size=21, anchor="middle")
    s += el(500, 492, "Sin selección de chip o tiempos físicos asignados todavía.", size=16, color='#647781', anchor="middle")
    return paper("Del flip-flop al primer registro de Aula-8", "Ocho bits almacenados a la vez; no son ocho memorias direccionables.", s)


def fig_nand_pinout():
    """Patillaje PDIP-14 cotejado con TI SCLS062F, top view, página 3."""
    left = [(1,'1A'),(2,'1B'),(3,'1Y'),(4,'2A'),(5,'2B'),(6,'2Y'),(7,'GND')]
    right = [(14,'VCC'),(13,'4B'),(12,'4A'),(11,'4Y'),(10,'3B'),(9,'3A'),(8,'3Y')]
    assert [p for p,_ in left] == list(range(1,8))
    assert [p for p,_ in right] == list(range(14,7,-1))
    s = rect(338,154,324,354,'#e5e9ea','#50636e',r=12)
    s += '<path d="M466 154 Q500 185 534 154" stroke="#50636e" fill="#fbfaf7" stroke-width="3"/>'
    s += el(500,292,'U1',size=32,weight='bold',anchor='middle')
    s += el(500,335,'SN74HCT00N',size=23,mono=True,anchor='middle')
    s += el(500,367,'cuatro NAND',size=18,anchor='middle')
    s += el(500,393,'vista superior',size=18,color='#586e7a',anchor='middle')
    for i, (l,r) in enumerate(zip(left,right)):
        yy = 186+i*47
        ln, la = l; rn, ra = r
        highlight_l = ln <= 6
        s += rect(313,yy-16,32,23,MINT if highlight_l else '#fcfcf8','#768c97',r=3)
        s += rect(657,yy-16,32,23,'#fcfcf8','#768c97',r=3)
        s += el(304,yy+1,f'{ln:>2}  {la}',size=19,mono=True,anchor='end')
        s += el(700,yy+1,f'{rn:>2}  {ra}',size=19,mono=True)
    s += el(500,543,'Para el latch: puentes externos 3 → 5 y 6 → 2.',size=21,anchor='middle',weight='bold')
    s += el(500,578,'14 = +5 V; 7 = GND. Desacoplo de 0,1 µF; entradas libres no flotantes.',
            size=17,anchor='middle')
    s += el(500,607,'Un patillaje permite reconocer pines; NO equivale a un montaje probado.',
            size=16,anchor='middle',color='#647781')
    return paper('Leer las catorce patas de una NAND comercial',
                 'SN74HCT00N · encapsulado PDIP-14 · muesca arriba · vista desde arriba.',s,639)


def fig_bus():
    s = rect(40, 157, 225, 292, '#deecf4') + rect(741, 157, 219, 292, '#e4f2e1')
    s += el(152, 208, 'CPU Aula-8', size=25, weight='bold', anchor='middle')
    s += el(848, 208, 'RAM / ROM', size=24, weight='bold', anchor='middle')
    s += el(152, 260, 'MAR (16 bits)', size=18, anchor='middle')
    s += el(152, 331, 'MDR (8 bits)', size=18, anchor='middle')
    s += el(848, 259, 'A15 … A0', size=18, anchor='middle')
    s += el(848, 331, 'D7 … D0', size=18, anchor='middle')
    s += el(152, 398, 'Control RD/WR', size=17, anchor='middle')
    s += el(848, 398, 'CE / OE / WE', size=17, anchor='middle')
    s += line(268, 242, 733, 242, arrow=True, width=8)
    s += el(502, 230, 'DIRECCIONES 16 bits', size=18, weight='bold', anchor='middle')
    s += line(270, 310, 730, 310, width=8)
    s += line(270, 340, 730, 340, width=8)
    s += line(707, 340, 736, 340, arrow=True, width=3)
    s += line(294, 310, 265, 310, arrow=True, width=3)
    s += el(502, 299, 'DATOS 8 bits, sentido variable', size=17, weight='bold', anchor='middle')
    s += line(267, 388, 733, 388, width=4, arrow=True)
    s += el(502, 376, 'LECTURA O ESCRITURA, nunca a la vez', size=15, anchor='middle')
    s += el(500, 502, 'El diagrama describe un contrato de señales; aún faltan chips, pines y timing.',
            size=16, color='#566b77', anchor='middle')
    return paper('Los dos buses no transportan lo mismo',
                 'El de direcciones indica dónde; el de datos transporta el valor.', s)


def fig_datapath():
    blocks = [(26, 163, 198, 124, LIGHT, 'R0–R3', 'registros de 8 bits'),
              (293, 163, 181, 124, '#f5e9d7', 'ALU8', 'resultado y flags'),
              (550, 163, 172, 124, '#e7f1f4', 'MDR', 'dato de 8 bits'),
              (803, 163, 173, 124, MINT, 'RAM / ROM', 'D7…D0'),
              (26, 384, 244, 109, '#eeeaf5', 'PC / SP / X', 'direcciones 16 bits'),
              (354, 384, 215, 109, '#e7f1f4', 'MAR', 'dirección de 16 bits'),
              (692, 384, 284, 109, GRAY, 'CONTROL', 'habilita y selecciona')]
    s = ''
    for x,y,w,h,fill,name,detail in blocks:
        s += rect(x,y,w,h,fill)
        s += el(x+w/2,y+47,name,size=24,weight='bold',anchor='middle')
        s += el(x+w/2,y+83,detail,size=16,anchor='middle')
    s += line(224,221,286,221,arrow=True)
    s += line(474,221,543,221,arrow=True)
    s += line(722,220,796,220,arrow=True,width=4)
    s += line(799,258,725,258,arrow=True,width=4)
    s += '<path d="M385 287 L385 322 L128 322 L128 293" stroke="'+BLUE+'" stroke-width="3" fill="none" marker-end="url(#arrow)"/>'
    s += el(278, 316, 'resultado interno hacia registro',size=13,anchor='middle')
    s += line(270,436,347,436,arrow=True)
    s += route([(569,428),(629,428),(629,350),(887,350),(887,292)],color=BLUE,width=4)
    s += el(758,343, 'A15…A0 (16 bits)',size=15,anchor='middle')
    s += line(950,380,950,291,arrow=True,width=3)
    s += el(500,528,'La ruta de datos pasa por MDR; la de direcciones pasa por MAR.',
            size=16,color='#566b77',anchor='middle')
    return paper('Aula-8 crece por conexiones verificables',
                 'El registro y la ALU ya aparecen dentro de la ruta CPU–memoria.',s)


def memory_grid(rows, *, header='RAM de programa', x=55, y=138, w=605, row_h=40):
    height = 37 + row_h * len(rows)
    s=rect(x,y,w,height,'#fff','#a7b8c0',r=5)
    s+=rect(x,y,w,37,BLUE,BLUE,r=5)
    s+=el(x+20,y+26,header,size=17,color='#fff',weight='bold')
    for i,(addr,byte,meaning,state) in enumerate(rows):
        cy=y+37+i*row_h
        fill={'executed':'#e7f3e5','skip':'#efefed','fetch':'#e4f0f5','halt':'#fff0d6'}.get(state,'#fff')
        s+=rect(x+2,cy,w-4,row_h,fill,fill,r=0)
        s+=f'<path d="M{x} {cy+row_h} H{x+w}" stroke="#cdd7da" stroke-width="1"/>'
        s+=el(x+22,cy+row_h*.7,f'0x{addr:04X}',size=18,mono=True,
              color='#7f8b90' if state=='skip' else INK)
        s+=el(x+190,cy+row_h*.7,f'{byte:02X}',size=19,mono=True,weight='bold',
              color='#7f8b90' if state=='skip' else INK)
        s+=el(x+285,cy+row_h*.7,meaning,size=17,
              color='#7f8b90' if state=='skip' else INK)
    return s, y+37+row_h*len(rows)


def fig_program(original):
    raw=[int(v,16) for v in original['bytes_hex'].split()]
    assert len(raw)==8 and original['origin']==0x6000
    labels=['LDI: opcode','Registro R0','Inmediato 42','ST: opcode','Modo absoluto/R0',
            'Destino bajo','Destino alto','HALT']
    states=['fetch']*3+['executed']*4+['halt']
    s,end=memory_grid([(0x6000+i,byte,labels[i],states[i]) for i,byte in enumerate(raw)],w=652)
    s+=rect(756,252,200,127,MINT)
    s+=el(856,284,'Dato en RAM',size=19,weight='bold',anchor='middle')
    s+=el(856,324,'0x6F00',size=21,mono=True,anchor='middle')
    s+=el(856,358,'0x2A',size=25,mono=True,weight='bold',anchor='middle')
    s+=route([(711,295),(732,295),(732,314),(752,314)])
    s+=el(502,515,'Los ocho bytes del programa están en posiciones consecutivas.',size=17,anchor='middle')
    s+=el(502,543,'La CPU primero lee instrucciones; ST escribe el dato 0x2A en otra dirección.',
          size=15,color='#576d79',anchor='middle')
    return paper('El programa ocupa una franja real de RAM',
                 'La memoria no entiende «LDI» o «ST»: contiene bytes contiguos.',s,580)


def fig_jump(op):
    program=[op['JMP'],0x06,0x60,op['LDI'],0,1,op['LDI'],0,0x2A,op['HALT']]
    labels=['JMP: opcode','Destino bajo','Destino alto','LDI omitido','Registro R0','Constante 1',
            'LDI ejecutado','Registro R0','Constante 42','HALT']
    s,end=memory_grid([(0x6000+i,byte,labels[i],
                        'skip' if 3<=i<=5 else ('halt' if i==9 else 'executed'))
                        for i,byte in enumerate(program)],y=127,w=660,row_h=38)
    y1=127+37+2*38+19
    y2=127+37+6*38+19
    s+=route([(721,y1),(763,y1),(763,y2),(721,y2)])
    s+=el(791,274,'PC toma',size=18,weight='bold')
    s+=el(791,303,'0x6006',size=23,mono=True,weight='bold')
    s+=el(791,369,'Los bytes',size=17)
    s+=el(791,394,'6003–6005',size=18,mono=True)
    s+=el(791,419,'no se ejecutan.',size=16)
    s+=el(503,558,'Flecha naranja: cambio del PC. No representa un cable de la computadora.',
          size=15,color='#576d79',anchor='middle')
    return paper('JMP cambia la próxima lectura, no la RAM',
                 'Un salto absoluto se codifica con opcode y dos bytes little-endian.',s,588)


def fig_loop(loop):
    raw=[int(v,16) for v in loop['bytes_hex'].split()]
    labels=['LDI R0','Registro R0','Constante 3','DEC','Registro R0','JNZ','Destino bajo','Destino alto','HALT']
    s,end=memory_grid([(0x6000+i,b,labels[i],'halt' if i==8 else 'executed')
                       for i,b in enumerate(raw)],y=137,w=643,row_h=40)
    s+=route([(701,137+37+7*40+20),(740,137+37+7*40+20),
              (740,137+37+3*40+20),(701,137+37+3*40+20)])
    s+=el(776,298,'JNZ → 0x6003',size=19,weight='bold')
    s+=el(776,333,'R0 = 2: vuelve',size=16)
    s+=el(776,363,'R0 = 1: vuelve',size=16)
    s+=el(776,393,'R0 = 0: continúa',size=16)
    s+=el(500,562,'Las tres lecturas del salto ocurren también cuando Z=1 y no se toma.',
          size=16,color='#576d79',anchor='middle')
    return paper('Un bucle recorre los mismos bytes varias veces',
                 'El contenido de RAM permanece quieto; el PC decide volver a 6003.',s,589)


def fig_call(op):
    assert op['CALL']==0x35 and op['RET']==0x02
    s=''
    for x,title,rows in [
       (33,'Programa llamador',[(0x6000,0x35,'CALL'),(0x6001,0x10,'Destino bajo'),
                                  (0x6002,0x60,'Destino alto'),(0x6003,0x01,'HALT')]),
       (381,'Subrutina',[(0x6010,0x11,'LDI'),(0x6011,0x00,'R0'),
                          (0x6012,0x2A,'42'),(0x6013,0x02,'RET')])]:
        s+=rect(x,151,315,244,'#fff')
        s+=rect(x,151,315,39,BLUE,BLUE)
        s+=el(x+13,177,title,size=17,weight='bold',color='#fff')
        for i,(addr,byte,lab) in enumerate(rows):
            yy=193+i*49
            s+=rect(x+2,yy,311,49, MINT if i in (0,3) else '#f1f4f4',r=0)
            s+=el(x+11,yy+31,f'{addr:04X}',size=17,mono=True)
            s+=el(x+103,yy+31,f'{byte:02X}',size=17,mono=True,weight='bold')
            s+=el(x+164,yy+31,lab,size=16)
    s+=rect(730,151,232,244,'#fff')
    s+=rect(730,151,232,39,BLUE,BLUE)
    s+=el(743,177,'Pila RAM',size=19,color='#fff',weight='bold')
    s+=el(746,239,'7FFE  03',size=22,mono=True)
    s+=el(746,288,'7FFF  60',size=22,mono=True)
    s+=el(746,342,'SP=7FFE',size=18,mono=True)
    s+=route([(348,216),(368,216)])
    s+=route([(696,351),(710,351),(710,419),(210,419),(210,396)])
    s+=line(697,315,725,315,arrow=True,color=BLUE,width=3)
    s+=el(506,450,'CALL guarda retorno 0x6003; RET lo recupera en little-endian.',
          size=17,anchor='middle',weight='bold')
    s+=el(506,483,'Después de RET: PC=0x6003 y SP vuelve a 0x8000.',
          size=17,anchor='middle')
    s+=el(506,533,'Cada tabla es un tramo contiguo; 6004–600F quedan fuera de esta vista.',
          size=15,anchor='middle',color='#576d79')
    return paper('CALL y RET enlazan programa, rutina y pila',
                 'Dos tramos de código y dos posiciones consecutivas de la pila.',s,565)


def fig_banks():
    s=rect(44,160,266,287,LIGHT)+rect(384,160,262,287,MINT)+rect(711,160,248,287,'#f5ebdc')
    s+=el(177,209,'CPU Aula-16',size=23,weight='bold',anchor='middle')
    s+=el(177,267,'D15 … D0',size=22,mono=True,anchor='middle')
    s+=el(177,313,'A15 … A0',size=19,mono=True,anchor='middle')
    s+=el(177,367,'BE / dirección',size=16,anchor='middle')
    s+=el(516,207,'Banco bajo',size=22,weight='bold',anchor='middle')
    s+=el(516,262,'D7 … D0',size=21,mono=True,anchor='middle')
    s+=el(516,316,'0x2000 → 34',size=18,mono=True,anchor='middle')
    s+=el(835,207,'Banco alto',size=22,weight='bold',anchor='middle')
    s+=el(835,262,'D15 … D8',size=21,mono=True,anchor='middle')
    s+=el(835,316,'0x2001 → 12',size=18,mono=True,anchor='middle')
    # Es una LECTURA: cada banco entrega su carril a la CPU. No se conectan
    # los bancos en cascada ni se invierte el sentido de las flechas.
    s+=line(381,273,317,273,arrow=True,width=7)
    s+='<path d="M709 224 L671 224 L671 133 L331 133 L331 386 L316 386" stroke="'+BLUE+'" stroke-width="5" fill="none" marker-end="url(#arrow)"/>'
    s+=el(500,475,'Lectura de palabra 0x1234 desde dirección par 0x2000: ambos bancos.',
          size=16,weight='bold',anchor='middle')
    s+=el(500,511,'Un byte impar utiliza carril alto; una palabra impar se rechaza en V1.',
          size=16,anchor='middle')
    return paper('Aula-16 necesita dos carriles de ocho bits',
                 'La dirección nombra bytes; el bus externo completo transporta 16 bits.',s)


def output_figures():
    op, original, loop=validate_isa()
    mapping={
      'c05_fig05_sn74hct00_patillaje':fig_nand_pinout(),
      'c07_fig05_registro_aula8':fig_register(),
      'c08_fig05_buses_aula8':fig_bus(),
      'c12_fig05_ruta_acumulada_aula8':fig_datapath(),
      'c14_fig05_ram_contigua_deposito':fig_program(original),
      'c14_fig06_ram_salto':fig_jump(op),
      'c16_fig05_ram_y_pila_call_ret':fig_call(op),
      'c16_fig06_ram_bucle_jnz':fig_loop(loop),
      'c22_fig05_dos_bancos_aula16':fig_banks(),
    }
    inkscape=shutil.which('inkscape') or shutil.which('inkscape.com')
    if not inkscape:
        raise RuntimeError('Inkscape es necesario para exportar SVG a PNG')
    FIG.mkdir(parents=True,exist_ok=True)
    for name,svg in mapping.items():
        path=FIG/(name+'.svg')
        ET.fromstring(svg)
        path.write_text(svg,encoding='utf-8')
        png = FIG / (name+'.png')
        for attempt in range(2):
            subprocess.run([inkscape,str(path),'--export-filename='+str(png),
                            '--export-width=1800'],check=True,capture_output=True)
            try:
                with Image.open(png) as im:
                    im.verify()
                break
            except (OSError, ValueError):
                if attempt:
                    raise RuntimeError(f'Exportación PNG incompleta: {name}')
        assert png.stat().st_size>30_000,name
    print(f'REGENERACIÓN C27: {len(mapping)} SVG/PNG válidos desde contratos candidatos.')
    return mapping


if __name__=='__main__':
    output_figures()
