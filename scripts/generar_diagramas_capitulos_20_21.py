#!/usr/bin/env python3
"""Genera diagramas funcionales originales de C20 y C21 (SVG/PNG).

No son netlists ni esquemas físicos; valida constantes con los contratos
y el programa del ensamblador anfitrión antes de dibujar.
Uso: python3 scripts/generar_diagramas_capitulos_20_21.py
"""

from pathlib import Path
import json
import subprocess
import xml.etree.ElementTree as ET

from ensamblador_dos_pasadas_aula8_educativo import assemble
from generar_diagramas_tecnicos_aula8 import arrow, box, lane, page, resolver_inkscape, t
from generar_figuras_capitulo_01 import ROOT

OUT = ROOT / 'libro/figuras'


def contract():
    state=json.loads((ROOT/'ESTADO_PORTABLE.json').read_text(encoding='utf-8'))
    isa=json.loads((ROOT/'simulador-javafx/ISA_AULA8_CANDIDATA.json').read_text(encoding='utf-8'))
    aula8=state['architecture']['aula8']
    aula16=state['architecture']['aula16']
    assert aula8['general_registers']==aula16['general_registers']==4
    assert aula8['register_bits']==8 and aula8['external_data_bus_bits']==8
    assert aula16['register_bits']==16 and aula16['external_data_bus_bits']==16
    assert state['architecture']['address_bus_bits']==16
    assert state['architecture']['addressable_bytes']==65536
    assert state['aula8_isa_candidate']['status']=='propuesta_no_aprobada'
    assert not state['aula8_isa_candidate']['cpu_execution_verified']
    program=assemble((ROOT/'libro/programas/c20_euclides_aula8.asm').read_text(encoding='utf-8'))
    assert len(program.data)==29
    assert program.symbols=={'BUCLE':0x6006,'RESTAR_A':0x6013,'FIN':0x6018}
    assert program.data.hex(' ').upper().startswith('11 00 30 11 01 12 24 01 31 18 60')
    assert 'opcodes' in isa or 'instructions' in isa or isinstance(isa, dict)
    return program


