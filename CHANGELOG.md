# Historial del proyecto

## C28-T — 2026-11-09 — Del bit a la ruta ADD/SUB de 134 NAND (sin pruebas)

- Dos láminas técnicas originales en **SVG y PNG**: sumador completo de
  nueve NAND con conexiones N1…N9 y bloques de ocho bits de ADD/SUB,
  con un presupuesto de **134 NAND** y banderas C/V/Z/N.
- Nuevo texto didáctico `libro/SUPLEMENTO_C28T_DEL_BIT_A_134_NAND.md`
  con tablas, recorrido de señales, ejemplos y límites físicos.
- Mapa preciso de inserción para capítulos 4, 10 y 11. **El maestro
  Word/PDF C28-G de 248 páginas no se modificó**.
- Madurez editorial ponderada **87,3 → 88,5 %**, estimación, no una
  certificación ni una medida de hardware.
- **Sin nuevas pruebas** por petición de Marcos. Última evidencia Windows
  confirmada: 24/24 en C28-Q; los 28 controles previstos de C28-R/S
  siguen pendientes. La ISA y las políticas de PC continúan abiertas.


## C28-S — 2026-11-09 — NAND de ADD/SUB y revisión del maestro completo

- **Entrada real:** 24/24 controles Windows aprobados y 5/5 fotos históricas
  descargadas en `Retroalimentacion_GLOBAL_C28H_20261109_200941.zip`.
- **C28-R:** red serializada de 134 NAND para ADD/SUB de ocho bits;
  Verilog derivado del mismo modelo y testbench independiente.
  En anfitrión pasan 131.072 combinaciones aritméticas incluyendo
  C7/Cout, acarreo/préstamo, desbordamiento firmado, cero y signo.
  No se implementa ALU completa ni se decide ISA/temporización.
- **C28-S:** examen geométrico local de 248 páginas PDF, 17.216 fragmentos
  de texto y 127 bloques de imagen, sin cajas fuera de página ni U+FFFD;
  ocho hojas de contacto visualmente repasadas a escala de composición,
  26/26 entradas de índice coincidentes y 247/247 folios concordantes.
  Permanece pendiente lectura fina del texto y cada ilustración.
- Suite global ampliada con dos controles Python y compilación/simulación
  Icarus de C28-R. **Objetivo 28/28**, pendiente en Windows.
- Madurez editorial estimada **85 → 87,3 %**. Word/PDF C28-G intactos;
  C28-H/C28-O siguen complementos sin integrar y ambas políticas PC
  continúan candidatas.

## C28-Q — 2026-11-09 — trazabilidad de conexiones NAND y HDL

- **Entrada real:** 19/19 controles Windows aprobados, sin fallos ni pendientes.
- Nuevos JSON de redes XOR (4 NAND) y latch SR (2 NAND) y auditor autónomo
  del cableado lógico serializado; repite 8.336 verificaciones del selector
  C28-D (51 NAND) y 32.768 combinaciones del PC/MAR C28-F (177 NAND).
  Se cotejaron rutas SVG y tabla de patillas con límites eléctricos explícitos.
- Matriz de diez circuitos: figura, red/modelo, pruebas y pendientes.
- Suite global ampliada con `LIBRO_C28Q_NETLIST_Y_FIGURAS` y cuatro
  controles para registro8 C28-A y PC16 C28-E en Icarus.
  **Próxima meta: 24/24**, pendiente de ejecutar en Windows.
- Madurez editorial estimada **84 → 85 %**. Maestro C28-G y decisiones
  pendientes de PC, ISA, firmware y hardware permanecen sin modificar.

## C28-P — 2026-11-09 — auditoría final de lecciones 15–24

- **Entrada real:** 18/18 controles de Windows aprobados, 5/5 fotografías
  históricas descargadas y atlas de siete páginas íntegro.
- Nuevo verificador de 11 lecciones, 50 figuras PNG/SVG, pila y CALL/RET,
  saltos, mapa de memoria, AEX1, Euclides, Fibonacci, bancos Aula-16 y
  32.768 posiciones de píxel. Pruebas documentales, no CPU integrada.
- La suite global incorpora `LIBRO_C28P_TRAMO_FINAL`: próxima meta
  **19 controles** en Windows. Word/PDF maestro C28-G sin modificar;
  la revisión visual integral y la elección de política PC continúan
  pendientes. Madurez editorial estimada 82 → 84 %.

## Libro C26-0.1 — 2026-11-08 — revisión de lectura y diagramas

- Los puentes P07B y P23V se titularon **capítulos 7B y 23B**, respetando los 24 capítulos base; la edición maestra ofrece **156 actividades seleccionadas** con soluciones, mientras las 312 originales permanecen en los fascículos.
- Se corrigió el rótulo que chocaba con el circuito de LED y el rótulo de despacho de microcontrol, se añadieron **conexiones de protoboard** y un **diagrama de bus Aula-16 con carriles D7..D0 y D15..D8**.
- Se corrigió el formato matemático del exponente cero en la conversión hexadecimal; ecuaciones Word con potencias OfficeMath y comprobación visual focal del PDF.
- Bibliografía final única, fuentes externas ampliadas en `FUENTES_CONSULTADAS.txt`; menos referencias de proceso y verificación repetidas en la narración.
- PDF y Word nuevos; la antigua C25 se conserva para recuperación. La corrección literaria completa y las imágenes históricas/portada ilustrada siguen pendientes; la lógica de vídeo V1 no cambió.

## Libro C25-0.1 — 2026-11-08 — edición maestra paginada

- Reunidos **24 capítulos y P07B/P23V** en un Word editable y un PDF maestro de **225 páginas**; portada y guía de lectura, índice de páginas reales y bibliografía de 24 fuentes externas.
- Conservadas **105 figuras originales, 333 ecuaciones OMML y 312 ejercicios resueltos**; el índice se deriva del PDF mediante herramienta reproducible, sin marcadores ficticios.
- Se detectó y regeneró el PNG de `c24_fig01_alcances_y_evidencias` desde su SVG original para corregir un truncamiento presente en el paquete base C24.
- `scripts/verificar_libro_maestro.py` audita el contenido, el formato editable, los vínculos de fuentes y el orden de páginas. El libro requiere todavía corrección humana final de fondo y trámites editoriales; no hay validación de CPU, firmware, circuitos ni vídeo físico.

## Libro C24-0.1 — 2026-11-08 — capítulo final e interludio visual

