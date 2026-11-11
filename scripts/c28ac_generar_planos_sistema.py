#!/usr/bin/env python3
"""Láminas originales SVG basadas en C28-W y memoria candidata Aula-16."""
from html import escape
from pathlib import Path
from subprocess import run

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'c28_ac/activos_app'
OUT.mkdir(parents=True,exist_ok=True)
PALETTE=['#147cb4','#078c8c','#428a37','#a27a1b','#b65e26','#9b4b8e','#5e5ca6','#c04352']


class Drawing:
    def __init__(self,w,h):
        self.w=w;self.h=h
        self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'<rect width="{w}" height="{h}" fill="#f8fbfd"/>',
        '<style>text{font-family:DejaVu Sans,sans-serif;fill:#17334b}.title{font-size:38px;font-weight:750}.sub{font-size:20px;fill:#537086}.block{font-size:26px;font-weight:700}.tiny{font-size:18px}.micro{font-size:15px}.wire{fill:none;stroke-linejoin:round;stroke-linecap:round}.mono{font-family:DejaVu Sans Mono,monospace}</style>']
    def rect(self,x,y,w,h,fill='#ffffff',stroke='#bed2e0',rx=16,sw=2):
        self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def txt(self,x,y,s,cl='tiny',col=None,anchor=None):
        attrib=(f' fill="{col}"' if col else '')+(f' text-anchor="{anchor}"' if anchor else '')
        self.s.append(f'<text x="{x}" y="{y}" class="{cl}"{attrib}>{escape(str(s))}</text>')
    def path(self,pts,col='#3f7092',sw=3,dash=None):
        p=' '.join(f'{x},{y}' for x,y in pts)
        a=f' stroke-dasharray="{dash}"' if dash else ''
        self.s.append(f'<polyline points="{p}" class="wire" stroke="{col}" stroke-width="{sw}"{a}/>')
    def dot(self,x,y,col='#255b7b',r=4):
        self.s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')
    def arr(self,x,y,col='#396682'):
        self.s.append(f'<path d="M{x-10},{y-6} L{x},{y} L{x-10},{y+6}" class="wire" stroke="{col}" stroke-width="2.5"/>')
    def bus(self,points,count=8,sep=5):
        for bit in range(count):
            off=(bit-(count-1)/2)*sep
            self.path([(x,y+off) for x,y in points],PALETTE[bit%8],2.1)
        self.arr(*points[-1])
    def save(self,filename,width=1600):
        p=OUT/filename;p.write_text('\n'.join(self.s+['</svg>'])+'\n',encoding='utf-8')
        q=p.with_suffix('.png')
        run(['inkscape',str(p),'--export-type=png','--export-width='+str(width),'--export-filename='+str(q)],check=True,capture_output=True)
        print('[PLANO]',p.name,q.stat().st_size)


