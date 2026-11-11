# Registro de decisiones

## Decisiones editoriales C26-0.1 — 2026-11-08

- **CONFIRMADO por el autor:** convertir las secciones antiguamente llamadas interludios en capítulos sin cambiar su contenido fundamental. Adoptada la numeración complementaria **7B y 23B**, que preserva las referencias a los 24 capítulos originales.
- **CONFIRMADO por el autor:** referencias bibliográficas sin interrumpir repetidamente la enseñanza. Inventario `FUENTES_CONSULTADAS.txt` y bibliografía única al final de la edición de lectura.
- **DISEÑO BASE de maquetación:** seis ejercicios esenciales con solución en cada uno de los 26 capítulos del libro maestro. Los doce por capítulo se conservan completos en los fascículos y el Markdown, de modo que el material de trabajo no se pierde.
- **CONFIRMADO por el autor:** arreglar diagramas y la notación de exponentes, añadir esquemas cuando explican realmente una conexión física o el ancho de un bus. C01 incorpora protoboard y C22 distingue carriles y selección de bancos; no se alteran señales ni arquitectura física aprobada.
- **PENDIENTE:** cubierta ilustrativa, iconografía histórica, permisos y lectura final de estilo. Ninguna imagen del circuito constituye montaje validado.


Convenciones: **CONFIRMADO** por el usuario, **DISEÑO BASE** adoptado en la planificación, **PENDIENTE** de cálculo/prototipo/especificación y **FUERA DE ALCANCE V1**.

