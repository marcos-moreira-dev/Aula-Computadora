# Aula-8 — microsecuenciador y control por acciones lógicas (R0.5)

**Estado: propuesta NO APROBADA.** Este documento continúa la [microarquitectura candidata R0.4](MICROARQUITECTURA_AULA8_BORRADOR.md) y los [36 opcodes candidatos R0.3](ISA_AULA8_CANDIDATA.md). **No contiene microcódigo binario, netlist, cronograma eléctrico ni una CPU ejecutable.**

## 1. ¿Para qué sirve la unidad de control?

Cuando el programa contiene `LDI R0, 42`, la ALU no puede adivinar dónde están los tres bytes de esa instrucción. Alguien debe pedir memoria, registrar cada byte, elegir el registro correcto, habilitar su carga y volver a buscar la instrucción siguiente. Esa es la tarea de la **unidad de control**.

Proponemos una unidad **microprogramada**: la ROM interna de control emite señales y el microsecuenciador decide la siguiente acción. La ROM de control **no es la ROM de firmware de 8 KiB** situada en el espacio de direcciones del programa. La primera organiza los movimientos internos de CPU; la segunda guarda el monitor, rutinas de servicio y vector de arranque.

~~~mermaid
flowchart TB
    ir["IR8: opcode"] --> dispatch["Despacho y condiciones"]
    upc["µPC: microdirección"] --> control["ROM de control"]
    dispatch --> upc
    control --> signals["Señales para datapath y memoria"]
    control --> next["Control de próximo microestado"]
    next --> upc
~~~

Las flechas son **funciones**, no pistas físicas ni una propuesta cerrada de puertas. Un futuro esquema deberá resolver buses, multiplexores, latches, retardo de propagación y propiedad exclusiva de cada señal.

## 2. Registros y recursos indispensables

Se conservan `PC16`, `MAR16`, `MDR8`, `IR8`, `SEL8`, `TMP8`, `R0–R3`, `SP16`, `X16`, `FLAGS` y `ADDR_CARRY` de R0.4. Para explicar `ST` absoluto con seguridad, añadimos **dos latches candidatos `ADDR_LO` y `ADDR_HI` de 8 bits**. No damos por hecho que deban ser chips separados: podrían compartir almacenamiento temporal una vez probados los tiempos de vida.

¿Por qué hace falta mantener ambos bytes? Para leer el byte alto de una dirección, el CPU vuelve a poner `PC` en `MAR` y sobrescribe `MDR`. Si el byte bajo estaba únicamente en `MDR`, se pierde. El modelo debe preservar ambos hasta formar `MAR ← ADDR_HI:ADDR_LO`.

También debemos **preparar el dato en `MDR` antes de activar escritura**. La lectura del byte alto de la dirección dejó en `MDR` un valor diferente del que queremos grabar. Una señal de `WR` sin esta preparación escribiría el byte equivocado.

## 3. Campos de control candidatos, sin inventar sus bits

| Grupo | Acciones representativas | Invariante |
| --- | --- | --- |
| Fuente para bus interno | `PC_LOW`, `PC_HIGH`, `MDR`, `REG`, `TMP`, `ADDR_*` | Un único conductor activo por segmento de bus. |
| Destino de registro | carga de `MAR`, `IR`, `SEL`, `TMP`, `ADDR_LO`, `ADDR_HI`, `R0..R3` | Solo destinos explícitos cambian. |
| Cálculo | `PC_INC`, `ALU_OP`, `ADDR_CARRY` | Aritmética de direcciones no altera flags de datos. |
| Memoria externa | lectura, escritura, reposo | `RD` y `WR` nunca coinciden; ROM sin escritura normal. |
| Estado | `HALTED`, `FAULT`, `RESET` | Detención y fallo no equivalen a volver al monitor. |
| Próxima microdirección | avanzar, salto fijo, despacho por `IR`, condición de flags | Una única transición definida por estado. |

