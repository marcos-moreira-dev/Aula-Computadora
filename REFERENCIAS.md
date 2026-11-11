# Fuentes y comprobaciones

## Vídeo histórico, modos de texto/gráficos y caracteres (contrato V1)

- **Commodore, *Commodore 64 Programmer's Reference Guide*, capítulo «Programming Graphics»**, manual del fabricante: https://www.commodore.ca/manuals/c64_programmers_reference/c64-programmers_reference_guide-03-programming_graphics.pdf — documenta ROM de caracteres, código de pantalla, memoria de color, bitmap y el VIC-II que selecciona modos; es **referencia histórica**, no arquitectura clonada por Aula.
- **Texas Instruments, *TMS9918A/TMS9928A/TMS9929A Video Display Processors Data Manual* (1982)**, manual técnico original: https://computers.baffa.tec.br/pages/datasheet/TMS9918A_TMS9928A_TMS9929A_Video_Display_Processors_Data_Manual_Nov82.pdf — ejemplo de controlador independiente con registros, VRAM, planos y modos de texto/gráficos. Aula adopta **sus propios registros y dimensiones**, no equivalencia eléctrica con ese chip.
- **Unicode Consortium, *FAQ — UTF-8, UTF-16, UTF-32 & BOM***: https://www.unicode.org/faq/utf_bom.html — UTF-8 codifica texto Unicode en bytes; una ROM de 256 glifos con tabla explícita **no** necesita decodificar UTF-8 por píxel.
- **Unicode Consortium, *Unicode Technical Report #17 — Character Encoding Model***: https://www.unicode.org/reports/tr17/ — distingue caracteres y glifos; para el libro no se debe equiparar toda secuencia Unicode a un solo mapa de 8×8.
- **W3C, *SVG 2 — Paths***: https://www.w3.org/TR/SVG/paths.html — especifica segmentos cúbicos y cuadráticos de Bézier para representar contornos geométricos. La A del interludio es un diseño original; SVG es la **herramienta de dibujo**, no un supuesto formato de ROM de Aula.
- **Microsoft Learn, *Introducing DirectWrite***: https://learn.microsoft.com/en-us/windows/win32/directwrite/introducing-directwrite — expone conversión entre contornos y mapas de bits y colocación de glifos; **no** se implementa DirectWrite en el controlador Aula.
- **Microsoft Learn, *Desktop Window Manager — Overview***: https://learn.microsoft.com/en-us/windows/win32/dwm/dwm-overview — documenta que la composición del escritorio apareció en Windows Vista. [Compatibilidad de DWM](https://learn.microsoft.com/en-us/windows/compatibility/desktop-window-manager-is-always-on) distingue su activación con Aero en Windows Vista/7 y la política posterior. Windows XP y 7 se usan solo como **contexto didáctico**, no como arquitecturas idénticas.
- El [contrato Aula V1](simulador-javafx/CONTRATO_VIDEO_AULA_V1.md) es **diseño original de proyecto**, con salida de vídeo **lógica, sin señal física y sin ejecución de firmware**. Las cifras 512/8192/2048 bytes se verifican matemáticamente; no deben atribuirse a una hoja de datos comercial.
- El [interludio P23V](libro/capitulos/23v_de_mapas_de_caracteres_a_escritorio_grafico.md) y el [capítulo 24](libro/capitulos/24_una_computadora_que_podemos_explicar.md) incorporan **once esquemas SVG/PNG originales** generados por código, 26 expresiones OMML y 24 ejercicios. Su [verificador](scripts/verificar_entrega_c24.py) contrasta 65536 coordenadas de mapas mono y 2bpp más documentos, pero **no simula los protocolos físicos VGA ni certifica CPU**.

## Fuentes internas y fidelidad de los capítulos 18 a 21

