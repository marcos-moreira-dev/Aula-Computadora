# Capítulo 22. Un bus externo de 16 bits

*Parte VI · Aula-16 y comparación · Aula-Computadora*

Imagina que el registro R0 de Aula-16 contiene `0x1234`. Queremos guardarlo en RAM y, más tarde, recuperarlo sin alterar un solo bit. El capítulo anterior explicó por qué una ALU de dieciséis posiciones puede manejar esa palabra. Ahora aparece otra pregunta: **si cada dirección identifica un byte, ¿cómo transporta la computadora dos bytes a la vez sin confundir sus posiciones?**

La solución didáctica será un **bus externo de datos de 16 bits, dividido en dos carriles de ocho**. Cada carril se conecta a un banco de memoria de ocho bits. Una dirección par puede seleccionar los dos bancos para transferir una palabra; una transferencia de un solo byte selecciona únicamente el banco que le corresponde. Estudiaremos las decisiones lógicas y sus pruebas. No dibujaremos todavía un esquemático físico definitivo, tiempos de reloj ni pines de una placa real.

## 1. Direcciones y datos responden preguntas distintas

Un bus de direcciones pregunta **dónde** se realiza una operación; un bus de datos transporta **qué valor** entra o sale. Aula-16 mantiene direcciones de dieciséis bits como Aula-8, pero duplica el ancho de su camino externo de datos. La unidad mínima direccionable continúa siendo **un byte**, no una palabra de dieciséis bits.

[[EQ:Cantidad de direcciones de byte = 2^16 = 65536]]

[[EQ:Espacio de direcciones = 65536 bytes = 64 × 1024 bytes = 64 KiB]]

El espacio de direcciones no equivale a memoria RAM instalada. Algunos intervalos se reservan a ROM, periféricos o huecos. Una máquina con bus de dieciséis bits **no obtiene automáticamente el doble de RAM**. La anchura del camino y la capacidad del dispositivo son dimensiones independientes.

| Propiedad | Aula-8 | Aula-16 |
| --- | --- | --- |
| Bus externo de datos | 8 bits | 16 bits |
| Bus de direcciones | 16 bits | 16 bits |
| Dirección mínima | 1 byte | 1 byte |
| Transferencia natural | Byte | Palabra alineada de 2 bytes |
| Espacio direccionable | 64 KiB | 64 KiB |

## 2. Dos memorias de ocho bits forman el camino de dieciséis

Dividamos la memoria de datos en **banco bajo** y **banco alto**. El bajo entrega o recibe `D7..D0`; el alto, `D15..D8`. La dirección de byte `A0` determina si el destino tiene paridad par o impar. En el espacio **lógico** de 64 KiB, `A15..A1` identifica la pareja de direcciones de byte. Sin embargo, los chips de la **RAM inicial de 32 KiB** solo necesitan 14 bits para elegir una de sus 16384 filas: **`A14..A1`**. `A15` participa en la selección de la región RAM (0000–7FFF), no se conecta como un decimoquinto bit de fila al chip. Esta distinción entre dirección de CPU, decodificación de región y dirección interna de banco evita imaginar chips más grandes que los instalados.

[[EQ:Fila = dirección_de_byte >> 1]]

[[EQ:Banco = dirección_de_byte AND 1]]

En el modelo lógico, la dirección `0x2000` accede a la fila `0x1000` del banco bajo; `0x2001` accede a **la misma fila** del banco alto. Una palabra alineada que comienza en `0x2000` utiliza simultáneamente las dos posiciones. La memoria sigue siendo direccionable byte a byte porque ambas posiciones **tienen direcciones diferentes**.

[[FIG:c22_fig01_bancos_y_carriles|Figura 1. Dos bancos de ocho bits comparten fila, pero tienen líneas de datos distintas.|El banco de direcciones pares usa D7 a D0 y el de impares D15 a D8; en la RAM 0000–7FFF, A14 a A1 seleccionan la fila y A15 decodifica la región. A0 participa en la selección de carril, no agrega memoria.]]

