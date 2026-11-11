#!/usr/bin/env python3
"""C28-AC: netlist real + láminas vectoriales + visor portable para el futuro app.

No simula electricidad analógica; conserva la identidad exacta de cada NAND
del C28-U y su conectividad. Requiere Graphviz `dot` e Inkscape solo al generar
SVG/PNG, no al consumir el JSON de la aplicación.
"""

from collections import Counter, defaultdict
from hashlib import sha256
from html import escape as html_escape
from pathlib import Path
from subprocess import run
import json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "c28_u/netlists/alu8_seis_rutas_359nand.json"
OUT = ROOT / "c28_ac/activos_app"
OUT.mkdir(parents=True, exist_ok=True)


def trace(spec):
    inputs = spec["inputs"]
    gates = spec["gates"]
    depth = {name: 0 for name in inputs}
    consumers = defaultdict(list)
    for g in gates:
        a,b=g["inputs"]
        assert a in depth and b in depth, g
        assert g["name"] not in depth, g
        depth[g["name"]] = 1+max(depth[a],depth[b])
        consumers[a].append((g["name"], "A"))
        consumers[b].append((g["name"], "B"))
    output_names = [*spec["outputs"]["S"], *(spec["outputs"][k] for k in
                     ("N","Z","C_arith","V_arith","CV_valid"))]
    fanout = {k:len(v) for k,v in consumers.items()}
    repeated=Counter()
    for g in gates:
        if g["inputs"][0] == g["inputs"][1]:repeated[g["inputs"][0]]+=1
    stats = {
        "entradas_externas": len(inputs),
        "NAND2": len(gates),
        "patillas_de_entrada_NAND": 2*len(gates),
        "origenes_de_senal": len(inputs)+len(gates),
        "arcos_unicos_senal_a_compuerta": len({(x,g["name"]) for g in gates for x in g["inputs"]}),
        "salidas_visibles": len(output_names),
        "nodos_de_salida_distintos": len(set(output_names)),
        "compuertas_NAND_con_ambas_entradas_unidas": sum(repeated.values()),
        "CMOS_estatico_MOS_por_NAND2": 4,
        "MOS_condicionales_ALU_solo_NAND2": 4*len(gates),
        "profundidad_NAND_maxima": max(depth.values()),
        "profundidad_por_salida": {name:depth[name] for name in set(output_names)},
        "fanout_maximo_conteo_pines": max(fanout.values()),
        "fuentes_con_mas_carga": dict(sorted(fanout.items(),key=lambda x:x[1],reverse=True)[:12]),
        "distribucion_capas_logicas": dict(sorted(Counter(depth[g["name"]] for g in gates).items())),
    }
    return depth, consumers, stats


def category(name):
    if name.startswith("arith_"):return "Aritmética"
    if name.startswith("logic_"):return "Lógica"
    if name.startswith("mux_") or name.startswith("OUT"):return "Selección de ruta"
    if name.startswith("z_"):return "Bandera cero"
    if name.startswith("valid_"):return "Validez C/V"
    return "Entrada"


COLORS={"Aritmética":"#b66a0b","Lógica":"#09827f","Selección de ruta":"#186eae",
        "Bandera cero":"#7639a6","Validez C/V":"#b44a54","Entrada":"#56667b"}


