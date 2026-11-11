# Aula-Computadora

> **Primer taller JavaFX R0.5 (11-nov-2026):** montaje NAND2 de cuatro MOS
> en 2D y 3D conceptual, inspección de la lógica dentro de una cucarachita,
> trazos de red, transistores de tres patas, paneles plegables, zoom/paneo,
> **prueba de entradas A/B en vivo** y captura F12. Pruebas automáticas de Java
> 21 en GitHub Actions; la GUI aún necesita observación visual ocasional.
> No es CPU ejecutable ni PCB validada.
> [Descomprimir, probar, ejecutar y recopilar capturas](simulador-javafx/docs/PRIMER_TALLER_EJECUCION.md).

**Estado de trabajo 9-nov-2026: C28-T — 88,5 % de madurez editorial estimada.**
La retroalimentación más reciente confirmó **24/24 pruebas Windows** y
**5/5 fotografías históricas**. C28-R incorpora una ruta ADD/SUB de
**134 NAND con 131.072 vectores comprobados** y HDL aún sin probar en
Windows; C28-S inspecciona la geometría de las **248 páginas** del maestro
con ocho hojas de contacto. **C28-T incorpora dos figuras técnicas
SVG/PNG, un suplemento con el recorrido de las nueve NAND por bit y
un plan de inserción para capítulos 4, 10 y 11; sin nuevas pruebas.**
La próxima ronda de pruebas, cuando proceda, mantiene **28 controles pendientes**.
Los 26 capítulos y el Word/PDF maestro
**C28-G de 248 páginas** se conservan. El suplemento secuencial C28-H
y el atlas histórico C28-O aún no se insertan en el maestro. Ver
[informe acumulativo C28-R/S](INFORME_C28_S_ALU_Y_REVISION_PDF.md),
[informe y figuras C28-T](INFORME_C28_T_DOCUMENTACION_Y_DIAGRAMAS.md),
[suplemento paso a paso](libro/SUPLEMENTO_C28T_DEL_BIT_A_134_NAND.md),
[informe C28-Q](INFORME_C28_Q_RED_NAND_Y_RTL.md),
[matriz de circuitos](libro/MATRIZ_CIRCUITOS_C28Q.md) y
[plan de cierre](libro/PLAN_CIERRE_EDITORIAL_C28I.md). Este avance
no significa tener una CPU, firmware o hardware completos.

**Un solo repositorio de GitHub para el libro completo y el futuro simulador de Aula-8/Aula-16.**

Base técnica preservada: **R0.14 — carga LOADX candidata**. La edición editorial **C27-0.1** contiene [26 capítulos](libro/README.md), incluidos 7B y 23B, en el [PDF maestro](libro/Aula_Computadora_C27_0_1_MAESTRO.pdf) y [Word editable](libro/Aula_Computadora_C27_0_1_MAESTRO.docx): **236 páginas, 115 figuras y 110 ejercicios seleccionados y resueltos**. Los 312 originales continúan en los fascículos. Se introdujo la construcción acumulativa de Aula-8, RAM contigua con flechas de salto, buses y un patillaje comercial; la portada es arte original conceptual. **Quedan la lectura humana integral, las licencias de imágenes históricas y toda CPU/firmware/simulador ejecutables**. El contrato lógico de vídeo sigue sin hardware físico. Ver [entrega C27](ENTREGA_C27.md) y [matriz de evidencia](MATRIZ_TRAZABILIDAD_C27.md).

Este repositorio albergará dos productos relacionados, con calendarios de ejecución diferentes:

1. **libro/**: manual original en español que enseña a construir y comprender una computadora desde electricidad y transistores hasta firmware, ensamblador, Mini C y un pequeño sistema operativo.
2. **simulador-javafx/**: aplicación educativa de escritorio que, posteriormente, permitirá explorar y ensamblar de manera guiada las computadoras Aula-8 y Aula-16, con esquemas 2D y representaciones 3D.

El orden acordado es **primero asegurar la documentación, después desarrollar el libro y mucho más adelante implementar el simulador**. El libro será autónomo y no mencionará JavaFX en su contenido.

## Leer antes de continuar

| Documento | Función |
| --- | --- |
| [CONTEXTO_MAESTRO.md](CONTEXTO_MAESTRO.md) | Memoria portable de objetivos, acuerdos, fuentes y límites |
| [DECISIONES.md](DECISIONES.md) | Registro de decisiones y su estado |
| [ARQUITECTURA.md](ARQUITECTURA.md) | Contrato conceptual de las dos CPU y sus memorias |
| [HOJA_DE_RUTA.md](HOJA_DE_RUTA.md) | Orden de implementación y criterios para avanzar |
| [MATRIZ_TRAZABILIDAD.md](MATRIZ_TRAZABILIDAD.md) | Relación entre conocimiento, circuitos, capítulos y pruebas |
| [POLITICA_CALIDAD.md](POLITICA_CALIDAD.md) | Evidencia y definición de verificación |
| [REFERENCIAS.md](REFERENCIAS.md) | Fuentes primarias y documentos del usuario |
| [FUENTES_CONSULTADAS.txt](FUENTES_CONSULTADAS.txt) | Lista de referencias externas sin interrumpir la explicación del libro |
| [AGENTS.md](AGENTS.md) | Instrucciones de continuidad para asistentes de IA |
| [PUBLICAR_GITHUB.md](PUBLICAR_GITHUB.md) | Publicación segura del mismo repositorio |
| [ESTADO_PORTABLE.json](ESTADO_PORTABLE.json) | Resumen estructurado y legible por herramientas |
| [CHANGELOG.md](CHANGELOG.md) | Historial de entregas y límites de cada release |
| [ENTREGA_C21.md](ENTREGA_C21.md) | Inventario C21-0.1, nuevas pruebas, comandos Windows y límites de fidelidad |
| [ENTREGA_C23.md](ENTREGA_C23.md) | Inventario C23-0.1 y guía de fusión incremental con C21-0.3 |
| [ENTREGA_C24.md](ENTREGA_C24.md) | Entrega vigente: P23V y capítulo final, restauración global o parche desde C23 |
| [ENTREGA_C25.md](ENTREGA_C25.md) | Entrega histórica: primera edición maestra y parche desde C24 |
| [ENTREGA_C26.md](ENTREGA_C26.md) | **Entrega vigente:** revisión de diagramas, matemáticas, capítulos puente y actividades seleccionadas; parche desde C25 |
| [ENTREGA_C27.md](ENTREGA_C27.md) | **Entrega vigente C27:** lectura progresiva de Aula-8, 115 figuras, portada conceptual, 110 ejercicios esenciales y verificaciones |
| [PROPUESTA_VIDEO_TEXTO_GRAFICOS_ROM.md](simulador-javafx/PROPUESTA_VIDEO_TEXTO_GRAFICOS_ROM.md) | **Histórico, superado:** debate sobre ROM de firmware/glifos, VRAM, monocromo y color |
| [CUESTIONARIO_MAPA_VIDEO_MMIO.md](simulador-javafx/CUESTIONARIO_MAPA_VIDEO_MMIO.md) | **Histórico, respondido:** 16 preguntas originales y elecciones por delegación; prevalece contrato V1 |
| [PLAN_INTERLUDIO_P23V_TEXTO_GRAFICOS_TIPOGRAFIA.md](libro/PLAN_INTERLUDIO_P23V_TEXTO_GRAFICOS_TIPOGRAFIA.md) | **Plan editorial histórico ya ejecutado**: P23V ahora existe en Markdown, Word y PDF |
| [verificar_modelo_video_texto_grafico.py](scripts/verificar_modelo_video_texto_grafico.py) | Verificador matemático de índices de píxel, 1/2 bpp y ROM de glifos de ejemplo; **solo anfitrión**, no CPU |
| [CONTRATO_VIDEO_AULA_V1.md](simulador-javafx/CONTRATO_VIDEO_AULA_V1.md) | **Diseño lógico congelado por delegación:** pantalla única, registros `C020–C02F`, ROM de glifos 2 KiB, texto 512 B y bitmap cuatro colores 8 KiB; sin hardware implementado |
| [VIDEO_AULA_V1_CONTRATO.json](simulador-javafx/VIDEO_AULA_V1_CONTRATO.json) | Codificación estructurada de registro, direcciones, profundidad de color y memoria de vídeo |
| [verificar_contrato_video_aula_v1.py](scripts/verificar_contrato_video_aula_v1.py) | Auditoría del contrato lógico; **no** prueba de CPU, controladora real ni vídeo físico |
| [PROGRAMACION_DESDE_CERO.md](simulador-javafx/PROGRAMACION_DESDE_CERO.md) | Del panel manual a monitor, editor, ensamblador y mini sistema |
| [PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md](simulador-javafx/PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md) | Estimación revisable de ROM/RAM y construcción de herramientas desde cero |
| [ISA_AULA8_CANDIDATA.md](simulador-javafx/ISA_AULA8_CANDIDATA.md) | **Borrador**, 36 opcodes Aula-8 y tres programas introducidos byte a byte |
| [MICROARQUITECTURA_AULA8_BORRADOR.md](simulador-javafx/MICROARQUITECTURA_AULA8_BORRADOR.md) | **Borrador**, registros internos, buses, control y trazado de LDI/ST/HALT |
| [UNIDAD_CONTROL_AULA8_BORRADOR.md](simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md) | **Borrador**, fetch compartido, microsecuenciador y acciones lógicas de LDI/ST/HALT |
| [CONTROL_FLUJO_PILA_AULA8_BORRADOR.md](simulador-javafx/CONTROL_FLUJO_PILA_AULA8_BORRADOR.md) | **Borrador**, CALL/RET, pila little-endian, JMP y saltos de flags |
| [PILA_Y_BANDERAS_AULA8_BORRADOR.md](simulador-javafx/PILA_Y_BANDERAS_AULA8_BORRADOR.md) | **Borrador**, PUSH/POP/PUSHX/POPX/INC/DEC, flags y casos límite |
| [DIRECCIONAMIENTO_INDEXADO_AULA8_BORRADOR.md](simulador-javafx/DIRECCIONAMIENTO_INDEXADO_AULA8_BORRADOR.md) | **Borrador**, LD/ST por X/SP, desplazamientos con signo, sumas de dos pasadas ALU8 y prueba de escritorio |
| [AJUSTES_X_SP_Y_MARCOS_AULA8_BORRADOR.md](simulador-javafx/AJUSTES_X_SP_Y_MARCOS_AULA8_BORRADOR.md) | **Borrador**, LEAX/ADJSP/ADDXW/SETSP/XFROMSP y marco de una función CALL/RET |
| [ABI_MINIC_AULA8_R0_10_BORRADOR.md](simulador-javafx/ABI_MINIC_AULA8_R0_10_BORRADOR.md) | **Borrador**, argumentos de dos bytes, prólogo/epílogo fijo, registros preservados, retorno u16 y recursividad teórica |
| [ROM_MONITOR_AULA8_R0_11_BORRADOR.md](simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.md) | **Borrador**, 32 ranuras ROM reservadas (4 definidas), bytes JMP/NOP, reset, ABI de firmware y monitor con RUN/RET/HALT |
| [CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md](simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md) | **Borrador**, registros de bloques 256 B en C010–C01F, protocolo READ/WRITE, estados, persistencia de referencia y sintaxis futura LOAD |
| [EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md](simulador-javafx/EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md) | **Borrador**, cabecera AEX1 de 32 B, dos ventanas RAM, CRC16, precarga completa en anfitrión y futuro LOADX independiente de LOAD |
| [LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md](simulador-javafx/LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md) | **Borrador**, prevalidación completa y copia por segunda lectura usando un bloque temporal; falla sin habilitar ejecución, RAM no atómica |
| [ESTADO_Y_PENDIENTES_R0_14.md](libro/ESTADO_Y_PENDIENTES_R0_14.md) | Auditoría realista de los 24 capítulos y entregables pendientes del libro, excluida la portada |
| [ESTADO_EDITORIAL_C01.md](libro/ESTADO_EDITORIAL_C01.md) | Estado real después de redactar y revisar la muestra del capítulo 1 |
| [ESTADO_EDITORIAL_C02.md](libro/ESTADO_EDITORIAL_C02.md) | Estado actualizado tras producir el capítulo 2 y trabajos pendientes del libro |
| [ESTADO_EDITORIAL_C03.md](libro/ESTADO_EDITORIAL_C03.md) | Estado actualizado tras producir el capítulo 3, sus comprobaciones y pendientes |
| [ESTADO_EDITORIAL_C04.md](libro/ESTADO_EDITORIAL_C04.md) | Estado actualizado tras producir el capítulo 4: compuertas, Word/PDF, 146 controles y 20 pendientes |
| [ESTADO_EDITORIAL_C05.md](libro/ESTADO_EDITORIAL_C05.md) | Estado actualizado tras producir el capítulo 5: latch SR, Word/PDF, 123 controles y 19 pendientes |
| [ESTADO_EDITORIAL_C06.md](libro/ESTADO_EDITORIAL_C06.md) | Estado actualizado tras producir el capítulo 6: latch D, flip-flop, Word/PDF, 171 controles y 18 pendientes |
| [ESTADO_EDITORIAL_C07.md](libro/ESTADO_EDITORIAL_C07.md) | Estado actualizado tras producir el capítulo 7: bytes, registro de ocho bits, bus triestado, Word/PDF y 17 pendientes |
| [ESTADO_EDITORIAL_P07B.md](libro/ESTADO_EDITORIAL_P07B.md) | Estado después del interludio: lectura semántica de bits, Word/PDF, 70 páginas acumuladas, 17 capítulos numerados pendientes |
| [ESTADO_EDITORIAL_C08.md](libro/ESTADO_EDITORIAL_C08.md) | Estado actualizado: capítulo 8, dirección/dato/buses, Word/PDF, 79 páginas acumuladas, 16 pendientes |
| [ESTADO_EDITORIAL_C09.md](libro/ESTADO_EDITORIAL_C09.md) | Estado actualizado: capítulo 9, SRAM/EEPROM, mapa ilustrativo, Word/PDF, 87 páginas acumuladas, 15 pendientes |
| [ESTADO_EDITORIAL_C10.md](libro/ESTADO_EDITORIAL_C10.md) | Estado actualizado: capítulo 10, sumadores, acarreos, banderas, Word/PDF, 95 páginas acumuladas, 14 pendientes |
| [ESTADO_EDITORIAL_C11.md](libro/ESTADO_EDITORIAL_C11.md) | Estado actualizado: capítulo 11, resta, lógica, comparación, flags, Word/PDF, 103 páginas acumuladas, 13 pendientes |
| [ESTADO_EDITORIAL_C12.md](libro/ESTADO_EDITORIAL_C12.md) | Estado actualizado: capítulo 12, registros, buses, lectura/escritura, direcciones en dos pasadas, Word/PDF, 112 páginas acumuladas, 12 pendientes |
| [ESTADO_EDITORIAL_C13.md](libro/ESTADO_EDITORIAL_C13.md) | Estado actualizado: capítulo 13, microoperaciones, ROM de control, despacho y ST seguro, Word/PDF, 120 páginas acumuladas, 11 pendientes |
| [ESTADO_EDITORIAL_C14.md](libro/ESTADO_EDITORIAL_C14.md) | Estado actualizado: capítulo 14, opcodes, hexadecimal, direccionamiento, depósito manual, Word/PDF, 129 páginas acumuladas, 10 pendientes |
| [ESTADO_EDITORIAL_C15.md](libro/ESTADO_EDITORIAL_C15.md) | Estado actualizado: capítulo 15, fetch/decode/execute, registros y transacciones lógicas, Word/PDF, 137 páginas acumuladas, 9 pendientes |
| [ESTADO_EDITORIAL_C16.md](libro/ESTADO_EDITORIAL_C16.md) | Capítulo 16, CALL/RET, pila little-endian y saltos, Word/PDF, 144 páginas acumuladas, 8 pendientes |
| [ESTADO_EDITORIAL_C17.md](libro/ESTADO_EDITORIAL_C17.md) | Capítulo 17, ROM, RESET, vector de arranque y monitor, Word/PDF, 152 páginas acumuladas, 7 pendientes |
| [ESTADO_EDITORIAL_C18.md](libro/ESTADO_EDITORIAL_C18.md) | Capítulo 18, terminal, E/S mapeada, eco de caracteres y cadenas, Word/PDF |
| [ESTADO_EDITORIAL_C19.md](libro/ESTADO_EDITORIAL_C19.md) | Capítulo 19, bloques persistentes, transferencias y carga cruda/AEX1, Word/PDF, 5 pendientes |
| [ESTADO_EDITORIAL_C20.md](libro/ESTADO_EDITORIAL_C20.md) | Capítulo 20, ensamblador de dos pasadas, suma/Euclides/Fibonacci y mini sistema propuesto |
| [ESTADO_EDITORIAL_C21.md](libro/ESTADO_EDITORIAL_C21.md) | Capítulo 21, registros y ALU de 16 bits, bus de datos y banderas, 3 capítulos pendientes |
| [ESTADO_EDITORIAL_C23.md](libro/ESTADO_EDITORIAL_C23.md) | Capítulos 22–23, bancos de RAM y programación conceptual Aula-16; queda capítulo 24 |
| [ESTADO_EDITORIAL_C24.md](libro/ESTADO_EDITORIAL_C24.md) | **Estado vigente**: 24/24 capítulos, interludios P07B/P23V, pendientes de volumen maestro y hardware |
| [ESTADO_EDITORIAL_C25.md](libro/ESTADO_EDITORIAL_C25.md) | **Estado vigente:** manuscritos y libro maestro de 225 páginas presentes, revisión editorial de fondo pendiente |
| [ESTADO_EDITORIAL_C26.md](libro/ESTADO_EDITORIAL_C26.md) | **Estado editorial vigente:** revisión C26, límites y pendientes reales |
| [ESCALERA_DE_PROGRAMAS_AULA8.md](libro/ESCALERA_DE_PROGRAMAS_AULA8.md) | Secuencia de prácticas, desde una variable a Euclides, Fibonacci y mini sistema, condicionada a pruebas de CPU |
| [GUIA_DE_FIDELIDAD_DE_FIGURAS.md](libro/GUIA_DE_FIDELIDAD_DE_FIGURAS.md) | Regeneración de esquemas originales y límites de fidelidad entre diagrama funcional y circuito físico |
| [PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md](libro/PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md) | Origen del interludio desarrollado tras el capítulo 7, sin cambiar el currículo numerado |

## Lo que existe y lo que no

- **Existe:** contexto, currículo, arquitectura conceptual, catálogo preliminar de componentes, riesgos, criterios de pruebas, **24 capítulos más P07B/P23V con Word/PDF individual y libro maestro integrado**; un ensamblador Python de referencia y dos archivos ASM del capítulo 20 ejecutables/traducibles en PC.
- **No existe aún:** una **corrección editorial humana completa del libro maestro**, esquemas físicos del sistema entero, ISA **definitiva** congelada, compilador, firmware ejecutable ni aplicación JavaFX. Sí existe una **codificación candidata** de Aula-8, sin CPU que la ejecute.
- **Planificado, todavía no implementado:** panel de carga byte a byte; monitor en ROM; editor de líneas y ensamblador **nativos en Aula-8**; MiniC compilado en el anfitrión; compilación MiniC nativa opcional posterior.
- **No se ha certificado** un circuito físico ni un software inexistente.

### Comprobación de la línea base

~~~bash
python3 scripts/verificar_contexto.py
python3 scripts/verificar_modelo_video_texto_grafico.py
python3 scripts/verificar_contrato_video_aula_v1.py
python3 scripts/verificar_isa_aula8_borrador.py
python3 scripts/verificar_microtraza_aula8_borrador.py
python3 scripts/verificar_microsecuencias_aula8_borrador.py
python3 scripts/verificar_flujo_aula8_r0_6_borrador.py
python3 scripts/verificar_pila_flags_aula8_r0_7_borrador.py
python3 scripts/verificar_indices_aula8_r0_8_borrador.py
python3 scripts/verificar_ajustes_aula8_r0_9_borrador.py
python3 scripts/verificar_abi_minic_aula8_r0_10_borrador.py
python3 scripts/verificar_rom_monitor_aula8_r0_11_borrador.py
python3 scripts/verificar_bloques_aula8_r0_12_borrador.py
python3 scripts/verificar_ejecutable_aula8_r0_13_borrador.py
python3 scripts/verificar_loadx_aula8_r0_14_borrador.py
python3 scripts/verificar_capitulo_01.py
python3 scripts/verificar_capitulo_02.py
python3 scripts/verificar_capitulo_03.py
python3 scripts/verificar_capitulo_04.py
python3 scripts/verificar_capitulo_05.py
python3 scripts/verificar_capitulo_06.py
python3 scripts/verificar_capitulo_07.py
python3 scripts/verificar_puente_07b.py
python3 scripts/verificar_capitulo_08.py
python3 scripts/verificar_capitulo_09.py
python3 scripts/verificar_capitulo_10.py
python3 scripts/verificar_capitulo_11.py
python3 scripts/verificar_capitulo_12.py
python3 scripts/verificar_capitulo_13.py
python3 scripts/verificar_capitulo_14.py
python3 scripts/verificar_capitulo_15.py
python3 scripts/verificar_capitulo_16.py
python3 scripts/verificar_capitulo_17.py
python3 scripts/verificar_capitulo_18.py
python3 scripts/verificar_capitulo_19.py
python3 scripts/verificar_capitulo_20.py
python3 scripts/verificar_capitulo_21.py
python3 scripts/verificar_capitulo_22.py
python3 scripts/verificar_capitulo_23.py
python3 scripts/verificar_entrega_c24.py
python3 scripts/verificar_libro_maestro.py
python3 scripts/verificar_escalera_programas_aula8.py
~~~

Estas pruebas comprueban integridad documental, **codificaciones de ISA candidata**, **trazas de bus esperadas**, consistencia de **acciones de microcontrol descritas en papel**, pila, fórmulas de banderas, aritmética modular de direcciones, marcos, convenio de MiniC, **tabla ROM y parser teóricos**, modelo de almacenamiento, formato AEX1 y LOADX de dos pasadas, siempre en Python sobre el anfitrión. Las pruebas editoriales inspeccionan cálculos, ecuaciones Word, figuras y texto PDF de los 24 capítulos y dos interludios; P23V/C24 agregan 66576 controles de mapa de vídeo, glifos y documentos. **No prueban una CPU ni un circuito físico**. Se incluye un workflow de CI para las verificaciones documentales al publicar el repositorio.

El **100 % de planificación** alcanzado en la conversación significa que se cerraron el alcance y la secuencia general de trabajo. **No es un porcentaje de implementación.**

## Arquitecturas acordadas

| Aspecto | Aula-8 | Aula-16 |
| --- | --- | --- |
| Datos de CPU | 8 bits | 16 bits |
| Bus externo de datos | 8 bits | **16 bits** |
| Direcciones | 16 bits | 16 bits |
| Espacio de direcciones | 64 KiB | 64 KiB |
| Registros generales | R0–R3, 8 bits | R0–R3, 16 bits |
| PC / SP / X | 16 bits | 16 bits |
| RAM / ROM / E/S | Sí | Sí |

**Advertencia de continuidad:** el usuario eligió expresamente **16 bits de bus externo para Aula-16**. No revertirlo a 8 bits por comodidad de implementación.

## Estado de publicación

Esta R0 es un proyecto documental, empaquetable y listo para inicializar o publicar en GitHub. Una copia ZIP no supone por sí misma que exista ya un repositorio remoto. La visibilidad y URL de GitHub se decidirán con el propietario antes de la publicación.