- P23V **redactado entre los capítulos 23 y 24**: 10 páginas Word/PDF, siete SVG/PNG deterministas, 13 ecuaciones OMML y doce ejercicios. Del código ASCII 0x41 a glifos, texto 32×16, bitmap de 2bpp, cuatro colores, tipografía y escritorios gráficos. No altera la numeración ni los registros de vídeo V1.
- Capítulo 24 **«Una computadora que podemos explicar»**: nueve páginas Word/PDF, cuatro SVG/PNG, 13 OMML, doce ejercicios. Distingue diseño documental, pruebas anfitrionas, firmware ausente y validación física futura.
- **66576 comprobaciones exactas** de coordenadas, bitmaps, ROM de glifos de muestra, fuentes SVG, documentos y PDFs mediante `scripts/verificar_entrega_c24.py`; incorporado a CI.
- **Acumulado: 24/24 capítulos numerados + P07B/P23V, 220 páginas, 105 diagramas, 312 ejercicios, 333 ecuaciones OMML**. Quedan libro maestro, revisión integral, simulador, firmware y hardware; estos últimos no están implementados.

## Libro C23-0.1 — 2026-11-08 — Bus Aula-16 y programación de palabras

- **Capítulo 22:** dos bancos de ocho bits, carril bajo y alto, A0 y fila A15..A1, byte par/impar, palabra alineada, little-endian y accesos de MMIO de ocho bits; diagramas funcionales, sin bus eléctrico montado.
- **Capítulo 23:** suma de tres palabras (`0x0202`), MCD por Euclides (`6`), Fibonacci y límites de u16, formas de direccionamiento, ABI y ensamblado cruzado como **objetivos**, sin codificación de ISA Aula-16 fingida.
- **Novedades:** 16 páginas Word/PDF, ocho diagramas propios SVG/PNG, 27 ecuaciones editables y 24 ejercicios; **142737 + 77951** verificaciones de modelos y documentos en anfitrión.
- **Acumulado:** **23/24 capítulos** y P07B, **201 páginas, 94 figuras, 288 ejercicios resueltos, 307 OMML**. Pendientes capítulo 24, interludio P23V planeado, volumen maestro y hardware/software real. Se mantiene sin cambios el **contrato lógico de vídeo V1**.

## Video V1 lógico congelado — 2026-11-08 — Delegación del usuario y direccionamiento

- Marcos delegó al asistente **resolver y congelar las 16 elecciones** del vídeo didáctico. Se conserva **una pantalla** que alterna texto/bitmap; el controlador se comunica mediante **seis registros MMIO de 8 bits en C020–C02A**, con C02C/C02E y direcciones impares reservadas.
- VRAM **indirecta** fuera de RAM CPU: **512 B de texto** + **8192 B de bitmap a 2 bpp (cuatro colores)**; ROM de 256 glifos × 8 B = **2048 B**, separada de firmware. Los buffers se preservan al cambiar de modo. `C000/C002` continúan como interfaz de consola en la misma pantalla.
- Se congeló codificación de `VIDEO_MODE`, `VIDEO_STATUS`, `VRAM_ADDR_LO/HI`, `VRAM_DATA` y `VIDEO_CTRL`, con registros, flags de error, selección de banco y autoincremento documentados en [contrato](simulador-javafx/CONTRATO_VIDEO_AULA_V1.md) y [JSON](simulador-javafx/VIDEO_AULA_V1_CONTRATO.json).
- Se diferencian **modos de direccionamiento de CPU**, **decodificación de direcciones MMIO** y **punteros internos a VRAM**. La ISA, micro-ROM y ROM de firmware público **no se alteraron**. Verificación nueva solo de contrato/modelo anfitrión; no CPU, pantalla o electrónica reales.

## Plan de vídeo y tipografía C21-VP — 2026-11-08 — Documentación, sin nueva implementación

- Se separan formalmente micro-ROM, firmware ROM y posible ROM de glifos; se explica por qué el controlador/VRAM, y no un opcode gráfico, convertiría datos en puntos visibles.
- Se conserva la terminal actual y se registra una **opción no aprobada** de vídeo integrado. Comparativa exacta de 1/2/4/8 bits por píxel, ejemplo 256×128, 4 KiB de VRAM monocroma y 2 KiB de glifos opcionales.
- Se traza un **interludio de libro todavía no escrito** sobre texto, semigráficos, mapas de bits, fuentes y evolución histórica. Las decisiones de monocromo y color, periférico, tamaños, MMIO y nuevas rutinas ROM quedan **PENDIENTES**.
- Un verificador matemático reproducible contrasta posiciones de todos los píxeles a 1/2 bpp y patrones de glifos; **únicamente modelo Python de anfitrión**.
- Un [cuestionario de 16 elecciones](simulador-javafx/CUESTIONARIO_MAPA_VIDEO_MMIO.md) detalla alternativas para el mapa MMIO propuesto `C020–C02F`, buffers, fuentes, color y firmware. **Ninguna opción se declara escogida**.
- No cambian los **21 capítulos redactados**, ISA, mapa de memoria, contrato R0.11 de firmware ni hardware; no se agrega un nuevo capítulo a los 24.

## Libro C21-0.1 — 2026-11-08 — Programas y palabra de 16 bits

- **Capítulo 20:** editor/ensamblador de dos pasadas como diseño; **ensamblador de referencia ejecutable en el anfitrión** para un subconjunto de ISA Aula-8 candidata, ejemplos suma de 13 bytes y Euclides de 29 bytes, Fibonacci y restricciones de ABI/pila. Novedad: listados reproducibles `.asm` y verificación de errores, no CPU construida.
- **Capítulo 21:** comparación rigurosa de ALU/registros de 8/16 bits, C/V/Z/N, suma por bytes y palabra, 16 direcciones frente a 16 datos, 64 KiB direccionables sin duplicación, y little-endian en RAM. Bus y control físico Aula-16 pendientes.
- **Nuevos artefactos:** 17 páginas Word/PDF, 8 esquemas SVG/PNG reproducibles, 32 ecuaciones OMML y 24 ejercicios resueltos; pruebas nuevas con **130685 + 126921** comprobaciones matemáticas/documentales.
- **Acumulado:** **21 de 24 capítulos** más P07B; **185 páginas, 86 figuras, 264 ejercicios y 280 ecuaciones OMML**. Faltan 22–24, el volumen maestro y la implementación de hardware/firmware/simulador.

## Libro C19-0.1 — 2026-11-08 — Guardar y recuperar programas

