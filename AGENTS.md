# AGENTS.md — continuidad del proyecto Aula-Computadora

Instrucciones para futuros asistentes y colaboradores que trabajen en este repositorio.

**Actualización 11-nov-2026 — primer taller ejecutable:** Marcos autorizó
expresamente comenzar código a pesar de la secuencia histórica «libro,
después app». Se creó el primer corte Java 21/JavaFX/Maven de la etapa
NAND2, con montaje 2D interactivo, inspección conceptual y modelo digital
independiente. Ejecutar y evaluar en Windows según
`simulador-javafx/docs/PRIMER_TALLER_EJECUCION.md`. Este inicio **no
autoriza** alterar ISA, ABI, buses, mapa de memoria, ROM, capítulos ni
declarar CPU/hardware/3D construidos; los límites siguen vigentes. El
contrato visual rector es UX V5 con botones/paneles de radio cero.

**Retroalimentación Windows / R0.2 (11-nov-2026):** Marcos aportó dos
capturas de R0.1 y observó iconos improvisados, franjitas en los paneles,
esquema de chip separado de su carcasa y ausencia de zoom/paneo/3D.
Se programaron vistas/captura revisadas; **la ejecución y apariencia real
de R0.2 todavía deben probarse en Windows**. Conservar el circuito lógico
compartido y no usar más iteraciones artísticas IA como prueba funcional.

**Retroalimentación R0.3:** en cuatro capturas reales de R0.2, Marcos validó
la interacción de zoom/paneo y el potencial de la vista 3D, pero pidió redes
visibles en placa, corregir la triangulación en 3D, símbolos más sobrios,
diálogos completos, paneles laterales plegables y organización de documentos.
R0.3 solo representa **las redes monobit del NAND2**; no añadir buses de una
CPU inexistente. Preservar el histórico de documentación; mover únicamente
archivos cuyo conjunto de enlaces se pueda actualizar de forma segura.

**Retroalimentación R0.4:** un ZIP de Windows confirma 8/8 pruebas JUnit y
ejecución JavaFX R0.3 sin fallos. La nueva captura muestra etiquetas MOS
reflejadas sobre los bloques 3D y patillas casi invisibles. La revisión R0.4
gira la cara del texto y agrega tres terminales metálicos salientes por MOS
en 2D y 3D. Son componentes discretos, **no DIP-8 ni buses de ocho bits**.
La forma exacta del encapsulado sigue conceptual hasta elegir componentes
y verificar sus hojas de datos.

**R0.5 (11-nov-2026):** por petición de Marcos, publicar cambios en el
repositorio de GitHub y reducir las pruebas manuales recurrentes. GitHub
Actions ejecuta automáticamente Java 21/JUnit y el smoke test del circuito.
El Inspector permite explorar A/B→Y y el interior colorea la conducción
ideal de MOS instalados desde el único modelo `Nand2Lesson`; no es prueba
eléctrica real. Las comprobaciones visuales de JavaFX siguen pendientes de
captura real cuando hay cambios relevantes.

**R0.6:** ambas vistas de montaje reciben los mismos bits A/B y Y calculada
en `Nand2Lesson`, colorean las redes definidas por `BoardRouting` y resaltan
MOS activos. MID permanece neutral, sin inferir su nivel. El script de
verificación sin JavaFX comprueba también las rutas y tintas dinámicas;
preservar esta separación entre cálculo lógico y representación.

**Actualización 9-nov-2026 C28-T:** global con 26 capítulos, maestro
Word/PDF **C28-G de 248 páginas**, suplemento secuencial C28-H y atlas
histórico C28-O. La última retroalimentación Windows confirmó **24/24**
controles y cinco fotos auténticas. C28-R genera de una misma topología
**134 NAND** y RTL para ADD/SUB y verifica **131.072 vectores** de ocho bits;
el testbench nuevo aún espera Icarus Windows. C28-S revisa automáticamente
las **248 páginas PDF** (cajas fuera de página: cero) y guarda ocho hojas
de contacto: no equivale a una lectura humana completa. C28-T añade
**dos láminas SVG/PNG** con las nueve NAND del sumador completo y los
134 NAND de ADD/SUB de ocho bits, más un suplemento didáctico y mapa
de inserción para C4/C10/C11. **No hubo nuevas pruebas en C28-T**;
los **28 controles previstos** siguen pendientes de Windows.
**Madurez editorial estimada: 88,5 %**; el Word/PDF C28-G permanece intacto.
Consultar `INFORME_C28_T_DOCUMENTACION_Y_DIAGRAMAS.md`,
`libro/SUPLEMENTO_C28T_DEL_BIT_A_134_NAND.md` y
`libro/PLAN_INSERCION_C28T_SIN_REEDITAR_MAESTRO.md`, además de
`INFORME_C28_S_ALU_Y_REVISION_PDF.md`,
`INFORME_C28_Q_RED_NAND_Y_RTL.md`,
`libro/MATRIZ_CIRCUITOS_C28Q.md` y
`libro/PLAN_CIERRE_EDITORIAL_C28I.md`. El estado C27 descrito enseguida
es histórico; la ISA, las dos políticas de PC y el hardware siguen sin
aprobarse como diseños físicos.