def dot_for(spec, names=None, title="ALU Aula-8 · 359 NAND2"):
    allg={g["name"]:g for g in spec["gates"]}
    if names is None:names=set(allg)
    else:names=set(names)
    deps={x for name in names for x in allg[name]["inputs"] if x not in names}
    emit=[f'digraph Circuito {{', '  graph [rankdir=LR,splines=ortho,ranksep="0.62",nodesep="0.19",pad="0.28",bgcolor="white",fontname="DejaVu Sans",fontcolor="#183149",fontsize=23,label="'+title+'",labelloc=t];',
          '  node [shape=record,style="filled,rounded",fontname="DejaVu Sans Mono",fontsize=10,margin="0.08,0.045",penwidth=1.2];',
          '  edge [color="#8196aa",arrowsize=0.52,penwidth=1.05];']
    for name in sorted(deps):
        emit.append(f'  "{name}" [label="{name}",shape=ellipse,fillcolor="#eef1f5",color="#778698"];')
    for group in ("Aritmética","Lógica","Selección de ruta","Bandera cero","Validez C/V"):
        gs=[g for g in spec["gates"] if g["name"] in names and category(g["name"])==group]
        if not gs:continue
        col=COLORS[group]
        # Evitar subgrupos que distorsionen el orden topológico global.
        emit.append(f'  subgraph "cluster_{group}" {{ label="{group} · {len(gs)} NAND2"; color="{col}"; fontcolor="{col}"; fontsize=13; style="rounded,dashed";')
        for g in gs:
            n=g["name"]
            emit.append(f'    "{n}" [label="{{{{<A>A | <B>B}} | {n} | <Y>Y}}",fillcolor="#ffffff",color="{col}"];')
        emit.append('  }')
    for g in spec["gates"]:
        if g["name"] not in names:continue
        for port,s in zip(("A","B"),g["inputs"]):
            emit.append(f'  "{s}" -> "{g["name"]}":{port} [color="{COLORS[category(g["name"])]}"];')
    for tag,outs in spec["outputs"].items():
        if not isinstance(outs,list):outs=[outs]
        for bit,name in enumerate(outs):
            if name not in names:continue
            sink=f"PIN_{tag}{bit if tag=='S' else ''}"
            emit.append(f'  "{sink}" [label="{tag}{bit if tag=="S" else ""}",shape=ellipse,fillcolor="#d9eefa",color="#186eae"];')
            emit.append(f'  "{name}" -> "{sink}" [color="#186eae",penwidth=2];')
    emit.append('}')
    return "\n".join(emit)


def ancestor_gate_names(spec, target):
    table={g["name"]:g for g in spec["gates"]}
    out=set()
    def walk(n):
        if n not in table or n in out:return
        out.add(n)
        for x in table[n]["inputs"]:walk(x)
    walk(target)
    return out


def export_graph(spec, name, selected=None, title=""):
    dot=OUT/(name+".dot")
    svg=OUT/(name+".svg")
    dot.write_text(dot_for(spec,selected,title),encoding="utf-8")
    run(["dot","-Tsvg",str(dot),"-o",str(svg)],check=True,capture_output=True)
    print("[SVG]",svg.name,svg.stat().st_size)
    return svg


def export_cmos_nand():
    # Esquema original del NAND2 CMOS estático. A/B → PMOS paralelo / NMOS serie.
    # Los círculos son uniones (no resistencias ni fuentes eléctricas simuladas).
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1140" height="1010" viewBox="0 0 1140 1010">',
           '<rect width="1140" height="1010" fill="white"/>',
           '<style>text{font-family:DejaVu Sans,sans-serif;fill:#173149}.title{font-size:32px;font-weight:700}.sub{font-size:20px;fill:#567}.label{font-size:25px;font-weight:700}.tiny{font-size:17px} .wire{stroke:#183d58;stroke-width:4;fill:none}.gate{stroke:#b46925;stroke-width:5;fill:none}</style>',
           '<text x="50" y="65" class="title">NAND2 CMOS estático · cuatro transistores</text>',
           '<text x="50" y="100" class="sub">Una compuerta de las 359 de Aula-8; símbolos eléctricos, no huella física de encapsulado.</text>']
    def line(x1,y1,x2,y2,cls="wire"):
        parts.append(f'<path class="{cls}" d="M{x1},{y1} L{x2},{y2}"/>')
    def text(x,y,s,cl="tiny"):
        parts.append(f'<text x="{x}" y="{y}" class="{cl}">{html_escape(s)}</text>')
    def circle(x,y,r=6):
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#173149"/>')
    text(523,170,"VDD", "label")
    line(570,178,570,220);line(280,220,830,220)
    for x,tag,yn in ((330,"P1 · PMOS",300),(790,"P2 · PMOS",300)):
        line(x,220,x,278)
        line(x,278,x,318)
        line(x,318,x,388)
        # Canal de transistor y puerta separada por aislante.
        line(x-7,280,x-7,339,"gate")
        line(x-35,309,x-13,309,"gate")
        parts.append(f'<circle cx="{x-45}" cy="309" r="9" fill="white" stroke="#b46925" stroke-width="4"/>')
        line(x-54,309,x-125,309)
        text(x-88,289,"A" if x==330 else "B","label")
        text(x-75,371,tag)
        line(x,388,x,423)
    line(330,423,790,423);circle(570,423)
    line(570,423,960,423);text(973,432,"Y = ¬(A · B)","label")
    # Ruta NMOS en serie, desde salida hasta masa.
    line(570,423,570,492)
    for y,tag,g in ((520,"N1 · NMOS","A"),(695,"N2 · NMOS","B")):
        line(570,y-28,570,y+28)
        line(560,y-27,560,y+27,"gate")
        line(470,y,552,y,"gate")
        text(435,y-12,g,"label")
        text(630,y+8,tag)
    line(570,548,570,667)
    line(570,723,570,797)
    line(535,797,605,797);line(546,810,594,810);line(558,823,582,823)
    text(615,817,"GND", "label")
    parts.append('<rect x="60" y="863" width="1020" height="103" rx="14" fill="#e8f1f8" stroke="#b7cad9" stroke-width="2"/>')
    text(86,903,"PMOS en paralelo: Y sube si A=0 o B=0.")
    text(86,935,"NMOS en serie: Y baja solo cuando A=1 y B=1.")
    parts.append('</svg>')
    p=OUT/'CMOS_NAND2_4_MOS.svg'
    p.write_text('\n'.join(parts),encoding='utf-8')
    run(['inkscape',str(p),'--export-type=png',f'--export-filename={OUT/"CMOS_NAND2_4_MOS.png"}','--export-width=1600'],check=True,capture_output=True)
    print('[SVG]',p.name)
    return p