- Capítulo 18: `simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.json` establece la tabla pública FF00/FF04/FF08/FF0C; `simulador-javafx/ISA_AULA8_CANDIDATA.json` proporciona la codificación propuesta. La terminal y sus direcciones son un modelo didáctico, **no un periférico implementado**. `scripts/verificar_capitulo_18.py` comprueba bytes y archivos editoriales, no una CPU.
- Capítulo 19: `simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.json` define registros, estados y bloques crudos; `simulador-javafx/EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.json` y `simulador-javafx/LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.json` distinguen cargador crudo y formato AEX1. Los ensayos utilizan una **imagen temporal en el anfitrión**; no garantizan persistencia de un chip físico ni ejecución.
- Capítulo 20: `simulador-javafx/ISA_AULA8_CANDIDATA.json` es el contrato candidato. `scripts/ensamblador_dos_pasadas_aula8_educativo.py`, `libro/programas/c20_*.asm` y `scripts/verificar_capitulo_20.py` son referencias **en el anfitrión**, con dos pasadas y modelo matemático contrastado con `math.gcd`. No hay ejecución nativa.
- Capítulo 21: `ARQUITECTURA.md`, `ESTADO_PORTABLE.json` y `scripts/verificar_capitulo_21.py` sustentan el contraste de palabras, sumas, flags, byte-addressing y little-endian. Los dos bancos de memoria se desarrollarán en el capítulo 22; todavía **no** se ha materializado un bus externo ni se han elegido chips físicos Aula-16.
- Las ocho figuras de ambos capítulos son originales. `scripts/generar_diagramas_tecnicos_aula8.py` verifica direcciones contra las especificaciones antes de exportar SVG y PNG. [La guía de fidelidad](libro/GUIA_DE_FIDELIDAD_DE_FIGURAS.md) distingue diagramas funcionales de netlists y pruebas eléctricas. Scott y *Una Historia en 8 Bits* orientan la didáctica, sin copiar sus diagramas.

## Fuentes y límites de los capítulos 22 y 23

- **Intel, *The 8086 Family User's Manual* (1979)**: https://bitsavers.org/components/intel/8086/9800722-03_The_8086_Family_Users_Manual_Oct79.pdf — antecedente histórico primario de organización en bancos de 8 bits, interfaz externa de 16 bits, bytes en direcciones pares/impares y little-endian. **Aula-16 no clona el 8086:** mantiene 16 líneas de dirección, memoria y alineación propias, sin adoptar BHE# ni ciclos desalineados del Intel.
- **GNU Binutils, documentación de `as`**: https://sourceware.org/binutils/docs/as/ — fuente primaria para el concepto de ensamblado, símbolos y traducción de instrucciones una vez exista una ISA. **El capítulo 23 no reclama que GNU `as` ensamble Aula-16.**
- Fuente interna: `ARQUITECTURA.md`, `simulador-javafx/CONTRATO_VIDEO_AULA_V1.md`, `ESTADO_PORTABLE.json` y los verificadores `scripts/verificar_capitulo_22.py` y `scripts/verificar_capitulo_23.py`. Los esquemas reproducibles en SVG/PNG proceden de `scripts/generar_diagramas_capitulos_22_23.py`; son modelos originales funcionales, no netlists ni mediciones de temporización. Los cálculos de Euclides y Fibonacci son referencias matemáticas ejecutadas en el anfitrión; ninguna CPU Aula-16 ejecutó binarios.

## Material aportado por el usuario

1. **J. Clark Scott, *But How Do It Know? The Basic Principles of Computers for Everyone*.** Referencia conceptual para motivar el estudio de CPU/memoria desde los fundamentos. **No se redistribuye, traduce literalmente ni reproduce en este repositorio.**
2. **Fernando Sandoval Galárraga y Marcos Alejandro Moreira Merino, *Una Historia en 8 Bits*.** Manuscrito inacabado de 843 páginas, coautoría. Interesan especialmente capítulos de numeración, compuertas, el sumador, diagramas de CPU, el programa LOAD/ADD/NOT/STORE, teletipos, firmware y apuntes de microcomputadoras. Se aprovecharán ideas pedagógicas, no se copiarán figuras o pasajes sin resolver derechos.
3. **Estándar editorial para artefactos didácticos, versión 2.0 (4 de noviembre de 2026).** 28 páginas. Contrato del documento libro, salida Word/PDF y perfil condicionado DocuPodcast.

Los tres PDF fueron adjuntados para análisis; **no se incluyen automáticamente** en una distribución GitHub.

## Manuales originales y hojas de datos

### Fuentes de electricidad para el capítulo 1

