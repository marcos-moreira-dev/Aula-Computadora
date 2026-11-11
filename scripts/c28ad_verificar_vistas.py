#!/usr/bin/env python3
"""Verifica recursos enlazados y geometrías visuales C28-AD sin simular física."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'c28_ad'
manifest=json.loads((BASE/'modelo_compartido_libro_app.json').read_text(encoding='utf-8'))
assert manifest['schema']=='aula.modelo_vistas.v1'
stages=manifest['etapas']
assert [x['id'] for x in stages]==['E01_NAND2','E02_ALU359','E03_CONTROL_C28W','E04_MEMORIA_AULA16']
for step in stages:
    for key in ('libro','app_digital'):
        value=step[key]
        if value is not None:assert (ROOT/value).is_file(),(step['id'],key,value)

alu=json.loads((ROOT/manifest['fuente_alu_real']).read_text(encoding='utf-8'))
assert len([n for n in alu['nodes'] if n['kind']=='NAND2'])==359
control=(ROOT/manifest['fuente_control_rtl']).read_text(encoding='utf-8')
assert 'assign BUS_DATA = load_b ? B_IN : A_IN;' in control

layout=manifest['placa_conceptual']
mods={m['id']:m for m in layout['modulos']}
assert len(mods)==len(layout['modulos'])==9
buses=layout['buses']
assert len(buses)==8 and len(set(b['id'] for b in buses))==8
assert sum(b['bits'] for b in buses)==61
expected={('ENTRADA_A','MUX8'),('ENTRADA_B','MUX8'),('MUX8','REG_A'),('MUX8','REG_B'),
          ('REG_A','ALU359'),('REG_B','ALU359'),('ALU359','RESULT_Q'),('ALU359','FLAGS')}
assert {(b['origen'],b['destino']) for b in buses}==expected
assert [b.get('senal_logica') for b in buses if b['origen']=='MUX8']==['BUS_DATA','BUS_DATA']
for bus in buses:
    assert bus['bits'] in (5,8)
    assert len(bus['puntos'])>=2
    for x,y in bus['puntos']:
        assert 0<=x<=layout['ancho'] and 0<=y<=layout['alto']

path=BASE/'figuras/AULA8_MAINBOARD_CONCEPTUAL_8_BITraces.svg'
svg=ET.parse(path).getroot()
assert svg.tag.endswith('svg')
tracks=svg.findall('{http://www.w3.org/2000/svg}polyline')
assert len(tracks)==61,(len(tracks),'líneas individuales de datos y banderas')
png=path.with_suffix('.png')
assert png.is_file() and png.stat().st_size>20000
report={'estado':'APROBADO','etapa':'C28-AD','recursos_libro':len(stages),
        'modulos_representados':len(mods),'buses_logicos_escenificados':len(buses),
        'pistas_visualizadas':len(tracks),'topologia_alu_NAND2':359,
        'alcance':'Sin footprints, posiciones físicas reales, netlist eléctrica ni JavaFX compilado.'}
audit=BASE/'auditoria/C28_AD_RESULTADOS.json'
audit.parent.mkdir(parents=True,exist_ok=True)
audit.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('C28-AD APROBADO: 4 etapas, 9 módulos, 8 buses, 61 líneas visuales, ALU 359 NAND2')
