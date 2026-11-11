#!/usr/bin/env python3
"""Genera lámina de mainboard conceptual desde un manifiesto común libro/app.

Las posiciones físicas son de enseñanza, no PCB, Gerber ni encapsulados reales.
El SVG no inventa las interconexiones del control aún sin netlist discreta.
"""
import json
from html import escape
from pathlib import Path
from subprocess import run

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'c28_ad/modelo_compartido_libro_app.json'
OUT=ROOT/'c28_ad/figuras'
OUT.mkdir(parents=True,exist_ok=True)
COLORS=['#80e0fb','#7ed5a7','#e3c35d','#f0a976','#d599df','#84c5dc','#bfdd6f','#f38f9c']


def main():
    model=json.loads(DATA.read_text(encoding='utf-8'))
    board=model['placa_conceptual']
    mods={m['id']:m for m in board['modulos']}
    W,H=1960,1250
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="1960" height="1250" fill="#edf4f7"/>',
       '<style>text{font-family:DejaVu Sans,Arial,sans-serif}.title{font-size:39px;font-weight:750;fill:#143a4a}.sub{font-size:20px;fill:#55717b}.chip{font-size:22px;font-weight:700;fill:#edf8f1}.micro{font-size:16px;fill:#abcac3}.note{font-size:18px;fill:#1d3e50}.mono{font-family:DejaVu Sans Mono,monospace}</style>',
       '<text x="80" y="73" class="title">Aula-8 · placa de montaje virtual, vista superior conceptual</text>',
       '<text x="80" y="114" class="sub">Los mismos módulos y buses del circuito digital; las geometrías se refinan después en JavaFX 3D.</text>']
    def append(x):s.append(x)
    def txt(x,y,t,klass='note',color=None):
        a=f' fill="{color}"' if color else ''
        append(f'<text x="{x}" y="{y}" class="{klass}"{a}>{escape(str(t))}</text>')
    BX,BY=85,182
    append(f'<rect x="{BX+13}" y="{BY+18}" width="{board["ancho"]}" height="{board["alto"]}" rx="30" fill="#16362e" opacity="0.25"/>')
    append(f'<rect x="{BX}" y="{BY}" width="{board["ancho"]}" height="{board["alto"]}" rx="28" fill="#095347" stroke="#073d35" stroke-width="8"/>')
    # Retícula tenue de pistas del sustrato; ornamentación sin significado eléctrico.
    for x in range(145,1790,48):append(f'<path d="M{x},{BY+32} V{BY+board["alto"]-32}" stroke="#237668" stroke-width="0.8" opacity="0.26"/>')
    for y in range(235,990,48):append(f'<path d="M{BX+24},{y} H{BX+board["ancho"]-24}" stroke="#237668" stroke-width="0.8" opacity="0.26"/>')
    for x in (127,1816):
        for y in (218,975):
            append(f'<circle cx="{x}" cy="{y}" r="15" fill="#e2eadb" stroke="#b9bfae" stroke-width="4"/>')
            append(f'<circle cx="{x}" cy="{y}" r="7" fill="#173d3b"/>')
    txt(153,263,'AULA / REV C28-AD','micro','#b5d7c7')
    txt(1405,266,'8 LÍNEAS POR BUS','micro','#b5d7c7')

    # Trazas de datos, una línea de bit por cada ruta especificada en el JSON.
    # Se pintan antes de las siluetas; no representan routing final de PCB.
    for bus in board['buses']:
        pts=bus['puntos']
        assert bus['bits'] in (5,8)
        assert bus['origen'] in mods and bus['destino'] in mods
        for b in range(bus['bits']):
            delta=(b-3.5)*4.8
            coords=' '.join(f'{BX+x:.1f},{BY+y+delta:.1f}' for x,y in pts)
            append(f'<polyline points="{coords}" fill="none" stroke="{COLORS[b]}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round"/>')
        tx,ty=pts[-1]
        append(f'<path d="M{BX+tx-12},{BY+ty-9} L{BX+tx},{BY+ty} L{BX+tx-12},{BY+ty+9}" fill="none" stroke="#eaf9ed" stroke-width="3"/>')
        if bus['id'] in ('NET_A_Q','NET_B_Q','NET_RESULT','NET_FLAGS'):
            first=pts[0]
            bit_label='[7:0]' if bus['bits']==8 else '[4:0]'
            txt(BX+first[0]+4,BY+first[1]-35,bus['id']+' '+bit_label,'micro','#effaed')

    # Huellas ilustrativas de subsistemas; no cuentan como circuitos integrados reales.
    for m in board['modulos']:
        x,y,w,h=BX+m['x'],BY+m['y'],m['w'],m['h']
        append(f'<rect x="{x+5}" y="{y+8}" width="{w}" height="{h}" rx="12" fill="#062d31" opacity="0.6"/>')
        append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#183d42" stroke="#a2d8b8" stroke-width="2.4"/>')
        for ix in range(0,max(3,(w-35)//21)):
            dx=x+22+ix*21
            if dx>x+w-15:break
            for py in (y-12,y+h+2):
                append(f'<rect x="{dx}" y="{py}" width="10" height="12" rx="2" fill="#d7ba79"/>')
        txt(x+20,y+52,m['titulo'],'chip')
        txt(x+20,y+83,m['id'],'micro','#92d8c8')
        state={'panel_didactico':'Entrada de prueba (8 bits)',
               'rtl_sin_footprint':'Comportamiento RTL',
               'netlist_logica_sin_footprint':'359 NAND: interior ampliable'}[m['estado']]
        txt(x+20,y+112,state,'micro','#bcd6d3')
        if m['id']=='ALU359':
            txt(x+22,y+163,'ADD / SUB · AND / OR','micro','#bcecc4')
            txt(x+22,y+199,'XOR / NOT A','micro','#bcecc4')

    append('<rect x="85" y="1062" width="1780" height="142" rx="14" fill="#ffffff" stroke="#b8cdd5" stroke-width="2"/>')
    txt(116,1106,'LO QUE ESTA VISTA SÍ REPRESENTA','note')
    txt(116,1147,'Posiciones, subsistemas, siete tramos de ocho bits y un tramo de cinco banderas.','note')
    txt(116,1181,'No fija encapsulados, pines, alimentación, geometría real de placa ni circuito eléctrico ensamblado.','note')
    append('</svg>')
    svg=OUT/'AULA8_MAINBOARD_CONCEPTUAL_8_BITraces.svg'
    svg.write_text('\n'.join(s)+'\n',encoding='utf-8')
    png=svg.with_suffix('.png')
    run(['inkscape',str(svg),'--export-type=png',f'--export-filename={png}','--export-width=1960'],check=True,capture_output=True)
    print('C28-AD:',svg,png)


if __name__=='__main__':main()
