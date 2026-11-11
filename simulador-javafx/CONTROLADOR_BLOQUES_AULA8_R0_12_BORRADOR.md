# Aula-8 R0.12 — almacenamiento de bloques y futura carga a RAM

**PROPUESTA NO APROBADA.** Esta entrega contiene un contrato de registros,
un modelo de referencia en Python ejecutado por la computadora anfitriona
y pruebas reproducibles. No contiene controlador digital por netlist, CPU,
firmware, ROM de servicios, sistema de archivos ni cargador nativo.

## 1. Una tarjeta de memoria elemental, no un disco duro simulado

Imaginemos que la primera herramienta de Aula-8 —un editor de líneas— ocupa
4096 bytes. Si su binario se guarda como bloques de **256 bytes**, se requieren:

```text
bloques necesarios = techo(tamaño_en_bytes / 256)
4096 / 256 = 16 bloques
```

Un controlador deja al procesador seleccionar un bloque y transferir sus 256
bytes **de uno en uno**. Los datos viven en una imagen de almacenamiento
persistente; el *modelo de referencia* de R0.12 guarda esa imagen en un
archivo del anfitrión. En el futuro, un circuito o simulador de hardware
deberá implementar la misma interfaz de registros.

No existe todavía directorio: «bloque 0002» significa posición numérica
de 256 B, **no** un archivo denominado `0002`.

## 2. Direcciones que ya estaban reservadas

La arquitectura propone un periférico en `0xC010–0xC01F`, dentro de la
región de E/S `0xC000–0xC0FF`. Para Aula-8 proponemos ocho registros,
todos de **8 bits** y en direcciones pares:

| Dirección | Registro | Dirección de acceso | Función |
| --- | --- | --- | --- |
| `C010` | `COMMAND` | Escritura | `00` NOP, `01` READ, `02` WRITE, `03` RESET |
| `C012` | `STATUS` | Lectura | Bits de transferencia, fin o error |
| `C014` | `BLOCK_LO` | Lectura/escritura | Octeto bajo del número de bloque |
| `C016` | `BLOCK_HI` | Lectura/escritura | Octeto alto del número de bloque |
| `C018` | `DATA` | Lectura/escritura según orden | Puerto secuencial de datos |
| `C01A` | `ERROR` | Lectura | Último código de fallo |
| `C01C` | `COUNT_LO` | Lectura | Bytes transferidos, octeto bajo |
| `C01E` | `COUNT_HI` | Lectura | Bytes transferidos, octeto alto |

Las direcciones impares de este intervalo quedan **reservadas**: no son
alias mágicos de la dirección par anterior. Aula-8 accede a bytes.
La eventual compatibilidad de Aula-16 debe respetar **su bus externo de
16 bits** y elegir carril correctamente; no se prescriben aquí ciclos
de palabra ni una ISA Aula-16.

El número de bloque es little-endian:

```text
numero_de_bloque = BLOCK_LO + 256 × BLOCK_HI
Ejemplo: BLOCK_LO=02 y BLOCK_HI=01 → bloque 0x0102
```

Dos octetos permiten seleccionar `0x0000–0xFFFF`: como máximo **65536
bloques**, equivalentes a **16 MiB** si la imagen tiene esa capacidad.
La capacidad real no se deduce del ancho del registro: depende de cuántos
bloques contenga la imagen conectada. Para las pruebas se crea una imagen
minúscula de ocho bloques; para enseñar se sugiere una de 256 bloques
(64 KiB), pero **ninguna capacidad está impuesta aún al hardware**.

## 3. Estado y errores sin interpretación ambigua

`STATUS` es una máscara candidata:

| Bit | Nombre | Significado |
| --- | --- | --- |
| 0 = `01` | BUSY | Transferencia todavía abierta |
| 1 = `02` | DRQ | Se puede transferir un byte por DATA |
| 2 = `04` | DONE | Se terminaron los 256 bytes correctamente |
| 3 = `08` | ERROR | Operación abortada o rechazada; leer ERROR |
| 4–7 | Reservados | Deben leerse cero en el modelo |

Estados nominales:

| Estado | STATUS | Conteo |
| --- | --- | --- |
| Inactivo/tras RESET | `00` | 0 |
| Transferencia de 256 B | `03` | 0..255 |
| Finalizado | `04` | 256 (COUNT_LO=00, COUNT_HI=01) |
| Fallo | `08` | Cantidad transferida antes del fallo |

