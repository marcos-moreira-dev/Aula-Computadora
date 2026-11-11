#!/usr/bin/env python3
"""Auditoría portable de C28-AC; --exhaustivo recorre 393.216 vectores con numpy.

Comprueba conectividad, equivalencia lógica y serialización para la futura app.
No certifica comportamiento eléctrico ni temporización de transistores.
"""

from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'c28_u/netlists/alu8_seis_rutas_359nand.json'
ASSETS = ROOT / 'c28_ac/activos_app'
REPORT = ROOT / 'c28_ac/auditoria/C28_AC_RESULTADOS.json'
MODES = ('ADD', 'SUB', 'AND', 'OR', 'XOR', 'NOT_A')


def oracle(mode, a, b):
    if mode == 0:
        value = (a+b)&255
        c, v = int(a+b>255), int(bool((~(a^b)&(a^value))&128))
    elif mode == 1:
        value = (a-b)&255
        c, v = int(a<b), int(bool(((a^b)&(a^value))&128))
    elif mode == 2: value, c, v = a&b, None, None
    elif mode == 3: value, c, v = a|b, None, None
    elif mode == 4: value, c, v = a^b, None, None
    else: value, c, v = (~a)&255, None, None
    return (value, (value>>7)&1, int(value==0), c, v, int(mode<2))


def prepare():
    src = json.loads(SRC.read_text(encoding='utf-8'))
    app = json.loads((ASSETS/'Aula8_ALU359_APP_NETLIST.json').read_text(encoding='utf-8'))
    assert app['source_netlist_sha256'] == sha256(SRC.read_bytes()).hexdigest()
    assert app['schema']=='aula.circuito.logico.v1'
    assert len(src['gates'])==359 and len(src['inputs'])==22
    assert len(app['nodes'])==22+359+13
    assert len(app['connections'])==718+13
    nodes = {node['id']:node for node in app['nodes']}
    assert len(nodes)==len(app['nodes'])
    pins = set()
    for node in app['nodes']:
        if node['kind']=='input':pins.add(node['id']+'.OUT')
        elif node['kind']=='NAND2':
            pins.update(node['id']+('.A','.B','.Y')[i] for i in range(3))
        else:pins.add(node['id']+'.IN')
    targets = set()
    for edge in app['connections']:
        assert edge['from'] in pins and edge['to'] in pins, edge
        assert edge['to'] not in targets, edge
        targets.add(edge['to'])
    assert len(targets)==731
    expected_edges=set()
    external=set(src['inputs'])
    for gate in src['gates']:
        for port,signal in zip(('A','B'),gate['inputs']):
            origin='IN.'+signal+'.OUT' if signal in external else 'G.'+signal+'.Y'
            expected_edges.add((origin,'G.'+gate['name']+'.'+port,signal))
    for kind,signal_list in src['outputs'].items():
        if not isinstance(signal_list,list):signal_list=[signal_list]
        for i,signal in enumerate(signal_list):
            destination='OUT.'+kind+(str(i) if kind=='S' else '')+'.IN'
            expected_edges.add(('G.'+signal+'.Y',destination,signal))
    actual_edges={(edge['from'],edge['to'],edge['signal']) for edge in app['connections']}
    assert actual_edges==expected_edges,'El JSON de la aplicación no coincide con las conexiones fuente'
    figure_previews=(
        ('ALU359_DIAGRAMA_COMPLETO.svg','ALU359_VISTA_GENERAL.png'),
        ('ALU_BIT0_NAND_DESPLEGADO.svg','ALU_BIT0_VISTA.png'),
        ('CMOS_NAND2_4_MOS.svg','CMOS_NAND2_4_MOS.png'),
        ('AULA8_C28W_BUS_DATAPATH_8_LINEAS.svg','AULA8_C28W_BUS_DATAPATH_8_LINEAS.png'),
        ('AULA16_MEMORIA_DOS_BANCOS_16_LINEAS.svg','AULA16_MEMORIA_DOS_BANCOS_16_LINEAS.png'))
    for name,preview in figure_previews:
        root=ET.parse(ASSETS/name).getroot()
        assert root.tag.endswith('svg')
        assert (ASSETS/preview).is_file()
    html=(ASSETS/'Visor_ALU359_ZOOM.html').read_text(encoding='utf-8')
    assert '<svg' in html and '359 NAND2' in html and 'aula.circuito.logico.v1' in html
    steps=(ASSETS/'Visor_PASO_A_PASO_C28W.html').read_text(encoding='utf-8')
    assert '<svg' in steps and 'CAPTURA_A' in steps and 'LOAD_A' in steps and 'DATA' in steps
    indexes={name:i for i,name in enumerate(src['inputs'])}
    gates=[]
    for gate in src['gates']:
        assert gate['op']=='NAND'
        assert gate['name'] not in indexes
        assert all(x in indexes for x in gate['inputs'])
        gates.append(tuple(indexes[x] for x in gate['inputs']))
        indexes[gate['name']]=len(indexes)
    outs=[indexes[n] for n in src['outputs']['S']]
    flags={n:indexes[src['outputs'][n]] for n in ('N','Z','C_arith','V_arith','CV_valid')}
    return src,app,gates,outs,flags


