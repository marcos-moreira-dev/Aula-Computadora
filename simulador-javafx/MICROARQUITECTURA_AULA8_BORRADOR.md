# Aula-8 — propuesta de datapath y microoperaciones

**Estado R0.4: diseño conceptual para revisión, NO microcódigo, esquema físico ni CPU implementada.** Esta propuesta se deriva de [la ISA Aula-8 candidata R0.3](ISA_AULA8_CANDIDATA.md), que continúa **sin aprobarse**. Si cambia su encoding, se revisa también este documento.

## 1. Qué debemos lograr con circuitos reales

La CPU recibe instrucciones desde RAM o ROM, mueve bytes entre registros, calcula, lee/escribe memoria y modifica PC. No bastaría con dibujar un bloque «procesador» que haga esas cosas mágicamente: cada movimiento necesita registros, conexiones, control y un estado temporal comprensible.

### Exterior de la CPU

| Conexión | Ancho | Función inicial |
| --- | ---: | --- |
| `A0..A15` | 16 bits | Dirección de RAM, ROM o registro de E/S |
| `D0..D7` | 8 bits bidireccionales | Byte leído o escrito |
| `RD`, `WR` | 1 señal cada una | Solicitar lectura o escritura; nunca simultáneas |
| `CLK` | 1 | Sincronización de la lógica secuencial |
| `RESET` | 1 | Entrada al protocolo de arranque |
| `HALTED`, `FAULT` | Estado lógico propuesto | Indicar detención normal o fallo de instrucción |

La polaridad final de `RD`, `WR` y su traducción a pines concretos (`OE`, `WE`, `CS`) se decidirá con los componentes y sus hojas de datos. Aquí se describen **acciones lógicas** y no se establecen tensiones o temporizaciones eléctricas.

### Interior mínimo propuesto

| Módulo / registro | Ancho | Motivo de su presencia |
| --- | ---: | --- |
| `R0–R3` | 4 × 8 bits | Datos ordinarios del programa |
| `PC` | 16 bits | Dirección del próximo byte de instrucción |
| `SP` | 16 bits | Pila descendente y marcos de llamada |
| `X` | 16 bits | Direcciones indexadas y arreglos |
| `MAR` | 16 bits | Mantener estable la dirección sobre el bus externo |
| `MDR` | 8 bits | Capturar o preparar byte transferido a memoria |
| `IR` | 8 bits | Opcode actual |
| `SEL` | 8 bits | Registro, modo de direccionamiento o selector de operandos |
| `TMP` | 8 bits o latches reutilizables | Inmediatos, desplazamientos y datos temporales |
| `ALU` | 8 bits | Suma, resta, comparación y funciones lógicas |
| `FLAGS` | 4 bits (`Z/N/C/V`) | Estado visible de resultados de operaciones sobre datos |
| `ADDR_CARRY` | 1 bit interno | Acarreo temporal para actualizar direcciones de 16 bits **sin alterar C visible** |
| `µPC` y ROM de control | Por dimensionar | Elegir microoperación y próximo microestado |

Los registros temporales pueden compartirse en diseños posteriores, siempre que **una operación nunca sobrescriba un valor que aún necesita**. Esta es una propuesta estructural, no el recuento definitivo de biestables o transistores.

### Diagrama funcional de bloques (no esquema eléctrico)

~~~mermaid
flowchart TB
    urom["ROM de microcontrol"] --> ctl["Unidad de control"]
    ctl --> bus["Bus interno de 8 bits"]
    ctl --> mar["MAR16 y MDR8"]
    regs["R0–R3 de 8 bits"] <--> bus
    alu["ALU8 y flags"] <--> bus
    wider["PC, SP y X de 16 bits"] <--> bus
    wider --> mar
    bus <--> mar
    mar <--> ext["RAM, ROM y E/S en bus externo"]
~~~

Las flechas dobles representan **rutas posibles**, no varios drivers activos simultáneamente. Un esquema electrónico posterior deberá dibujar multiplexores, buffers, selección de chips y pines concretos.

## 2. Un datapath didáctico, sin ALU de 16 bits escondida

Se propone un **bus interno de datos de 8 bits** y registros de 16 bits accesibles por mitades. El sumador/ALU general sigue siendo de 8 bits.

El problema es que `PC`, `SP`, `X` y `MAR` son de 16 bits. Hay tres caminos:

| Alternativa | Ventaja | Costo educativo/eléctrico | Estado |
| --- | --- | --- | --- |
| A. Incrementador dedicado de 16 bits solo para PC; ALU8 para resto | Fetch fácil de seguir; flags de datos aislados | Añade lógica de incremento PC | **Preferida provisionalmente** |
| B. Todas las sumas de dirección pasan por ALU8 | Reutiliza circuito aritmético | Más microestados, multiplexores y manejo de acarreo interno | Alternativa viable |
| C. ALU completa de 16 bits | Algunas direcciones se calculan directamente | Contradice la sencillez buscada para Aula-8 | No recomendada |