def create():
    program=contract()
    figures={}
    a=''
    steps=[('EDITOR','líneas de texto','#e7f1fb'),('ENSAMBLADOR','dos pasadas en PC','#f9eedc'),
           ('CARGA','RAM; aún futura','#e9f4e6'),('EJECUCIÓN','CPU Aula-8 pendiente','#fce8e8')]
    for i,(name,desc,color) in enumerate(steps):
        x=24+i*246
        a+=lane(x,158,216,169,color,name,desc)
        if i<3:a+=arrow(x+216,240,x+246,240)
    a+=t(500,384,'Fuente de texto ≠ bytes ensamblados ≠ programa ejecutándose.', 'small','middle')
    a+=t(500,426,'ROM y soporte persistente son contratos; no hay firmware funcionando.', 'tiny','middle')
    figures['c20_fig01_herramientas_y_capas']=page('De texto a una aplicación sobre Aula-8',
        'Secuencia de herramientas propuestas; solo el ensamblador anfitrión funciona.',a)

    a=lane(30,142,405,250,'#e7f1fb','PASADA 1','medir instrucciones')
    for idx,(label,addr) in enumerate(program.symbols.items()):
        a+=t(232,272+idx*39,f'{label} = {addr:04X}','small','middle')
    a+=lane(565,142,405,250,'#e9f4e6','PASADA 2','resolver etiquetas')
    a+=t(766,269,'JZ FIN  →  31 18 60','label','middle')
    a+=t(766,312,'destino 6018 (bajo 18, alto 60)','small','middle')
    a+=arrow(435,264,565,264)
    a+=t(500,430,'Los tamaños de instrucción determinan las direcciones.', 'small','middle')
    figures['c20_fig02_dos_pasadas_y_etiquetas']=page('Por qué hacen falta dos pasadas',
        'Una referencia adelantada se convierte en dos bytes de destino.',a)

    pairs=[('48','18'),('30','18'),('12','18'),('12','6'),('6','6')]
    a=''
    for i,(v0,v1) in enumerate(pairs):
        x=18+i*196
        a+=lane(x,167,176,169,'#e9f4e6' if i==4 else '#e7f1fb',f'PASO {i}',f'R0={v0}, R1={v1}')
        if i<4:a+=arrow(x+176,252,x+196,252)
    a+=t(500,393,'CMP decide la rama; SUB reduce el mayor de los dos enteros.', 'small','middle')
    a+=t(500,437,'FIN: RAM[6F00] = 06  |  Precondición: ambos enteros positivos.', 'small','middle')
    figures['c20_fig03_euclides_estados']=page('Euclides por restas, desde 48 y 18 hasta 6',
        'La secuencia se verifica con aritmética; la CPU no la ha ejecutado.',a)

    panels=[('ROM','E000-FFFF','Monitor propuesto','#e7f1fb'),
            ('HERRAMIENTAS','1000-2FFF','Editor/ASM futuros','#f9eedc'),
            ('PRÁCTICA','6000-6EFF','Programas de usuario','#e9f4e6'),
            ('DATOS','6F00','Variable ejemplo','#e7f1fb')]
    a=''
    for i,(name,addr,detail,color) in enumerate(panels):
        x=24+i*246
        a+=lane(x,150,216,189,color,name,addr)
        a+=t(x+108,309,detail,'tiny','middle')
    a+=t(500,398,'Soporte por bloques: requiere LOAD/LOADX para copiar a RAM.', 'small','middle')
    a+=t(500,436,'Mapa y capacidades candidatos; no existe sistema operativo ejecutable.', 'tiny','middle')
    figures['c20_fig04_mini_sistema_y_pruebas']=page('Una microcomputadora con zonas y responsabilidades',
        'Cuatro regiones funcionales, no tamaños de binarios medidos.',a)

    a=lane(38,160,418,221,'#e7f1fb','AULA-8','R0 = 8 bits  |  ALU = 8 bits')
    a+=lane(544,160,418,221,'#e9f4e6','AULA-16','R0 = 16 bits  |  ALU = 16 bits')
    a+=t(245,331,'Bus externo: 8 bits','small','middle')
    a+=t(756,331,'Bus externo: 16 bits','small','middle')
    a+=t(500,425,'LAS DOS: 16 bits de dirección → 65536 direcciones de bytes.', 'label','middle')
    figures['c21_fig01_palabra_y_direcciones']=page('El dato se ensancha; el espacio direccionable no',
        'No confundir ancho de bus de datos y ancho de direcciones.',a)

    a=lane(30,168,390,184,'#e7f1fb','SUMADOR BAJO','bits 0..7')
    a+=lane(582,168,390,184,'#e9f4e6','SUMADOR ALTO','bits 8..15')
    a+=arrow(420,247,582,247)
    a+=t(500,220,'C8','label','middle')
    a+=t(800,396,'acarreo final C16','small','middle')
    a+=arrow(775,352,775,376)
    a+=t(500,453,'16 posiciones funcionales; retrasos de propagación aún no medidos.', 'tiny','middle')
    figures['c21_fig02_acarreo_16_bits']=page('Dos grupos de ocho bits forman una suma de 16',
        'El acarreo intermedio pasa de la posición 7 a la posición 8.',a)

    a=lane(24,154,443,208,'#f9eedc','AULA-8','FF+01 → 00 y C=1')
    a+=t(245,322,'01+00+C → 02','label','middle')
    a+=lane(533,154,443,208,'#e9f4e6','AULA-16','01FF + 0001')
    a+=t(755,322,'resultado 0200','label','middle')
    a+=t(500,415,'Dos operaciones de byte frente a una operación de palabra.', 'small','middle')
    a+=t(500,455,'No es una estimación de ciclos, frecuencia o rendimiento real.', 'tiny','middle')
    figures['c21_fig03_suma_dos_anchos']=page('Una misma suma, dos anchos naturales',
        'La comparación es de operaciones aritméticas, no de tiempo de ejecución.',a)

    a=lane(305,127,390,116,'#e7f1fb','REGISTRO DE 16 BITS','1234 hexadecimal')
    a+=lane(85,324,353,112,'#e9f4e6','DIRECCIÓN 2000','byte bajo 34')
    a+=lane(562,324,353,112,'#f9eedc','DIRECCIÓN 2001','byte alto 12')
    a+=arrow(398,243,270,324)
    a+=arrow(604,243,739,324)
    a+=t(500,474,'Little-endian: dos direcciones de BYTE, una palabra alineada.', 'tiny','middle')
    figures['c21_fig04_registro_a_ram']=page('Guardar 1234 sobre RAM direccionada por bytes',
        'El orden little-endian separa el byte bajo del alto.',a)

    OUT.mkdir(parents=True,exist_ok=True)
    inkscape=resolver_inkscape()
    for name,svg in figures.items():
        source=OUT/(name+'.svg')
        png=OUT/(name+'.png')
        ET.fromstring(svg)
        source.write_text(svg,encoding='utf-8')
        subprocess.run([inkscape,str(source),'--export-type=png',f'--export-filename={png}',
                        '--export-width=2000'],check=True,capture_output=True,text=True)
        assert png.is_file() and png.stat().st_size>10000
        print(name,source.stat().st_size,png.stat().st_size)


if __name__=='__main__':
    create()