**Referencia histórica:** C27-0.1 (8 de noviembre de 2026), 26 capítulos,
236 páginas maestras, 115 figuras, 110 ejercicios seleccionados (312 en las
fuentes y fascículos). Empezar por `ENTREGA_C27.md`,
`libro/ESTADO_EDITORIAL_C27.md` y `MATRIZ_TRAZABILIDAD_C27.md`. Las entradas
C01–C26 inferiores son un registro histórico y **no sustituyen** esta fecha.

## Prioridad de lectura

1. README.md.
2. CONTEXTO_MAESTRO.md y DECISIONES.md.
3. ARQUITECTURA.md y HOJA_DE_RUTA.md.
4. Documentación específica del área que se modificará.

Estos archivos contienen decisiones de usuario que **no deben cambiarse silenciosamente**. Si una propuesta entra en conflicto con ellas, registrar la alternativa y consultar al usuario.

## Identidad del proyecto

- El usuario es Marcos Moreira, estudiante de Computación en ESPOL, Ecuador.
- Quiere un manual verdaderamente didáctico, de cero a nivel técnico universitario razonable, no un inventario de tecnologías.
- Quiere una computadora original y constructible como modelo educativo, inspirada en la cultura de microcomputadoras de 1970–1980.
- **Aula-8 y Aula-16 son procesadores diferentes**, no simplemente dos temas de un mismo capítulo.
- El futuro programa es un **taller guiado de una computadora prediseñada**, no un clon de Proteus ni un diseñador universal.
- La interfaz 3D se planifica más adelante. **No mencionar JavaFX dentro del libro.**
- El libro terminado y todo el código del programa compartirán **un único repositorio de GitHub**.

## Decisiones que no deben perderse