Incluso en la opción A, `SP±n`, `X±n` y dirección efectiva pueden utilizar dos operaciones de 8 bits: byte bajo, acarreo/préstamo interno, byte alto. **No deben escribir accidentalmente `FLAGS.C`** durante el cálculo de direcciones.

### Una dirección de 16 bits con desplazamiento de 8

Ejemplo: `X=0x12FF`, desplazamiento `+2`.

1. Extender el desplazamiento con signo a 16 bits: `0x0002`.
2. Sumar bytes bajos `0xFF + 0x02 = 0x101`; conservar `0x01` y acarreo interno 1.
3. Sumar altos `0x12 + 0x00 + 1 = 0x13`.
4. Dirección efectiva `0x1301`, cargar `MAR` y realizar lectura/escritura.

Para `d=-1`, extensión `0xFFFF` y suma modular sobre los dos bytes. Debe verificarse correctamente el acarreo entre mitades sin modificar la bandera C del programa.

## 3. Lectura y escritura: protocolo de propiedad del bus

**Lectura:** `MAR` conduce dirección; CPU activa `RD`; el dispositivo seleccionado presenta el byte en `D0..D7`; `MDR` lo captura cuando sea válido; se libera la lectura.

**Escritura:** `MAR` conduce dirección; `MDR`/salida de CPU presenta un byte estable; se activa `WR`; solo el dispositivo seleccionado captura datos; se desactiva escritura.

Invariantes por verificar cuando exista lógica:

- En una transacción no pueden estar activos `RD` y `WR` a la vez.
- Durante lectura, CPU **no** debe conducir el bus de datos externo.
- Durante escritura, RAM/E/S **no** deben conducir el bus de datos externo.
- Solo una memoria o dispositivo debe responder a una dirección.
- ROM no acepta escritura normal; la EEPROM física no se «reprograma» mediante `ST` ordinario.
- El panel manual obtiene el bus únicamente al detener/aislar CPU; la entrada a modo manual debe tener mecanismo explícito.
- El reloj admisible dependerá de tiempos de memoria y propagación reales. Esta especificación **no** fija MHz ni ciclos de reloj por instrucción.

## 4. Fetch común para instrucciones de longitud variable

Un ciclo de instrucción tiene tantas lecturas de bytes como exija el formato. El esquema conceptual siguiente es una **secuencia de dependencias**, no una promesa de microinstrucciones de un solo reloj:

| Fase lógica | Acción y valores |
| --- | --- |
| `F_ADDR` | `MAR ← PC`, CPU solicita lectura |
| `F_DATA` | `MDR ← memoria[MAR]`, cuando el dato sea válido |
| `F_INC` | `PC ← PC+1`, conservando Z/N/C/V |
| `F_IR` | `IR ← MDR`, decodificar opcode y formato |
| `F_DISPATCH` | Ir a microprograma de `IR`, o entrar en estado de fallo si no es válido |

Los operandos posteriores usan un patrón de lectura similar, pero en vez de entrar en `IR` se guardan en `SEL`, `TMP`, byte bajo de dirección y byte alto de dirección, según corresponda.

Para la ROM de control: preferir un **fetch común reutilizable** y entrada por opcode a microsecuencias; evitar duplicar los pasos completos de lectura de instrucción en 36 filas independientes. La **anchura, capacidad, campos y pinout** de la micro-ROM permanecen pendientes.

## 5. Microoperaciones del primer programa

El ejemplo proviene de R0.3 y comienza en `0x6000`:

~~~text
6000: 11 00 2A    LDI R0, 42
6003: 13 00 00 6F ST [0x6F00], R0
6007: 01          HALT
~~~

### LDI R0, 42

1. Fetch del opcode `11` en `PC=0x6000`, incrementando PC a `0x6001`.
2. Leer selector `00` desde `0x6001`; validar `R0` y actualizar PC a `0x6002`.
3. Leer inmediato `2A` desde `0x6002`; avanzar PC a `0x6003`.
4. Habilitar escritura en `R0` y cargar `2A`; **no cambiar flags**.

### ST [0x6F00], R0

1. Fetch de opcode `13` desde `0x6003`; avanzar PC a `0x6004`.
2. Leer selector `00` (modo absoluto, R0) desde `0x6004`.
3. Leer bajo `00` desde `0x6005` y alto `6F` desde `0x6006`.
4. Formar `MAR=0x6F00`; presentar `2A` desde R0 en el camino de escritura (mediante `MDR` o registro conductor apropiado).
5. Activar `WR` de RAM; capturar `2A` en dirección `0x6F00`; desactivar `WR` y liberar bus. PC queda `0x6007`.