La figura anterior agrupa ocho conductores en un trazo grueso por comodidad. Pero un bus de dieciséis bits **no consta de dos cables**: son dieciséis líneas independientes que deben conservar su correspondencia entre CPU y memoria. Vamos a desplegarlas una a una. Las ocho superiores (`D15…D8`) llegan al banco alto; las ocho inferiores (`D7…D0`), al banco bajo. Así se ve qué significa realmente transportar una palabra en paralelo.

[[FIG:c28c_aula16_dieciséis_carriles|Lámina complementaria 22A. Las dieciséis líneas de datos de Aula-16, agrupadas en dos bancos de ocho bits.|Esquema funcional con dieciséis conductores D15 a D0 identificados por separado. D15 a D8 llegan al banco alto y D7 a D0 al banco bajo. Las direcciones A14 a A1 determinan una fila de la RAM inicial de 32 KiB; A15 selecciona región y A0 selecciona el carril del byte.]]

No confundas este despliegue de señales con un plano para soldar: aún faltan decodificadores, habilitación de cada banco, adaptación de lecturas de byte y los tiempos reales de los chips. Tampoco quiere decir que las dieciséis líneas **siempre** transporten datos válidos: en una lectura de byte solo participa el carril que corresponde a esa dirección. La lámina muestra las conexiones lógicas que deberemos respetar al diseñar el circuito verificable.

Para construir 64 KiB de **RAM total** con este esquema serían necesarios 32768 bytes por banco. Si la máquina solo instala 32 KiB de RAM en total, cada banco contendría 16384 bytes para la región RAM elegida. Esos números son capacidades del ejemplo lógico: la distribución final entre chips y regiones no está certificada.

[[EQ:Capacidad total de dos bancos de 16 KiB = 2 × 16384 = 32768 bytes]]

## 3. Qué significa que una dirección sea par o impar

Un entero es par si su bit menos significativo vale cero. Así, `0x2000` es par y `0x2001` es impar; ambos apuntan a **bytes**, no a tipos de datos diferentes. Para una operación de **lectura de byte**, el sistema habilita el carril que contiene ese byte. El procesador recibe el valor en la parte útil de ocho bits de su destino, aunque haya llegado por las líneas superiores del bus físico.

| Operación lógica | Dirección inicial | Banco bajo | Banco alto | Resultado |
| --- | --- | --- | --- | --- |
| Leer un byte par | `2000` | Activo | Inactivo | Byte de `2000` |
| Leer un byte impar | `2001` | Inactivo | Activo | Byte de `2001` |
| Leer palabra par | `2000` | Activo | Activo | Bytes `2000` y `2001` |
| Leer palabra impar | `2001` | **Error V1** | **Error V1** | Sin transferencia de palabra |

Una implementación necesita señales de habilitación y lógica de encaminamiento del byte alto al registro destino. Para razonar llamaremos `SEL_BAJO` y `SEL_ALTO` a dos **salidas abstractas** del controlador, sin fijar si serán activas en alto o en bajo. El histórico Intel 8086 también utilizó bancos de bytes y señales de habilitación, pero **Aula-16 es un diseño propio** y no copia su mapa de direcciones ni su repertorio de instrucciones.

[[EQ:0x2000 AND 1 = 0; 0x2001 AND 1 = 1]]

## 4. Little-endian: el orden se ve en la memoria, no en el número

La palabra `0x1234` contiene el byte alto `0x12` y el bajo `0x34`. La convención **little-endian** coloca el byte menos significativo en la dirección menor. Si el destino empieza en `0x2000`, el contenido de memoria esperado es `RAM[2000]=34` y `RAM[2001]=12`. El registro continúa conteniendo el número `0x1234`: **little-endian no invierte los bits dentro de cada byte**.

[[EQ:0x1234 = 0x34 + (0x12 × 256)]]

[[EQ:RAM[0x2000] = 0x34; RAM[0x2001] = 0x12]]

[[FIG:c22_fig02_palabra_y_little_endian|Figura 2. Una palabra de registro llega a dos direcciones de byte y se reconstruye sin pérdida.|El valor 1234 se descompone en bajo 34 en 2000 y alto 12 en 2001; la lectura recompone 34 más 12 por 256. Los bytes del número no se invierten internamente.]]

