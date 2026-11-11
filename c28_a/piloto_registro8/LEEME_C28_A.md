# Aula-8: el primer registro que podemos probar

*Piloto C28-A — 8 de noviembre de 2026*

Imagina que ya sabes construir una memoria de un bit. Ahora colocamos ocho de
esas memorias una junto a otra. No basta con dibujar ocho cajitas: necesitamos
decidir qué guarda cada una, cuándo cambia y quién tiene permiso para colocar
sus datos en los cables compartidos de la computadora.

El primer componente concreto de **nuestra Aula-8** será un registro general
de ocho bits, al que llamaremos **R0**. Esta entrega lo prueba como **modelo
lógico**, antes de seleccionar integrados o construir su placa.

## Del cable al byte que permanece

Mira `c28a_registro8_celda.svg` (o su PNG). La entrada `IN_i` puede variar
continuamente. El **MUX 2:1** selecciona entre ese dato nuevo y el viejo
`Q_i` que regresa por el lazo de realimentación. Esta decisión depende de
`LOAD`:

- `LOAD=1`: dejamos preparado el dato nuevo para la próxima captura.
- `LOAD=0`: dejamos preparado el mismo dato que ya teníamos, para conservarlo.

El flip-flop D solo acepta esa propuesta en el **flanco ascendente de CLK**.
Por eso un cambio en `LOAD` no equivale por sí solo a escribir en R0.
Necesitamos la coincidencia con el flanco correspondiente.

Al lado hay un **búfer de tres estados**. Su `OE_n` es activo en bajo: con
`OE_n=0` transmite el bit almacenado a `BUS_i`; con `OE_n=1` ofrece alta
impedancia (`Z`). No almacena el símbolo Z dentro del registro: sencillamente
deja de conducir esa línea.

El segundo dibujo, `c28a_registro8_ocho_carriles.svg`, repite la ruta ocho
veces: desde `IN7` hasta `IN0`, y desde `BUS7` hasta `BUS0`. Los ocho bits
capturan bajo el mismo CLK. Las señales LOAD y OE_n también se comparten.
El dibujo por carriles es una vista desglosada; el circuito de una celda es
el que muestra con detalle el retorno `Q_i` al MUX.

## Nuestra primera prueba concreta

Considera estos sucesos, uno detrás de otro. El valor de R0 es **desconocido
al encender** si no hay circuito o procedimiento previo que lo inicialice.

| Instante | Acción | R0 guardado | Salida al bus |
|---|---|---|---|
| Encendido | `OE_n=1` | Desconocido (`X`) | `Z` |
| 1 | `IN=0x3C`, `LOAD=1`, llega CLK ↑ | `0x3C` | `Z` |
| 2 | `OE_n=0` | `0x3C` | `0x3C` |
| 3 | `IN=0xF0`, `LOAD=0`, llega CLK ↑ | `0x3C` | `0x3C` |
| 4 | `OE_n=1` | `0x3C` | `Z` |
| 5 | `IN=0xA5`, `LOAD=1`, llega CLK ↑ | `0xA5` | `Z` |
| 6 | `OE_n=0` | `0xA5` | `0xA5` |

El paso 3 es especialmente importante. Una línea de entrada puede ofrecer
`0xF0` y **no cambiar lo almacenado**. En el paso 4 desaparece la salida
visible, pero R0 conserva su byte. Estas diferencias son las que permitirán
que R0 conviva con R1, R2 y R3 sin que todos intenten hablar al mismo tiempo.

Para relacionarlo con el futuro taller: el valor guardado se verá en los
flip-flops y la línea del bus mostrará 0/1 o Z. Cuando haya otra fuente,
un controlador tendrá que garantizar que no existan dos conductores activos
en conflicto. Ese arbitraje **no está implementado todavía**.

## Fuente única, figuras y verificadores

`registro8_contrato.json` concentra las decisiones comunes:

- Ocho celdas; por celda MUX 2:1, DFF de flanco ascendente y búfer triestado.
- `LOAD` activo alto y `OE_n` activo bajo.
- Sin reset obligatorio ni valor inicial inventado.

El programa `scripts/c28_generar_piloto_registro8.py` toma ese contrato para
generar las figuras. `scripts/c28_verificar_piloto.py` consulta el mismo
contrato y contrasta un MUX formado por puertas NAND, estados y flancos con
un oráculo independiente. El archivo `registro8.v` modela el comportamiento
equivalente en Verilog, y `tb_registro8.v` contiene pruebas para Icarus
Verilog. El código Verilog **no se ejecutó en el entorno de esta tanda**,
porque allí no estaba instalado Icarus.

Desde la raíz del repositorio:

```powershell
py scripts\c28_verificar_piloto.py
py scripts\c28_generar_piloto_registro8.py
```

En un equipo con Icarus Verilog instalado, situarse en
`c28_a\piloto_registro8` y ejecutar:

```powershell
iverilog -g2012 -o registro8_tb registro8.v tb_registro8.v
vvp registro8_tb
```

## Lo que este piloto sí demuestra y lo que todavía falta

**Demuestra, por software**, conservación, carga por flanco y salida
desconectable de un registro lógico de ocho bits. Las pruebas de Python
obtuvieron 509.268 comparaciones correctas con el oráculo.

**No demuestra** que un circuito físico resista determinada frecuencia,
voltaje o corriente. No hay red de pines comerciales, fuente de alimentación,
desacoplo, tiempo de propagación, revisión ERC, simulación SPICE, ni montaje.
Para la siguiente etapa habrá que transformar esta celda en símbolos y
conexiones de una herramienta EDA y comprobar las restricciones de los
integrados escogidos. Eso puede acabar en un esquema KiCad, pero no debe
confundirse el dibujo lógico de hoy con un plano eléctrico listo para soldar.

La futura aplicación de Aula-8 debe **consumir o reproducir el contrato**;
no inventar una versión alternativa con distintos flancos y señales.