El registro `ERROR` tiene esta codificación **propuesta**:

- `00`: ninguno.
- `01`: comando inválido.
- `02`: bloque inexistente o fuera de la capacidad de la imagen.
- `03`: DATA leído/escrito en dirección o estado incorrectos.
- `04`: nuevo comando/configuración durante transferencia; operación abortada.
- `05`: fallo de almacenamiento de la imagen.

Escribir `RESET` (`03` en COMMAND) borra estado y contador y cancela el
buffer temporal, **sin borrar bloques persistidos**. Una nueva orden válida
tras DONE/ERROR también comienza con ERROR=00 y contador=0. Una nueva orden
—**incluso NOP**— o cambio de BLOCK_LO/HI durante BUSY se considera error y aborta;
RESET cancela limpiamente. Así no
quedan mezclados 128 bytes de un bloque y 128 de otro.

`STATUS=03` significa BUSY y DRQ a la vez: se está desarrollando la
transferencia, pero el siguiente acceso al registro DATA ya está permitido.
No se exige interrupción; la CPU lee STATUS periódicamente (*polling*).
No se han diseñado tiempos reales de espera, interrupciones ni señales físicas.

## 4. Secuencia READ de un bloque

Queremos cargar el bloque `0x0002`. Se propone:

1. Escribir `02` a BLOCK_LO (`C014`) y `00` a BLOCK_HI (`C016`).
2. Escribir `01` a COMMAND (`C010`). Si ese bloque existe,
   el controlador prepara 256 bytes y muestra STATUS=`03`.
3. Leer STATUS hasta que indique DRQ o ERROR. El monitor no debería
   confundirse entre «esperando» y «terminal congelada».
4. Leer **exactamente 256 veces** el puerto DATA (`C018`),
   guardando cada byte en el búfer protegido de RAM.
5. Después del último byte, COUNT=`0x0100` y STATUS=`04`.
   Un paso de más sobre DATA debe reportar error, no repetir el último byte.

Al leer la imagen en el anfitrión no se altera el archivo. En la CPU real
cada acceso sería una instrucción/ciclo de E/S, **todavía inexistente**.

## 5. Secuencia WRITE y alcance de la persistencia

Para escribir un bloque:

1. Indicar número de bloque y escribir `02` a COMMAND.
2. Esperar DRQ sin ERROR.
3. Escribir exactamente 256 bytes consecutivos en DATA.
4. Solo al recibir el **byte número 256** se considera completo un bloque;
   aparece DONE y los datos pueden persistirse.

Un `RESET`, un comando incompatible o una interrupción de la transferencia
antes del byte 256 descartan los bytes pendientes: **no se debe cambiar
media imagen por accidente**. El modelo de referencia escribe la imagen
entera en un archivo temporal y reemplaza el anterior después de completar
un bloque. Esta protección de software se comprueba al reabrir la imagen.

**Límite fundamental:** `os.replace` más `fsync` en un sistema anfitrión no
demuestran tolerancia a pérdidas súbitas de energía de un almacenamiento
físico, ni equivalen a un controlador de flash/EEPROM fabricado. La
recuperación ante cortes de corriente y checksum por bloque se definirán
cuando exista formato de imagen versionado/journaling o almacenamiento
físico. Tampoco hay semántica de «archivo guardado» antes de un directorio.

## 6. Preparar LOAD sin inventar un sistema de archivos

El borrador R0.11 marca `LOAD` como NO DISPONIBLE. Aquí se diseña
**la futura sintaxis, aún no ejecutable**:

```text
LOAD <bloque_hex4> <destino_ram_hex4> <cantidad_hex2>
LOAD 0002 1000 02
```

El ejemplo pediría los bloques `0002` y `0003`, es decir **512 bytes**,
para copiarlos desde `0x1000` hasta `0x11FF`. No se cargarían nombres
de archivo ni cabeceras: un binario crudo solo se podrá ejecutar si se
conocen externamente origen, tamaño, CPU destino y punto de entrada.

Para evitar pisar el monitor, el documento y la pila, solo se permitirían:

- **Overlay de herramientas** `1000–2FFF`, hasta 32 bloques.
- **Código de práctica** `6000–6FFF`, hasta 16 bloques.
- Dirección de RAM de destino **alineada a 256 B** (termina en `00`).
- Uno a 32 bloques por orden y **sin cruzar** el final de la ventana elegida.
- Bloque de origen y cantidad dentro de la imagen física presente.

