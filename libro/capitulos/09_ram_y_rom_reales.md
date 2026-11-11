# Capítulo 9. RAM y ROM reales

*Parte III · Memoria, buses y aritmética · Aula-Computadora*

En el capítulo 8 imaginamos que una dirección de dieciséis bits escogía un cajón y que, al leerlo, aparecía el byte guardado. Esa explicación era útil para entender los buses, pero dejaba una pregunta abierta: **¿qué circuito contiene miles de cajones y responde a una dirección?** Para una computadora educativa es posible construir algunas celdas con compuertas; fabricar a mano 32 768 bytes, con sus controles, sería una tarea desproporcionada. Por eso usaremos integrados de memoria como bloques reales y aprenderemos a leer sus conexiones.

Este capítulo distingue **SRAM, ROM y EEPROM**, sigue una lectura y una escritura en una SRAM comercial, calcula capacidades sin confundir bits con bytes y muestra cómo seleccionar chips mediante las líneas altas de dirección. Las configuraciones de Aula que se dibujan siguen siendo **ejemplos de arquitectura**, no una placa terminada ni un mapa físico definitivo.

## 1. Del registro a una memoria de muchas posiciones

Un registro de ocho bits permite conservar **un byte**. Si queremos conservar 32 768 bytes, necesitaríamos 32 768 grupos de ocho bits más mecanismos para elegir uno de ellos. Una memoria comercial reúne una matriz de celdas, decodificadores, circuitos de lectura, circuitos de escritura y pines para comunicarse con el exterior.

El fabricante acostumbra escribir la organización como `N × W`: **N posiciones** de **W bits cada una**. Por ejemplo, `32K × 8` significa que hay 32 × 1024 posiciones, cada una con ocho bits. La letra K de esa organización representa 1024 posiciones en este contexto; **32K × 8 son 32 KiB de datos, no 256 KiB**.

[[EQ:32 × 1 024 = 32 768 posiciones]]

[[EQ:32 768 posiciones × 8 bits = 262 144 bits = 32 768 bytes]]

Un circuito de `32K × 8` necesita **15 entradas de dirección** para elegir internamente una posición: desde `000 0000 0000 0000` hasta `111 1111 1111 1111`. Sus ocho pines de datos transportan el contenido de la posición elegida. No tiene 32 768 pines de dirección: el **decodificador interno** convierte las quince entradas en la selección necesaria.

[[EQ:2¹⁵ = 32 768;  A14…A0 son 15 entradas]]

En este punto no hemos decidido dónde se conectará el integrado dentro del espacio de direcciones de Aula-8. Sabemos solamente cuántas posiciones **contiene el chip**. Su ubicación entre `0x0000` y `0xFFFF` dependerá de las señales de selección que diseñemos fuera de él.

## 2. Cómo conserva un bit una celda SRAM

**SRAM** significa *Static Random-Access Memory*, memoria estática de acceso aleatorio. La expresión «acceso aleatorio» no significa que los datos se entreguen al azar: significa que podemos escoger una dirección directamente, sin recorrer las anteriores. La memoria **SRAM convencional es volátil**: conserva los datos mientras mantengamos su alimentación dentro de las condiciones requeridas, pero no debemos esperar que sobrevivan a una interrupción total de energía.

En una celda SRAM CMOS habitual de **seis transistores (6T)**, cuatro transistores forman dos inversores conectados en realimentación. Esa realimentación retiene uno de dos estados estables. Otros dos transistores de acceso, controlados por una **línea de palabra** (*word line*, WL), permiten conectar el estado a dos líneas de bit complementarias, `BL` y `BL̅`. La figura 1 resume esa idea. Se dibujan **bloques lógicos** y accesos, no las seis geometrías de transistores ni el circuito analógico de lectura.

[[FIG:c09_fig01_celda_sram_conceptual|Figura 1. Una celda SRAM mantiene su estado por realimentación y se comunica mediante una línea de palabra y dos líneas de bit.|Diagrama conceptual de una celda SRAM con dos inversores cruzados, dos accesos controlados por WL y líneas BL y BL complementaria; no representa el diseño transistor a transistor.]]

