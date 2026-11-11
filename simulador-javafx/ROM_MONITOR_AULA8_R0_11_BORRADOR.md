# Aula-8 R0.11 — ROM pública, RESET y monitor hexadecimal (borrador)

**Estado: PROPUESTA NO APROBADA.** Es una especificación original de interfaz,
no una EEPROM grabable, firmware compilado, simulación de CPU ni circuito.
La ROM de *microcontrol* de Aula-8 es distinta de esta **ROM de firmware**.
Este contrato concierne a Aula-8. Aula-16 tendrá imagen y código máquina propios:
su **bus externo de datos sigue siendo de 16 bits**.

## 1. Por qué una tabla de servicios

Un programador de Aula-8 no debería memorizar la posición interna de la rutina
que imprime una letra. Si una corrección cambia esa rutina de `0xE100` a
`0xE250`, un programa anterior puede seguir invocando `FW_PUTC` en
`0xFF00`. Para conseguirlo, reservamos una **ranura fija** que salta a la
implementación. Solo el firmware conoce dónde se encuentra ahora la rutina.

`CALL 0xFF00` no es igual que `JMP 0xFF00`: `CALL` guarda una dirección de
retorno en la pila. La ranura ejecuta `JMP` hacia la rutina real y esta termina
en `RET`, devolviendo el control al programa que hizo `CALL`. La instrucción
`NOP` que completa la ranura de cuatro bytes es **relleno reservado**; en el
flujo normal no se ejecuta.

### 1.1. Tabla candidata, sin reservar toda la ROM

| Dirección estable | Servicio | Entrada | Resultado observable |
| --- | --- | --- | --- |
| `0xFF00` | `FW_PUTC` | R0: carácter | Envía un carácter y espera salida disponible |
| `0xFF04` | `FW_GETC` | Ninguna | R0: carácter leído; espera hasta recibir uno |
| `0xFF08` | `FW_PUTS` | X: dirección de cadena terminada en `00` | Emite los bytes anteriores al terminador |
| `0xFF0C` | `FW_STATUS` | Ninguna | R0: máscara candidata de estado del terminal |

Se propone reservar **32 ranuras de cuatro bytes**, exactamente
`0xFF00–0xFF7F` (128 B). Solo las primeras cuatro tienen nombre público
en R0.11. Las demás quedan **sin asignar, no invocables**. En particular,
`FW_READ_BLOCK` y `FW_WRITE_BLOCK` **no** reciben direcciones públicas todavía:
faltan el protocolo y las garantías de persistencia del controlador.

La ROM de firmware ocupa `0xE000–0xFFFF` (**8192 B**). `0xFF80–0xFFFB`
permanece disponible para código/datos de firmware según mapa de enlace;
`0xFFFC–0xFFFD` contiene el vector de RESET y `0xFFFE–0xFFFF` está reservado.
No inferir que todos los bytes disponibles se podrán ocupar sin medir el
enlazado de un firmware real.

### 1.2. ¿Qué bytes se introducirían?

Con la ISA **candidata** R0.3, `JMP` = `30`, dirección inmediata de 16 bits
en orden little-endian y `NOP` = `00`. Una ranura tiene el esquema:

```text
dirección +0: 30     opcode JMP
dirección +1: LL     byte BAJO de destino
dirección +2: HH     byte ALTO de destino
dirección +3: 00     NOP de relleno
```

Ejemplo **ilustrativo, no direcciones de rutinas existentes**:

| Dirección | Bytes hexadecimales | Interpretación |
| --- | --- | --- |
| `FF00` | `30 00 E1 00` | `JMP E100`, rutina hipotética PUTC |
| `FF04` | `30 40 E1 00` | `JMP E140`, rutina hipotética GETC |
| `FF08` | `30 80 E1 00` | `JMP E180`, rutina hipotética PUTS |
| `FF0C` | `30 C0 E1 00` | `JMP E1C0`, rutina hipotética STATUS |

Los destinos son **marcadores didácticos**. No se debe ejecutar esta tabla
como si hubiese subrutinas reales en tales direcciones.

El *presupuesto* anterior asignaba 512 B a vector, tabla y alineación. Esta
propuesta consume **128 B** de ese techo en ranuras y **2 B** en vector,
dejando **382 B** de margen de ese mismo rubro para otros usos/ubicaciones
a definir. No se deduce cabida de las rutinas: los seis techos que suman
8192 B continúan siendo estimaciones sin mapa de enlace.

## 2. ¿Cómo arranca Aula-8 desde una ROM ya grabada?

Al encender, no debemos suponer que RAM contiene ceros ni que contiene un
monitor. Primero hay que haber **grabado una imagen de firmware** en EEPROM.
El mecanismo candidato de RESET obtiene el **byte bajo** de `0xFFFC` y el
**byte alto** de `0xFFFD`; al combinarlos carga PC. Una hipotética entrada
`0xE000` se representaría con los dos bytes `00 E0`:

1. CPU pasa a estado RESET, sin ejecutar un programa de RAM aleatoria.
2. Lee `[FFFC] = 00` y `[FFFD] = E0` de la ROM de firmware.
3. Forma `PC = (E0 << 8) | 00 = E000`.
4. El código real en E000, cuando exista, configura `SP=8000`, estado de
   CPU, búferes estrictamente necesarios y controlador de terminal.
5. Presenta un mensaje e inicia el bucle `leer línea → validar → responder`
   por *polling*. Nunca confía en datos de RAM sin inicializarlos.

La ROM interna de microcontrol y el bus necesario para leer el vector todavía
**no están implementados**. El ejemplo `E000` es una entrada sugerida, no
una imagen final ejecutable.

## 3. ABI de firmware: contrato de entrada distinto del de MiniC

Proponemos que el programa use `CALL` a la ranura pública, no una llamada
directa a la implementación. La rutina debe conservar **R2, R3 y X** y
devolver `SP` al mismo valor que había justo después del `CALL` del usuario;
`RET` elimina la dirección de retorno por el mecanismo R0.6. **R0, R1 y
Z/N/C/V son volátiles**; el programador debe tratar sus valores finales como
indeterminados salvo la salida explícita de la rutina.

Esto **no es** adoptar el prólogo de MiniC R0.10 dentro de ROM: no se obliga
al firmware a crear el marco con X, ni a recibir argumentos en las ranuras
de dos bytes de MiniC. Es una ABI pública **diferente**, que casualmente
comparte la regla propuesta de registros preservados.

- `FW_PUTC`: entrada R0 = byte de carácter. Puede esperar a que TX esté listo.
  Sin valor de retorno garantizado en R0.
- `FW_GETC`: espera por *polling* hasta recibir un byte; devuelve ese byte
  en R0. El bloqueo sin teclado no es un fallo de CPU.
- `FW_PUTS`: X señala el primer byte de una cadena terminada en `00`. X se
  conserva. El programa debe proporcionar una cadena legible, terminada y
  dentro de RAM o ROM; **sin protección de memoria implementada**, las
  cadenas corruptas siguen siendo un riesgo.
- `FW_STATUS`: R0 devuelve una máscara **candidata**: bit 0 = RX disponible,
  bit 1 = TX listo, los demás = 0. Esta codificación de la API no fija todavía
  el cableado ni la codificación real del registro MMIO.

La interfaz física acordada del terminal continúa en `0xC000` (**DATA**) y
`0xC002` (**STATUS**), con caracteres de ocho bits compatibles con ASCII.
Los detalles eléctricos de esos registros siguen pendientes. Ni `FW_STATUS`
ni las rutinas anteriores constituyen un UART probado.

### 3.1. Ejemplo: de un byte de programa a la consola

Supongamos un programa ensamblado en `0x6000` que imprime una letra:

```text
6000  11 00 41    LDI R0, 0x41    ; 'A' en ASCII
6003  35 00 FF    CALL 0xFF00     ; FW_PUTC
6006  02          RET             ; vuelve al monitor si RUN usó CALL
```

La primera instrucción carga `0x41` en R0. `CALL` apila `0x6006` y entra
en `0xFF00`. Allí un hipotético `JMP E100` enlaza con el servicio. El
`RET` del **servicio** lleva a `0x6006`. El `RET` del **programa** lleva
de vuelta al monitor, **solo si el monitor lo inició mediante CALL**.
Este recorrido de dos retornos explica por qué no son intercambiables
`CALL`, `JMP` y `HALT`.

El listado es un **ejemplo de bytes pendientes de CPU/firmware real**.
Tampoco asegura que haya espacio libre en `E100` para una rutina.

## 4. El monitor: una consola deliberadamente primitiva

Se propone que reconozca palabras ASCII sin importar mayúsculas, y que los
números sean **hexadecimales sin prefijo**:

- Direcciones: exactamente cuatro cifras (`6000`, `FF00`).
- Bytes: exactamente dos cifras (`2A`, `00`).
- Longitud de `MEM`: una a cuatro cifras; desde `1` hasta `100`
  (máximo 256 bytes), interpretadas en hexadecimal.
- Separadores: espacios simples o repetidos. Se rechazan argumentos
  incompletos, caracteres no hexadecimales y parámetros adicionales.

| Comando | Ejemplo | Semántica **candidata** |
| --- | --- | --- |
| `HELP` | `HELP` | Muestra sintaxis y los comandos pendientes |
| `MEM direccion [longitud]` | `MEM 6000 10` | Lee 16 bytes; si se omite longitud, lee 16 (`0x10`) |
| `POKE direccion byte` | `POKE 6000 2A` | Escribe un byte **solo** en ventana de práctica `6000–6FFF` |
| `RUN direccion` | `RUN 6000` | Desde el monitor realiza **CALL** al programa de la ventana de práctica |
| `REG` | `REG` | **No disponible** hasta definir captura fiable de registros |
| `LOAD` | `LOAD` | **No disponible** hasta definir controlador de bloques y formato crudo |