def datapath():
    d=Drawing(2000,1260)
    d.txt(80,74,'AULA-8 · circuito de datos controlado, 8 conexiones por bus','title')
    d.txt(80,113,'Equivalente de señales de C28-W; los registros y el mux siguen a nivel RTL, la ALU sí tiene red NAND desplegada.','sub')
    d.rect(75,175,260,150,'#e6f4fa','#8dbad0')
    d.txt(104,218,'A_IN[7:0]','block');d.txt(104,265,'8 señales binarias','tiny')
    d.rect(75,550,260,150,'#e6f4fa','#8dbad0')
    d.txt(104,596,'B_IN[7:0]','block');d.txt(104,642,'8 señales binarias','tiny')
    d.rect(460,355,246,184,'#dcefe9','#7eb7a7')
    d.txt(490,399,'MUX 2 a 1 × 8','block');d.txt(490,435,'selección LOAD_B','tiny')
    d.txt(490,474,'BUS_DATA[7:0]','tiny')
    d.bus([(335,245),(395,245),(395,413),(460,413)])
    d.bus([(335,625),(415,625),(415,481),(460,481)])
    d.bus([(706,445),(765,445),(765,303),(870,303)])
    d.bus([(765,445),(787,445),(787,673),(870,673)])
    d.txt(716,428,'BUS_DATA[7:0]','tiny')
    d.rect(870,229,252,160,'#e8e8fa','#a4a7d8')
    d.txt(902,273,'REGISTRO A','block');d.txt(902,315,'A_Q[7:0] · 8 FF','tiny');d.txt(902,347,'LOAD_A','tiny')
    d.rect(870,600,252,160,'#e8e8fa','#a4a7d8')
    d.txt(902,644,'REGISTRO B','block');d.txt(902,687,'B_Q[7:0] · 8 FF','tiny');d.txt(902,719,'LOAD_B','tiny')
    d.bus([(1122,303),(1205,303),(1205,433),(1310,433)])
    d.bus([(1122,673),(1224,673),(1224,548),(1310,548)])
    d.txt(1145,283,'A_Q[7:0]','tiny');d.txt(1145,704,'B_Q[7:0]','tiny')
    d.rect(1310,332,303,330,'#fff4df','#d3a65b',18,3)
    d.txt(1356,392,'ALU Aula-8','block')
    d.txt(1352,433,'359 puertas NAND2','tiny')
    for i,op in enumerate(('ADD  SUB','AND  OR','XOR  NOT A')):d.txt(1350,473+37*i,op,'tiny')
    d.txt(1350,618,'Red completa → plano NAND','micro')
    d.bus([(1613,488),(1705,488),(1705,475),(1747,475)])
    d.rect(1747,396,215,181,'#e8e8fa','#a4a7d8')
    d.txt(1765,438,'RESULT_Q','block');d.txt(1765,478,'8 flip-flops','tiny')
    d.txt(1765,524,'EXECUTE','tiny')
    d.path([(1564,662),(1564,735),(1765,735)],'#a64b84',3)
    d.arr(1765,735,'#a64b84');d.txt(1505,715,'N Z C V CV_valid · 5 FF','tiny')
    d.rect(1765,749,200,88,'#f6e8f6','#b998bb')
    d.txt(1792,785,'Banderas','block');d.txt(1792,812,'5 bits','tiny')
    d.path([(1471,777),(1471,662)],'#b17324',3)
    d.arr(1471,662,'#b17324');d.txt(1350,809,'SEL[5:0]: ONE-HOT','tiny')
    d.rect(620,855,803,159,'#e9f3fb','#84b1d0')
    d.txt(659,902,'CONTROL C28-W · cinco estados','block')
    d.txt(659,941,'IDLE → CAPTURA_A → CAPTURA_B → CALCULA → TERMINO','tiny')
    d.txt(659,973,'CLK, RESET síncrono solo para control, START. No borra los registros.','micro')
    d.path([(935,855),(935,790),(996,790),(996,760)],'#a54f77',3,dash='10 7')
    d.path([(1111,855),(1111,803),(1195,803),(1195,521),(1310,521)],'#a54f77',3,dash='10 7')
    d.path([(745,855),(745,820),(816,820),(816,349),(870,349)],'#a54f77',3,dash='10 7')
    d.txt(738,817,'LOAD_A','micro')
    d.rect(74,1052,1878,151,'#ffffff','#b7d0e1')
    d.txt(107,1092,'Flancos de reloj del ejemplo · START aceptado con controlador listo','block')
    for i,(head,body) in enumerate([('t₀','START → CAPTURA_A'),('t₁','carga A_Q'),('t₂','carga B_Q'),('t₃','captura resultado → DONE')]):
        x=108+i*448
        d.txt(x,1143,head,'block');d.txt(x+67,1143,body,'tiny')
        if i<3:d.arr(x+390,1135)
    d.save('AULA8_C28W_BUS_DATAPATH_8_LINEAS.svg',width=2000)