**Pendiente para R1:** valores binarios de selectores, polaridad física, ancho de palabra de control, tamaño de µROM, ubicación de despacho, codificación real de estados, duración de accesos y manejo de memoria lenta. No asignar MHz ni «1 microestado = 1 reloj».

## 4. Una acción lógica no es un ciclo de reloj

El JSON de R0.5 utiliza **macros descriptivas** como `READ_PC_TO_IR`. Su expansión física razonable necesita, como mínimo, estos pasos ordenados:

1. `MAR ← PC` y establecer selección del dispositivo.
2. Activar `RD`; esperar que la memoria cumpla sus tiempos de acceso.
3. Capturar dato válido en `MDR`; desactivar `RD` y liberar control de lectura.
4. Copiar `MDR` al destino (`IR`, `SEL`, `TMP`, `ADDR_LO` o `ADDR_HI`).
5. `PC ← PC + 1` mediante lógica de incremento **candidata**; no cambiar `Z/N/C/V`.

El orden exacto de los pasos 3–5, las posibles superposiciones y el reloj quedan para un diseño eléctrico verificable. La macro **no** garantiza cinco ciclos ni uno solo. El secuenciador podría esperar por una condición de memoria lista si el hardware la incorpora; tampoco se presume que ya exista `READY`.

El fetch común lee exclusivamente el **opcode**, lo carga en `IR` y pasa al despacho. Las lecturas de operandos son responsabilidad de cada instrucción.

## 5. Microsecuencias candidatas del primer programa

El caso de [R0.4](MICROTRAZA_AULA8_BORRADOR.json) comienza en `0x6000`, con estos bytes:

~~~text
6000  11 00 2A       LDI R0, 42
6003  13 00 00 6F    ST [0x6F00], R0
6007  01             HALT
~~~

### 5.1 Fetch compartido y despacho

| Estado lógico | Acción | Resultado |
| --- | --- | --- |
| `FETCH_OPCODE` | `READ_PC_TO_IR` | `IR` captura opcode y `PC` avanza. |
| `DECODE` | Consultar `IR` y ruta de control | Salto a inicio de microsecuencia; opcode ilegal → `FAULT`; opcode legal aún no modelado → ruta **pendiente**, no fallo definitivo. |

Para el primer byte, `IR=0x11` y `PC=0x6001`. Ni el `µPC` ni la dirección en ROM de control son direcciones de RAM del programa.

### 5.2 `LDI R0, 42`

| Estado | Acción | Estado relevante después |
| --- | --- | --- |
| `LDI_SELECTOR` | `READ_PC_TO_SEL` | `SEL=0x00`; `PC=0x6002`. |
| `LDI_CHECK` | Verificar que `SEL` designa un registro válido `R0–R3` | Si no es válido, `FAULT` sin escribir destino. |
| `LDI_IMMEDIATE` | `READ_PC_TO_TMP` | `TMP=0x2A`; `PC=0x6003`. |
| `LDI_COMMIT` | `R[SEL] ← TMP` | `R0=0x2A`; `FLAGS` intactas. |
| `LDI_END` | Retornar a fetch común | Próximo opcode en `0x6003`. |

### 5.3 `ST [0x6F00], R0`

| Estado | Acción | Estado relevante después |
| --- | --- | --- |
| `ST_SELECTOR` | `READ_PC_TO_SEL` | `SEL=0x00`; `PC=0x6005`. |
| `ST_CHECK` | Verificar modo absoluto (`SEL` entre `0x00` y `0x03`) | El modo no admitido por **esta** microsecuencia falla; otros modos de `ST` tienen rutas futuras. |
| `ST_ADDR_LOW` | `READ_PC_TO_ADDR_LOW` | `ADDR_LO=0x00`; `PC=0x6006`. |
| `ST_ADDR_HIGH` | `READ_PC_TO_ADDR_HIGH` | `ADDR_HI=0x6F`; `PC=0x6007`. |
| `ST_BUILD_MAR` | `MAR ← ADDR_HI:ADDR_LO` | Dirección de datos `0x6F00`; **ya no** la del opcode. |
| `ST_STAGE_DATA` | `MDR ← R0` | `MDR=0x2A`; CPU lista para conducir bus de datos. |
| `ST_WRITE` | `WRITE_MDR_AT_MAR` | Una sola escritura de `0x2A` en `0x6F00`; `FLAGS` intactas. |
| `ST_END` | Retornar a fetch común | Próximo opcode en `0x6007`. |