- Modelo de bloques persistentes de 256 bytes, mapa MMIO `C010–C01F`, lectura/escritura, `COUNT=0100`, estados `IDLE/BUSY+DRQ/DONE/ERROR`, y diferencias entre RAM y soporte persistente.
- Escenarios `LOAD` crudo y AEX1/`LOADX` como **futuros**, con cabecera de 32 bytes, verificación en anfitrión y limitaciones de ejecución real.
- **8 páginas Word/PDF, 4 esquemas SVG/PNG reproducibles, 15 OMML, 12 ejercicios resueltos, 205037 comprobaciones**; ninguna CPU ni bloque físico ejecutado.
- **Acumulado:** 19 capítulos numerados más P07B, **168 páginas, 78 figuras, 240 ejercicios, 248 OMML; faltan 5 (20–24)**.
- Se documentó una [escalera de programas](libro/ESCALERA_DE_PROGRAMAS_AULA8.md) de variable/suma a Euclides/Fibonacci y una [guía de fidelidad](libro/GUIA_DE_FIDELIDAD_DE_FIGURAS.md) para los diagramas.

## Libro C18-0.1 — 2026-11-08 — Hablar con la máquina

- Terminal, E/S mapeada, servicios ROM de caracteres, diferencias entre registro `STATUS` y API pública `FW_STATUS`; programa de salida `A`, eco de entrada y almacenamiento en RAM, `PUTS` con terminador cero.
- **8 páginas Word/PDF, 4 figuras vectoriales regenerables, 14 OMML y 12 ejercicios**, con **646 comprobaciones documentales**, sin CPU, firmware ni terminal físicos.

## Libro C17-0.1 — 2026-11-08 — Encender una computadora

- Arranque conceptual por vector little-endian FFFC/FFFD, ROM E000–FFFF de 8 KiB, pila y diferencias entre micro-ROM y firmware, ROM grabada y RAM indeterminada.
- Tabla pública FF00–FF7F con 32 ranuras reservadas y solo 4 asignadas; comandos candidatos HELP, MEM, POKE y RUN con validación de regiones. REG y LOAD todavía no disponibles.
- Diferencia crítica: RUN del monitor utiliza CALL; un RET equilibrado regresa al prompt, mientras HALT detiene la CPU.
- **Ocho páginas Word/PDF, cuatro diagramas SVG/PNG, doce OMML y doce ejercicios resueltos**. **196727 comprobaciones matemáticas/documentales**, sin firmware ni CPU ejecutados.
- **Acumulado:** 17 capítulos numerados y P07B, **152 páginas, 70 figuras, 216 ejercicios y 219 OMML**. Quedan siete capítulos (18–24).

## Libro C16-0.1 — 2026-11-08 — Subrutinas y pila

- CALL/RET, SP descendente, retorno de 16 bits little-endian en 7FFE/7FFF, llamadas anidadas LIFO y saltos JNZ con lectura de dos operandos incluso cuando el salto falla.
- Recorrido `6000 CALL→6010 LDI→6013 RET→6003 HALT`: 10 lecturas y 2 escrituras **esperadas**, no 12 ciclos de reloj.
- **Siete páginas Word/PDF, cuatro figuras, doce OMML, doce ejercicios resueltos y 184283 comprobaciones documentales**, sin CPU o circuito físico construido.

## Libro C15-0.1 — 2026-11-08 — La instrucción en movimiento

- Recorrido paso a paso de `LDI R0,42`, `ST [0x6F00],R0` y `HALT` con PC/MAR/MDR/IR/SEL/TMP y los latches ADDR_LO/ADDR_HI: **fetch, decode, execute** de una ISA todavía candidata.
- Lectura de `0x6000–0x6007`, validación del selector, escritura de `0x2A` en `0x6F00` y detención prevista con PC=`0x6008`.
- Se hace explícito el paso indispensable `ST_STAGE_DATA`: reemplazar `0x6F` de MDR por `0x2A` antes de `WR`; se conservan las banderas iniciales sin asignarlas arbitrariamente a cero.
- **Ocho páginas Word/PDF**, cuatro diagramas SVG/PNG originales, doce ecuaciones OMML, doce ejercicios resueltos y **143464 comprobaciones de modelo/documento**, integradas en CI.
- **Acumulado:** 15 capítulos numerados + P07B, **137 páginas, 62 figuras, 192 ejercicios y 195 OMML**. Restan **9 capítulos (16–24)** y la edición maestra.

**Límite:** las ocho lecturas y la escritura son accesos externos esperados, no ciclos medidos. No existe CPU, micro-ROM, firmware o montaje eléctrico probado.

## Libro C14-0.1 — 2026-11-08 — De números a instrucciones

- Del decimal 42 al byte `0x2A`: nibbles, hexadecimal, diferencia entre dato numérico y caracteres, opcodes, selectores y formatos de longitud variable de la ISA Aula-8 candidata.
- Codificación manual de `LDI R0,42` (`11 00 2A`), `ST [0x6F00],R0` (`13 00 00 6F`) y `HALT` (`01`); ocho bytes en `0x6000–0x6007`, destino `0x6F00`, PC esperado `0x6008`.
- Dirección absoluta, X+disp8 y SP+disp8; selector `modo×4+registro`, complemento a dos `0xFF=−1`, little-endian para direcciones y ejemplo de salto `JNZ` candidato.
- Contraste entre **depósito manual seguro con CPU detenida/bus cedido** y un **monitor que necesitaría firmware en ROM**. El reset, `RUN`, `HALT` y `RET` no son sinónimos.
- **Nueve páginas Word/PDF**, cuatro ilustraciones originales, 12 expresiones OMML editables y 12 ejercicios resueltos, con **132993 comprobaciones** de conversiones, direccionamiento, codificación, depósito simulado, figuras, XML Word y PDF e integración en CI.
- **Acumulado:** 14 capítulos numerados + P07B, **129 páginas, 58 figuras, 180 ejercicios y 183 expresiones OMML**. Restan **10 capítulos (15–24)**, revisión editorial y el Word/PDF maestro.

**Límite:** las operaciones se comprobaron como contratos matemáticos/documentales. Aula-8 no dispone aún de CPU ejecutable, panel eléctrico, monitor nativo ni ensamblador real.

## Libro C13-0.1 — 2026-11-08 — La unidad de control

- Se redactó una explicación funcional de la unidad de control Aula-8: instrucción visible, acciones lógicas internas, fetch compartido, despacho y diferencia entre ROM de microcontrol y ROM de firmware.
- Se ilustraron `READ_PC_TO_IR`, `LDI R0,42`, `ST [0x6F00],R0` y HALT mediante cuatro diagramas originales; el orden **validar → capturar dirección → preparar MDR → escribir** evita la pérdida de datos en el ejemplo.
- Se distinguieron `FAULT` de una instrucción ilegal y `PENDING_ROUTE` de una instrucción conocida aún sin microsecuencia; los **36 opcodes candidatos** no se presentan como 36 secuencias implementadas.
- **Ocho páginas Word/PDF**, cuatro figuras, 8 OMML y 12 ejercicios resueltos; **196771 comprobaciones de modelo/documento** con verificaciones de rutas, direccionamiento, selector, figuras, XML Word y PDF, integradas en CI.
- **Acumulado:** 13 capítulos numerados + P07B, **120 páginas, 54 figuras, 168 ejercicios y 171 expresiones OMML**. Restan **11 capítulos (14–24)**, revisión editorial y el Word/PDF maestro.