- NIST, *Guide for the Use of the International System of Units*, SP 811: https://physics.nist.gov/cuu/pdf/sp811.pdf — notación de unidades y prefijos.
- SparkFun, *Resistors*, sección LED Current Limiting: https://learn.sparkfun.com/tutorials/resistors — resistencia en serie y cálculo de corriente aproximada en LED.
- Fluke, *87 True RMS Multimeter — Users Manual*: https://media.fluke.com/e76c91b6-f364-48ea-9c09-b10800bed531_original%20file.pdf — conexión en paralelo para tensión y en serie para corriente.
- El LED de 2,0 V del capítulo 1 es una **hipótesis didáctica**, no un modelo comprado. **Falta** seleccionar y citar hoja de datos comercial antes de convertir la práctica en una lista definitiva de compra o en validación física.

### Fuentes primarias para el capítulo 2

- onsemi, *2N3904 NPN General-Purpose Amplifier*, hoja de datos: https://www.onsemi.com/download/data-sheet/pdf/2n3904-d.pdf — terminales de la versión TO-92, límites absolutos y VCE(sat) ≤ 0,2 V a IC = 10 mA / IB = 1 mA. La aproximación VBE = 0,7 V y la caída de LED = 2 V **no son mediciones**.
- ROHM, *NPN Transistor: Low-Side Switch Fundamentals*: https://techweb.rohm.com/product/transistors-diodes/transistors/27354/ — polarización de la base, saturación y ramas de control y carga.
- Texas Instruments, nota técnica sobre BJT en saturación: https://www.ti.com/document-viewer/lit/html/SSZTBM9/GUID-E6584C27-2056-49A5-8305-1C98C74F6175 — distinción de conmutación y condiciones de saturación.
- Los diagramas del capítulo 2 son **ilustraciones originales conceptuales**, no la certificación de un esquema o una placa montada. Si se realiza la práctica, comprobar hoja de datos del fabricante concreto y polaridad real del LED.

### Fuente primaria para el capítulo 3

- Texas Instruments, *SN74HCT00 Quadruple 2-Input Positive-NAND Gates*, hoja de datos: https://www.ti.com/lit/ds/symlink/sn74hct00.pdf — alimentación recomendada 4,5–5,5 V, entradas VIL ≤ 0,8 V / VIH ≥ 2,0 V, capacidad de salida ±4 mA a 5 V y pinout de la variante SN74HCT00N PDIP-14. Especificaciones atribuibles a esa familia y condiciones concretas, **no** al transistor del capítulo 2 ni a cualquier NAND de otro fabricante.
- El LED rojo de 2,0 V y VOL de 0,3 V usados para dimensionar 1 kΩ son **suposiciones numéricas explícitas**, no valores medidos ni garantizados para cualquier carga. Los dibujos del capítulo 3 son originales; la tabla de verdad ideal se verifica matemáticamente, pero el montaje práctico está pendiente.

### Fuentes y alcance del capítulo 4

- Texas Instruments, *SN74HCT00 Quadruple 2-Input Positive-NAND Gates*: https://www.ti.com/lit/ds/symlink/sn74hct00.pdf — referencia física para indicar que un integrado contiene cuatro NAND de dos entradas. La síntesis XOR se demuestra independientemente con su **tabla de verdad**, sin afirmar que se haya cableado un chip real.
- Las tablas OR/NOR/XOR, la expresión XOR de suma de productos y la identidad `(A AND B) OR (A AND NOT B) = A` son demostraciones elementales del álgebra booleana, comprobadas de forma exhaustiva para sus entradas. No constituyen mediciones ni caracterización de retardos.
- El [puente sobre bits, representación y significado](libro/PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md) es **plan didáctico no desarrollado**. Usará ASCII, complemento a dos, ISA y tipos de datos como ejemplos con convenios explícitos; cualquier cita normativa se incorporará al redactarlo.

### Fuentes y alcance del capítulo 5