Cuando WL no habilita los accesos, la celda conserva su estado con alimentación adecuada. Durante lectura, la electrónica de la memoria prepara las líneas de bit y detecta pequeñas diferencias mediante circuitos de lectura. Durante escritura, sus circuitos fuerzan las condiciones que llevan la celda al nuevo estado. Los amplificadores, la organización de filas y columnas y los retardos no se reducen a dos interruptores ideales: forman parte del diseño real del chip.

Por eso sería inexacto afirmar que una celda SRAM es simplemente «un flip-flop D con reloj». Comparten la idea de **conservar información mediante realimentación**, pero el acceso y la estructura interna son diferentes. El registro del capítulo 7 estaba pensado para capturar un byte bajo una señal de carga; una SRAM contiene miles de posiciones seleccionables mediante direcciones.

## 3. Leer una hoja de datos de SRAM

Tomemos un modelo comercial como referencia: **AS6C62256**, una SRAM asíncrona de Alliance Memory organizada como `32K × 8`. La hoja de datos identifica quince entradas de dirección `A0…A14`, ocho pines bidireccionales `DQ0…DQ7` y tres controles activos en bajo: `CE#`, `OE#` y `WE#`. Los símbolos `#` y `_n` se usan aquí para expresar la misma idea de **activación con nivel bajo**; no son una resta ni una negación aritmética.

| Grupo de pines | Cantidad | Función |
|---|---|---|
| `A0…A14` | 15 | Dirección interna del byte |
| `DQ0…DQ7` | 8 | Datos de entrada o salida |
| `CE#`, `OE#`, `WE#` | 3 | Selección, habilitación de salida y escritura |
| `VCC`, `VSS` | 2 | Alimentación y referencia eléctrica |