**Límite:** no se ejecutaron instrucciones sobre una CPU Aula, no hay micro-ROM programada, reloj caracterizado, firmware ni montaje físico verificado.

## Libro C12-0.1 — 2026-11-08 — Arquitectura Aula-8

- Se redactó la primera arquitectura de bloques educativa: registros generales R0–R3, PC/SP/X, MAR/MDR, IR/SEL/TMP, FLAGS, ALU8, unidad de control, buses externos y bus interno.
- Se explicó el dueño único del bus de datos en lecturas `RD` y escrituras `WR`, sin atribuir polaridades de pines ni latencias al dibujo.
- Se ilustró la lectura conceptual `11 00 2A` desde `0x6000` (`LDI R0,42`) y el avance de `PC` a `0x6003`; **ISA y secuencia siguen siendo borradores**.
- Se descompuso `X=0x12FF+2=0x1301` en dos operaciones de ocho bits, separando `ADDR_CARRY` de la bandera visible `FLAGS.C`.
- **Nueve páginas Word/PDF**, cuatro figuras originales, 12 OMML, 12 ejercicios resueltos y **2752599 controles aritméticos/documentales** integrados en CI.
- **Acumulado:** 12 capítulos numerados + P07B, **112 páginas, 50 figuras, 156 ejercicios y 163 ecuaciones OMML**. Restan **12 capítulos (13–24)**, edición maestra y etapas físicas/software.

**Límite:** no hay CPU, ROM de control, firmware ni montaje demostrado; una traza lógica candidata no es un ciclo de reloj medido.

## Libro C11-0.1 — 2026-11-08 — ALU, resta y comparaciones

- Se produjo «La unidad aritmético-lógica»: reutilización del sumador de ocho bits para `A−B`, complemento a dos, `13−9`, `9−13`, aritmética módulo 256 y bandera de préstamo candidata.
- Se distinguieron **acarreo (ADD)**, **préstamo (SUB)**, **overflow firmado V**, bit de signo N y cero Z. `0xFF` frente a `0x01` muestra la diferencia entre comparar con signo y sin signo.
- Se añadieron AND, OR, XOR, NOT, máscaras y un multiplexor que selecciona resultados; **la política de flags de lógica queda expresamente sin decidir**.
- Referencias primarias TI CD74HC283, SN74HC86 y SN74HC157; cuatro figuras originales; ocho páginas Word/PDF, 21 OMML, 12 ejercicios y **786524 verificaciones matemáticas/documentales**, integradas en CI.
- **Acumulado:** 11 capítulos numerados + P07B, **103 páginas, 46 figuras, 144 ejercicios y 151 ecuaciones OMML**. Faltan **13 capítulos (12–24)**, el libro maestro y el prototipo/firmware/simulador.

**Límite:** ninguna de las comprobaciones demuestra una CPU ejecutable, conexión física o tiempos reales. La ISA y la microarquitectura siguen siendo candidatas.

## Libro C10-0.1 — 2026-11-07 — Medio sumador, sumador completo y acarreo

- Se completó «El circuito que suma»: medio sumador XOR/AND, sumador completo mediante dos medios sumadores y OR, tabla de ocho combinaciones y acarreo propagado por ocho etapas.
- Ejemplo de **13+9=22** con ocho columnas y acarreos C1/C4; límites de ocho bits sin signo y con signo, diferencias entre indicadores C/V/Z/N y suma de dos bytes `0x01FF+0x0001=0x0200`.
- Referencias primarias Texas Instruments CD74HC283 y SN74HC86, sin extrapolar su pinout, voltajes ni retardos a una computadora no implementada.
- **Ocho páginas Word/PDF**, cuatro figuras SVG/PNG, 17 OMML, 12 ejercicios, **786541 controles matemáticos/documentales** y verificación en CI.
- **Acumulado:** capítulos 1–10 más P07B, **95 páginas**, 42 figuras y 132 ejercicios. Faltan **14 capítulos (11–24)** y la edición maestra del libro.

**Límite:** los esquemas son funcionales; no constituyen ALU, CPU ni montaje eléctrico ensayado. La convención completa de banderas e instrucciones sigue pendiente de consolidación técnica.

## Libro C09-0.1 — 2026-11-06 — SRAM, ROM, EEPROM y mapa de memoria

- Se completó «RAM y ROM reales», desde la celda SRAM y el chip AS6C62256 (`32K × 8`) hasta la EEPROM AT28C64B (`8K × 8`) y su función de memoria de arranque. Se distinguen volatilidad, lectura, escritura y tiempos de programación.
- Se explicó un **mapa ilustrativo, no aprobado**, de 32 KiB SRAM, 24 KiB sin asignar y 8 KiB EEPROM dentro del espacio de 64 KiB. Se muestra la traducción `0xE123 → 0x0123`.
- Se comparan expansión de profundidad `64K × 8` y de anchura `32K × 16` sin cambiar los acuerdos de Aula-8/Aula-16.
- **Ocho páginas Word/PDF**, cuatro figuras SVG/PNG, diez ecuaciones OMML, doce ejercicios, **368752 controles matemáticos/documentales** y validación en CI.
- **Acumulado:** capítulos 1–9 más interludio P07B, 87 páginas, 38 figuras, 120 ejercicios. Faltan **15 capítulos (10–24)** y la maquetación del libro completo.

**Límite:** ni el mapa ni los dispositivos de memoria están construidos o validados eléctricamente; CPU, firmware y simulador siguen sin implementar.

## Libro C08-0.1 — 2026-11-06 — Direcciones, buses y selección de memoria

- Se redactó «Direcciones y buses» con decodificador 2→4, dirección frente a dato, buses independientes, controles de lectura/escritura, alta impedancia y ejemplo completo de `0x1200`/`0x1201`.
- Se diferencian Aula-8 (bus de datos de 8 bits) y Aula-16 (bus de datos de 16 bits); ambas conservan 16 bits de dirección y direccionamiento por byte. Se explica little-endian con la palabra `0x1234` sin congelar la temporización o el mapa físico.
- **Word/PDF de nueve páginas, 4 figuras SVG/PNG, 12 ecuaciones OMML y 12 ejercicios con solucionario.** Un verificador efectuó **459379 pruebas matemáticas y documentales** y se incorporó a CI.
- **Acumulado:** 8 capítulos numerados + interludio P07B, 79 páginas, 34 figuras y 108 ejercicios. Faltan **16 capítulos (9–24)**, libro maestro y validación de hardware real.