- Texas Instruments, *SNx4HCT00 Quadruple 2-Input Positive-NAND Gates*: https://www.ti.com/lit/ds/symlink/sn74hct00.pdf — pines del SN74HCT00N en encapsulado PDIP-14, cuatro NAND, tensión de alimentación recomendada, niveles definidos para entradas no utilizadas y desacoplo sugerido de 0,1 µF.
- Texas Instruments, *Artículo técnico SSZTCV9 sobre latches SR*: https://www.ti.com/document-viewer/lit/html/SSZTCV9 — referencia conceptual de controles SET/RESET y realimentación. El capítulo desarrolla específicamente dos NAND cruzadas sin prioridad.
- Las ecuaciones de **dos NAND cruzadas** se comprueban exhaustivamente para los estados estables de sus dos salidas. No se probaron tiempos de transición, encendido, liberación simultánea ni metastabilidad de un circuito físico; los dibujos son originales y no sustituyen esquemas de montaje certificados.

### Fuentes y alcance del capítulo 6

- Texas Instruments, *SNx4HC373 Octal Transparent D-Type Latches With 3-State Outputs*: https://www.ti.com/lit/ds/symlink/sn74hc373.pdf — habilitación LE alta permite que Q siga D; LE baja conserva el estado. OE_n controla la conexión triestado de la salida **sin borrar el estado interno**.
- Texas Instruments, *SNx4HC74 Dual D-Type Positive-Edge-Triggered Flip-Flops With Clear and Preset*: https://www.ti.com/lit/ds/symlink/sn74hc74.pdf — dos flip-flops D de flanco ascendente, entradas asíncronas de preset/clear; requisitos de temporización que no deben inventarse ni extrapolarse.
- El capítulo presenta una red booleana ideal que transforma D/LE en SET/RESET activos en bajo y verifica secuencias de estados. **No** se midieron setup/hold, clock-to-Q, metastabilidad, funcionamiento de pulsadores ni un montaje físico. Los cuatro diagramas son originales.

### Fuentes y alcance del capítulo 7

- Texas Instruments, *SNx4HC377 Octal D-Type Flip-Flops With Clock Enable*: https://www.ti.com/lit/ds/symlink/sn74hc377.pdf — banco de ocho flip-flops de flanco ascendente con habilitación `CLKEN` activa en bajo; no atribuirle un reset común ni salida triestado que no forman parte de su contrato.
- Texas Instruments, *SNx4HC245 Octal Bus Transceivers With 3-State Outputs*: https://www.ti.com/lit/ds/symlink/sn74hc245.pdf — transceptor para ocho líneas, DIR selecciona sentido y `OE_n` alto aísla los lados. **No guarda un byte**: la retención pertenece a registros separados.
- Las ecuaciones de carga con multiplexores, la conversión `0xB6` y el ejemplo A→B son del modelo educativo. Se comprobaron en Python como álgebra y estados ideales; no representan medidas de un bus físico ni aseguran que el cableado de estos dos chips sea por sí solo suficiente.

### Fuentes y alcance del interludio P07B

- IETF RFC Editor, **RFC 3629**, *UTF-8, a transformation format of ISO 10646*: https://www.rfc-editor.org/rfc/rfc3629.html — especifica los bytes 00–7F para caracteres ASCII y la codificación UTF-8 de uno a cuatro bytes. El manuscrito usa `A` como `41` y `é` como `C3 A9`.
- Unicode Consortium, **The Unicode Standard**, formas de codificación Unicode: https://www.unicode.org/versions/latest/ — distingue caracteres, puntos de código y representaciones; útil para no confundir carácter con byte.
- NAND, latch, registro y señales lógicas: desarrollo original de los capítulos 3–7 de este libro. Los umbrales eléctricos citados para chips concretos deben conservar sus propias hojas de datos, sin extrapolarlos a todas las tecnologías.
- Los enteros de ocho bits en complemento a dos, los indicadores b6/b0 y la memoria `RAM[0x1200] = 0x41` son **ejemplos matemáticos o ficticios**. Las interpretaciones como opcodes requieren una ISA definida; no se atribuye `0x41` a una instrucción oficial de Aula.

### Fuentes y alcance del capítulo 8

