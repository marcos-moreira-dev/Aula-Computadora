# Aula-8 — llamadas, retornos y saltos de control (R0.6)

**Estado: PROPUESTA NO APROBADA.** Continúa la [ISA candidata R0.3](ISA_AULA8_CANDIDATA.md), la [microarquitectura R0.4](MICROARQUITECTURA_AULA8_BORRADOR.md) y el [fetch común R0.5](UNIDAD_CONTROL_AULA8_BORRADOR.md). Aquí se definen **acciones lógicas**, no microcódigo binario ni ciclos eléctricos.

## 1. El problema real: entrar a una subrutina y poder volver

Una instrucción `JMP 0x6010` cambia el PC y olvida de dónde vino. `CALL 0x6010` debe recordar **la dirección posterior a sus propios operandos**. `RET` necesita recuperarla. Esa es la idea de una *subrutina*, mecanismo imprescindible para reutilizar servicios de la ROM y para implementar funciones de MiniC-Aula.

El libro mostrará primero un salto, luego `CALL/RET`, y solo después los convenios de parámetros y registros. Este anexo de ingeniería **no se insertará literalmente** en el manuscrito.

## 2. Convención de pila candidata: dirección libre por encima

La RAM inicial ocupa `0x0000–0x7FFF`. El firmware propondrá inicialmente `SP=0x8000`, es decir, **una dirección más allá del último byte**, sin escribir allí.

Para un `CALL` con `SP=0x8000` y retorno `0x6003`:

1. Tras leer opcode y los dos bytes de destino, `PC` ya apunta a `0x6003`.
2. Guardar temporalmente ese valor: `RET_LO=0x03`, `RET_HI=0x60`.
3. Calcular `SP ← SP-2 = 0x7FFE`. La operación sobre direcciones no modifica `Z/N/C/V`.
4. Guardar el **byte bajo** `0x03` en `RAM[0x7FFE]`.
5. Guardar el **byte alto** `0x60` en `RAM[0x7FFF]`.
6. Cargar el destino `0x6010` en `PC` y continuar la búsqueda de instrucciones.

Para `RET`, ocurre lo inverso: leer bajo desde `[SP]`, alto desde `[SP+1]`, avanzar `SP` dos posiciones y cargar `PC` con ambos bytes.

| Instante | SP | RAM[0x7FFE] | RAM[0x7FFF] | PC |
| --- | --- | --- | --- | --- |
| Antes de CALL | `8000` | Indeterminado | Indeterminado | `6000` |
| Luego de CALL | `7FFE` | `03` | `60` | `6010` |
| Luego de RET | `8000` | `03` (residuo) | `60` (residuo) | `6003` |

**Importante:** `RET` no borra los bytes antiguos de RAM. Los considera liberados porque avanzó SP. El valor se sobrescribirá en llamadas posteriores. No asumir que la pila se limpia sola.

La elección de guardar primero bajo y luego alto **coincide con el contrato candidato de R0.3**; no cambia la ISA ni la ABI sin aprobación.

## 3. Recursos temporales mínimos para explicar la secuencia

Reutilizamos `ADDR_LO/ADDR_HI` de R0.5 para mantener el **destino del salto**, incluso cuando `MAR` se reutiliza para escribir la pila. Se proponen `RET_LO/RET_HI` para conservar la **dirección de retorno** después de consumir operandos en `PC`.

Para `RET`, los mismos `RET_LO/RET_HI` pueden capturar los bytes leídos de pila antes de sobrescribir PC. Esto es almacenamiento **lógico candidato**, no necesariamente cuatro chips nuevos: en R1 se decidirá qué latches se comparten sin destruir datos vivos.

`MAR ← SP+1` es una **dirección temporal**; no incrementa SP y no modifica flags. Las sumas de 16 bits pueden emplear dos pasadas ALU8 y `ADDR_CARRY` privado. No introducimos una segunda ALU de 16 bits oculta.

## 4. Flujo de CALL y RET

El fetch compartido siempre lee opcode y avanza PC. Las rutas de esta tanda comienzan **después** de ese fetch.

### CALL (opcode `35`, destino absoluto de 16 bits)

| Etapa lógica | Acción | Condición observable |
| --- | --- | --- |
| Destino bajo/alto | Leer dos bytes siguientes a `ADDR_LO/HI` | PC avanza dos posiciones más. |
| Conservar retorno | Copiar PC ya actualizado a `RET_LO/HI` | No se pierde dirección del llamador. |
| Reservar pila | `SP ← SP-2` | Dos posiciones contiguas en memoria. |
| Escritura baja | `MAR ← SP`, `MDR ← RET_LO`, escribir | Una escritura en `[SP]`. |
| Escritura alta | `MAR ← SP+1`, `MDR ← RET_HI`, escribir | Una escritura en `[SP+1]`. |
| Transferencia | `PC ← ADDR_HI:ADDR_LO` | Fetch siguiente comienza en destino. |

Nunca activar `WR` sin preparar **MAR y MDR**. Una CPU física debe impedir contención con memoria y panel. Un `CALL` hacia ROM es válido como **lectura/ejecución**; su retorno se apila en **RAM**, no se escribe en ROM.

### RET (opcode `02`, sin operandos)

| Etapa lógica | Acción | Condición observable |
| --- | --- | --- |
| Byte bajo | `MAR ← SP`; leer en `RET_LO` | Una lectura de RAM. |
| Byte alto | `MAR ← SP+1`; leer en `RET_HI` | Segunda lectura de RAM. |
| Liberar pila | `SP ← SP+2` | No borra contenidos antiguos. |
| Recuperar retorno | `PC ← RET_HI:RET_LO` | Fetch siguiente en el llamador. |