**Límite:** no se ha implementado una CPU Aula ni verificado un circuito de memoria; las señales de control del capítulo son un modelo didáctico.

## Libro P07B-0.1 — 2026-11-06 — Interludio del bit al significado

- Se redactó y maquetó el puente editorial entre los capítulos 7 y 8, **sin modificar el currículo numerado de 24 capítulos**.
- Se distinguen niveles eléctricos y semántica de control en hardware, patrón almacenado, lectura sin signo o complemento a dos, ASCII/UTF-8, direcciones, opcodes, tipos y estructuras.
- Se incluyeron 4 diagramas originales SVG/PNG, Word/PDF de ocho páginas, 9 ecuaciones OMML y 12 ejercicios con soluciones.
- Se realizaron **1383 controles** matemáticos y documentales, incorporados al workflow de CI.
- **Acumulado:** 7 de 24 capítulos numerados + 1 interludio, 70 páginas, 30 figuras y 96 ejercicios. Siguen pendientes los capítulos 8–24, el Word/PDF maestro, la portada y la validación física/CPU.

**Límite:** no hay CPU Aula ejecutable, circuitos eléctricos medidos ni ISA definitiva. La POO aparece solo como contexto conceptual.

## Libro C07-0.1 — 2026-11-06 — Ocho bits como registro y bus compartido

- Se redactó y maquetó «Del bit al registro» con ocho flip-flops, potencias de dos, conversión manual de `10110110` y ejemplo de transferencia A→B.
- Se generaron cuatro ilustraciones SVG/PNG, Word/PDF de ocho páginas, nueve ecuaciones OMML y doce ejercicios con solucionario.
- Un verificador comprueba exhaustivamente 256×256 combinaciones de dos valores de byte para LOAD=0, LOAD=1 y ausencia de flanco, 256 codificaciones binarias y hexadecimales, arbitraje de bus y estructura Word/PDF: **198502 controles**.
- Referencias TI SN74HC377 (almacenamiento sin triestado) y SN74HC245 (triestado sin almacenamiento). Se incorpora la verificación a CI.
- **Estado acumulado:** siete de 24 capítulos, **17 pendientes**, 62 páginas, 26 figuras y 84 ejercicios. Próximo hito sugerido: interludio semántico sin numerar, seguido del capítulo 8.

**Límite:** no hay prueba analógica/eléctrica, CPU ejecutable, firmware ni Word/PDF maestro integrado.

## Libro C06-0.1 — 2026-11-06 — Memoria con habilitación y reloj

- Se redactó y maquetó «Memorizar en el tiempo» con latch D, flip-flop de flanco ascendente, reset, preset, setup/hold y dos secuencias de estados resueltas.
- Se generaron cuatro figuras originales, Word/PDF de ocho páginas, nueve ecuaciones OMML y doce ejercicios con solucionario.
- Un verificador independiente ejecuta **171 controles** sobre lógica de captura, transformaciones NAND, frecuencia, documentación y estructura de los archivos. Añadido a CI.
- Se utilizó documentación primaria de Texas Instruments SN74HC373 y SN74HC74. No se atribuyeron mediciones eléctricas ni certificados de un circuito no construido.
- **Estado acumulado:** seis borradores de 24, **18 pendientes**, 54 páginas, 22 figuras y 72 ejercicios. Próximo capítulo: «Del bit al registro».

**Límite:** no existe montaje físico, CPU ejecutable, firmware, simulador o Word/PDF maestro integrado.

## Libro C05-0.1 — 2026-11-06 — Primer bit de memoria

- Se redactó y maquetó el capítulo 5, «La realimentación conserva información», con SET/RESET/HOLD de dos NAND cruzadas, controles activos en bajo y estado prohibido.
- Se incorporaron cuatro figuras originales (SVG/PNG), 11 ecuaciones editables OMML, 12 ejercicios resueltos y Word/PDF de ocho páginas.
- El verificador C05 recorre todos los puntos fijos booleanos y la secuencia de cinco momentos, comprueba archivos y texto: **123 controles**. Agregado al workflow de documentación.
- El puente «Del bit al significado» distingue semántica lógica de hardware, interpretación de datos y semántica de software. La programación orientada a objetos aparece solo como contextualización futura.
- **Estado acumulado:** cinco borradores de 24 capítulos, 19 pendientes; 46 páginas, 18 figuras y 60 ejercicios. Próximo capítulo 6, «Memorizar en el tiempo».

**Límite:** ninguna medida física, simulación analógica, comprobación de power-on o CPU/firmware ejecutable.

## Libro C04-0.1 — 2026-11-06 — Cuarto capítulo y propuesta semántica

- Se redactó «Construir funciones con compuertas»: OR, NOR, XOR, expresión de suma de productos, recorrido de una XOR de cuatro NAND y simplificación booleana con prueba por tabla.
- Se produjeron cuatro figuras propias SVG/PNG, un Word de nueve páginas con trece ecuaciones OMML y texto alternativo, y un PDF de nueve páginas con texto seleccionable; doce ejercicios con respuestas.
- Un verificador nuevo comprueba **146 condiciones** de lógica, señales intermedias de la red XOR, documentación, figuras, integridad del Word y PDF; se incluye en CI.
- A petición de Marcos, se registró la [propuesta «Del bit al significado»](libro/PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md) para explorar el salto desde estados eléctricos hasta datos, caracteres, instrucciones y estructuras. Por ahora es interludio propuesto después del capítulo 7 **sin renumerar los 24 capítulos**.
- **Avance editorial: cuatro de 24 capítulos numerados; 20 pendientes.** El siguiente será el capítulo 5 de realimentación y latch SR. El libro maestro y la portada siguen pendientes.

**Límite:** no se ha montado ni medido un circuito, no se ejecutó ninguna CPU ni se redactó todavía el capítulo puente.

## Libro C03-0.1 — 2026-11-06 — Tercer capítulo redactado