No se «deduce» una escritura solamente porque el LED de una celda se ilumine: la operación implica dirección y dato estables, selección de RAM y un pulso de escritura con exclusión de otros controladores de datos.

### 5.4 `HALT`

| Estado | Acción | Resultado |
| --- | --- | --- |
| `HALT_ENTER` | Desactivar transacciones externas, poner `HALTED=1` | `PC=0x6008`; CPU no busca otro opcode ni retorna por sí misma al monitor. |

El reinicio o la intervención externa necesita una ruta de control distinta; **no** se inventa aquí una reanudación automática.

## 6. Recorrido verificable sin confundirlo con ejecución

La expansión documental produce **8 lecturas externas + 1 escritura = 9 transacciones**:

| Instrucción | Lectura opcode | Lecturas operandos | Escrituras | Total |
| --- | ---: | ---: | ---: | ---: |
| `LDI` | 1 | 2 | 0 | 3 |
| `ST` absoluto | 1 | 3 | 1 | 5 |
| `HALT` | 1 | 0 | 0 | 1 |
| **Total** | **3** | **5** | **1** | **9** |

Este recuento **no equivale a nueve ciclos de reloj**. El archivo [MICROSECUENCIAS_AULA8_BORRADOR.json](MICROSECUENCIAS_AULA8_BORRADOR.json) y su verificador contrastan los pasos *escritos* con [la traza R0.4](MICROTRAZA_AULA8_BORRADOR.json) y la ISA candidata. No modelan electricidad, puertas, tiempo ni ejecución de una CPU.

## 7. Fallos, límites y ruta hacia diseño físico

- **Selector erróneo:** antes de modificar cualquier registro o RAM se verifica que el formato es válido. Para el caso ilustrado se admite `ST` absoluto; los modos X/SP reconocidos por la ISA candidata quedan **sin microsecuencia diseñada**, no prohibidos en la CPU futura.
- **Despacho parcial:** R0.5 solo detalla tres de los 36 opcodes candidatos. `PENDING_ROUTE` indica *instrucción prevista todavía sin descripción*, mientras `FAULT` es la propuesta ante un opcode inexistente. No interpretar ausencia de ruta como fallo de software válido.
- **Contención:** lectura exige conductor de datos externo = memoria, escritura exige conductor = CPU; panel manual debe estar aislado.
- **ROM de control frente a ROM de firmware:** son dominios separados y con presupuestos diferentes; los 8 KiB de firmware no «incluyen» la micro-ROM.
- **Flags preservadas:** `LDI`, `ST`, fetch e incremento de PC no escriben `Z/N/C/V`.
- **Estado inicial:** no se presume que RAM ni FLAGS arranquen a cero; el ejemplo solo fija `R0` antes de escribir.
- **Extensiones pendientes:** `LD`, memoria relativa a X/SP, `CALL/RET`, instrucciones ALU, saltos condicionales y manejo concreto de `FAULT`.
- **Validación por venir:** diseñar el formato real de microinstrucción, netlist, temporización, interfaz de memoria y un intérprete ISA independiente; después comparar trazas ejecutadas y, por separado, instrumentos físicos.

**Resultado R0.5:** ya podemos enseñar cómo la CPU *debería coordinar* sus primeros tres opcodes sin esconder la persistencia de operandos. **No** podemos construir todavía una ROM de control a partir de este documento: su encoding y su diagrama eléctrico permanecen abiertos.