- Texas Instruments, *SNx4HC138 3-Line To 8-Line Decoders/Demultiplexers*: https://www.ti.com/lit/ds/symlink/sn74hc138.pdf — decodificación de tres a ocho, habilitaciones y **salidas activas en bajo**. La figura de dos a cuatro salidas activas en alto es una abstracción de enseñanza distinta.
- Alliance Memory, *AS6C62256 32K × 8 Low-Power Asynchronous SRAM*: https://www.alliancememory.com/as6c62256/ — SRAM comercial de 32 KiB × 8 bits, selección de chip, lectura/escritura, estados de alta impedancia y temporización que deben verificarse para cada dispositivo elegido.
- El espacio de 65536 direcciones, la conversión `0x1200`, el decodificador 2→4 y las transacciones `0x41` / `0x53` son ejemplos del modelo educativo. **No** prueban instalación de 64 KiB de RAM, mapa definitivo, hardware Aula ni tiempos de una memoria física. El orden little-endian de Aula-16 es una decisión de arquitectura del proyecto, no una característica atribuida a los dos chips anteriores.

### Fuentes y alcance del capítulo 9

- Alliance Memory, *AS6C62256 32K × 8 Low Power CMOS SRAM*, hoja de datos revisión 1.2: https://www.alliancememory.com/wp-content/uploads/AS6C62256-23-March-2016-rev1.2.pdf — quince pines A0–A14, ocho DQ0–DQ7, CE#/OE#/WE#, tabla de modos, salidas Z, operación asíncrona y ejemplo de variante con acceso 55 ns. La alimentación de referencia 2,7–5,5 V no se extrapola a EEPROM ni a otros chips.
- Microchip, *AT28C64B 64-Kbit (8K × 8) Industrial Parallel EEPROM*, DS20006432B: https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/AT28C64B-64-Kbit-8Kx8-Parallel-EEPROM-with-Page-Write-and-Software-Data-Protection-DS20006432.pdf — memoria no volátil paralela, trece direcciones, ciclos de programación internos, protección y detección de fin de escritura. El máximo de hasta 10 ms depende de la variante y las condiciones.
- La representación funcional de una SRAM CMOS de seis transistores, el reparto de 64 KiB (32K SRAM, 24K sin asignar, 8K EEPROM), las ecuaciones de selección y el ejemplo de `0xE123` son material didáctico original. **No constituyen un netlist, una placa, el mapa final aprobado de Aula ni verificación de voltajes/tiempos.**

### Fuentes y alcance del capítulo 10

- Texas Instruments, *CD74HC283 High-Speed CMOS Logic 4-Bit Binary Full Adder with Fast Carry*, hoja de datos: https://www.ti.com/lit/ds/symlink/cd74hc283.pdf — referencia de un sumador completo integrado para **dos operandos de cuatro bits y acarreo de entrada/salida**. No equivale a afirmar que la futura ALU Aula-8 utiliza este componente ni que sus retardos sean los de una cadena abstracta de compuertas.
- Texas Instruments, *SNx4HC86 Quadruple 2-Input XOR Gates*: https://www.ti.com/lit/ds/symlink/sn74hc86.pdf — cuatro compuertas XOR de dos entradas en una sola pieza, como referencia del mecanismo de suma. Antes del montaje real hay que consultar los límites de alimentación, polaridad, pines y tiempos del encapsulado escogido.
- Las tablas exhaustivas de medio sumador y sumador completo, los ocho pasos de `13+9=22`, el truncamiento `250+10→4,C=1`, la distinción `127+1→0x80,V=1` y las cuatro figuras son **elaboraciones originales, verificadas matemáticamente**. No demuestran un circuito real, consumo, tiempo de propagación, conexión entre chips o CPU ejecutable.

### Fuentes y alcance del capítulo 12

- `simulador-javafx/MICROARQUITECTURA_AULA8_BORRADOR.md`: anchos de registros y buses, datapath provisional, sumas de dirección en dos pasadas y acarreo privado `ADDR_CARRY`. **No es un diagrama de cableado aprobado.**
- `simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md`: fuentes/destinos, acciones de lectura, latches de direcciones, traza didáctica `LDI/ST/HALT` y separación entre ROM de microcontrol y firmware. **No hay microcódigo ejecutable ni medición de ciclos.**
- `simulador-javafx/ISA_AULA8_CANDIDATA.md`: codificación propuesta de `LDI R0,42` (`11 00 2A`), `ST [0x6F00],R0` (`13 00 00 6F`) y HALT (`01`). Los bytes están sujetos a revisión; no se han ejecutado sobre una CPU construida.
- Las cuatro figuras de bloques, la explicación del bus compartido, los doce ejercicios, los modelos de dos pasadas y la validación en Python son **creaciones editoriales originales**. No prueban voltajes, pinout, compatibilidad física, frecuencia ni firmware.