- Se escribió «De interruptores a lógica», puente didáctico entre el interruptor NPN y las funciones booleanas: 0/1, NOT, AND, NAND, tabla de verdad y construcción de otras funciones con NAND.
- Se eligió un ejemplo de integrado real **SN74HCT00N PDIP-14** con referencias a la hoja de datos de Texas Instruments, umbrales 0,8/2,0 V, pines y entradas no utilizadas a nivel definido.
- Se entregan cuatro figuras originales SVG/PNG, un Word de diez páginas con 14 expresiones OMML editables y un PDF de diez páginas; doce ejercicios y solucionario independiente.
- Se repararon la proximidad de la etiqueta +5 V al subtítulo y la tabla que se aislaba al inicio de una página. El verificador nuevo realiza **132 comprobaciones** y se suma a CI.
- **Cobertura editorial actual: 3 de 24 capítulos; faltan 21.** Sigue pendiente la revisión del usuario, la integración del Word/PDF maestro y la portada.

**Límite:** los umbrales proceden de la hoja de datos y las corrientes son estimaciones; no se realizó ensayo físico ni se ha implementado una CPU, un firmware o el simulador.

## Libro C02-0.1 — 2026-11-05 — Segundo capítulo redactado

- Se redactó **«El transistor como interruptor»**, una secuencia desde la necesidad de controlar una carga hasta las dos ramas de un NPN y sus estados de corte/saturación.
- Se tomaron los valores del **2N3904 onsemi como referencia documentada**, distinguiendo las condiciones de ensayo de la hoja de datos de los cálculos aproximados del circuito de 5 V, LED, 330 Ω y 4,7 kΩ.
- Se crearon **tres diagramas SVG originales** (terminales E/B/C; LED encendido; LED apagado), exportaciones PNG y diez páginas Word/PDF con 13 expresiones OMML y 12 ejercicios resueltos.
- Se verificó el PDF visualmente, corrigió un corte de tabla y se añadieron **87 controles automáticos del capítulo 2**, que se ejecutan junto con el capítulo 1 en CI.
- **Estado acumulado:** dos borradores de 24 capítulos; 22 aún pendientes. El siguiente es «De interruptores a lógica».

**Límite:** no se realizaron mediciones físicas, montaje de protoboard, simulación de componentes comerciales, integración de Word/PDF maestro ni prueba de DocuPodcast.

## Libro C01-0.1 — 2026-11-05 — Primer capítulo redactado

- Se redactó **«La corriente y sus caminos»**, manuscrito original introductorio sobre tensión, corriente, resistencia, potencia, LED y mediciones seguras.
- Se incluyeron **tres diagramas vectoriales originales** (fuente + resistor + LED; voltímetro en paralelo; amperímetro en serie), con exportaciones PNG para el Word.
- Se produjeron un **DOCX editable con 13 expresiones OMML** y un **PDF de nueve páginas con texto seleccionable**, más 12 ejercicios con respuestas separadas del enunciado.
- Se añadieron generadores reproducibles y **57 controles automáticos**; la maquetación se inspeccionó en las nueve páginas.
- Se separó el estado de escritura del estado R0.14 de diseño técnico: el capítulo 1 está disponible para revisión; **23 capítulos y el libro maestro siguen pendientes**.

**Límite:** la práctica de LED es un ejemplo calculado; no hay medición física, compatibilidad DocuPodcast certificada ni validación de un LED comercial específico.

## R0.14 — 2026-11-05 — LOADX de dos pasadas y pendientes del libro

- Un modelo Python de referencia verifica **todos los bloques AEX1** con CRC16 incremental antes de escribir RAM y vuelve a leerlos para copiar **solo el programa útil** mediante bloques temporales de hasta 256 B.
- Si la **primera** pasada falla, RAM de programa queda intacta. Si la **segunda** falla, puede quedar RAM **parcial**, pero el modelo **no ofrece punto de entrada habilitado**. No se promete atomicidad, recuperación ante corte eléctrico ni enforcement efectivo en firmware.
- Se realizaron **30 pruebas nuevas** de máximo tamaño de herramienta, cambios entre lecturas, sectores truncados, CRC, fallo tardío y preservación de memoria ajena. Continúan las 42 de AEX1 y las 20 del controlador de R0.12.
- Se agregó la [auditoría del libro](libro/ESTADO_Y_PENDIENTES_R0_14.md): **24 capítulos pendientes de redacción**, figuras, verificaciones, programas, ejercicios, derechos y Word/PDF. **No** iniciar más R0 como sustituto de la escritura.

**Límite:** no hay firmware, CPU Aula-8, ROM compilada, emulador, editor/ensamblador nativo ni implementación física. Aula-16 sigue con **bus externo de 16 bits**.

## R0.13 — 2026-11-05 — Paquete de programa AEX1 candidato

- Se especifica una cabecera binaria **AEX1** de 32 B con firma, versión, CPU Aula-8, tipo, origen RAM, entrada, longitud, bloques necesarios y dos CRC16; bytes de reserva y relleno deben ser cero.
- El contenido útil se aloja en bloques crudos R0.12 de 256 B; el encabezado nunca se copia a RAM. Tipos candidatos: práctica 6000–6FFF y herramienta en overlay 1000–2FFF.
- `LOAD` crudo y futuro `LOADX bloque_hex4` **permanecen NO DISPONIBLES** en el monitor; la referencia anfitriona valida paquete entero antes de producir una copia de RAM.
- Se entregan empaquetador/inspector ejecutables en Python, modelo de referencia y **42 pruebas reproducibles**, entre ellas corrupción, rangos, CPU incorrecta, padding, sectores faltantes y no sobrescritura de archivo de salida.
- Se deja explícita una **limitación pendiente**: staging provisional 0200–0FFF = 3584 B, menor que el máximo de herramienta 8160 B. No certificar atomicidad o cabida real sin resolverla.

**Límite:** formato NO APROBADO, sin CPU, firmware, ensamblador, editor, LOADX nativo, ROM compilada, validación eléctrica ni ejecutable Aula-16. Aula-16 mantiene **16 bits externos**.

## R0.12 — 2026-11-05 — Controlador de bloques y carga cruda candidatos

- Se describen ocho registros de 8 bits en direcciones pares C010–C01E, dentro de la ventana ya reservada C010–C01F: COMMAND, STATUS, BLOCK_LO/HI, DATA, ERROR y COUNT_LO/HI.
- El contrato propone READ/WRITE/RESET y NOP, números de bloque little-endian de 16 bits, transferencias exactas de 256 B y estados BUSY/DRQ/DONE/ERROR.
- Un **modelo de referencia Python ejecutado en el anfitrión** conserva escrituras completas en archivo temporal, comprueba reapertura, aborta escrituras parciales y detecta errores de acceso, sector y reemplazo.
- El futuro `LOAD bloque_hex4 destino_hex4 cantidad_hex2` queda documentado con alineación y ventanas RAM 1000–2FFF o 6000–6FFF. **No** se habilita en el monitor: no existe el firmware Aula; una carga parcial no puede ejecutarse.
- Se añaden **20 pruebas** automatizadas del modelo de anfitrión, CI y actualización de decisiones, contexto, currículo, calidad y trazabilidad.