def verify_portable(gates, outs, flags):
    observed_counts = {}
    for mode, name in enumerate(MODES):
        cases={(a,b) for a in (0,1,7,8,13,127,128,254,255) for b in (0,1,7,8,9,13,127,128,254,255)}
        for x in range(256):cases.add((x, (x*73+mode*37)&255))
        for a,b in sorted(cases):
            values=[0]*(22+359)
            for bit in range(8):
                values[bit]=(a>>bit)&1
                values[8+bit]=(b>>bit)&1
            for bit in range(6):values[16+bit]=int(bit==mode)
            for index,(left,right) in enumerate(gates):
                values[22+index] = 1-(values[left]&values[right])
            s=sum(values[idx]<<i for i,idx in enumerate(outs))
            actual=(s,values[flags['N']],values[flags['Z']],values[flags['C_arith']],values[flags['V_arith']],values[flags['CV_valid']])
            expected=oracle(mode,a,b)
            assert actual[:3]==expected[:3] and actual[5]==expected[5],(name,a,b,actual,expected)
            if expected[5]:assert actual[3:5]==expected[3:5],(name,a,b,actual,expected)
        observed_counts[name]=len(cases)
    return observed_counts


def verify_exhaustive(gates, outs, flags):
    try:import numpy as np
    except ImportError as exc:raise RuntimeError('Para --exhaustivo se requiere numpy; el modo normal es portable') from exc
    a=np.repeat(np.arange(256,dtype=np.uint16),256)
    b=np.tile(np.arange(256,dtype=np.uint16),256)
    count={}
    for mode,name in enumerate(MODES):
        values=[((a>>bit)&1).astype(np.uint8) for bit in range(8)]
        values += [((b>>bit)&1).astype(np.uint8) for bit in range(8)]
        values += [np.full(65536,int(bit==mode),dtype=np.uint8) for bit in range(6)]
        for x,y in gates:values.append(1-(values[x]&values[y]))
        result=np.zeros(65536,dtype=np.uint16)
        for bit,index in enumerate(outs):result |= values[index].astype(np.uint16)<<bit
        if mode==0:
            expected=(a+b)&255
            c=(a+b>255).astype(np.uint8)
            v=((~(a^b)&(a^expected)&128)!=0).astype(np.uint8)
        elif mode==1:
            expected=(a-b)&255
            c=(a<b).astype(np.uint8)
            v=(((a^b)&(a^expected)&128)!=0).astype(np.uint8)
        elif mode==2:expected=a&b
        elif mode==3:expected=a|b
        elif mode==4:expected=a^b
        else:expected=(~a)&255
        assert np.array_equal(result,expected),name
        assert np.array_equal(values[flags['N']],((expected>>7)&1)),name
        assert np.array_equal(values[flags['Z']],(expected==0).astype(np.uint8)),name
        assert np.all(values[flags['CV_valid']]==int(mode<2)),name
        if mode<2:
            assert np.array_equal(values[flags['C_arith']],c),name
            assert np.array_equal(values[flags['V_arith']],v),name
        count[name]=65536
    return count


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--exhaustivo',action='store_true')
    args=parser.parse_args()
    src,app,gates,outs,flags=prepare()
    portable=verify_portable(gates,outs,flags)
    exhaustive=verify_exhaustive(gates,outs,flags) if args.exhaustivo else None
    report={'estado':'APROBADO','tipo':'equivalencia_logica_ideal_y_serializacion_no_electrica',
            'NAND':len(gates),'cobertura_portable_por_modo':portable,
            'cobertura_exhaustiva_por_modo':exhaustive,
            'cobertura_exhaustiva_total':sum(exhaustive.values()) if exhaustive else None,
            'archivos_svg_verificados':5,'visores_html':2,'grafo_conexiones':len(app['connections']),
            'nota':'No valida atrasos, potencia, VDD, cortocircuitos ni geometria de protoboard.'}
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('C28-AC APROBADO: NAND={}, conexiones={}, vectores-portables={}'.format(
        len(gates),len(app['connections']),sum(portable.values())))
    if exhaustive:print('C28-AC EXHAUSTIVO: {} vectores completos'.format(sum(exhaustive.values())))


if __name__=='__main__':main()