Para `MEM` se permiten rangos **completamente legibles** dentro de RAM
`0000–7FFF` o ROM `E000–FFFF`. Si el rango atraviesa RAM/expansión,
`0xC000` de periféricos, o el final del espacio, se **rechaza toda la
operación** en vez de inventar bytes. Para `POKE` limitamos **por
seguridad del monitor, provisionalmente**, la escritura interactiva a
`6000–6FFF`. El panel detenido puede tener otro mecanismo con arbitraje
eléctrico y supervisión; esta regla **no** hace que la CPU tenga protección
de memoria. La ROM no es escribible mediante `POKE`.

En `RUN`, la dirección se restringe provisionalmente a `6000–6FFF`,
pero un futuro cargador de herramientas nativas necesitará llamar también
a la región *overlay* mediante un camino de control explícito. Ejecutar
RAM sin cargar código coherente es responsabilidad del usuario; el monitor
no puede adivinar si los bytes son instrucciones válidas.

### 4.1. ¿Y el retorno al prompt?

**Ruta que regresa:** `RUN 6000` → CALL al inicio → programa termina
mediante `RET` → el monitor recupera su continuación y vuelve al prompt.
El programa debe respetar su contrato de pila; el monitor necesitará
proteger su propio contexto, algo **todavía sin código ni pruebas reales**.

**Ruta que se detiene:** si el programa ejecuta `HALT`, la CPU se detiene.
**No aparece por arte de magia un prompt**. Para recuperar el monitor
habrá que realizar RESET o diseñar posteriormente un mecanismo explícito
de interrupción/depuración. No fingir retorno tras un HALT.

**Comando REG:** el propio monitor altera registros al procesar texto. Para
mostrar registros *del programa detenido* se necesita captura por un
mecanismo de depuración/trap o un contrato de guardado. Por eso, la versión
documentada aquí dice `NO DISPONIBLE`, en vez de mostrar valores falsos.

**Comando LOAD:** los bloques persistentes son de 256 B, pero faltan
registros del controlador, errores, formato crudo y transporte. No se
promete `LOAD archivo` ni `DIR` sin un directorio implementado.

### 4.2. Sesión ilustrativa

```text
AULA-8 MONITOR (propuesto)
> HELP
HELP MEM POKE RUN | REG y LOAD: PENDIENTES
> POKE 6000 11
OK
> POKE 6001 00
OK
> POKE 6002 41
OK
> POKE 6003 35
OK
> POKE 6004 00
OK
> POKE 6005 FF
OK
> POKE 6006 02
OK
> MEM 6000 07
6000: 11 00 41 35 00 FF 02
> RUN 6000
A
>
```

La sesión muestra el **resultado exigido cuando haya hardware y firmware**.
No son capturas de una aplicación funcionando. Los bytes se depositan en
`RAM` mediante el monitor de ROM; éste ya tiene que existir en EEPROM.

## 5. Qué se puede comprobar ahora, y qué no

El contrato acompañante [JSON](ROM_MONITOR_AULA8_R0_11_BORRADOR.json)
y `scripts/verificar_rom_monitor_aula8_r0_11_borrador.py` comprueban:

1. Que cuatro ranuras codificadas con `JMP` de la ISA candidata caben
   en la reserva de 32 ranuras sin tocar el vector.
2. Que el vector little-endian podría apuntar a `E000` sin salir de ROM.
3. Que `POKE` rechaza ROM, E/S y RAM reservada según la ventana **candidata**.
4. Que `MEM` detecta rangos desbordados y caracteres inválidos.
5. Que `RUN` modela `RET` distinto de `HALT`, sin inventar un trap.
6. Que el presupuesto completo de ROM continúa sumando 8192 B y Aula-16
   conserva sus 16 bits de bus de datos externo.

Los resultados son **cálculos y validación de interfaz**, no llamadas
reales ejecutadas por la CPU, parser grabado, EEPROM montada, medidas de
ROM/RAM, control de la pila ni persistencia.

## 6. Bloqueos reales antes de fabricar el firmware

- Congelar ISA, RESET, latches, protocolo MMIO y ABI de firmware.
- Crear un ensamblador cruzado que emita **bytes reales** y un enlazador
  que sitúe rutinas sin invadir `FF00–FF7F` ni `FFFC–FFFF`.
- Implementar CPU y memoria; probar CALL al slot, JMP interno, doble RET,
  flags y restauración de SP sobre instrucciones efectivamente ejecutadas.
- Escribir el monitor, verificar RAM no inicializada, entradas inválidas,
  bloqueo del terminal y límites de memoria.
- Medir los **8192 B** efectivos del firmware; si no cabe, trasladar
  comandos secundarios a RAM en vez de afirmar mágicamente que cabe.
- Especificar dispositivo de bloques antes de hacer `LOAD` o asignar
  ranuras de servicios de lectura/escritura.

Hasta completar eso, esta R0.11 es una **propuesta útil para enseñar y revisar**,
pero no un firmware instalado en ninguna computadora.