### Ejemplo completo de escritura y lectura

1. En el modelo, R0 vale `0x1234` y la dirección efectiva vale `0x2000`.
2. El controlador verifica que la operación sea de palabra, que `0x2000` sea par y que las dos posiciones correspondan a una región de RAM válida.
3. Presenta `0x34` por `D7..D0` al banco bajo y `0x12` por `D15..D8` al banco alto; habilita la escritura de ambos bancos.
4. Una lectura posterior de palabra desde la misma dirección reúne el byte del banco bajo y el del alto.
5. El registro destino recupera `0x1234`; la memoria conserva exactamente las dos celdas escritas.

No hemos contado **ciclos de reloj**: el número de transferencias lógicas no determina los tiempos de espera, la duración de las señales ni el número de microinstrucciones. Eso pertenece al diseño y verificación electrónica que aún falta.

## 5. Acceder al segundo byte sin destruir el primero

Supón que la palabra `0x1234` ya está en `2000–2001` y quieres modificar **solo** el byte de la dirección impar `0x2001` para escribir `0xAB`. Un controlador correcto debe habilitar **únicamente el banco alto**. El banco bajo no puede recibir una señal de escritura accidental; su `0x34` permanece intacto.

[[EQ:Escritura_byte(0x2001, 0xAB) → RAM[2000]=0x34, RAM[2001]=0xAB]]

[[EQ:Lectura_palabra(0x2000) = 0xAB34]]

La dificultad no es aritmética: es **aislamiento de carriles y propiedad del bus**. En una lectura, el dispositivo seleccionado conduce su parte autorizada del bus; en una escritura, conduce el procesador o el controlador de origen. Dos dispositivos no deben forzar valores opuestos sobre las mismas líneas eléctricas. Para diseñar el circuito definitivo habrá que indicar estados de alta impedancia, habilitaciones, tiempos y transceptores con hojas de datos, no solo con flechas.

[[FIG:c22_fig03_matriz_operaciones|Figura 3. La matriz de operaciones deja claro qué carril trabaja en cada acceso.|Para lectura o escritura de byte par, carril bajo; byte impar, carril alto; palabra en dirección par, ambos. Palabra en dirección impar, error en Aula-16 V1.]]

## 6. Alineación y bordes del espacio direccionable

Dos bytes consecutivos forman una palabra válida siempre que ambos pertenezcan a la misma operación permitida. En Aula-16 V1 solo aceptaremos **palabras con dirección inicial par**. El último comienzo alineado posible es `0xFFFE`, porque `0xFFFE+1=0xFFFF`. Eso no significa que esa dirección esté necesariamente asociada a RAM: puede corresponder a ROM o a una zona restringida. El controlador debe verificar **alineación, región y permisos**.

En la primera versión, una dirección de inicio de palabra es **válida para una transferencia alineada** cuando el bit menos significativo de esa dirección es cero. Dicho de otra forma: `(dirección AND 1) = 0`. Esto solo comprueba la alineación; **los permisos y la región de memoria son condiciones adicionales**.

[[EQ:Última pareja del espacio: 0xFFFE y 0xFFFF]]

| Intento | ¿Alineado? | ¿Acceso autorizado? |
| --- | --- | --- |
| Palabra en `0x2000` sobre RAM | Sí | Sí, en el ejemplo RAM |
| Byte en `0x2001` sobre RAM | No aplica a byte | Sí |
| Palabra en `0x2001` | No | No en V1 |
| Palabra en `0xFFFF` | No | No en V1 y excede la pareja |
| Palabra en `0xFFFE` | Sí | Depende del mapa y los permisos |

En una máquina histórica como el 8086 existía tratamiento para ciertas palabras no alineadas, a costa de más accesos de bus. **No vamos a atribuir esa capacidad a Aula-16**: la versión didáctica reporta error en lugar de intentar dos transferencias. Así podemos aprender primero un contrato verificable y añadir opciones solo con diseño y pruebas nuevos.

## 7. ¿Y qué ocurre con ROM y registros de periféricos?