### HALT

1. Leer opcode `01` desde `0x6007`, avanzar PC candidato a `0x6008`.
2. Entrar en `HALTED=1`; dejar de ejecutar instrucciones hasta el mecanismo de control explícito.
3. El panel puede examinar `0x6F00` **solo** cuando posee el bus, no durante una escritura de CPU.

El rastro de las **nueve transacciones externas esperadas** está representado en [MICROTRAZA_AULA8_BORRADOR.json](MICROTRAZA_AULA8_BORRADOR.json): ocho lecturas de bytes de instrucciones y una escritura en RAM. Comprobar esta lista no mide reloj, no ejecuta un sumador y no certifica la electricidad.

## 6. Microoperaciones por familia que quedan por diseñar

| Familia | Necesidades y riesgos principales |
| --- | --- |
| MOV/LDI | Decodificar registro de destino, habilitar una sola carga, conservar flags |
| LD/ST absoluto | Capturar dos bytes de dirección en orden little-endian y controlar RD/WR |
| LD/ST indexado por X | Extender desplazamiento firmado, sumar en 16 bits, no alterar C visible |
| LD/ST relativo a SP | Preservar SP mientras se calcula MAR para argumentos/locales |
| ADD/ADC/SUB/SBC | Fuentes ALU, carry/borrow entrante y saliente, cálculo exacto de Z/N/C/V |
| CMP | Actualizar flags sin habilitar escritura al registro comparado |
| INC/DEC/SHL/SHR | Semántica exacta de flags y bits desplazados |
| Saltos | Leer destino, comprobar Z/C, cargar PC solo si se cumple condición |
| CALL | Leer destino, guardar PC siguiente en pila como dos bytes, cambiar PC |
| RET | Leer dos bytes de retorno, restaurar PC y SP sin corromper flags |
| PUSH/POP/PUSHX/POPX | Orden de bytes, SP descendente, límites de RAM y posible solapamiento |
| SETX/LEAX/ADDXW | Modificar 16 bits por microoperaciones byte a byte, flags preservadas |
| SETSP/ADJSP/XFROMSP | Pila, marcos locales, seguridad de límites y transferencia por mitades |
| HALT/FAULT | Distinguir parada normal de opcode inválido, sin retorno automático a ROM |

La unidad de control deberá tener un mecanismo que pueda **distinguir éxito de lectura, instrucción completa y condición de salto**, no limitarse a encender LED como indicador visual.

## 7. Arranque y panel de programación: dos entradas diferentes

- **Arranque normal por RESET:** se leen dos bytes de la ROM de firmware en `0xFFFC–0xFFFD`; se forma una dirección de 16 bits, se carga PC y se entra en fetch. La ROM **debe estar preprogramada** con un vector válido.
- **Depósito manual:** CPU está detenida o eléctricamente aislada; panel conduce dirección/datos y pulso de escritura de RAM. Después la CPU necesita un mecanismo explícito para iniciar PC en la dirección elegida (`LOAD_PC`, inyección de salto u otro circuito a diseñar).
- `RESET` no implica necesariamente «ejecutar los bytes que acabo de depositar en RAM»: si el vector sigue en ROM, arrancará el firmware. Esta diferencia debe verse en el manual y en las lecciones.

## 8. Plan de validación antes de congelar control

1. Enumerar todos los **drivers** del bus interno/externo y las combinaciones prohibidas.
2. Verificar una sola escritura de destino por microestado, salvo transferencia expresamente multiciclo.
3. Confirmar que operaciones de dirección **no contaminan Z/N/C/V**.
4. Formalizar temporización de SRAM/EEPROM e I/O real antes de elegir frecuencia.
5. Acordar si PC tiene incrementador propio o comparte ALU8, midiendo compuertas y microestados requeridos.
6. Diseñar microsecuencias exactas de `CALL`, `RET`, `PUSHX`, acceso por X/SP y errores de opcode.
7. Comparar CPU por microestados con intérprete ISA independiente **cuando existan ambos**.
8. Confirmar que los ejemplos de R0.3 se comportan como sus resultados esperados; hoy solo existe una verificación de codificación y traza manual.
9. Validar aparte esquemas físicos, fan-out, alimentación, márgenes y comportamiento con instrumentos; esto no lo puede sustituir el motor digital.

## 9. Alcance de esta tanda

**Hecho:** propuesta de bloques y buses; decisión candidata sobre PC; separación de flags y acarreo de direcciones; fetch conceptual; recorrido lógico de `LDI`, `ST` y `HALT`; dependencia de arranque ROM y depósito manual; criterios para diseñar microcódigo.

**No hecho:** RTL o netlist físico, microinstrucciones codificadas en bytes, reloj/ciclos definitivos, CPU ejecutable, ROM real, PC de panel, circuitos medidos o simulación 3D.