- Aula-8: registros R0–R3 de 8 bits; bus externo de 8; direcciones de 16.
- Aula-16: registros R0–R3 de 16 bits; **bus externo de 16**; direcciones de 16.
- Ambos: PC/SP/X de 16 bits; indicadores Z/C/N/V; ROM, RAM, E/S mapeada, almacenamiento persistente por bloques.
- Aula-16: memoria direccionable por bytes, dos bancos de 8 bits, little-endian y acceso de palabras alineadas en la primera versión.
- Firmware: ROM con vector de reset y tabla pública de rutinas de entrada estable.
- Software: ensambladores por arquitectura, MiniC-Aula de alcance limitado y mini sistema con monitor de comandos.
- Programación: panel de depósito manual, monitor de ROM, editor de líneas y **ensamblador nativos en Aula-8**. El compilador MiniC nativo es una extensión, pero el MiniC cruzado en anfitrión sí está planificado.
- El reparto R0.2 de ROM 8 KiB y RAM 32 KiB, incluyendo el *overlay* de herramientas, es **provisional**. No afirmar que cabe realmente hasta compilar herramientas y medir mapas de enlace.
- Los opcodes de [ISA_AULA8_CANDIDATA.md](simulador-javafx/ISA_AULA8_CANDIDATA.md) son **PROPUESTA NO APROBADA**. La revisión documental de su JSON no equivale a una CPU ejecutable; no pasar este borrador a hardware, libro o compilador como si estuviera congelado.
- La [microarquitectura Aula-8 R0.4](simulador-javafx/MICROARQUITECTURA_AULA8_BORRADOR.md) es **candidata**, no un netlist o secuencia temporal validada. Sus nueve transacciones son expectativas de un programa, no resultados de ejecución.
- La [unidad de control R0.5](simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md) es **candidata**: fetch, despacho y tres microsecuencias descritas en **acciones lógicas**. El JSON de control no especifica bits de micro-ROM ni ciclos. Latches de dirección `ADDR_LO/HI` son propuestos, no componentes certificados.
- El [control de flujo/pila R0.6](simulador-javafx/CONTROL_FLUJO_PILA_AULA8_BORRADOR.md) también es **candidato**. CALL conserva PC posterior a sus tres bytes, apila retorno bajo en `[SP]` y alto en `[SP+1]` tras decrementar SP dos posiciones; RET lo restaura. Saltos leen dos bytes incluso si no se toman. Las 12 transacciones del ejemplo son expectativas documentales, no ejecución; jamás prometer protecciones físicas de pila aún no diseñadas.
- La [pila/ALU de R0.7](simulador-javafx/PILA_Y_BANDERAS_AULA8_BORRADOR.md) es **candidata**: PUSH/POP usan un byte, PUSHX/POPX dos little-endian; `INC/DEC` conservan C, actualizan Z/N/V. El verificador de fórmulas es prueba matemática, no motor digital ni CPU; conservar esta distinción en futuras tandas.
- El [direccionamiento indexado de R0.8](simulador-javafx/DIRECCIONAMIENTO_INDEXADO_AULA8_BORRADOR.md) es **candidato**: X/SP + desplazamiento firmado8 mediante ALU8 en dos pasadas y acarreo privado; `LD/ST` indexadas tienen tres bytes. Comprobar selector, signo, módulo 65536 y región de memoria; los 526592 contrastes matemáticos no son ejecución digital ni eléctrica. `ADJSP`, ABI y micro-ROM siguen pendientes.
- El [marco de pila y las cinco instrucciones de R0.9](simulador-javafx/AJUSTES_X_SP_Y_MARCOS_AULA8_BORRADOR.md) tienen **microacciones documentales candidatas**, no CPU: LEAX/ADJSP con disp8 firmado, ADDXW con R1:R0, SETSP inmediato16 y XFROMSP. Se realizó contraste matemático en 1572864 casos y traza de escritorio CALL→PUSHX→ADJSP→POPX→RET de 29 lecturas+5 escrituras previstas. La ABI, señales físicas, reserva segura de pila y ejecución de un circuito real continúan pendientes.
- La [ABI candidata R0.10](simulador-javafx/ABI_MINIC_AULA8_R0_10_BORRADOR.md) propone ranuras de parámetros de 2 B, argumentos derecha a izquierda, PUSH alto luego bajo, limpieza a cargo del llamador, X como marco fijo tras salvar X/R2/R3, retorno u16 en R1:R0, FLAGS volátiles. El ejemplo SUMAR_UNO 0x01FF→0x0200 documenta 73 lecturas+10 escrituras y 640 casos de marcos, **sin ejecutar CPU ni MiniC**. No confundir con la ABI pública de ROM ni declararlo aprobado.
- La [ROM y monitor R0.11](simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.md) son **contrato candidato, no firmware**. Tabla pública propuesta FF00–FF7F con 32 ranuras de 4 B, solo 4 asignadas (PUTC/GETC/PUTS/STATUS), JMP absoluto16 little-endian + NOP; E100/E140/E180/E1C0 son destinos didácticos **ficticios**. RESET FFFC–FFFD se ejemplifica con bytes 00 E0→E000. ABI ROM propia: CALL/JMP/RET, preserva R2/R3/X; R0/R1/FLAGS volátiles. POKE/RUN candidato solo 6000–6FFF; RUN termina por RET, no HALT; REG/LOAD siguen no disponibles. El verificador de parser/slots es **documental**, no CPU, ROM grabada ni controlador implementado. Aula-16 conserva bus externo **16 bits**.
- El [almacenamiento R0.12](simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md) **no** es hardware ni cargador nativo. Rango acordado C010–C01F, ocho registros pares de 8 bits, índices de bloque little-endian de 16 bits, READ/WRITE/RESET sobre bloques de 256 B y estados BUSY/DRQ/DONE/ERROR candidatos. LOAD crudo sigue NO DISPONIBLE, pero su sintaxis futura es `LOAD bloque_hex4 destino_hex4 cantidad_hex2` con ventanas alineadas 1000–2FFF o 6000–6FFF; **prohibido ejecutar cargas parciales**. [Modelo Python](scripts/modelo_bloques_aula8_r0_12.py) y 20 pruebas verifican imágenes temporales solo **en anfitrión**, no CPU Aula, EEPROM, tiempos eléctricos, pérdida de energía ni seguridad de programa. No asignar todavía ranuras ROM para bloques ni nombres de archivo.
- El [formato AEX1 R0.13](simulador-javafx/EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md) es **candidato, no ejecutable Aula ni firmware**. Cabecera 32 B delante de payload en bloques 256 B; CPU ID 08, CRC16 para cabecera/payload, tipos 01 práctica (6000–6FFF) y 02 herramienta (1000–2FFF), origen alineado y entrada dentro de payload. `LOADX bloque_hex4` propuesto **no disponible**, independiente del `LOAD` crudo R0.12. 42 pruebas de Python en anfitrión, sin validar instrucciones ni código ejecutable real. **Riesgo abierto**: staging 0200–0FFF tiene 3584 B, menor que el máximo AEX1 de herramienta (8160 B); no prometer carga atómica real sin resolver. Aula-16 mantiene **bus externo de 16 bits**.
- El [modelo LOADX R0.14](simulador-javafx/LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md) **propone una verificación en dos pasadas** para evitar staging completo de 8160 B: CRC incremental de todos los bloques antes de copiar; segunda lectura con copia por máximo 256 B y nueva CRC. 30 pruebas anfitrión, **sin CPU ni firmware**. Fallo segunda pasada puede dejar **RAM parcialmente sobrescrita**; la entrada no debe habilitarse. La atomicidad, estabilidad de la imagen y enforcement de RUN/overlay **siguen PENDIENTES**.
- [Auditoría R0.14](libro/ESTADO_Y_PENDIENTES_R0_14.md) conserva el estado histórico antes de escribir. [Avance C01-0.1](libro/ESTADO_EDITORIAL_C01.md): **capítulo 1 redactado** en Word/PDF con tres diagramas y 12 ejercicios; **23 capítulos pendientes**. No reabrir más series R0 de metadatos como sustituto de escribir. Libro autónomo: no mencionar JavaFX en texto.
- [Avance editorial C02-0.1](libro/ESTADO_EDITORIAL_C02.md): **capítulos 1 y 2 redactados** en Word/PDF con tres diagramas y 12 ejercicios cada uno; **22 capítulos pendientes**. El capítulo 2 utiliza un interruptor NPN 2N3904 (referencia onsemi), cálculo de saturación **estimado** y dos ramas a 5 V. Los dibujos son conceptuales; no se ha construido ni medido el circuito. El siguiente capítulo será «De interruptores a lógica», sin alterar propuestas R0.14 ni adelantar el simulador.
- [Avance editorial C03-0.1](libro/ESTADO_EDITORIAL_C03.md): **capítulos 1–3 redactados** en Word/PDF, con 12 ejercicios por capítulo y 21 pendientes. El capítulo 3 conecta interruptor NPN con NOT/AND/NAND, usa la hoja de datos TI del SN74HCT00N (4,5–5,5 V, VIL hasta 0,8 V, VIH desde 2,0 V) y cuatro figuras originales. **132 controles lógicos/documentales** no equivalen a ensamblaje o medida física. Siguiente: capítulo 4 «Construir funciones con compuertas»; mantener el simulador sin iniciar y R0.14 como referencia teórica.
- [Avance editorial C04-0.1](libro/ESTADO_EDITORIAL_C04.md): **capítulos 1–4 redactados** en Word/PDF, con 12 ejercicios por capítulo y 20 restantes del currículo oficial de 24. El capítulo 4 introduce OR/NOR/XOR, síntesis de XOR con cuatro NAND, simplificación y tabla de ocho filas; cuatro figuras y 146 controles documentales. **No hay montaje físico ni medida de retardos**. Siguiente: capítulo 5 sobre latch SR. El futuro simulador sigue sin iniciar y R0.14 continúa solo como base técnica candidata.
- [Avance editorial C05-0.1](libro/ESTADO_EDITORIAL_C05.md): **capítulos 1–5 redactados** en Word/PDF; quedan 19 del currículo de 24. El capítulo 5 explica dos NAND cruzadas, SET/RESET/HOLD con controles activos en bajo, estado prohibido, 4 figuras y 123 pruebas documentales. **Sin medición física ni simulación de transitorios**. Sigue capítulo 6, sobre memoria temporizada. Se conserva el currículo actual.
- [Avance editorial C06-0.1](libro/ESTADO_EDITORIAL_C06.md): **capítulos 1–6 redactados** en Word/PDF; quedan 18 del currículo numerado. El capítulo 6 trata latch D (LE=1 transparente), flip-flop D de flanco ascendente, reset/preset, setup/hold y clock-to-Q con cuatro figuras; **171 controles documentales**. No afirmar que un circuito físico fue medido ni que conocemos su arranque sin reset. Siguiente: capítulo 7, «Del bit al registro», antes del puente semántico.
- [Avance editorial C07-0.1](libro/ESTADO_EDITORIAL_C07.md): **capítulos 1–7 redactados** en Word/PDF, restan **17** numerados. Capítulo 7: 8 flip-flops, LOAD, mux de realimentación, OE_n, triestado, conducción exclusiva de bus y copia de 0x3C entre A/B; **198502 controles ideales y documentales**, 4 figuras, 12 ejercicios. TI SN74HC377 tiene almacenamiento sin triestado; SN74HC245 tiene triestado sin almacenamiento. Ningún modelo es circuito físico verificado. Sigue el puente semántico intercalado sin renumerar o el capítulo 8, pendiente de decisión editorial.
- Marcos propuso [«Del bit al significado»](libro/PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md) para distinguir tensión, bit, patrón, número, letra, opcode y semántica de programa. Esa propuesta **ya se desarrolló como el interludio P07B** descrito en el punto siguiente. Conservar la decisión de **no renumerar los 24 capítulos sin consentimiento**. La semántica lógica de circuitos, la interpretación convencional de patrones y la POO solo contextual siguen siendo criterios editoriales.
- [Avance editorial P07B-0.1](libro/ESTADO_EDITORIAL_P07B.md): **interludio «Del bit al significado» redactado**, Word/PDF de ocho páginas, cuatro figuras y doce ejercicios; **1383 comprobaciones** de aritmética/archivos. Se ubica entre capítulo 7 y 8 **sin cambiar la numeración de 24 capítulos**, de los cuales 17 quedan pendientes. Explica señal lógica activa en bajo, NAND, `01000001` como 65/A/máscara b6+b0, `11111111` firmado y sin signo, UTF-8, dirección/valor, opcodes dependientes de ISA y POO solo contextual. **Siguiente capítulo 8 «Direcciones y buses»**. No se verificó CPU ni electrónica física.
- [Avance editorial C08-0.1](libro/ESTADO_EDITORIAL_C08.md): **capítulo 8 «Direcciones y buses» redactado**, Word/PDF de 9 páginas, cuatro figuras, doce ecuaciones OMML y doce ejercicios; **459379 comprobaciones matemáticas/documentales**. Dirección 16 bits ≠ datos 8/16 bits; espacio de 64 KiB por bytes **no equivale** a RAM instalada. Decodificador 2→4, CS_n/RD_n/WR_n didácticos, lectura/escritura y contención. Aula-16 mantiene bus externo **16 bits**, dos bancos de 8, little-endian, palabra alineada. Referencias TI SN74HC138 y Alliance Memory AS6C62256; **no** se verificó circuito eléctrico. Llevamos 8 de 24 capítulos numerados más P07B; **16 pendientes**. Siguiente capítulo 9 «RAM y ROM reales».
- [Avance editorial C09-0.1](libro/ESTADO_EDITORIAL_C09.md): **capítulo 9 «RAM y ROM reales» redactado**, Word/PDF de 8 páginas, cuatro figuras, diez ecuaciones OMML y doce ejercicios; **368752 comprobaciones matemáticas/documentales**. AS6C62256 `32K × 8` SRAM: 15 direcciones internas, CE#/OE#/WE#; AT28C64B `8K × 8` EEPROM: 13 direcciones internas y escritura interna en milisegundos. Un mapa ilustrativo 0000–7FFF SRAM, 8000–DFFF sin asignar, E000–FFFF ROM **no es mapa Aula aprobado**; la selección real, tensiones, tiempos y hardware siguen pendientes. Quedan **15 capítulos (10–24)**. Siguiente capítulo 10 «El circuito que suma».
- [Avance editorial C10-0.1](libro/ESTADO_EDITORIAL_C10.md): **capítulo 10 «El circuito que suma» redactado**, Word/PDF de 8 páginas, 4 figuras, 17 ecuaciones OMML y 12 ejercicios. Medio sumador XOR/AND; sumador completo con Cin; cadena de ocho etapas y **13+9=22** con acarreos C1 y C4; `250+10` produce C=1, V=0 y `127+1` C=0, V=1; suma `01FF+0001=0200` en dos pasadas. Referencias TI CD74HC283/SN74HC86, sin ensayos físicos ni tiempos determinados. **786541 controles matemáticos/documentales**; acumulado 10/24 más P07B, 95 páginas, 42 figuras, 132 ejercicios, **14 capítulos pendientes (11–24)**. Siguiente capítulo 11 «La unidad aritmético-lógica»; no congelar banderas ni ISA física con estos modelos.
- [Avance editorial C11-0.1](libro/ESTADO_EDITORIAL_C11.md): **capítulo 11 «La unidad aritmético-lógica» redactado**, Word/PDF de ocho páginas, 4 figuras, 21 OMML y 12 ejercicios. SUB usa `A+NOT(B)+1`; **en la propuesta Aula-8 C=préstamo para resta**, inversión del `Cout` interno, y **C=acarreo para suma**. Comparaciones sin signo leen C/Z; con signo leen N XOR V/Z; `FF` frente a `01` demuestra la diferencia. AND/OR/XOR/NOT y selección por MUX, pero **no se definieron flags de lógica ni una ALU o CPU física**. **786524 controles matemáticos/documentales**; acumulado **11/24 más P07B, 103 páginas, 46 figuras, 144 ejercicios, 151 OMML; 13 pendientes (12–24)**. Sigue capítulo 12 «Arquitectura Aula-8», respetando diseños candidatos.
- [Avance editorial C12-0.1](libro/ESTADO_EDITORIAL_C12.md): **capítulo 12 «Arquitectura Aula-8» redactado**, Word/PDF de nueve páginas, cuatro figuras, 12 OMML y 12 ejercicios. Distingue R0–R3 (8 bits), PC/SP/X/MAR (16), MDR/IR/SEL/TMP (8), bus interno de 8, dirección externa de 16, y control del bus de datos durante RD/WR. Ejemplo **LDI 11 00 2A** que deja PC en 6003 y **12FF+2=1301** por dos pasadas, con `ADDR_CARRY` privado que no altera `FLAGS.C`. Todo es **microarquitectura e ISA candidatas, no ejecución de CPU ni temporización física**. **2752599 verificaciones matemáticas/documentales**; acumulado **12/24 más P07B, 112 páginas, 50 figuras, 156 ejercicios, 163 OMML; 12 pendientes (13–24)**. Sigue capítulo 13 «La unidad de control».
- [Avance editorial C13-0.1](libro/ESTADO_EDITORIAL_C13.md): **capítulo 13 «La unidad de control» redactado**, Word/PDF de ocho páginas, cuatro figuras, ocho OMML y doce ejercicios. Distingue ROM de control de firmware, fetch lógico (MAR/RD/MDR/IR/PC) de duración de reloj física, despacho LDI/ST/HALT y `FAULT` de `PENDING_ROUTE`. El selector de LDI se comprueba antes de escribir; ST retiene `ADDR_LO`/`ADDR_HI`, construye MAR y **recarga MDR con R0 antes de WR**. Las ocho lecturas y una escritura son esperadas, no observadas en CPU. **196771 controles documentales/modelados**; acumulado **13/24 más P07B, 120 páginas, 54 figuras, 168 ejercicios, 171 OMML; 11 pendientes (14–24)**. Sigue capítulo 14 «De números a instrucciones»; ni la ISA ni la micro-ROM están congeladas.
- [Avance editorial C14-0.1](libro/ESTADO_EDITORIAL_C14.md): **capítulo 14 «De números a instrucciones» redactado**, Word/PDF de nueve páginas, cuatro figuras, doce OMML y doce ejercicios. Traduce valores decimales/binarios/hexadecimales, `LDI R0,42` → `11 00 2A`, `ST [0x6F00],R0` → `13 00 00 6F`, modos absoluto/X/SP, `JNZ`, depósito/examen byte a byte y arranque. Distingue **panel con CPU detenida** de monitor en ROM y **HALT** de **RET**. **132993 pruebas de modelos/archivos**, sin CPU ni panel construido; acumulado **14/24 más P07B, 129 páginas, 58 figuras, 180 ejercicios, 183 OMML; 10 pendientes (15–24)**. Sigue el capítulo 15 «La instrucción en movimiento».
- [Avance editorial C15-0.1](libro/ESTADO_EDITORIAL_C15.md): **capítulo 15 «La instrucción en movimiento» redactado**, Word/PDF de ocho páginas, cuatro figuras, doce OMML y doce ejercicios. Recorrido fetch/decode/execute del programa de ocho bytes con PC/MAR/MDR/IR/SEL/TMP, ADDR_LO/HI, ocho lecturas externas y una escritura. La acción `ST_STAGE_DATA` reemplaza el dato `0x6F` leído para la dirección por `0x2A` antes de escribir RAM. **143464 comprobaciones de modelos/archivos**, sin CPU ni ciclos medidos; acumulado **15/24 más P07B, 137 páginas, 62 figuras, 192 ejercicios, 195 OMML; 9 pendientes (16–24)**. Sigue el capítulo 16 «Subrutinas y pila».
- [Avance editorial C16-0.1](libro/ESTADO_EDITORIAL_C16.md): **capítulo 16 «Subrutinas y pila» redactado**, Word/PDF de siete páginas, cuatro figuras, doce OMML y doce ejercicios. CALL `35 10 60` desde `6000` apila retorno `6003` con SP `8000→7FFE` y low/high `03 60`, ejecuta LDI R0,42 y RET vuelve al HALT del llamador; **10 lecturas + 2 escrituras son transacciones candidatas, no ciclos**. Saltos JNZ y anidamiento explicados, **184283 controles de modelos/archivos**. Sigue el capítulo 17.
- [Avance editorial C17-0.1](libro/ESTADO_EDITORIAL_C17.md): **capítulo 17 «Encender una computadora» redactado**, Word/PDF de ocho páginas, cuatro figuras, doce OMML y doce ejercicios. RESET lee `FFFC=00` y `FFFD=E0` para iniciar ilustrativamente en `E000`; ROM `E000–FFFF`, 32 ranuras FF00–FF7F de las que 4 se definen; monitor con HELP/MEM/POKE/RUN, `REG`/`LOAD` sin disponibilidad, `RET` no equivalente a `HALT`. **196727 controles documentales**, no firmware, imagen ROM o CPU ejecutados. Acumulado **17/24 más P07B: 152 páginas, 70 figuras, 216 ejercicios y 219 OMML; 7 pendientes (18–24)**. Próximo capítulo 18 «Hablar con la máquina».
- [Avance editorial C18-0.1](libro/ESTADO_EDITORIAL_C18.md): **capítulo 18 «Hablar con la máquina» redactado**, Word/PDF de ocho páginas, cuatro figuras vectoriales reproducibles, catorce OMML y doce ejercicios. Terminal con `DATA=C000`, `STATUS=C002` candidatos, API `FW_PUTC/GETC/PUTS/STATUS` en FF00/FF04/FF08/FF0C, programa que imprime `A`, eco de carácter, RAM[6F00] y `HOLA\0`. **646 controles documentales**, sin firmware/CPU/terminal ejecutados.
- [Avance editorial C19-0.1](libro/ESTADO_EDITORIAL_C19.md): **capítulo 19 «Guardar y recuperar programas» redactado**, Word/PDF de ocho páginas, cuatro figuras SVG/PNG, quince OMML y doce ejercicios; bloques de 256 bytes, controlador de MMIO C010–C01F, lectura/escritura por modelo anfitrión, `LOAD` crudo y AEX1/`LOADX` candidatos indisponibles. **205037 controles de modelo y documento**. La [escalera de programas](libro/ESCALERA_DE_PROGRAMAS_AULA8.md) añade secuencia variable→suma→Euclides→Fibonacci con puertas de validación y **4113 controles aritméticos en el anfitrión**. Los dibujos se generan con [script común](scripts/generar_diagramas_tecnicos_aula8.py) y [guía de fidelidad](libro/GUIA_DE_FIDELIDAD_DE_FIGURAS.md), **sin netlist ni medición eléctrica**. Acumulado **19/24 más P07B: 168 páginas, 78 figuras, 240 ejercicios y 248 OMML; 5 pendientes (20–24)**. Próximo: capítulo 20.
- [Avance editorial C21-0.1](libro/ESTADO_EDITORIAL_C21.md): redactados **capítulos 20 («Programar un pequeño sistema») y 21 («Qué implica ampliar la palabra»)**, 9 y 8 páginas Word/PDF respectivamente, cuatro figuras originales y 12 ejercicios cada uno, 14 y 18 OMML. El ensamblador Python de dos pasadas funciona **solo en PC** y produce 13 bytes de suma y 29 de Euclides; las 130685 comprobaciones C20 no son ejecución de CPU. La aritmética de 16 bits y banderas C21 supera 126921 comprobaciones, conservando **16 bits de direcciones, 64 KiB direccionados por byte y bus externo Aula-16 de 16 bits**. **Acumulado 21/24 + P07B: 185 páginas, 86 figuras, 264 ejercicios y 280 OMML; faltan 22–24 y el volumen maestro**. Regenerar esquemas con [script C20/C21](scripts/generar_diagramas_capitulos_20_21.py). **No afirmar que existen CPU, monitor nativo, hardware o simulador JavaFX**.
- **[Contrato lógico de vídeo V1 CONGELADO por delegación de Marcos](simulador-javafx/CONTRATO_VIDEO_AULA_V1.md)** (2026-11-08): una **única pantalla** en texto o bitmap, consola C000/C002 conservada, **registros C020/C022/C024/C026/C028/C02A de 8 bits**, direcciones impares sin alias, VRAM **indirecta** separada de la RAM CPU: **512 B de texto + 8192 B de gráficos (256×128×2bpp, cuatro colores)** y **ROM de glifos de 2 KiB**. Modos exclusivos, buffers se conservan, RESET texto, sin atribuir inicialización automática de RAM. Acceso al banco y autoincremento mediante CTRL, sin nuevas instrucciones gráficas ni entradas ROM públicas. **Aula-16 mantiene bus externo 16 bits** y usaría el mismo periférico con acceso de byte. [JSON estructurado](simulador-javafx/VIDEO_AULA_V1_CONTRATO.json) y [prueba del contrato](scripts/verificar_contrato_video_aula_v1.py) **documentales, no hardware**.
- El [cuestionario original](simulador-javafx/CUESTIONARIO_MAPA_VIDEO_MMIO.md) y la [propuesta previa](simulador-javafx/PROPUESTA_VIDEO_TEXTO_GRAFICOS_ROM.md) son **históricos y fueron superados**. No reutilizar 4 KiB mono/VRAM compartida como decisión actual. Distinguir **µROM**, **ROM de firmware** y **ROM de caracteres**. Los **modos de direccionamiento ISA** (inmediato, absoluto, X+disp, SP+disp) no son el mapa MMIO ni el offset interno de VRAM; la ISA sigue pendiente. [Interludio P23V](libro/PLAN_INTERLUDIO_P23V_TEXTO_GRAFICOS_TIPOGRAFIA.md) solo **planificado**, no capítulo escrito; el estado actual de capítulos está en el avance C23.
- [**Avance C23-0.1**](libro/ESTADO_EDITORIAL_C23.md): capítulos 22 «Un bus externo de 16 bits» y 23 «Programación para Aula-16» redactados en ocho páginas Word/PDF cada uno, 4 figuras SVG/PNG y 12 ejercicios por capítulo, 13+14 OMML. **142737+77951** verificaciones de modelo y documentación en anfitrión. Los bancos RAM se modelan como 16 KiB bajos y 16 KiB altos (total 32 KiB), los accesos de palabra se alinean a par y los bytes impares usan el carril alto; no confundir dirección de CPU con offset VRAM. Los programas Aula-16 prueban suma, Euclides y Fibonacci **sin binario Aula-16** (ISA/ABI incompletas). **Acumulado 23/24 más P07B: 201 páginas, 94 figuras, 288 ejercicios y 307 OMML; falta el capítulo 24, el interludio P23V y la edición maestra**. Los 16 acuerdos de vídeo V1 siguen congelados, no se ha construido controlador, CPU, microcódigo, ROM ni aplicación JavaFX.
- [**Avance C24-0.1: estado vigente**](libro/ESTADO_EDITORIAL_C24.md): **24/24 capítulos numerados y dos interludios P07B/P23V redactados y maquetados individualmente**, 220 páginas, 105 figuras, 312 ejercicios resueltos y 333 OMML. P23V tiene 10 páginas/7 figuras, C24 tiene 9 páginas/4 figuras; 66576 verificaciones de coordenadas, glifos, convenio MMIO y documentos. Se mantiene el **contrato lógico de vídeo V1 sin cambio**: una pantalla de dos modos excluyentes, text 32×16, bitmap 256×128 2bpp, seis registros en C020–C02A y ROM de caracteres de capacidad 2 KiB, cuyos bytes concretos no se han escrito. **Faltan libro maestro, revisión transversal y desarrollo de simulador, ISA final, firmware y hardware.** No confundir «24/24 manuscritos» con proyecto completo.
- [**Avance C25-0.1: estado histórico**](libro/ESTADO_EDITORIAL_C25.md): el primer libro maestro Word/PDF de 225 páginas conservaba los 24 capítulos y dos interludios, **105 figuras, 333 ecuaciones OMML, 312 ejercicios**, índice paginado y 24 fuentes. Esa versión no se borra.
- [**Avance C26-0.1: estado editorial vigente**](libro/ESTADO_EDITORIAL_C26.md): los dos interludios pasan a titularse **capítulos 7B y 23B** sin renumerar los 24 troncales. Volumen de lectura con **156 ejercicios esenciales resueltos**, conservando 312 en los fascículos. **106 figuras**, incluida protoboard y buses Aula-16 por carriles; se corrigieron etiquetas superpuestas y potencias `16⁰`. Referencias externas agrupadas en `FUENTES_CONSULTADAS.txt`. Se requiere todavía revisión humana integral, licencia, portada/ilustraciones históricas y todo el hardware, firmware y simulador.
- Construcción virtual: transistor, compuerta, latch, bit, byte, registro, ALU, CPU; módulos reutilizables y vista bajo demanda.
- Se recomienda empezar físicamente por circuitos pequeños, y usar SRAM/EEPROM comerciales para equipos completos.
- Para operaciones que afecten al hardware real, verificar hoja de datos, límites de tensión/corriente, temporización y esquema.