**Límite:** no hay CPU, bus, EEPROM, controlador digital, LOAD nativo, sistema de archivos, CRC ni garantías eléctricas de persistencia. Aula-16 **conserva bus externo de 16 bits**.

## R0.11 — 2026-11-05 — ROM y monitor hexadecimales candidatos

- Se reserva como **propuesta** una tabla de 32 ranuras ROM de cuatro bytes, FF00–FF7F; cuatro nombres públicos estables: FW_PUTC, FW_GETC, FW_PUTS y FW_STATUS.
- Se especifican bytes ilustrativos JMP absoluto little-endian de 3 B y NOP de relleno (destinos internos ficticios), y vector RESET little-endian en FFFC–FFFD, con ejemplo de salto a E000.
- Se diferencia ABI pública de firmware respecto a MiniC: CALL al slot, JMP hacia implementación, RET de vuelta; R2/R3/X preservados y R0/R1/FLAGS volátiles.
- El monitor hexadecimal propuesto define HELP, MEM, POKE y RUN, con ventana de práctica para escrituras/ejecución; RUN utiliza CALL y vuelve al prompt **solo por RET**, mientras HALT detiene la CPU. REG y LOAD quedan NO DISPONIBLE hasta sus contratos de hardware.
- El verificador comprueba cuatro entradas y 40 casos de sintaxis, límites y retorno teórico, sincronizados con decisiones, contexto portable, trazabilidad, calidad, README y CI.

**Límite:** no hay ROM binaria grabable, firmware ejecutable, CPU, compilador, controlador serial/almacenamiento ni validación física. Aula-16 **conserva bus externo de 16 bits**.

## R0.10 — 2026-11-05 — ABI MiniC-Aula8 candidata

- Se documenta un convenio binario de llamadas: parámetros u8/char/u16 de 2 bytes, orden derecha a izquierda, PUSH de alto antes que bajo y limpieza de argumentos por el llamador.
- Se propone un marco de función de offsets fijos: conservar siempre X/R2/R3, X como base, retorno en X+4/5 y primer argumento en X+6/7. R0/R1/FLAGS son volátiles; retorno u8 en R0 y u16 en R1:R0.
- Se introduce programa candidato SUMAR_UNO(0x01FF) de 63 bytes, con respuesta 0x0200, pila/índice restaurados y 73 lecturas más 10 escrituras externas previstas.
- Un verificador de escritorio contrasta la traza y 640 disposiciones reproducibles de 0 a 4 argumentos; el límite de recursión de 409 marcos se registra solo como cuenta idealizada.
- Se conserva Aula-16 con bus externo de 16 bits y se actualizan decisiones, contexto, trazabilidad, calidad, documentación y CI.

**Límite:** la ABI no está aprobada, las verificaciones son modelos de escritorio; no hay ejecutable MiniC, CPU, micro-ROM, firmware ROM ni electrónica implementada.

## R0.9 — 2026-11-05 — Ajustes de X/SP y marcos de función

- Se describen cinco instrucciones ya propuestas por R0.3: LEAX, ADDXW, SETSP, ADJSP y XFROMSP, con desplazamientos firmados, palabra R1:R0 y flags preservadas.
- La aritmética de 16 bits se modela en dos pasadas de ALU8 con acarreo de direcciones privado y confirmación lógica del destino al completar ambas.
- Se añade una función de 24 bytes que apila el retorno, salva X, obtiene marco con XFROMSP, reserva un local, lo lee y libera, restaura X y retorna.
- El ejemplo de escritorio prevé **29 lecturas y 5 escrituras** externas; se contrastaron **1572864 operaciones matemáticas** contra referencia de enteros.
- Se actualizan decisiones, contexto maestro, arquitectura, política de pruebas, trazabilidad y CI, sin modificar el bus externo Aula-16 de 16 bits.

**Límite:** verificadores documentales; no hay CPU ejecutada, ROM de microcódigo binario, ABI general aprobada, protección hardware de pila ni montaje eléctrico.

## R0.8 — 2026-11-05 — Direcciones indexadas X/SP y ALU8 en dos pasadas

- Se proponen `LD/ST` con base X o SP y desplazamiento firmado de ocho bits: selectores `0x04–0x0B`, instrucciones de tres bytes y conservación de flags.
- Se descompone la dirección efectiva de 16 bits en dos operaciones de ALU8 con extensión de signo y `ADDR_CARRY` privado, sin alterar X/SP.
- Se documentan rutas lógicas de `SETX`, `LD/ST` indexadas y un ejemplo de arreglo `0x6F01`, con 14 lecturas y una escritura esperadas.
- Se contrasta la suma por dos pasadas frente a una referencia matemática en **526592 casos** y se introduce un ejemplo de variable local SP+0, dejando `ADJSP` y ABI pendientes.
- Se actualizan contexto, decisiones, arquitectura, pruebas, trazabilidad y CI; Aula-16 retiene **16 bits externos**.

**Límite:** especificación R0.8 no aprobada; la prueba solo verifica aritmética y coherencia de documentos. No existen CPU, microcódigo binario, netlist eléctrico ni acceso real a memoria.

## R0.7 — 2026-11-05 — Pila de datos y banderas aritméticas candidatas

- Se diseñan secuencias lógicas de `PUSH/POP`, `PUSHX/POPX` e `INC/DEC`, respetando el convenio de pila descendente y el orden little-endian de R0.6.
- Se explican registros y banderas `Z/N/C/V`; `INC/DEC` preservan C aunque alteren Z/N/V. ADD/ADC expresan acarreo y SUB/SBC/CMP préstamo en C.
- Se incorpora una prueba matemática independiente de **459776 casos** para fórmulas candidatas de Z/N/C/V, además de vectores de borde declarados.
- El ejemplo LDI/PUSH/LDI/POP/DEC/HALT propone **14 lecturas y 1 escritura**, retorno de SP y R0=41; se revisa también el bucle DEC→JNZ de R0.3/R0.6.
- Se actualizan contexto, decisiones, trazabilidad, plan de pruebas, CI y continuidad; se conserva el bus externo de 16 bits de Aula-16.

**Límite:** ningún caso matemático ejecutó una CPU real; no existen microcódigo binario, netlist físico, mediciones, firmware ni simulador JavaFX.

## R0.6 — 2026-11-05 — CALL/RET, pila y saltos candidatos