[[FIG:c09_fig02_sram_pines|Figura 2. La SRAM de 32K por 8 recibe quince bits de dirección, intercambia ocho bits de datos y exige señales de control.|Bloque funcional de la AS6C62256 con A0 a A14, DQ0 a DQ7, CE#, OE#, WE#, alimentación y referencia; no es pinout físico de encapsulado.]]

Este es un **esquema funcional**: aún no asigna números a las patillas de un encapsulado de 28 pines. Si se arma un circuito, habrá que consultar el dibujo de pines del **encapsulado exacto** que se compre. La existencia de un mismo nombre de modelo tampoco permite cambiar sin revisión un DIP por un SOP o conectar dos memorias como si fueran piezas genéricas ideales.

La SRAM de este ejemplo admite una alimentación especificada de **2,7 a 5,5 V**; esa cifra pertenece a esta referencia y no autoriza a aplicar 5 V indiscriminadamente a otros chips. Las compatibilidades lógicas, límites de corriente, desacoplo, carga del bus y márgenes temporales deben comprobarse en el diseño de la placa.

## 4. Cuándo lee, escribe o desconecta sus pines

La hoja de datos de la AS6C62256 distingue cuatro modos básicos. Para leer la tabla, `0` es nivel bajo lógico, `1` nivel alto lógico y `X` significa «cualquiera de los dos» en esa condición. **X no es alta impedancia**: `Z` es el estado de una salida que ha dejado de conducir.

| Modo | `CE# OE# WE#` | Estado de `DQ0…DQ7` |
|---|---|---|
| Reposo/no seleccionado | `1 X X` | Salidas en Z |
| Salida deshabilitada | `0 1 1` | Salidas en Z |
| Lectura | `0 0 1` | Memoria entrega dato |
| Escritura | `0 X 0` | Memoria recibe dato |

Durante la **lectura**, primero deben estar válidas la dirección y las condiciones de control. La memoria pone el byte correspondiente en el bus una vez transcurridos los tiempos necesarios. Durante la **escritura**, el procesador conduce el dato y la memoria lo acepta según las ventanas de tiempo exigidas por el fabricante. Las señales del capítulo anterior `CS_n/RD_n/WR_n` eran un contrato didáctico general; **no se sustituyen literalmente por CE#/OE#/WE# sin diseñar el control**.

En una versión de la AS6C62256 se especifica un acceso de lectura de **55 ns** bajo sus condiciones de ensayo. No significa que cualquier computadora con ese chip complete todas sus instrucciones cada 55 ns: el sistema también debe incluir la propagación del decodificador, el asentamiento de la dirección, la captura de la CPU y los márgenes eléctricos. Para construir algo, habrá que leer los diagramas temporales de la hoja de datos, no extrapolar solo esa cifra.

Si `CE#=1`, el chip no participa en el intercambio y sus salidas de datos quedan en alta impedancia. Es lo que permite conectar varios dispositivos a un **bus compartido**, siempre que el diseño garantice que **no conduzca más de uno a la vez**. Dejar un chip en Z no hace que su contenido interno pase a cero.

## 5. Por qué SRAM y ROM no sirven para lo mismo

Una computadora necesita espacios para trabajar y espacios para **encontrar instrucciones de arranque al recibir alimentación**. La RAM resulta adecuada para datos temporales y programas en ejecución, pero su contenido no debe darse por preservado después de apagarla. Una **ROM** contiene información disponible para lectura sin requerir una carga previa cada vez que arranca la máquina.

El nombre ROM (*Read-Only Memory*) describe tradicionalmente una memoria de solo lectura durante el funcionamiento normal. Hay distintas tecnologías: una ROM de máscara se fabrica con datos fijados; algunas memorias se programan una vez; las **EEPROM** pueden borrarse y reprogramarse eléctricamente. **No es correcto afirmar que toda ROM es físicamente imposible de modificar.** Lo que importa para el arranque es que el contenido permanezca sin alimentación y pueda leerse cuando vuelve la energía.

| Tipo | Conserva sin energía | Escritura habitual |
|---|---|---|
| SRAM | No | Rápida y frecuente con alimentación |
| ROM de máscara | Sí | No se reprograma en uso |
| EEPROM | Sí | Eléctrica, con procedimiento y tiempo propios |

Para nuestro ejemplo utilizaremos una **EEPROM paralela AT28C64B** de Microchip, de `8K × 8`. Esto significa 8192 posiciones de byte, con **13 entradas de dirección** `A0…A12` y ocho líneas de datos. El integrado dispone de controles de selección, salida y escritura, pero no hay que confundir su ciclo de programación con una escritura SRAM ordinaria. La hoja de datos describe **escrituras internas que pueden tardar milisegundos**, protección de datos y comprobación del fin de la operación.

[[EQ:8 × 1 024 = 8 192 bytes = 8 KiB]]

[[EQ:2¹³ = 8 192 direcciones internas A12…A0]]

La AT28C64B de referencia requiere una alimentación de **5 V ±10 %**, mientras que la SRAM citada admite un rango distinto. Compartir ocho líneas de datos no garantiza por sí mismo compatibilidad eléctrica. Por ejemplo, determinadas variantes de AT28C64B documentan **hasta 10 ms** para completar una escritura interna de página. Su lectura puede ser mucho más rápida. Además existe una duración de vida especificada en ciclos de escritura: no deberíamos emplearla como si fuera un registro temporal que recibe escrituras ilimitadas. La programación de la EEPROM requiere un circuito, un procedimiento y una confirmación de finalización adecuados.

## 6. Ubicar dos memorias dentro de 64 KiB

Ahora reunimos el capítulo 8 y los chips de este capítulo. El procesador Aula-8 tiene un bus de **16 bits de dirección** (`A15…A0`), mientras que una SRAM `32K × 8` solo utiliza **15 bits internos**. Podemos usar el bit alto `A15` como parte de la lógica que decide **si participa esa SRAM**. De igual forma, una EEPROM `8K × 8` utiliza trece bits internos y necesitaría que la lógica superior examine los tres bits de mayor peso para asignarle una ventana sin solapamientos.

Consideremos un **mapa ilustrativo**, coherente con las capacidades planteadas para la máquina pero **no aprobado como mapa final**:

| Intervalo de CPU | Tamaño | Participante propuesto |
|---|---|---|
| `0x0000–0x7FFF` | 32 KiB | SRAM 32K × 8 |
| `0x8000–0xDFFF` | 24 KiB | Sin asignación aquí; futura E/S u otros |
| `0xE000–0xFFFF` | 8 KiB | EEPROM 8K × 8 usada como ROM |

[[EQ:32 KiB + 24 KiB + 8 KiB = 64 KiB]]

[[FIG:c09_fig03_mapa_64k_ejemplo|Figura 3. Un espacio de 64 KiB puede reservar una ventana para SRAM, otra para ROM y dejar posiciones para otros dispositivos.|Mapa de direcciones ilustrativo: 0000 a 7FFF SRAM 32 KiB, 8000 a DFFF sin asignar 24 KiB, E000 a FFFF EEPROM 8 KiB; no es un mapa Aula aprobado.]]

En este ejemplo, cuando `A15=0`, la CPU está dentro de `0x0000–0x7FFF`: la SRAM puede usar `A14…A0` como dirección interna. Para la ROM propuesta exigimos `A15=A14=A13=1`: eso selecciona `0xE000–0xFFFF`, y la EEPROM utiliza `A12…A0` para elegir el byte dentro de esa ventana.

[[EQ:SRAM seleccionada si A15 = 0;  ROM seleccionada si A15∧A14∧A13 = 1]]

Por ejemplo, al solicitar `0xE123`, los tres bits altos son `111`, así que seleccionamos la ventana de ROM. La dirección interna del chip es el desplazamiento respecto al inicio de esa ventana: `0xE123 − 0xE000 = 0x0123`. No entra una dirección de dieciséis bits entera por los trece pines de la EEPROM: **los tres bits altos se usaron para seleccionar el chip**.

[[EQ:0xE123 − 0xE000 = 0x0123 = 1×256 + 2×16 + 3 = 291]]

Este ejemplo deja 24 KiB sin asignar en el dibujo. **No significa** que sean automáticamente RAM libre ni que ya existan allí periféricos. La asignación de E/S y los detalles de protección deberán resolverse en el capítulo de arquitectura y arranque. La decodificación completa también debe considerar retardos y cambios de dirección antes de habilitar salidas reales.

## 7. Expandir profundidad y ampliar anchura no son lo mismo

Supongamos por un momento que queremos estudiar **dos SRAM de `32K × 8`**, sin reservar todavía ROM ni E/S. En paralelo, ambas pueden compartir las entradas de dirección `A14…A0` y las líneas bidireccionales `D7…D0`. Se usa `A15` para habilitar solamente la primera SRAM en la mitad baja y la segunda en la mitad alta. Obtenemos **64K × 8**: el doble de posiciones, pero sigue habiendo **ocho bits por posición**.

[[EQ:2 × (32K × 8) = 64K × 8 = 64 KiB de bytes]]

En cambio, si dos chips `32K × 8` se habilitaran juntos para que uno suministrara el byte bajo y otro el alto de una misma palabra, la organización conjunta sería **32K × 16**: el doble de anchura y el mismo número de posiciones de palabra. Eso **no** debe confundirse con el diseño byte-direccionable de Aula-16, que requerirá selección de bancos y reglas para accesos de uno o dos bytes. El capítulo 22 tratará esa variante con detalle.

[[EQ:2 × (32K × 8) en paralelo por anchura = 32K × 16 bits]]

[[FIG:c09_fig04_expansion_profundidad_anchura|Figura 4. Dos chips de 32K por 8 aumentan el número de posiciones si se seleccionan por separado, o la anchura si se usan juntos.|Comparación de dos SRAM 32K por 8: expansión de profundidad mediante A15 da 64K por 8; expansión de anchura con selección simultánea da 32K por 16. No es el cableado definitivo de Aula-16.]]

La primera disposición ocuparía **todo** el espacio de 64 KiB del ejemplo: si se implementara sin más, **no dejaría direcciones exclusivas para ROM o E/S mapeada**. Por eso la figura es una demostración de expansión, no una modificación silenciosa de la arquitectura ya acordada. En una microcomputadora completa debemos repartir las ventanas sin conflictos y documentar cómo se selecciona cada dispositivo.

## 8. Un ciclo de trabajo que podemos comprobar en papel

Pensemos de nuevo en `RAM[0x1200] = 0x41`. En el mapa ilustrativo, `0x1200` tiene `A15=0`; por ello se encuentra dentro de la ventana de SRAM. Sus quince bits inferiores corresponden a una dirección interna de la memoria comercial. Si solicitamos lectura con `CE#=0`, `OE#=0` y `WE#=1`, el chip podrá presentar `0x41` en `DQ7…DQ0` una vez cumplidos sus tiempos.

Si luego queremos guardar `0x53` en `0x1201`, se selecciona la misma SRAM, pero el procesador debe **conducir** el bus de datos y usar la condición de escritura `CE#=0`, `WE#=0` con los tiempos pertinentes. El fabricante permite que `OE#` sea indiferente en la fila de escritura de su tabla; esto no libera al diseñador de asegurar que los controladores externos no provoquen una contención. Al terminar correctamente, `RAM[0x1201]` devuelve `0x53`, mientras que `RAM[0x1200]` sigue en `0x41`.

Para leer una instrucción de arranque desde `0xE123` haríamos algo parecido con la **EEPROM**, pero aquí suponemos que **ya fue programada previamente**. No basta con instalar un chip vacío y esperar que «aparezca» un monitor. La CPU necesitará un circuito de reset, una dirección de comienzo documentada y un contenido de ROM válido. Todo eso se desarrollará más adelante.

El modelo de este capítulo es verificable mediante cálculos y tablas; **todavía no** responde preguntas decisivas de un prototipo: el nivel de alimentación de cada familia, el consumo, el condensador de desacoplo, la carga de salida, los tiempos de las compuertas de selección, los tiempos de establecimiento y mantenimiento, el estado al encender, y la seguridad al cambiar de un chip a otro. Antes de construir, esas respuestas deben salir de hojas de datos y de un esquema eléctrico concreto.

## Construimos Aula-8: un registro ya puede intercambiar bytes con RAM

La conexión del capítulo 8 adquiere ahora un destino realista. Un componente SRAM comercial ofrece numerosas posiciones de ocho bits; la **dirección** selecciona una de ellas y las señales de control deciden si se lee, escribe o libera el bus. La memoria propuesta para Aula-8 ocupa inicialmente `0x0000–0x7FFF` (32 KiB), mientras el firmware está previsto en `0xE000–0xFFFF`. Entre ambas zonas habrá regiones reservadas y periféricos, que no deben responder como si fueran RAM ordinaria.

Imagina que una operación lleva `0x3C` desde R0 a RAM en `0x1200`. El dato no abandona R0 por el mero hecho de escribirlo: la RAM obtiene **otra copia**. Si más tarde R0 cambia a `0xA5`, la celda `0x1200` puede seguir valiendo `0x3C` hasta otra escritura. Este contraste separa claramente **almacenamiento interno de un registro** y **posiciones direccionadas de memoria**. Aún faltan el decodificador final, las capacidades eléctricas, las habilitaciones y la temporización que harían construible la conexión física completa.

## Ejercicios del capítulo 9

Todos los ejercicios usan las capacidades y el mapa **ilustrativo** descritos arriba. Realiza las multiplicaciones, divisiones y conversiones a mano; no sustituyas una cantidad de bits por la misma cantidad de bytes.

**Ejercicio 1 — Organización comercial.** ¿Qué significa `32K × 8` y cuántos bytes totales guarda?

**Ejercicio 2 — Capacidad en bits.** Expresa la memoria anterior en bits y calcula cuántos KiB representa.

**Ejercicio 3 — Líneas internas.** ¿Por qué una SRAM `32K × 8` requiere quince bits de dirección interna y no dieciséis?

**Ejercicio 4 — Pines de control.** Para la AS6C62256, ¿qué valores de `CE#`, `OE#` y `WE#` permiten lectura?

**Ejercicio 5 — Dos estados distintos.** ¿Qué significan `X` y `Z` en una tabla de señales de un chip?

**Ejercicio 6 — EEPROM.** ¿Cuántos bytes guarda `8K × 8` y cuántas entradas de dirección interna necesita?

**Ejercicio 7 — Volatilidad.** ¿Por qué no debemos confiar en que una SRAM sin alimentación conserve un programa de arranque?

**Ejercicio 8 — Selección de SRAM.** Según el mapa de ejemplo, ¿qué chip responde a `0x1200` y qué bit alto decide esa selección?

**Ejercicio 9 — Offset de ROM.** Convierte la dirección `0xE123` en desplazamiento relativo a `0xE000` y expresa ese desplazamiento en decimal.

**Ejercicio 10 — Ventanas de memoria.** Suma 32 KiB de SRAM, 8 KiB de EEPROM y la región no asignada. ¿Cuántos KiB quedan sin asignar dentro de 64 KiB?

**Ejercicio 11 — Dos clases de expansión.** ¿Qué organización obtenemos al duplicar la profundidad de `32K × 8` y cuál al duplicar su anchura?

**Ejercicio 12 — Lectura y escritura.** Se parte de `RAM[0x1200]=0x41` y `RAM[0x1201]=0x00`. Tras escribir `0x53` en `0x1201`, ¿qué devolverán ambas posiciones? Expresa `0x53` como suma de potencias de dos y justifica por qué esta prueba no certifica un montaje físico.

## Solucionario del capítulo 9

**1.** `32K × 8` indica 32 × 1024 = **32 768 posiciones de ocho bits**. Cada posición contiene un byte: 32 768 bytes.

**2.** `32 768 × 8 = 262 144 bits`; al dividir por ocho se obtienen 32 768 bytes y al dividir por 1024, **32 KiB**.

**3.** `2¹⁵ = 32 768` posiciones internas. El bit adicional `A15` puede usarse externamente para decidir si participa el chip dentro del espacio de 16 bits de la CPU.

**4.** Lectura: `CE# = 0`, `OE# = 0`, `WE# = 1`, con dirección estable y tiempos cumplidos.

**5.** `X` significa que la condición acepta 0 o 1 sin cambiar el modo especificado. `Z` es una salida desconectada en alta impedancia. Ninguno debe confundirse con un bit de dato cero.

**6.** `8 × 1024 = 8192 bytes = 8 KiB`; `2¹³ = 8192`, así que hacen falta trece bits de dirección interna.

**7.** La SRAM convencional es volátil: la retención exige alimentación dentro de condiciones especificadas. Para arrancar desde código conservado sin energía necesitamos una memoria no volátil programada.

**8.** La SRAM de 32 KiB responde en la ventana ilustrativa `0x0000–0x7FFF`. Para `0x1200`, `A15=0`.

**9.** `0xE123 − 0xE000 = 0x0123`. Conversión: `1×256 + 2×16 + 3×1 = 256 + 32 + 3 = 291`.

**10.** `64 − 32 − 8 = 24 KiB`. Ese intervalo no es «RAM libre»: queda sin asignar en el mapa de enseñanza.

**11.** Por profundidad, `64K × 8` (65536 bytes). Por anchura, `32K × 16` (32768 posiciones de 16 bits). Las dos organizaciones suman la misma cantidad total de bits, pero se accede a ellas de distinta manera.

**12.** `0x1200 → 0x41` y `0x1201 → 0x53`. `0x53 = 0101 0011₂ = 0×128 + 1×64 + 0×32 + 1×16 + 0×8 + 0×4 + 1×2 + 1×1 = 83`. Es una operación lógica supuesta; no prueba niveles, retardos, escritura correcta del chip ni señales eléctricas.

## Para continuar

Conocemos ya la diferencia entre un registro, una celda, un chip comercial y un mapa de direcciones. La CPU puede seleccionar un lugar y recuperar un byte, pero todavía no **opera matemáticamente** con ese contenido. En el capítulo 10 construiremos el mecanismo de suma: primero dos bits y su acarreo, luego una suma de varios bits. Así llegaremos a una unidad aritmética sin recurrir a instrucciones que aún no hemos diseñado.

Fuentes primarias: Alliance Memory, *AS6C62256 32K × 8 Low Power CMOS SRAM*, https://www.alliancememory.com/wp-content/uploads/AS6C62256-23-March-2016-rev1.2.pdf; Microchip, *AT28C64B 64-Kbit (8K × 8) Industrial Parallel EEPROM*, https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/AT28C64B-64-Kbit-8Kx8-Parallel-EEPROM-with-Page-Write-and-Software-Data-Protection-DS20006432.pdf. Los esquemas del capítulo son originales y didácticos.