## Reglas de trabajo

1. No declarar «validado físicamente» nada que solo haya superado una tabla de verdad o simulación digital.
2. Proponer antes de implementar cambios que afecten ISA, buses, mapa de memoria, ABI, firmware público o currículo.
3. Mantener una **fuente de verdad** para componentes, terminales y conexiones; no duplicar un «circuito de dibujo» distinto del de simulación.
4. El libro explica objetos y mecanismos; comentarios de producción, progresos de agentes y herramientas pertenecen a informes o registros técnicos.
5. No reproducir contenido protegido de *But How Do It Know?*. Las ideas didácticas del manuscrito coescrito por Marcos y Fernando deben reescribirse y sus ilustraciones/derechos comprobarse.
6. Aplicar el estándar editorial suministrado: precisión, progresión de prerrequisitos, prosa natural, imágenes exactas, tablas y ejemplos justificados.
7. No iniciar una aplicación 3D o un compilador antes de las tareas de libro priorizadas en HOJA_DE_RUTA.md sin nueva instrucción explícita.
8. Registrar fuentes, decisiones y casos límite antes de que se pierdan en el chat.
9. Al afirmar que un editor, monitor o ensamblador es «nativo», exigir que se ejecute como código máquina de Aula; una utilidad implementada solo en Java es una herramienta del anfitrión.
10. Conservar las modificaciones del usuario; no realizar limpiezas destructivas.
11. Entregar comandos reproducibles para Windows/PowerShell cuando haya artefactos de software que probar.

## Convenciones de estado

- **CONFIRMADO:** decisión explícita del usuario o acuerdo ya fijado.
- **DISEÑO BASE:** propuesta de ingeniería adoptada para planificar; su implementación requiere especificación.
- **PENDIENTE:** requiere selección, cálculo, prototipo o pruebas antes de declararse definitiva.
- **FUERA DE ALCANCE V1:** no comprometer para la primera entrega.

El 100 % de preproducción significa **plan decidido**, no «código o electrónica terminados».