El futuro cargador debe leer primero un bloque **completo** en el búfer
protegido de RAM (`0200–0FFF`), comprobar DONE/ERROR y solo entonces
copiar sus 256 bytes al destino de programa. Si el segundo bloque falla,
el primero puede haber sido copiado: la orden completa **no es atómica**.
Debe informar carga incompleta, **no ejecutar** lo parcialmente cargado y
permitir reiniciar la carga. Una copia por bloques se puede implementar con
el hardware existente cuando se definan sus rutinas.

No hay mecanismo para detectar por sí mismo si el código corresponde a
Aula-8 o Aula-16 ni si está truncado; un encabezado de ejecutable y checksum
pertenecen a otro hito. El editor y el ensamblador **nativos** que se
cargarán en el overlay deberán ejecutarse como instrucciones de Aula-8,
no como Python o Java.

El monitor `RUN` R0.11 solo contempla inicialmente `6000–6FFF`.
La utilidad cargada al overlay deberá poder invocarse mediante **un camino
supervisado distinto** (por ejemplo, una CALL a su punto de entrada);
no se debe relajar POKE/RUN en silencio para acomodarla.

## 7. Un ejercicio que podremos realizar en Aula-8

Imaginemos una imagen de cuatro bloques y que su bloque `0001` comienza:

```text
11 00 41 35 00 FF 02 [249 bytes adicionales]
```

El primer byte `11` sería `LDI` en la ISA Aula-8 candidata, `41` el
carácter A, `35 00 FF` la llamada a la tabla pública de `FW_PUTC`,
y `02` el RET. Cuando el cargador y la CPU existan:

1. `LOAD 0001 6000 01` traerá 256 bytes desde el bloque 0001.
2. `MEM 6000 07` comprobará los siete bytes útiles.
3. `RUN 6000` llamará al programa, imprimirá A y recuperará el prompt
   mediante RET si el firmware existe y la pila está equilibrada.

**La práctica es un caso de aceptación pendiente**, no una sesión real
grabada del simulador. `LOAD` permanece NO DISPONIBLE en la línea base.

## 8. Qué verifica esta R0.12

El [contrato JSON](CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.json)
se contrasta con el mapa de memoria, la tabla ROM R0.11 y el presupuesto
provisional. El [modelo de referencia en Python](../scripts/modelo_bloques_aula8_r0_12.py)
implementa **solo en el anfitrión** los ocho registros, READ/WRITE,
contadores, estados, límites y persistencia por bloques en archivos de
prueba temporales. El [verificador](../scripts/verificar_bloques_aula8_r0_12_borrador.py)
somete ese modelo a pruebas reproducibles, entre ellas:

- Leer un bloque conocido completo, comprobar `COUNT=0100` y estado DONE.
- Escribir otro, cerrar y reabrir una imagen para confirmar el contenido.
- Abortarlo a los 255 bytes y verificar que el bloque anterior no cambió.
- Rechazar sector inexistente, comandos inválidos, lectura/escritura en
  dirección incorrecta y cambio de bloque mientras BUSY.
- Probar fallo de persistencia inyectado **antes de reemplazar** la imagen,
  confirmando que se conserva el archivo anterior.
- Validar ventanas/alineación del futuro LOAD, límites de sector y que la
  transferencia incompleta nunca se trate como lista para RUN.

Estos tests sí ejecutan el **modelo Python** y manejan un archivo temporal,
pero no prueban un bloque transferido por el bus de Aula, persistencia de
hardware físico, firmware ROM o MiniC. Tampoco se crea un directorio.

## 9. Preguntas abiertas de R1/R5

- ¿Cómo se conectarán realmente los ocho registros al bus y a memorias?
- ¿Qué tiempo pasa entre COMMAND y DRQ? ¿Se necesitará timeout?
- ¿Qué sucede ante fallo eléctrico entre escrituras y sincronización?
- ¿Se añadirán CRC, versión/encabezado de imagen, directorio y formato
  ejecutable que identifique Aula-8/Aula-16?
- ¿Dónde situar en ROM las rutinas de lectura y escritura sin sobrepasar
  el presupuesto de 8192 B? **No asignar aún ranuras públicas.**
- ¿Cómo proteger el contexto del monitor y certificar carga y ejecución
  de herramientas nativas en el overlay?

Hasta entonces, tratar las direcciones de registros y el protocolo de R0.12
como **candidatos revisables**, nunca como una controladora construida.