Si una subrutina ejecuta `HALT`, **no** hace `RET`. Una llamada anidada debe salvar en memoria cada retorno: no basta con un registro de «último retorno» de alcance global. Los `RET_LO/HI` son temporales para la operación actual; cada `CALL` deposita su par en la pila antes de saltar.

## 5. JMP y saltos condicionales

`JMP`, `JZ`, `JNZ`, `JC` y `JNC` utilizan el mismo operando **absoluto little-endian**: `OP bajo alto`. **Siempre se leen los dos bytes**, incluso si un salto condicional resulta no tomado.

1. Leer `ADDR_LO` desde `PC`; incrementar PC.
2. Leer `ADDR_HI` desde `PC`; incrementar PC.
3. Para `JMP`, cargar `PC ← destino`. Para las otras instrucciones, consultar flags **sin modificarlas**.
4. Si la condición se cumple, cargar el destino en PC; si no, conservar el PC que ya apunta a la instrucción siguiente.
5. Retornar al fetch común.

| Instrucción | Se toma cuando… | Si no se toma… |
| --- | --- | --- |
| `JMP` | Siempre | No aplica. |
| `JZ` | `Z=1` | Se conserva PC posterior al operando. |
| `JNZ` | `Z=0` | Se conserva PC posterior al operando. |
| `JC` | `C=1` | Se conserva PC posterior al operando. |
| `JNC` | `C=0` | Se conserva PC posterior al operando. |

Como propone la ISA R0.3, `C` significa **acarreo** después de suma y **préstamo** después de resta. Así, `JNC` tras `CMP` puede indicar «mayor o igual *sin signo*». Para condiciones con signo no se deben inferir saltos que la ISA todavía no implementa.

### Ejemplo: JNZ del contador

En el ejemplo R0.3, `DEC R0` termina con `Z=0, 0, 1` en tres iteraciones. La instrucción `32 03 60` (`JNZ 0x6003`) lee sus **dos operandos en cada iteración**, salta dos veces y en la tercera continúa hacia `HALT` en `0x6008`. La microsecuencia detallada de `DEC` aún está pendiente, por lo que esta comprobación es **semántica declarada**, no traza ejecutada.

## 6. Prueba de escritorio: CALL, LDI, RET, HALT

Colocamos los bytes en la **zona candidata de programas** `0x6000–0x6FFF`; las direcciones intermedias no utilizadas no se ejecutan.

~~~text
6000: 35 10 60      CALL 0x6010
6003: 01            HALT
...
6010: 11 00 2A      LDI R0, 42
6013: 02            RET
~~~

Suponiendo `SP=0x8000`, el flujo esperado es:

~~~text
PC 6000 → CALL guarda 6003 en 7FFE/7FFF → PC 6010
PC 6010 → LDI carga R0=2A                → PC 6013
PC 6013 → RET lee 6003, SP vuelve a 8000 → PC 6003
PC 6003 → HALT                           → PC 6004 (detenida)
~~~

**Transacciones externas esperadas:** `CALL` = 3 lecturas y 2 escrituras; `LDI` = 3 lecturas; `RET` = 3 lecturas (opcode + 2 pila); `HALT` = 1 lectura. **Total: 10 lecturas y 2 escrituras, 12 transacciones lógicas**, no 12 ciclos eléctricos. En la [especificación JSON](MICROFLUJO_AULA8_R0_6_BORRADOR.json) queda también enumerada la traza esperada para comprobarla sin ejecutar CPU.

## 7. Riesgos y límites deliberadamente abiertos

- **Pila fuera de RAM:** el modelo físico inicial no tiene protección de memoria definida. No prometer una excepción automática; el taller futuro puede advertirlo y R1 decidirá protecciones o convenciones de firmware.
- **CALL sin espacio:** no escribir parcialmente un retorno y declarar éxito. Falta especificar qué condiciones reales detectará la CPU y cuáles solamente el software didáctico.
- **RET sin CALL:** leerá bytes de memoria según SP; no se asumirá que existe mágicamente una dirección correcta. Falta diseñar política de fallo y pruebas de datos arbitrarios.
- **CALL anidado y recursividad:** debe probarse con una futura CPU independiente y verificar que cada retorno se apila en orden.
- **Señales eléctricas:** reloj, niveles, temporización de lecturas/escrituras, cuantía de ROM de control y latches compartibles siguen pendientes.
- **Firmware público:** una rutina como `FW_PUTC` podrá usar CALL/RET, pero hay que cerrar ABI, política de registros conservados y puntos de entrada ROM antes de prometer compatibilidad.
- **Aula-16:** sigue siendo otra CPU con **bus externo de datos de 16 bits**; no aplicamos esta codificación de Aula-8 a Aula-16.

## 8. Evidencia y siguiente frontera

La prueba `scripts/verificar_flujo_aula8_r0_6_borrador.py` valida **solo** transiciones documentales, orden little-endian, direcciones de pila, condiciones de branch y correspondencia con la ISA candidata. Un resultado verde **no** demuestra microcódigo, funcionamiento físico, protección ante errores ni que un compilador nativo exista.

La siguiente decisión técnica razonable, antes de congelar ISA y escribir capítulos definitivos, es diseñar `PUSH/POP`, actualización de `SP`, `DEC` y control de `Z/N/C/V` con pruebas de borde; después vincularlos a un intérprete ISA independiente y al microcontrol real.
