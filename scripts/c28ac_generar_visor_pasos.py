#!/usr/bin/env python3
"""Pequeño visor didáctico de ciclos C28-W; no pretende resolver electricidad."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'c28_ac/activos_app'
svg=(OUT/'AULA8_C28W_BUS_DATAPATH_8_LINEAS.svg').read_text(encoding='utf-8')
html=r'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Construye Aula-8 · Control de señales y flancos</title>
<style>
:root{font-family:system-ui,Segoe UI,sans-serif;color:#1b3448;background:#eef4f8}*{box-sizing:border-box}
body{margin:0}header{background:#0e304b;color:white;padding:22px clamp(18px,5vw,75px)}h1{font-size:clamp(1.5rem,3vw,2.2rem);margin:0 0 8px}p{line-height:1.55}header p{margin:0;color:#d5e4ef}main{max-width:1550px;margin:auto;padding:24px}section{background:white;border:1px solid #d6e3ed;border-radius:14px;margin-bottom:18px;padding:22px;box-shadow:0 4px 20px #1f4c6610}
.controls{display:flex;flex-wrap:wrap;gap:14px;align-items:end}.controls label{display:grid;gap:5px;font-weight:650}.controls input,.controls select{padding:10px;border-radius:8px;border:1px solid #a7becd;background:#fff;font:inherit;width:155px}
button{background:#176b9e;border:0;border-radius:8px;color:white;padding:11px 15px;font:inherit;font-weight:650;cursor:pointer}button:disabled{opacity:.42;cursor:not-allowed}.reset{background:#985363}.stage{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:7px;margin:16px 0}.stage div{border:1px solid #bdccd7;background:#edf2f6;padding:11px 6px;border-radius:8px;text-align:center;font-size:12px}.stage div.active{background:#145e8a;color:white;outline:3px solid #86c9e9}.stage strong{display:block;margin-bottom:5px;font-size:14px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:12px}.unit{border:1px solid #d5e0e8;border-radius:10px;padding:14px;background:#f6f9fc}.unit h3{margin:0 0 10px;font-size:17px}.bytes{display:flex;gap:4px;flex-wrap:wrap}.bit{display:inline-grid;place-items:center;width:24px;height:28px;border-radius:4px;background:#cbdce9;font:700 15px ui-monospace,SFMono-Regular,monospace}.bit.one{background:#146d9f;color:white}.muted{color:#536b7e;font-size:13px}.status{padding:13px 17px;border-left:4px solid #127aa3;background:#edf6fa;border-radius:5px;margin:12px 0}
.schematic{max-height:730px;overflow:auto;background:#f8fbfd;border-radius:9px}.schematic svg{display:block;width:100%;min-width:850px;height:auto}.flags{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px}.flags div{background:#f4eafa;border:1px solid #dbc2e1;padding:10px;border-radius:7px;text-align:center}.flags b{display:block;font-size:20px}.legend{font-size:13px;color:#586f80}
@media(max-width:700px){.stage{grid-template-columns:repeat(2,1fr)}.flags{grid-template-columns:repeat(3,1fr)}}
</style></head><body>
<header><h1>Aula-8 · mira qué ocurre en cada flanco del reloj</h1><p>Explorador de comportamiento del RTL C28-W con ALU de seis operaciones. Modelo digital ideal, no simulador analógico de protoboard.</p></header>
<main>
<section><h2>1. Elige una operación y mueve el reloj</h2>
<div class="controls">
<label>Operando A (0–255)<input id="a" type="number" min="0" max="255" value="13"></label>
<label>Operando B (0–255)<input id="b" type="number" min="0" max="255" value="9"></label>
<label>Selección (ONE-HOT)<select id="op"><option>ADD</option><option>SUB</option><option>AND</option><option>OR</option><option>XOR</option><option>NOT_A</option></select></label>
<button id="start">START (flanco t₀)</button><button id="clk">CLK: siguiente flanco</button><button class="reset" id="reset">RESET (un flanco)</button>
</div><p class="muted">START inicia en el flanco de reloj. Durante CAPTURA_A, CAPTURA_B y CALCULA, los operandos y la operación quedan bloqueados para cumplir el contrato C28-W.</p>
<div class="stage" id="stages"><div data-phase="IDLE"><strong>0 · IDLE</strong>Listo</div><div data-phase="CAPTURA_A"><strong>1 · CAPTURA_A</strong>Próximo CLK carga A</div><div data-phase="CAPTURA_B"><strong>2 · CAPTURA_B</strong>Próximo CLK carga B</div><div data-phase="CALCULA"><strong>3 · CALCULA</strong>Próximo CLK calcula</div><div data-phase="TERMINO"><strong>4 · TERMINO</strong>DONE y READY</div></div>
<div class="status" id="status">Estado IDLE. Los registros iniciales son desconocidos; no se inventa un valor tras encender.</div>
<div class="stats"><div class="unit"><h3>A_Q · registro A</h3><div id="aq" class="bytes"></div><p id="adec" class="muted"></p></div>
<div class="unit"><h3>B_Q · registro B</h3><div id="bq" class="bytes"></div><p id="bdec" class="muted"></p></div>
<div class="unit"><h3>RESULT_Q · resultado</h3><div id="rq" class="bytes"></div><p id="rdec" class="muted"></p></div>
<div class="unit"><h3>Fase / señales de control</h3><div id="signals" class="muted"></div></div></div>
<h3>Banderas capturadas</h3><div class="flags" id="flags"></div>
</section><section><h2>2. Plano de conexiones de ocho bits</h2><div class="schematic">__SVG__</div>
<p class="legend">Cada conjunto coloreado representa ocho líneas de datos individuales. El bloque ALU utiliza el archivo de red exacta de 359 NAND; su dibujo completo y la versión por bit están en el paquete adjunto.</p></section>
<section><h2>3. Qué se puede y qué no se puede concluir</h2><p>Este visor reproduce las microoperaciones de la etapa C28-W con operaciones aritméticas binarias ideales. No calcula resistencias, cargas capacitivas, niveles de tensión, cortocircuitos, propagación en nanosegundos ni ubicación de patas en un protoboard. Esos fenómenos se incorporarán cuando exista el modelo eléctrico de componentes y el diseño definitivo.</p></section>
</main>
<script>
const $=s=>document.querySelector(s);
const phaseCode={IDLE:0,CAPTURA_A:1,CAPTURA_B:2,CALCULA:3,TERMINO:4};
let phase='IDLE',edge=0,aq=null,bq=null,rq=null,f=null,valid=false,config=null;
const phases={IDLE:'Esperando START.',CAPTURA_A:'Siguiente flanco: BUS_DATA = A_IN, se captura A_Q.',CAPTURA_B:'Siguiente flanco: BUS_DATA = B_IN, se captura B_Q.',CALCULA:'Siguiente flanco: ALU → RESULT_Q y cinco banderas.',TERMINO:'DONE=1, READY=1. Esperando otro START.'};
function bits(id,value){let el=$(id);el.textContent='';for(let i=7;i>=0;i--){let bit=document.createElement('span');let b=value===null?'?':String((value>>i)&1);bit.className='bit'+(b==='1'?' one':'');bit.textContent=b;bit.title='bit '+i;el.append(bit)}}
function show(){
  document.querySelectorAll('[data-phase]').forEach(n=>n.classList.toggle('active',n.dataset.phase===phase));
  let busy=['CAPTURA_A','CAPTURA_B','CALCULA'].includes(phase);
  ['a','b','op'].forEach(id=>$('#'+id).disabled=busy);
  $('#start').disabled=busy;$('#clk').disabled=!busy;
  bits('#aq',aq);bits('#bq',bq);bits('#rq',rq);
  for(const [id,v] of [['adec',aq],['bdec',bq],['rdec',rq]])$('#'+id).textContent=v===null?'Indefinido: sin captura previa':`Decimal ${v} · hexadecimal 0x${v.toString(16).toUpperCase().padStart(2,'0')}`;
  $('#signals').innerHTML=`FASE = ${phaseCode[phase]}<p>LOAD_A = ${Number(phase==='CAPTURA_A')} · LOAD_B = ${Number(phase==='CAPTURA_B')}<p>EXECUTE = ${Number(phase==='CALCULA')}<p>BUSY = ${Number(busy)} · READY = ${Number(!busy)}<p>DONE = ${Number(phase==='TERMINO')} · RESULT_VALID = ${Number(valid)}`;
  let flags=['N','Z','C_arith','V_arith','CV_valid'];
  $('#flags').textContent='';flags.forEach(name=>{let card=document.createElement('div');let value=f===null?'?':String(f[name]);if(f&&['C_arith','V_arith'].includes(name)&&!f.CV_valid)value='no válida';let h=document.createElement('strong');h.textContent=name;let b=document.createElement('b');b.textContent=value;card.append(h,b);$('#flags').append(card)});
  $('#status').textContent=`Flanco ${edge}: ${phase}. ${phases[phase]} ${phase==='TERMINO'?'El dato de salida ya es válido.':''}`;
}
function compute(a,b,op){let s=0,c=0,v=0,cv=Number(['ADD','SUB'].includes(op));if(op==='ADD'){s=(a+b)&255;c=Number(a+b>255);v=Number(Boolean((~(a^b)&(a^s))&128))}else if(op==='SUB'){s=(a-b)&255;c=Number(a<b);v=Number(Boolean(((a^b)&(a^s))&128))}else if(op==='AND')s=a&b;else if(op==='OR')s=a|b;else if(op==='XOR')s=a^b;else s=(~a)&255;return {s,N:(s>>7)&1,Z:Number(s===0),C_arith:c,V_arith:v,CV_valid:cv}}
$('#start').onclick=()=>{if(!['IDLE','TERMINO'].includes(phase))return;let a=Number($('#a').value),b=Number($('#b').value);if(!Number.isInteger(a)||!Number.isInteger(b)||a<0||a>255||b<0||b>255){alert('Los operandos deben ser enteros de 0 a 255');return}config={a,b,op:$('#op').value};edge++;valid=false;phase='CAPTURA_A';show()};
$('#clk').onclick=()=>{if(phase==='CAPTURA_A'){aq=config.a;phase='CAPTURA_B'}else if(phase==='CAPTURA_B'){bq=config.b;phase='CALCULA'}else if(phase==='CALCULA'){let r=compute(aq,bq,config.op);rq=r.s;f=r;valid=true;phase='TERMINO'}else return;edge++;show()};
$('#reset').onclick=()=>{edge++;phase='IDLE';valid=false;show();$('#status').textContent+=' RESET síncrono aplicado a control; se conservaron los registros (sin valores iniciales garantizados).'};
show();
</script></body></html>
'''
(OUT/'Visor_PASO_A_PASO_C28W.html').write_text(html.replace('__SVG__',svg),encoding='utf-8')
print('[VISOR]',(OUT/'Visor_PASO_A_PASO_C28W.html').stat().st_size)