### Fuentes y alcance del capítulo 13

- `simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md` y `simulador-javafx/MICROSECUENCIAS_AULA8_BORRADOR.json`: fetch compartido, rutas de despacho, acciones lógicas LDI/ST/HALT, comprobación de selectores, separación entre ROM de control y ROM de firmware. **Son borradores, no microcódigo codificado.**
- `simulador-javafx/MICROARQUITECTURA_AULA8_BORRADOR.md` y `simulador-javafx/ISA_AULA8_CANDIDATA.md`: registros MAR/MDR/IR, retención `ADDR_LO/HI`, bus de datos y bytes ilustrativos `11 00 2A 13 00 00 6F 01`. No se afirma que esos bytes corran en una CPU real.
- Los diagramas de lectura, despacho, secuenciación y escritura, junto con sus 12 ejercicios, son trabajo editorial original. La secuencia de **8 lecturas y 1 escritura** es un presupuesto funcional de transacciones **sin medición de ciclos, voltajes, tiempos de bus o micro-ROM**.

### Fuentes y alcance del capítulo 15

- `simulador-javafx/MICROSECUENCIAS_AULA8_BORRADOR.json`: fetch común, despacho, rutas `LDI`, `ST_ABS`, `HALT`, validación del selector, pasos `ST_BUILD_MAR`, `ST_STAGE_DATA` y `ST_WRITE`. **Acciones lógicas propuestas, no ciclos de reloj ni microcódigo implementado.**
- `simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md`: control funcional, relación entre PC, MAR/MDR/IR, SEL, TMP y los latches ADDR_LO/HI; sin circuito de control aprobado.
- `simulador-javafx/ISA_AULA8_CANDIDATA.json`: programa `11 00 2A 13 00 00 6F 01`, disposición little-endian y destino `0x6F00`, todos provisionales.
- `simulador-javafx/MICROTRAZA_AULA8_BORRADOR.json`: **ocho lecturas externas y una escritura esperadas**, sin cronometraje o equipo real.
- Los cuatro esquemas y los ejercicios son propios. La prueba en Python recorre acciones del modelo para diferentes estados iniciales y reconstruye direcciones; **no demuestra CPU real, señales eléctricas, arbitraje, firmware o micro-ROM programada**.

### Fuentes y alcance del capítulo 14

- `simulador-javafx/ISA_AULA8_CANDIDATA.md` y `simulador-javafx/ISA_AULA8_CANDIDATA.json`: opcodes `11`/`13`/`01`, formatos variables, dirección little-endian, selector de modo y registro, desplazamientos firmados, salto JNZ y ejemplo de ocho bytes. **ISA propuesta, no congelada ni ejecutada.**
- `simulador-javafx/PROGRAMACION_DESDE_CERO.md`: progresión desde panel de carga manual detenido a monitor hexadecimal, editor y ensamblador nativos. Los programas de firmware siguen sin escribirse y la electrónica del panel **no está diseñada**.
- `simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.md`: vector RESET y condiciones de `POKE`, `RUN`, `RET` y `HALT`. Se usa como **contrato candidato**, no como monitor ejecutable.
- MITS, *Altair 8800 Operators Manual* (1975), y *Theory of Operation* (1975), ya referenciados abajo: antecedentes de depósito mediante panel y necesidad de control eléctrico; **Aula-8 es otro diseño**, no replica sus pines ni comandos.
- Las cuatro figuras y los ejercicios son elaboración original. Las verificaciones Python prueban conversiones, recomposición de bytes y un depósito ideal en memoria del anfitrión; **no sustituyen una prueba física ni un arranque de CPU**.

### Fuentes y alcance del capítulo 11