Los dos bancos explican cómo transportar datos en una región de memoria que admite ese acceso. No implican que **todos los dispositivos** tengan que exponer dos bytes a la vez. Por ejemplo, el terminal didáctico ya dispone de `DATA=C000` y `STATUS=C002` como registros de **ocho bits**; el controlador de bloques y el de vídeo también asignan registros pares de ocho bits.

En Aula-16 los accesos a esos registros serán operaciones **de byte**. Una lectura de palabra desde `C020` **no** debe combinar accidentalmente dos registros MMIO. El hecho de que `C020` sea par no lo convierte en una palabra de dieciséis bits. Igualmente, la ROM de glifos y la VRAM interna del controlador de pantalla se direccionan **mediante su propio mecanismo**, distinto de las direcciones de CPU.

| Nivel | Ejemplo | ¿Qué selecciona? |
| --- | --- | --- |
| Dirección efectiva de CPU | `0xC028` | Registro `VRAM_DATA` de 8 bits |
| Registro puntero de vídeo | `0x0002` | Byte 2 de una VRAM separada |
| Posición visual | `(x,y)` | Píxel calculado según modo y bpp |

[[EQ:Dirección efectiva de CPU ≠ desplazamiento interno de VRAM]]

**Modos de direccionamiento** tampoco significan «modo texto o modo gráfico». Una ISA puede calcular una dirección absoluta o `X+desplazamiento`, y el decodificador decide a qué periférico conduce. El controlador de pantalla interpreta después su puntero interno. Son tres responsabilidades diferentes; no hacen falta instrucciones gráficas especiales de CPU para explicar esta cadena.

## 8. Fallos diagnósticos que conviene provocar en el modelo

La enseñanza mejora cuando podemos anticipar **qué sale mal**. Si un programa guarda `0x1234` y la lectura obtiene `0x3412`, probablemente intercambió el orden de los bytes. Si una escritura de byte alto altera `RAM[2000]`, la habilitación de bancos es defectuosa. Si una palabra impar aparentemente funciona sin un mecanismo definido, el modelo está escondiendo una segunda transferencia o ignorando un error. Si `C020` se trata como dos registros unidos, el decodificador está confundiendo dispositivos de ocho bits con RAM de palabras.

[[FIG:c22_fig04_casos_fallo_bus|Figura 4. Cuatro síntomas diferentes permiten ubicar el defecto antes de construir el circuito.|Byte swap, escritura cruzada de carriles, palabra impar admitida y acceso de palabra a MMIO: cada error pertenece a una regla distinta.]]

Nuestras primeras pruebas serán **cálculos y simulaciones de transacciones en el equipo anfitrión**, no capturas de un analizador lógico. Las mediciones de un montaje real requerirían seleccionar chips, alimentación, reloj, control de habilitación y una placa.

## 9. Qué aprendimos y qué sigue

Un bus externo de dieciséis bits no obliga a abandonar la memoria por bytes. Su ventaja aparece cuando **dos bancos independientes cooperan** en una palabra alineada. El precio didáctico es la lógica que selecciona carriles, respeta permisos y mantiene el orden de los bytes. Ahora sí podemos pasar de dibujar el bus a preguntarnos cómo **un programa** sabe cuándo leer un byte, cuándo leer una palabra y cuándo llamar a una función. Ese es el tema del capítulo 23.

[[PAGEBREAK]]
## Construimos Aula-16: los dos carriles deben estar dibujados

El bus externo de Aula-16 contiene `D15…D0`. Para una palabra alineada, sus dieciséis líneas pueden participar en una misma transferencia, mientras el sistema selecciona los dos bancos de memoria de ocho bits. Si almacenamos `0x1234` desde `0x2000`, el banco bajo recibe `0x34` en la dirección par y el banco alto `0x12` en la dirección impar consecutiva. Esa diferencia **no desaparece** por presentar la RAM como un único rectángulo.

[[FIG:c22_fig05_dos_bancos_aula16|Figura 5. Aula-16 conecta un bus de datos externo de 16 bits a dos bancos de ocho bits y distingue direcciones pares e impares.|CPU de 16 bits con D15 a D0, banco bajo D7 a D0 con 0x34 en 0x2000 y banco alto D15 a D8 con 0x12 en 0x2001.]]