| ID | Estado | Decisión y consecuencia |
| --- | --- | --- |
| D-001 | CONFIRMADO | Un único repositorio GitHub contendrá libro completo y futuro programa. |
| D-002 | CONFIRMADO | Crear primero respaldo de contexto; elaborar después el libro; construir JavaFX bastante después. |
| D-003 | CONFIRMADO | El libro debe ser independiente y **no mencionar JavaFX en su texto**. |
| D-004 | CONFIRMADO | Dos CPU originales: Aula-8 y Aula-16, desde transistores a microprogramas. |
| D-005 | CONFIRMADO | **Bus externo Aula-16 de 16 bits**, no 8. |
| D-006 | CONFIRMADO | Simulador guiado de una computadora prediseñada; no clon general de Proteus. |
| D-007 | CONFIRMADO | Dos modos: computadora construida explorable / hazla tú mismo por etapas. |
| D-008 | CONFIRMADO | Modulación semántica: transistor -> bit -> byte -> registro -> CPU; 2D y 3D, luminosidad según estado. |
| D-009 | CONFIRMADO | Modelo de teclado, pantalla y almacenamiento fijo; foco en CPU, RAM, ROM y controladores indispensables. |
| D-010 | CONFIRMADO | Libro original en español, tono narrativo didáctico, estándar editorial suministrado. |
| D-011 | DISEÑO BASE | Aula-8: R0–R3 de 8, PC/SP/X de 16, direcciones de 16 y bus de datos de 8. |
| D-012 | DISEÑO BASE | Aula-16: R0–R3 y ALU de 16, PC/SP/X de 16, direcciones de 16 y datos externos de 16. |
| D-013 | DISEÑO BASE | Memoria byte-addressable; mapa de 64 KiB; ROM 8 KiB y RAM 32 KiB iniciales. |
| D-014 | DISEÑO BASE | Aula-16 little-endian, bancos par/impar, palabras alineadas, carril de bytes bidireccional. |
| D-015 | DISEÑO BASE | Flags Z, N, C, V; semántica exacta por operación se completa en especificación ISA. |
| D-016 | DISEÑO BASE | Control microprogramado de microoperaciones; ROM de control separada de ROM del sistema. |
| D-017 | DISEÑO BASE | Polling primero. Interrupciones opcionales posteriores. |
| D-018 | DISEÑO BASE | Tabla pública de servicios de ROM con entradas de 4 B a partir de 0xFF00; reset en 0xFFFC. |
| D-019 | DISEÑO BASE | Ensambladores cruzados para arranque y comparación, y compilador MiniC-Aula en anfitrión; los binarios se ejecutan en Aula-8 o Aula-16. Coexisten con el ensamblador nativo acordado en D-036. |
| D-020 | DISEÑO BASE | MiniC limitado: u8, u16, char, arrays fijos, funciones, locales, if/while/for; sin ISO C completo. |
| D-021 | DISEÑO BASE | Firmware monitor básico y almacenamiento digital por bloques de 256 B. |
| D-022 | DISEÑO BASE | Fuente de alimentación regulada de baja tensión, 5 V inicial, conforme a hojas de datos. |
| D-023 | DISEÑO BASE | 74HCT preferida en interfaces con memorias TTL-compatibles; no asumir equivalencia HC/HCT. |
| D-024 | DISEÑO BASE | Simulación digital jerárquica con advertencias eléctricas básicas, no solucionador analógico general. |
| D-025 | DISEÑO BASE | Java 21 + JavaFX + Maven; monolito modular por paquetes, núcleo probado sin interfaz. |
| D-026 | DISEÑO BASE | Libro: una obra de seis partes, unos 24 capítulos, Word + PDF, diagramas originales. |
| D-027 | DISEÑO BASE | Verificación por niveles: documentado, lógico, integrado y validado físicamente. |
| D-028 | PENDIENTE | ISA: asignación exacta de opcodes, bytes/palabras, flags para cada instrucción, microcódigo y ciclos. |
| D-029 | PENDIENTE | ABI definitiva, instrucciones SP-relativo, parámetros y retorno, datos u16 en Aula-8. |
| D-030 | PENDIENTE | BOM final, circuitos discretos, fuente, consumo, temporización y pruebas de oscilación/metastabilidad. |
| D-031 | PENDIENTE | Terminal físico concreto, esquema de interfaz, pinout y controlador de bloques. |
| D-032 | PENDIENTE | Formato exacto del MiniSO, directorio, archivos y artefactos ejecutables. |
| D-033 | PENDIENTE | Licencia para GitHub: verificar coautorías e imágenes de terceros antes de publicar. |
| D-034 | PENDIENTE | URL/nombre remoto y visibilidad del repositorio GitHub. |
| D-035 | FUERA DE ALCANCE V1 | Diseñador electrónico libre, simulación SPICE, GPU/ray tracing, C ISO completo, multiproceso, red o VGA. |
| D-036 | CONFIRMADO | Aula-8 contará con **editor primitivo de líneas y ensamblador nativos**, cargados en RAM; su código se ejecutará en el propio procesador Aula. |
| D-037 | DISEÑO BASE | Programación gradual: depósito manual byte a byte, monitor ROM por terminal, editor/ensamblador nativos, almacenamiento y mini sistema. La versión física del panel requiere diseño eléctrico posterior. |
| D-038 | FUERA DE ALCANCE V1 | Compilador **MiniC-Aula nativo** dentro de la microcomputadora. La compilación cruzada de MiniC sigue siendo el camino principal de V1. |
| D-039 | PENDIENTE | Contrato de `RUN`/`HALT`/retorno al monitor, propiedad del bus detenido, carga de utilidades, tamaños de binario, partición de RAM, formato de archivos y presupuesto efectivo de los 8 KiB de ROM. |
| D-040 | DISEÑO BASE | Propuesta de **overlay** en RAM: editor y ensamblador nativos se cargan alternativamente en una región común de hasta 8 KiB; conservar la fuente y salida en regiones separadas. Validación real pendiente. |
| D-041 | PENDIENTE | Verificar con imágenes reales que monitor y cargador entran en ROM 8 KiB; comprobar límites de editor, ensamblador, fuente, tabla de símbolos, binario y pila sobre RAM 32 KiB. |
| D-042 | PENDIENTE | ISA Aula-8 propuesta R0.3: 36 opcodes de 8 bits, registro/modo en byte adicional, palabras little-endian y modos absoluto/X/SP. **No aprobada ni congelada.** |
| D-043 | PENDIENTE | Banderas Aula-8 candidatas: `C=préstamo` en resta y `C=acarreo` en suma; LD/MOV/índice conservan flags; INC/DEC conservan C. Validar circuito, condiciones de overflow y MiniC antes de adoptar. |
| D-044 | PENDIENTE | ABI Aula-8 candidata: SP descendente inicial `0x8000` como siguiente posición libre, `CALL`/`RET` apilan retorno little-endian y parámetros iniciales en ranuras de 2 B. Pendiente de revisión y pruebas. |
| D-045 | PENDIENTE | Datapath Aula-8 R0.4 propuesto: bus interno de 8 bits; MAR16/MDR8/IR8/SEL8; flags de datos separados de acarreo temporal de direcciones. Requiere esquema y validación. |
| D-046 | PENDIENTE | Para incrementar PC16, preferencia provisional por incrementador dedicado; X/SP y direcciones efectivas mediante dos pasadas ALU8. Comparar costo de compuertas y microestados frente a reutilizar ALU8 para todo. |
| D-047 | PENDIENTE | RESET lee vector en ROM; modo panel detenido necesita arbitraje de bus y **mecanismo explícito de carga de PC** para ejecutar RAM. Aún no se ha diseñado el circuito físico. |
| D-048 | PENDIENTE | Control de Aula-8 R0.5: fetch compartido y despacho por `IR` a microsecuencias propuestas para LDI, ST absoluto y HALT. **Acciones lógicas, no microinstrucciones codificadas ni ciclos medidos.** |
| D-049 | PENDIENTE | Para `ST` absoluto se proponen latches `ADDR_LO` y `ADDR_HI` (o almacenamiento equivalente): leer el siguiente operando sobrescribe `MAR/MDR`; antes de activar `WR`, cargar `MAR` con dirección final y `MDR` con el dato del registro. |
| D-050 | PENDIENTE | Unidad de control debe mantener ROM interna distinta de firmware ROM; anchura de palabra, capacidad de µROM, despacho físico, reloj y líneas definitivas **sin determinar**. `HALT` detiene sin retorno automático al monitor. |
| D-051 | PENDIENTE | R0.6 conserva la convención **candidata** de CALL/RET R0.3: SP descendente en dos bytes, retorno bajo en `[SP]` y alto en `[SP+1]`, sin limpiar RAM al hacer RET. Requiere prueba en CPU. |
| D-052 | PENDIENTE | Se proponen `RET_LO/RET_HI` temporales para no destruir dirección de retorno al escribir/leer pila. Los latches `ADDR_LO/ADDR_HI` pueden reutilizarse como destino; número real de chips sin fijar. |
| D-053 | PENDIENTE | JMP/JZ/JNZ/JC/JNC leen ambos bytes de destino incluso si salto no tomado. Rutas lógicas en JSON, sin microcódigo binario, protección física de pila ni ciclos establecidos. |
| D-054 | PENDIENTE | R0.7 conserva `PUSH`/`POP` de 1 byte (decremento SP antes de escribir, incremento después de leer) y `PUSHX`/`POPX` de 2 bytes little-endian, como convenio candidato compatible con CALL/RET. |
| D-055 | PENDIENTE | `INC/DEC` calculan Z/N/V pero **conservan C**. R0.7 aporta vectores y contraste matemático, no ALU implementada. `ADD/ADC` producen carry; `SUB/SBC/CMP` producen **borrow** en C. |
| D-056 | PENDIENTE | Verificación de pila, flags y microacciones sigue siendo documental, sin protección física de stack, frecuencia, micro-ROM codificada ni CPU ejecutada. |
| D-057 | PENDIENTE | R0.8 propone `LD/ST` por X+disp8 y SP+disp8, desplazamiento firmado de −128 a +127, codificación de tres bytes y selectores `0x04–0x0B` de la ISA candidata. No están aprobados. |
| D-058 | PENDIENTE | Dirección efectiva de 16 bits mediante dos pasadas ALU8, extensión de signo y acarreo privado `ADDR_CARRY`. El cálculo se realiza módulo 65536 sin modificar X, SP ni Z/N/C/V; el decodificador de memoria determina si el acceso es válido. |
| D-059 | PENDIENTE | `SETX` y `LD/ST` indexado cuentan con microacciones documentales. `ADJSP`, `LEAX`, ABI de marcos, ciclos reales, micro-ROM binaria, memoria/CPU implementadas y protecciones de acceso permanecen pendientes. |
| D-060 | PENDIENTE | R0.9 concreta microacciones **candidatas** de `LEAX` (`15`), `ADDXW` (`16`), `SETSP` (`17`), `ADJSP` (`18`) y `XFROMSP` (`19`), conforme a los bytes reservados en R0.3; no hay implementación digital ni micro-ROM. |
| D-061 | PENDIENTE | `ADDXW` suma a X la palabra de 16 bits `R1:R0` (R1 alto, R0 bajo), módulo 65536, usando dos pasadas de ALU8 y acarreo privado; LEAX y ADJSP extienden disp8 con signo. Ninguna modifica Z/N/C/V. |
| D-062 | PENDIENTE | Ejemplo de función: CALL reserva retorno, PUSHX conserva X, XFROMSP lo usa de marco, ADJSP−1 reserva un local, POPX y RET restablecen X y SP. Esta disposición **no** congela la ABI de parámetros o retorno de valores. |
| D-063 | PENDIENTE | SETSP puede cargar el sentinela inicial 0x8000, pero escribir allí sería inválido: RAM acaba en 0x7FFF. No hay protección de pila, privilegios, validación eléctrica ni garantías de acceso al variar SP/X. |
| D-064 | PENDIENTE | Las 1572864 sumas de R0.9 y su traza de escritorio de 29 lecturas/5 escrituras comprueban consistencia matemática/documental, no una CPU ejecutando instrucciones ni pruebas físicas. |
| D-065 | PENDIENTE | ABI R0.10 **candidata**: hasta cuatro parámetros en ranuras de dos bytes, incluso u8/char con byte alto cero; llamador empuja de derecha a izquierda, y dentro de cada argumento empuja alto antes que bajo. |
| D-066 | PENDIENTE | El llamador retira sus parámetros mediante ADJSP tras RET; retornos u8/char en R0, u16 en R1:R0; R0/R1 y FLAGS volátiles, R2/R3/X preservados por la función. No congelar sin pruebas reales. |
| D-067 | PENDIENTE | Para V1 se propone prólogo fijo PUSHX/PUSH R2/PUSH R3/XFROMSP y ADJSP -L; epílogo inverso. X+0..X+3 guarda R3/R2/X, X+4..X+5 retorno, X+6.. parámetros; locales X-L..X-1. Esta disposición es contrato candidato específico de MiniC, no la ABI de firmware. |
| D-068 | PENDIENTE | R0.10: programa u16 SUMAR_UNO(0x01FF) espera R1:R0=0x0200, SP=0x8000, X/R2/R3 restaurados, 63 bytes de código, 73 lecturas+10 escrituras; solo modelo de escritorio y validación documental. |
| D-069 | PENDIENTE | Profundidad recursiva idealizada de 409 niveles para un caso de 10 bytes/nivel en 4096 bytes de pila NO equivale a límite seguro ni protección hardware. Confirmar ABI, stack, parámetros y servicios ROM en R1. |
| D-070 | PENDIENTE | R0.11 propone reservar 32 ranuras de ROM pública de 4 B entre 0xFF00 y 0xFF7F; solo FW_PUTC, FW_GETC, FW_PUTS y FW_STATUS ocupan las cuatro primeras. Otras posiciones **no son invocables** hasta asignar ABI. RESET permanece en 0xFFFC–0xFFFD. |
| D-071 | PENDIENTE | Cada ranura Aula-8 candidata codifica JMP absoluto16 little-endian en 3 B + NOP de relleno. Los destinos E100/E140/E180/E1C0 son **ilustrativos**, no rutinas ROM compiladas. Aula-16 seguirá con ISA y ROM separadas, **bus externo 16 bits**. |
| D-072 | PENDIENTE | ABI ROM candidata distinta de MiniC: entrada CALL a la ranura, salto interno JMP, salida RET, R2/R3/X preservados, R0/R1/FLAGS volátiles, argumentos simples por R0 o X según servicio. No implica que firmware use marcos MiniC. |
| D-073 | PENDIENTE | Monitor R0.11 candidato: MEM solo lee RAM o ROM sin cruzar regiones, POKE interactivo limitado a ventana de práctica 0x6000–0x6FFF, RUN hace CALL a la misma ventana; RET equilibrado vuelve al prompt, HALT detiene CPU y exige RESET/depuración. No existe parser ni mecanismo de recuperación probado. |
| D-074 | PENDIENTE | REG requiere captura fiable de registros y LOAD exige controlador de bloques crudos; R0.11 los marca NO DISPONIBLE, sin fingir implementación. FW_STATUS propone bits RX/TX de **API**, todavía sin fijar codificación eléctrica de registro MMIO. |
| D-075 | PENDIENTE | R0.12 concreta como **candidatos** ocho registros de 8 BITS en direcciones pares C010–C01E: COMMAND, STATUS, BLOCK_LO/HI, DATA, ERROR y COUNT_LO/HI. Preservar terminal C000/C002 y no usar las direcciones impares como alias. |
| D-076 | PENDIENTE | Protocolo candidato: bloques crudos de 256 B, índice little-endian de 16 bits; COMMAND NOP=00, READ=01, WRITE=02, RESET=03; STATUS BUSY=01, DRQ=02, DONE=04, ERROR=08. Transferencia completada exactamente a 256 bytes, COUNT=0100. No se ha medido hardware ni reloj real. |
| D-077 | PENDIENTE | Modelo anfitrión de R0.12 descarta escritura parcial antes de 256 bytes, aborta por comando/cambio de bloque durante BUSY, conserva código de error y verifica reapertura de archivo. Sustitución temporal del archivo **no** prueba tolerancia a cortes eléctricos ni controlador físico. |
| D-078 | PENDIENTE | Futuro LOAD crudo, NO IMPLEMENTADO: `LOAD bloque_hex4 destino_hex4 cantidad_hex2`, máximo 32 bloques alineados a 256 B, y solo ventanas RAM 1000–2FFF (overlay) o 6000–6FFF (programa), sin desbordamiento ni invasión de pila/ROM. |
| D-079 | PENDIENTE | El cargador deberá preparar un bloque completo en búfer antes de copiarlo a RAM; una carga de varios bloques **no es atómica**. En error parcial nunca ejecutar. El overlay requerirá una entrada supervisada separada de RUN R0.11. |
| D-080 | PENDIENTE | R0.12 no asigna ranuras ROM adicionales ni inventa archivos por nombre: formato de ejecutable, directorio, checksums, protección ante fallos físicos y binarios nativos verificables siguen en R1/R5. Aula-16 mantiene **16 bits externos**. |
| D-081 | PENDIENTE | R0.13 propone formato **AEX1** para Aula-8: cabecera de 32 B al inicio del primer bloque crudo de 256 B; payload inmediato y relleno de ceros; firma `AEX1`, versión 01 y CPU ID 08. **No es sistema de archivos ni contrato aprobado**. |
| D-082 | PENDIENTE | La cabecera AEX1 propone tipo 01 (práctica en 6000–6FFF) o 02 (herramienta en overlay 1000–2FFF), origen alineado 256 B, entrada dentro del payload, tamaño útil de 1..4064/8160 B respectivamente y número de sectores calculado. No asignar otros tipos ni RAM. |
| D-083 | PENDIENTE | AEX1 propone CRC-16/CCITT-FALSE del payload y otro CRC del encabezado 00–11 (offsets hex); reservas y relleno a cero. **CRC no es autenticación**, ni valida instrucciones CPU. |
| D-084 | PENDIENTE | `LOAD` crudo de R0.12 conserva sintaxis y sigue NO DISPONIBLE; nuevo `LOADX bloque_hex4` futuro debe comprobar **todos** los bloques y campos AEX1 antes de copiar su payload. No modifica MMIO, mapa ROM ni tabla pública de servicios. |
| D-085 | PENDIENTE | La prevalidación integral del paquete AEX1 se probó solo en **host Python** (42 pruebas). RAM 0200–0FFF tiene 3584 B y **no contiene** un AEX1 de herramienta de 8160 B: el mecanismo real de staging, rollback y protección de código residente sigue abierto. No atribuir atomicidad total al hardware. |
| D-086 | PENDIENTE | Una carga de herramienta AEX1 no puede usar el RUN restringido a 6000–6FFF de R0.11; requiere entrada supervisada independiente. Ningún paquete se ejecuta automáticamente tras cargar y ningún byte de código está validado aún por CPU Aula. |
| D-087 | PENDIENTE | Aula-16 conserva bus externo **16 bits**, ISA y ejecutables separados. AEX1 versión 01 con CPU ID=08 se rechaza si el destino es otra arquitectura; no prometer AEX1 como formato universal. |
| D-088 | PENDIENTE | LOADX R0.14 **propone** verificar AEX1 con CRC16 **incremental** en una primera lectura y copiar payload durante una segunda lectura, usando temporal máximo de 256 B. No necesita almacenar los 8160 B en el búfer de 3584 B. Solo modelo de anfitrión. |
| D-089 | PENDIENTE | Fallo de primera pasada: **cero modificaciones de RAM**. Fallo tardío en segunda pasada: **puede quedar RAM parcial**, y el modelo rechaza habilitar entrada. La copia **NO es atómica** ni garantiza recuperación ante corte/archivo cambiante o enforcement real de RUN en ROM. |
| D-090 | PENDIENTE | Confirmar la ejecución supervisada desde ROM, la invalidación efectiva del código tras error, protección del overlay y política de recarga antes de poner LOADX en firmware o asignar tabla pública ROM. |
| D-091 | CONFIRMADO | El libro sigue siendo el producto prioritario: **24 capítulos originales en seis partes**, independientes de la aplicación, Word editable + PDF. R0.14 deja la auditoría editorial; seguir creando contratos R0 no sustituye redactar capítulos y probar figuras. |
| D-092 | CONFIRMADO | El **libro** explicará el paso de *text mode* a *graphics mode*, mapas de caracteres, píxeles, ROM de glifos, fuentes tipográficas y evolución hacia interfaces gráficas; no implica desarrollar Windows ni una GPU. El alcance está propuesto en [P23V](libro/PLAN_INTERLUDIO_P23V_TEXTO_GRAFICOS_TIPOGRAFIA.md), todavía **no redactado**. |
| D-093 | DISEÑO BASE | Distinguir **µROM** (microcontrol), **ROM de firmware** (código y rutinas CALL/RET) y **ROM de glifos** (patrones de caracteres, si se integra vídeo). Una terminal externa puede conservar su fuente fuera de Aula-8; no confundir `PUTC` con dibujar píxeles. |
| D-094 | DISEÑO BASE | Un eventual vídeo de píxeles se modelará como **periférico separado con VRAM/controlador**. La CPU puede usar instrucciones normales de memoria, ALU y bits; **no se requieren opcodes gráficos**, ni se cambian ahora ISA, ROM de 8 KiB o mapa E/S. Tampoco equivale a aprobar hardware, tarjeta GPU o VGA. |
| D-095 | CONFIRMADO | **Delegación expresa de Marcos (2026-11-08):** congelar el diseño lógico de vídeo. **Una única pantalla** comparte consola existente (`C000/C002`) y presentación de texto o bitmap seleccionable; no se crean dos monitores ni se reemplaza la API de firmware de entrada/salida. [Contrato de vídeo V1](simulador-javafx/CONTRATO_VIDEO_AULA_V1.md). |
| D-096 | CONFIRMADO | Vídeo Aula V1: 32×16 celdas de texto, **1 byte por carácter**, glifos 8×8, **ROM de 256 glifos = 2048 B separada de firmware**, buffer texto **512 B**. Repertorio extendido incluirá acentos/semigráficos cuando se definan sus bytes; **no** requiere UTF-8 dentro de vídeo. |
| D-097 | CONFIRMADO | Vídeo gráfico Aula V1: resolución 256×128, **2 bits/píxel = cuatro índices de paleta**, bitmap **8192 B**, almacenado por separado del texto. **RAM de vídeo total = 8704 B**; los dos buffers sobreviven a cambio de modo. Monocromo 1bpp queda como **ejemplo pedagógico del libro**, no tercer modo hardware V1. |
| D-098 | CONFIRMADO | No introducir opcodes gráficos, ni reservar nuevas ranuras en la ROM pública `FF00–FF7F`. `FW_SETMODE`/`FW_PLOT` siguen **ideas futuras**; el acceso gráfico se enseña mediante `LD/ST` y MMIO, con biblioteca RAM opcional. Tampoco quedan aprobados VGA, GPU ni electrónica de vídeo física. |
| D-099 | CONFIRMADO | La VRAM **no** se mapea en la RAM CPU ni en `8000–BFFF`; se controla indirectamente mediante **seis registros de byte en direcciones pares C020/C022/C024/C026/C028/C02A**, con C02C/C02E pares reservados e impares sin alias. La terminal C000/C002 y bloques C010–C01F no cambian. |
| D-100 | CONFIRMADO | Vídeo MMIO V1: `VIDEO_MODE` 00=texto/01=2bpp, `STATUS` READY bit0 y ERROR persistente bit7, `ADDR_LO/HI` desplazamiento local, `DATA` R/W y `CTRL` con autoincremento opcional, banco de acceso independiente del modo visible, FG/BG de texto y borrado explícito de ERROR. Codificación exacta en [JSON](simulador-javafx/VIDEO_AULA_V1_CONTRATO.json). |
| D-101 | CONFIRMADO | RESET lógico selecciona texto y reinicia registros/cursor; **no** inventar RAM de vídeo inicialmente a cero. La inicialización se hace por software; cambiar de modo **no borra** buffers. La salida de terminal al buffer de texto continúa aunque el bitmap esté visible; el protocolo exacto de controles/scroll sigue pendiente. |
| D-102 | CONFIRMADO | Los *modos de direccionamiento* (inmediato, absoluto, X+disp, SP+disp) son mecanismos de la **ISA** para calcular la dirección efectiva CPU; la elección `C020` compete al **mapa/decodificador de dispositivos**, y la dirección 0000–1FFF de VRAM es un **espacio indirecto distinto**. Congelar vídeo **no** aprueba opcodes ni micro-ROM. |
| D-103 | CONFIRMADO | Aula-16 usará en el futuro el mismo bloque de registros de **8 bits**, mediante accesos de byte compatibles con su bus externo **16 bits** y selección de carril correcta. El contrato V1 solo está **documentado y probado matemáticamente**; sin hardware, temporización ni simulador completo. |
| D-104 | CONFIRMADO | **11-nov-2026, instrucción explícita de Marcos:** detener nuevas iteraciones de imágenes IA como sustituto de la experiencia real e **iniciar código ejecutable** de forma prudente. Primera rebanada vertical: etapa NAND2, molde transparente, arrastre/encaje, piezas incorrectas admitidas, inspección física/lógica, pruebas digitales y UI clásica de esquinas rectas. No se autoriza por ello congelar ISA, mapa MMIO, ABI, firmware ni hardware. |
| D-105 | DISEÑO BASE | **Primer corte JavaFX R0.1:** placa didáctica 2D conceptual (la 3D queda para siguiente iteración), cuatro posiciones compartidas `P1/P2/N1/N2`, kit 2 PMOS + 2 NMOS, comprobación ideal 00/01/10/11, guardado local del ejercicio y prueba JUnit. Las imágenes V5/V3 son referencias, no fuente de topología; el resultado en Windows requiere ejecución y capturas reales. |
| D-106 | DISEÑO BASE | **UX ejecutable R0.2, basado en las primeras capturas Windows de Marcos:** iconografía vectorial sin caracteres Unicode decorativos, cabeceras laterales de ancho completo, corte de chip didáctico **blanco con borde negro e interconexión A/B/VDD/GND/Y**, zoom/paneo 2D y placa 3D conceptual orbitable. No se ha certificado rendimiento, física 3D ni pinout; F12 captura la ventana a solicitud explícita y un guion Windows reúne pruebas/capturas para retroalimentación. |
| D-107 | DISEÑO BASE | **UX R0.3, segunda auditoría visual Windows:** el mainboard debe exhibir redes funcionales visibles y compartidas en 2D/3D; el NAND2 solo contiene conexiones de **un bit**, no buses CPU inventados. Los paneles laterales se pliegan con triángulos, los diálogos muestran texto completo y la geometría 3D evita diagonales propias de mallas wireframe. El onboarding se concentra en README + `docs/`; no reordenar masivamente borradores históricos ni romper enlaces del repositorio. Hasta nueva prueba Windows, el aspecto 3D y los diálogos siguen sin certificación. |
| D-108 | DISEÑO BASE | **UX R0.4, tercera auditoría Windows:** R0.3 pasa `mvn clean test` (8 JUnit correctos) y arranca/cierra JavaFX sin errores. La captura evidencia texto reflejado en el plano superior de los cuatro MOS y contactos metálicos poco visibles. Para R0.4 orientar la cara del texto hacia la superficie superior, dibujar tres patas metálicas salientes por transistor en 2D y 3D y conservar los tres terminales lógicos de cada MOS. **No convertir los transistores en encapsulados arbitrarios de 8/14 pines** ni confundir bits con pines. El aspecto final requiere nuevas capturas. |
| D-109 | DISEÑO BASE | **R0.5 y automatización, 11-nov-2026:** Marcos solicita continuar el código y publicar en GitHub sin depender de una prueba manual por cada versión. El Inspector permite conmutar las entradas binarias A/B y observar Y (0/1/X/Z) sobre el **mismo modelo NAND2** que usa la tabla de verdad; el interior resalta la conducción ideal de cada MOS. GitHub Actions compila Java 21 y ejecuta JUnit y smoke test en push/PR. La automatización **no sustituye** pruebas visuales de JavaFX ni validación eléctrica/PCB; sin cambios de ISA, ABI o buses CPU. |
| D-110 | DISEÑO BASE | **R0.6, respuesta visual compartida:** los cambios A/B se muestran sobre las redes normalizadas de las placas 2D y 3D, y la salida Y se colorea desde `Nand2Lesson.observe`. MID queda neutra: sin modelo de tensiones intermedias no se le asigna un cero o uno ficticio. Los MOS que conducen se resaltan sin confundirlo con corriente medida. Incluir pruebas de tintas y rutas en JUnit y en un smoke test ejecutable sin Maven/JavaFX. |

## Procedimiento para cambiar algo

1. Explicar qué requisito o evidencia motiva el cambio.
2. Identificar capítulos, pruebas, programa y esquema afectados.
3. Proponer transición, o compatibilidad con el formato anterior cuando proceda.
4. Pedir aprobación del usuario si cambia una decisión **CONFIRMADA**.
5. Actualizar esta tabla, ARQUITECTURA.md y los contratos afectados en un mismo cambio.