- Se describe la convención pendiente de confirmación para `CALL/RET`: reservar dos bytes de pila descendente, guardar retorno en little-endian, recuperar PC y liberar posiciones **sin borrarlas**.
- Se explican fuentes y destinos de `MAR/MDR`, temporales `RET_LO/RET_HI` candidatos y preservación de la dirección de destino de subrutina.
- Se documentan `JMP/JZ/JNZ/JC/JNC`: siempre consumir dos operandos, comprobar Z/C sin cambiarlos y conservar PC de continuación cuando el salto no se toma.
- Se añade ejemplo original `CALL→LDI→RET→HALT`, con **10 lecturas y 2 escrituras de bus esperadas**, y nueva comprobación estructural de JSON y bytes.
- Se actualizan contexto portable, arquitectura, decisiones, hoja de ruta, matriz, guía de continuidad, pruebas y CI, preservando el bus externo de 16 bits de Aula-16.

**Límite:** no existen CPU, microcódigo binario, pila protegida por hardware ni medidas eléctricas; la verificación es documental.

## R0.5 — 2026-11-05 — Microcontrol documentado hasta tres instrucciones

- Se propone un microsecuenciador con fetch de opcode compartido, despacho por `IR`, entrada a `LDI`, `ST` absoluto y `HALT`, y `FAULT` para opcode inválido.
- Se separan **acciones lógicas** de microinstrucciones eléctricas y ciclos de reloj; anchura y tamaño de ROM de control quedan por definir.
- Se documenta por qué `ST` requiere conservar `ADDR_LO` y `ADDR_HI` mientras las lecturas de operandos reutilizan `MAR/MDR`, y preparar `MDR` antes del pulso de `WR`.
- Las acciones se describen en JSON, con verificador de transiciones, flags conservadas y coherencia de ocho lecturas más una escritura esperadas por R0.4.
- Se actualizan estado portable, decisiones, currículo de hitos, trazabilidad, pruebas previstas, CI y reglas de continuidad. **Aula-16 conserva su bus de 16 bits.**

**Límite:** no se ha construido ROM de control, CPU, circuito ni simulador; ningún reloj o comportamiento eléctrico fue medido.

## R0.4 — 2026-11-05 — Datapath y microoperaciones esperadas

- Se propone microarquitectura de Aula-8 con R0–R3, PC/SP/X, MAR/MDR/IR/SEL, ALU8 y microcontrol independiente de la ROM de firmware.
- Se documentan buses externos de 16 direcciones y 8 datos, control de transacciones y aislamiento de flags de datos frente a acarreo de direcciones.
- Se analiza incremento dedicado del PC frente a uso exclusivo de ALU8; elección sin congelar.
- Se describe fetch lógico y la secuencia de LDI/ST/HALT, además de separar RESET por ROM de modo manual que debe cargar PC.
- Microtraza JSON de **ocho lecturas + una escritura** y verificador de consistencia documental, sin fijar ciclos ni alegar ejecución.

**Límite:** no hay microcódigo ensamblado, CPU lógica simulada ni prueba electrónica física.

## R0.3 — 2026-11-05 — ISA Aula-8 candidata (sin aprobación)

- Se documentan **36 opcodes propuestos** y siete formatos de instrucción para Aula-8, incluyendo memoria absoluta/indexada/SP, pila, saltos y ALU de 8 bits.
- Tres programas originales muestran bytes exactos para depósito manual, suma y un bucle, situados en zona RAM de programa `0x6000`.
- Se especifican reglas candidatas de flags, carry/borrow y pila descendente, todavía sujetas a revisión de R1.
- Se añade JSON autoconsistente y verificador documental que **no** implementa ensamblador, emulador ni CPU.
- Aula-16 no cambia; su bus externo **continúa siendo de 16 bits** y tendrá ISA propia.

**Límite:** el test comprueba opcodes, formatos y ejemplos de bytes, no funcionamiento físico, microcódigo o ejecución de programas.

## R0.2 — 2026-11-05 — Capacidad de ROM/RAM y bootstrap

- Se añade el documento [PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md](simulador-javafx/PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md).
- Se propone una partición contigua de 32768 B de RAM y un presupuesto de 8192 B de firmware, con criterios explícitos de medición posterior.
- Se detalla la carga alternada de editor/ensamblador sobre la CPU, preservación de fuente, salida y pila.
- Se explica el bootstrap: herramientas cruzadas iniciales, ROM preprogramada, cargador, herramientas nativas y persistencia.
- Se añaden riesgos de solapamiento y presupuesto, con pruebas previstas, sin afirmar que existe código compilado.

**Nota:** R0.2 no modifica opcodes ni ABI, no genera el libro y no inicia el simulador.

## R0.1 — 2026-11-05 — Programación desde cero

- Se confirma el editor de líneas y ensamblador **nativos** de Aula-8, ambos en RAM.
- Se conserva compilación cruzada de MiniC como principal; compilador MiniC nativo solo como extensión.
- Se desarrolla una secuencia de aprendizaje desde panel de depósito de bytes y monitor de ROM hasta utilidades cargadas de almacenamiento y un mini sistema.
- Se documentan restricciones de arbitraje del bus, arranque desde EEPROM previamente grabada, propiedad de RAM, retorno a monitor, errores y presupuesto de memoria.
- Se añaden pruebas previstas para panel, editor, dos pasadas del ensamblador, autenticidad de ejecución nativa y persistencia.
- Documento nuevo: [PROGRAMACION_DESDE_CERO.md](simulador-javafx/PROGRAMACION_DESDE_CERO.md).

**Límite:** extensión documental del R0. No se programó firmware, CPU, editor, ensamblador ni interfaz.

## R0 — 2026-11-05 — Respaldo de planificación

- Se fija un solo repositorio para el libro completo y el simulador JavaFX posterior.
- Se conservan las seis tandas de planificación como contexto estructurado.
- Se registran arquitecturas Aula-8 y Aula-16; **Aula-16 con bus externo de datos de 16 bits**.
- Se registra mapa de memoria de 64 KiB, ROM de arranque, buses, flags, pila y alcances de ISA.
- Se documentan tecnología electrónica candidata y límites de certificación.
- Se define currículo de un libro original de seis partes y 24 capítulos previstos.
- Se captura la inspiración del manuscrito *Una Historia en 8 Bits* y las restricciones de derechos.
- Se define taller guiado de construcción 2D/3D, ensambladores, MiniC y firmware.
- Se añade estado portable JSON, AGENTS.md y verificación documental reproducible.

**No incluye:** libro terminado, esquemas físicos definitivos, binarios de CPU, aplicación compilada, publicación GitHub remota ni pruebas de hardware.