Para escribir o leer solamente el byte de `0x2001`, el diseño necesitará activar **el banco alto** y resolver la transferencia de ese carril hacia la parte de registro donde el software espera el byte. Esto exige decodificación y *steering* bidireccional, que la figura no reemplaza por arte de magia. Para la primera versión se rechazan palabras iniciadas en dirección impar; una palabra alineada puede usar ambos bancos. Los tiempos y patillas de una SRAM específica quedan pendientes de una implementación eléctrica seleccionada.

## Ejercicios del capítulo 22

**Ejercicio 1 — Espacio.** ¿Cuántos bytes se direccionan con 16 bits de dirección y un bus de datos de 16?

**Ejercicio 2 — Banco.** ¿A qué banco pertenece la dirección `0x2001` y qué fila selecciona?

**Ejercicio 3 — Banco par.** Calcula fila y banco de `0x2A10`.

**Ejercicio 4 — Capacidad.** ¿Cuántos bytes suma un par de bancos de `16 KiB × 8 bits` cada uno?

**Ejercicio 5 — Endian.** Descompón `0xBEEF` en dos bytes little-endian desde `0x2400`.

**Ejercicio 6 — Reconstrucción.** Si `RAM[3000]=0xCD` y `RAM[3001]=0xAB`, ¿qué palabra se lee desde `3000`?

**Ejercicio 7 — Escritura parcial.** Desde la palabra `0x1234` en `2000–2001`, se escribe byte `0xAB` en `2001`. ¿Qué palabra queda?

**Ejercicio 8 — Impar.** ¿Por qué no admitimos una lectura de palabra desde `0x2001` en V1?

**Ejercicio 9 — Borde.** ¿Puede una palabra alineada comenzar en `0xFFFE`? ¿Es seguro afirmar que allí hay RAM?

**Ejercicio 10 — MMIO.** ¿Sería correcto leer `VIDEO_MODE` en `C020` como palabra de 16 bits?

**Ejercicio 11 — Diagnóstico.** Si `0x1234` vuelve como `0x3412`, señala la hipótesis de fallo más probable.

**Ejercicio 12 — Niveles.** Explica por qué la dirección absoluta de CPU `C028`, el offset VRAM `0002` y el píxel `(8,0)` no son tres modos de direccionamiento de la CPU.

[[PAGEBREAK]]
## Solucionario del capítulo 22

**1.** `2^16=65536 bytes=64 KiB` de **espacio direccionable**, no necesariamente de RAM instalada.

**2.** Dirección impar, banco alto, fila `0x2001 >> 1 = 0x1000`.

**3.** Banco bajo (`0x2A10 AND 1=0`), fila `0x1508`.

**4.** `2×16384=32768 bytes=32 KiB` de RAM total.

**5.** `RAM[2400]=EF` y `RAM[2401]=BE`.

**6.** `0xABCD`.

**7.** `0xAB34`; el bajo `0x34` no puede cambiar.

**8.** El contrato Aula-16 V1 **rechaza palabras no alineadas**; no hay mecanismo aprobado para dividirlas en dos accesos.

**9.** Sí, es el último comienzo par válido del espacio; no, la autorización depende de región/permiso.

**10.** No: el registro `C020` es de **ocho bits** y exige acceso byte, aunque su dirección sea par.

**11.** Inversión de bytes al escribir o reconstruir; revisar little-endian y cableado lógico de carriles.

**12.** `C028` es dirección efectiva **de CPU**, `0002` es un puntero **del periférico** y `(8,0)` es una coordenada **visual**. El modo de direccionamiento de CPU calcula únicamente su propia dirección efectiva.

## Para continuar

El capítulo 23 utilizará estos contratos para escribir **programas de palabra**, sumar arreglos y razonar sobre un convenio de llamadas propio de Aula-16. Su código se presentará como **ensamblador conceptual sin opcodes inventados**, hasta aprobar una ISA y construir herramientas de ejecución.