def memory():
    d=Drawing(1960,1180)
    d.txt(75,76,'AULA-16 · dos bancos de RAM de 8 bits, palabra de 16 bits','title')
    d.txt(75,115,'Arquitectura candidata: dirección de 16 bits, memoria direccionada por bytes, little-endian y palabra alineada.','sub')
    d.rect(65,215,320,230,'#e6f4fa','#8dbad0')
    d.txt(99,267,'CPU · interfaz','block');d.txt(99,311,'A[15:0] (16 líneas)','tiny')
    d.txt(99,355,'D[15:0] (16 líneas)','tiny');d.txt(99,398,'RD / WR (control)','tiny')
    d.rect(535,188,330,250,'#e6ecfa','#899fc6')
    d.txt(563,237,'Dirección de palabra','block');d.txt(563,281,'A[15:1] · 15 líneas','tiny')
    d.txt(563,326,'A0 selecciona byte','tiny');d.txt(563,367,'A0 = 0 → banco par','tiny')
    d.txt(563,404,'A0 = 1 → banco impar','tiny')
    d.bus([(385,292),(462,292),(462,274),(535,274)],count=15,sep=3)
    d.txt(406,247,'A[15:1] ×15','tiny')
    d.path([(385,413),(450,413),(450,351),(535,351)],'#ce7d32',4)
    d.dot(450,413,'#ce7d32')
    d.rect(1040,188,385,365,'#e7f3e8','#7ab288',18,3)
    d.txt(1075,248,'Banco PAR','block');d.txt(1075,292,'32.768 × 8 bits','tiny')
    d.txt(1075,342,'Direcciones byte: 0, 2, 4…','tiny')
    d.txt(1075,397,'D[7:0] · byte bajo','tiny')
    d.txt(1075,449,'A0 = 0 (selección)','tiny')
    d.rect(1490,188,385,365,'#f2e8f6','#b194c8',18,3)
    d.txt(1525,248,'Banco IMPAR','block');d.txt(1525,292,'32.768 × 8 bits','tiny')
    d.txt(1525,342,'Direcciones byte: 1, 3, 5…','tiny')
    d.txt(1525,397,'D[15:8] · byte alto','tiny')
    d.txt(1525,449,'A0 = 1 (selección)','tiny')
    d.bus([(865,274),(951,274),(951,328),(1040,328)],count=15,sep=3)
    d.bus([(865,274),(989,274),(989,165),(1680,165),(1680,188)],count=15,sep=3)
    d.txt(1180,130,'A[15:1]: mismas 15 líneas hacia ambos bancos','tiny')
    d.path([(865,350),(930,350),(930,484),(1040,484)],'#ce7d32',3)
    d.path([(930,350),(975,350),(975,590),(1700,590),(1700,553)],'#ce7d32',3)
    d.bus([(1040,415),(978,415),(978,685),(470,685),(470,345),(385,345)],count=8)
    d.bus([(1490,415),(1455,415),(1455,741),(437,741),(437,355),(385,355)],count=8)
    d.txt(492,664,'D[7:0] · 8 conexiones','tiny')
    d.txt(492,723,'D[15:8] · 8 conexiones','tiny')
    d.rect(80,838,1800,235,'#ffffff','#aabfd1',14)
    d.txt(112,887,'Ejemplo de memoria little-endian','block')
    d.txt(112,930,'Palabra 0x1234 en dirección par 0x6000:','tiny')
    d.txt(112,974,'RAM[0x6000] = 0x34 (byte bajo) · RAM[0x6001] = 0x12 (byte alto)','tiny')
    d.txt(112,1026,'Espacio: 2¹⁶ direcciones × 1 byte = 65.536 bytes (64 KiB). Palabras alineadas: 32.768.','tiny')
    d.txt(86,1138,'Nota: esquema de organización arquitectónica, no una RAM física construida ni una ISA definitiva.','sub')
    d.save('AULA16_MEMORIA_DOS_BANCOS_16_LINEAS.svg',width=1900)


if __name__=='__main__':
    datapath();memory()