- Texas Instruments, *CD74HC283 High-Speed CMOS Logic 4-Bit Binary Full Adder with Fast Carry*: https://www.ti.com/lit/ds/symlink/cd74hc283.pdf — el sumador integrado sirve para contextualizar la ruta aritmética y su acarreo interno.
- Texas Instruments, *SNx4HC86 Quadruple 2-Input XOR Gates*: https://www.ti.com/lit/ds/symlink/sn74hc86.pdf — cuatro XOR de dos entradas, apropiadas como referencia de inversiones condicionales o funciones XOR por posiciones.
- Texas Instruments, *SNx4HC157 Quadruple 2-Line to 1-Line Data Selectors/Multiplexers*: https://www.ti.com/lit/ds/symlink/sn74hc157.pdf — selección de una de dos fuentes por canal, sin afirmar que un único chip elija todas las operaciones de la ALU de ocho bits.
- El complemento a dos, las banderas de préstamo `C=1−Cout`, las comparaciones `N XOR V`, las tablas exhaustivas, los ejemplos y las cuatro láminas son **desarrollo didáctico propio**, verificado en Python. Las piezas citadas no constituyen una ALU completa ni certifican voltajes, frecuencia, compatibilidad o encendido de Aula.

- MITS, *Altair 8800 Operators Manual* (1975): https://vtda.org/docs/computing/MITS/MITS_Altari8800OperatorsManual_1975.pdf
  - Ejemplos originales de entrada manual por interruptores con `DEPOSIT NEXT`.
- MITS, *Altair 8800 Theory of Operation* (1975): https://vtda.org/docs/computing/MITS/MITS_Altair8800TheoryOperation_1975.pdf
  - Justifica que un panel manual requiere electrónica de control del bus; no basta con dibujar interruptores.
- Apple Computer, *Apple-1 Operation Manual* (1976): https://device.report/m/52627e26d76bf7b0639394eca3b3471d97580b7e6f2e743a079ccd4fede03833
  - Monitor hexadecimal de PROM, edición de RAM por terminal y ejecución de programas.
- MOS Technology, *KIM-1 User Manual* (1976): https://www.kim-1.com/docs/usrman.htm
  - Teclado hexadecimal y distinción entre RAM volátil y soportes de almacenamiento.
- Intel, *The 8086 Family User's Manual*, octubre de 1979: https://bitsavers.org/components/intel/8086/9800722-03_The_8086_Family_Users_Manual_Oct79.pdf
  - Precedente histórico de bus externo de 16 bits y organización de datos; Aula-16 tendrá diseño propio y 16 bits de direcciones, no los 20 del 8086.
- Texas Instruments, SN74HCT00 (NAND): https://www.ti.com/product/SN74HCT00
- Texas Instruments, CD74HCT173 (registro de cuatro bits): https://www.ti.com/product/CD74HCT173
- onsemi, hoja de datos 2N3904 NPN: https://www.onsemi.com/pdf/datasheet/2n3904-d.pdf
- Alliance Memory, AS6C62256 (SRAM 32K × 8): https://www.alliancememory.com/as6c62256/
- Microchip, AT28C64B (EEPROM 8K × 8): https://www.microchip.com/en-us/product/AT28C64B
- KiCad, comprobación ERC: https://docs.kicad.org/9.0/en/eeschema/eeschema.pdf
  - Útil para verificar reglas eléctricas comunes, no para certificar que el circuito físico funcionará.

## Arquitectura de software e interfaz

Los capítulos 16 y 17 se apoyan en los contratos internos **todavía no aprobados** `MICROFLUJO_AULA8_R0_6_BORRADOR.json` y `ROM_MONITOR_AULA8_R0_11_BORRADOR.json`, así como en `ISA_AULA8_CANDIDATA.json`. Las tablas, las ranuras y las trazas son ejemplos diseñados para Aula-8; no atribuirlos a manuales históricos como hechos de dispositivos reales. El *Apple-1 Operation Manual* y el manual KIM-1 citados arriba sirven únicamente de antecedentes de monitores y entrada hexadecimal.

- Documentación cc65 (compilación para 6502): https://cc65.github.io/doc/
- Documentación de GNU assembler: https://sourceware.org/binutils/docs/as/
- JavaFX 21 SubScene: https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/SubScene.html
- JavaFX 21 MeshView: https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/shape/MeshView.html

## Política de referencias

- Preferir fuentes originales, normas y hojas de datos del fabricante.
- Comprobar fecha, compatibilidad y disponibilidad de un SKU antes de recomendar compra.
- No presentar un dibujo 3D como diagrama electrónico verificable.
- Incluir procedencia de imágenes ajenas; preferir diagramas propios para el libro.
- Corregir inconsistencias detectadas del manuscrito de referencia antes de usar sus ideas.