def app_graph(spec, depth, stats):
    nodes=[{"id":"IN."+n,"kind":"input","signal":n,"width":1} for n in spec['inputs']]
    connections=[]
    for index,g in enumerate(spec['gates']):
        id='G.'+g['name']
        nodes.append({'id':id,'kind':'NAND2','gate':g['name'],
                      'category':category(g['name']),'depth':depth[g['name']],
                      'pins':['A','B','Y'],'topological_index':index})
        for port,n in zip(('A','B'),g['inputs']):
            source=('IN.'+n if n in spec['inputs'] else 'G.'+n)
            connections.append({'from':source+('.OUT' if source.startswith('IN.') else '.Y'),
                                'to':id+'.'+port,'signal':n})
    for name,out in spec['outputs'].items():
        if not isinstance(out,list):out=[out]
        for i,s in enumerate(out):
            target=('OUT.'+name+(str(i) if name=='S' else ''))
            nodes.append({'id':target,'kind':'output','signal':name,'bit':i if name=='S' else None})
            connections.append({'from':'G.'+s+'.Y','to':target+'.IN','signal':s})
    return {'schema':'aula.circuito.logico.v1','name':'Aula8_ALU_NAND359',
            'source_netlist_sha256':sha256(SRC.read_bytes()).hexdigest(),
            'logic_levels':'ideal_binary_combinatorial',
            'clocked':False,'selector_policy':'ONE_HOT_EXACTLY_ONE',
            'inputs':spec['inputs'],'outputs':spec['outputs'],
            'nodes':nodes,'connections':connections,
            'calculations':stats,
            'warning':'No incluye transistor sizing, tensiones, atrasos, ruido, corriente ni disipacion; no es protoboard electrico validado.'}


def truth_table(path):
    rows=[]
    for a in (0,1):
        for b in (0,1):rows.append({'A':a,'B':b,'Y':1-(a&b)})
    path.write_text(json.dumps({'componente':'NAND2','tabla':rows},indent=2)+'\n',encoding='utf-8')


def viewer(spec, graph, svg):
    # Archivo HTML autocontenido: ninguna CDN, cuenta o servidor requeridos.
    source=svg.read_text(encoding='utf-8')
    source=source[source.find('<svg'):]
    # Quitar encabezado XML; inline SVG conserva viewBox, grupos y title.
    model=json.dumps(graph,ensure_ascii=False).replace('</','<\\/')
    html='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Aula-8 · Visor de netlist NAND</title>
<style>body{margin:0;background:#eef3f7;color:#142b41;font:14px system-ui,sans-serif}header{display:flex;gap:12px;align-items:center;padding:12px 16px;background:#fff;border-bottom:1px solid #cdd8e0}button,input{font:inherit;padding:8px;border:1px solid #aabac7;border-radius:7px;background:white}button{cursor:pointer}#viewport{height:calc(100vh - 134px);overflow:hidden;cursor:grab;background:white}#viewport.grabbing{cursor:grabbing}#viewport svg{width:100%;height:100%}aside{background:#fff;padding:12px 16px;border-top:1px solid #cbd6df;min-height:35px}g.node.highlight polygon,g.node.highlight path,g.node.highlight ellipse{stroke:#e74d2e!important;stroke-width:4!important} .small{color:#526980}</style>
<header><strong>ALU Aula-8: 359 NAND2</strong><label>Buscar nodo <input id="search" placeholder="arith_C7, mux_m0_0…"></label><button id="find">Buscar</button><button id="plus">Ampliar +</button><button id="minus">Alejar −</button><button id="reset">Restablecer</button><span class="small">Arrastra el plano o usa la rueda. Haz clic sobre una compuerta.</span></header>
<main id="viewport">__SVG__</main><aside id="details">Selecciona un nodo. Señales: 22 entradas, 359 puertas NAND, 8 bits de salida y cinco indicadores.</aside>
<script type="application/json" id="model">__MODEL__</script>
<script>const root=document.querySelector('#viewport svg'),box=document.getElementById('viewport'),model=JSON.parse(document.getElementById('model').textContent),detail=document.getElementById('details');const map=new Map(model.nodes.filter(n=>n.kind==='NAND2').map(n=>[n.gate,n]));let init=root.viewBox.baseVal;let view={x:init.x,y:init.y,w:init.width,h:init.height};function repaint(){root.setAttribute('viewBox',[view.x,view.y,view.w,view.h].join(' '));}function zoom(f,cx=0.5,cy=0.5){let nw=view.w*f,nh=view.h*f;view.x+=(view.w-nw)*cx;view.y+=(view.h-nh)*cy;view.w=nw;view.h=nh;repaint();}document.getElementById('plus').onclick=()=>zoom(0.7);document.getElementById('minus').onclick=()=>zoom(1.42);document.getElementById('reset').onclick=()=>{view={x:init.x,y:init.y,w:init.width,h:init.height};repaint()};box.onwheel=e=>{e.preventDefault();const r=box.getBoundingClientRect();zoom(e.deltaY>0?1.25:.8,(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height)};let start;box.onpointerdown=e=>{start={x:e.clientX,y:e.clientY,vx:view.x,vy:view.y};box.classList.add('grabbing');box.setPointerCapture(e.pointerId)};box.onpointermove=e=>{if(!start)return;view.x=start.vx-(e.clientX-start.x)/box.clientWidth*view.w;view.y=start.vy-(e.clientY-start.y)/box.clientHeight*view.h;repaint()};box.onpointerup=()=>{start=null;box.classList.remove('grabbing')};function highlight(g){root.querySelectorAll('g.node.highlight').forEach(x=>x.classList.remove('highlight'));if(!g)return;g.classList.add('highlight');let n=g.querySelector('title')?.textContent;let data=map.get(n);detail.textContent=data?'Compuerta '+n+' · NAND2 · profundidad '+data.depth+' · '+data.category:'Señal '+n}root.addEventListener('click',e=>{let g=e.target.closest('g.node');highlight(g)});function find(){let q=document.getElementById('search').value.trim().toLowerCase();let g=[...root.querySelectorAll('g.node')].find(n=>n.querySelector('title')?.textContent.toLowerCase()===q);if(!g){detail.textContent='No se encontró el nodo: '+q;return}highlight(g);let p=g.getBBox();view={x:p.x-3*p.width,y:p.y-3*p.height,w:7*p.width,h:7*p.height};repaint()}document.getElementById('find').onclick=find;document.getElementById('search').onkeydown=e=>{if(e.key==='Enter')find()};</script></html>'''
    (OUT/'Visor_ALU359_ZOOM.html').write_text(html.replace('__SVG__',source).replace('__MODEL__',model),encoding='utf-8')


def main():
    spec=json.loads(SRC.read_text(encoding='utf-8'))
    assert len(spec['gates'])==359 and all(g['op']=='NAND' and len(g['inputs'])==2 for g in spec['gates'])
    depth,consumers,stats=trace(spec)
    assert stats['profundidad_NAND_maxima']==38
    graph=app_graph(spec,depth,stats)
    (OUT/'Aula8_ALU359_APP_NETLIST.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'CALCULOS_ALU359.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    truth_table(OUT/'NAND2_tabla_verdad.json')
    export_cmos_nand()
    full=export_graph(spec,'ALU359_DIAGRAMA_COMPLETO',title='Aula-8 · 359 NAND2 · netlist exacta C28-U')
    small=ancestor_gate_names(spec,spec['outputs']['S'][0])
    export_graph(spec,'ALU_BIT0_NAND_DESPLEGADO',small,title=f'Aula-8 · salida S0 · {len(small)} NAND2 relevantes')
    viewer(spec,graph,full)
    print('[CÁLCULOS]',json.dumps({k:stats[k] for k in ('NAND2','patillas_de_entrada_NAND','MOS_condicionales_ALU_solo_NAND2','profundidad_NAND_maxima','fanout_maximo_conteo_pines')},ensure_ascii=False))


if __name__=='__main__':main()
