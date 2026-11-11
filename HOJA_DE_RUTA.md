# Hoja de ruta y entregables

La **planificación general estaba cerrada (100 %)** para los 24 capítulos troncales. **Estado editorial C27-0.1 actual:** hay 26 capítulos Word/PDF (24 troncales y los dos puentes **7B y 23B**) y una edición maestra de **236 páginas, 115 figuras y 110 actividades esenciales resueltas**, con los 312 ejercicios de origen preservados en fascículos. C27 desarrolla la construcción incremental de Aula-8, programas como bytes contiguos en RAM, buses fieles y el pinout NAND. Sigue pendiente una **lectura humana integral de fondo**, fotos históricas con derechos y el simulador; no transformar el porcentaje de planificación en «porcentaje del libro» o «porcentaje del software».

## Hito editorial C27-0.1 — construcción acumulativa y memoria visible

La [entrega C27](ENTREGA_C27.md) y su [estado verificado](libro/ESTADO_EDITORIAL_C27.md) describen las nueve nuevas figuras, los veinte hitos narrativos, la portada ilustrativa conceptual, la reducción selectiva de ejercicios y la QA de PDF/Word. **Próximo:** dibujos eléctricos completos y verificaciones de circuitos antes del futuro taller, fotos históricas con derechos, y lectura editorial humana final. La ISA Aula-8, su microcontrol y el firmware siguen candidatos.

## Hito editorial C26-0.1 — corrección técnica de lectura

Revisar la continuidad entre explicación y figura; corregir colisiones visibles C01/C13, mostrar protoboard y dos carriles Aula-16, arreglar potencias como `16⁰`, titular capítulos 7B y 23B, concentrar referencias externas en `FUENTES_CONSULTADAS.txt` y priorizar seis ejercicios con solución por capítulo maestro. Ver [entrega C26](ENTREGA_C26.md) y [estado editorial](libro/ESTADO_EDITORIAL_C26.md). **Próximo:** edición humana narrativa y arte histórico, luego requisitos ejecutables del futuro taller; sin tocar contrato lógico de vídeo V1.

## Hito editorial C24-0.1 — cierre de manuscritos numerados

**P23V:** texto 32×16, ROM de glifos 8×8, framebuffer 256×128 2bpp, offsets, MMIO, cuatro colores, tipografía bitmap y contornos; 10 páginas/7 diagramas. **Capítulo 24:** síntesis de Aula-8 y Aula-16, mapa de memoria, escalera de programas y separación de evidencia/documentación/hardware; 9 páginas/4 diagramas. 26 OMML y 24 ejercicios nuevos. **Acumulado: 24/24 capítulos numerados más 2 interludios, 220 páginas, 105 figuras, 312 ejercicios, 333 OMML**. El verificador nuevo comprueba **66576** invariantes lógicos/documentales. El [estado vigente](libro/ESTADO_EDITORIAL_C24.md) distingue claramente **borrador completo** de **máquina construida**.

**Siguiente hito editorial:** montar Word/PDF maestro con índice, referencias y revisión de coherencia y accesibilidad; no expandir sin necesidad la ISA ni el alcance del simulador. **Siguiente hito técnico independiente:** implementar y probar ISA/CPU, firmware y controlador lógico de vídeo sin confundir con hardware físico.

## Hito editorial C21-0.1 — Programar un pequeño sistema y ampliar la palabra

**Estado:** C20 ofrece un ensamblador Python de **dos pasadas** y listado reproducible de suma/Euclides, referencias matemáticas de Fibonacci, modelo de monitor y compromisos de ABI. C21 distingue datos de 8/16 bits de direcciones de 16 bits, calcula transporte y banderas, y separa 16 bits de bus externo de 64 KiB de memoria por byte.

Los dos capítulos suman **17 páginas, 8 figuras SVG/PNG, 32 expresiones OMML y 24 ejercicios resueltos**; comprobaron **130685 + 126921** casos de anfitrión y documento. [Estado C20](libro/ESTADO_EDITORIAL_C20.md) · [estado C21](libro/ESTADO_EDITORIAL_C21.md).

**Acumulado:** **21/24** capítulos numerados más P07B; **185 páginas, 86 figuras, 264 ejercicios, 280 OMML**; restan 22–24. No existe ninguna CPU ni herramienta nativa Aula ejecutable.

## Hito editorial C19-0.1 — Guardar y recuperar programas

**Estado:** capítulo 19 maquetado en ocho páginas Word/PDF, cuatro SVG/PNG originales, quince ecuaciones editables y doce ejercicios con soluciones. Del almacenamiento como bloques de 256 bytes a la imagen persistente del anfitrión y una carga `LOAD`/`LOADX` todavía **no implementada**. Se comprobaron 205037 casos de modelo y documentos, sin CPU ni memoria física. [Manuscrito C19](libro/capitulos/19_guardar_y_recuperar_programas.md) y [estado editorial](libro/ESTADO_EDITORIAL_C19.md).

**Acumulado:** 19/24 capítulos numerados más P07B, 168 páginas, 78 figuras, 240 ejercicios, 248 OMML; **cinco capítulos pendientes (20–24)**. Se incorporó la [escalera didáctica progresiva](libro/ESCALERA_DE_PROGRAMAS_AULA8.md) y el [generador de figuras con guía de fidelidad](libro/GUIA_DE_FIDELIDAD_DE_FIGURAS.md).

## Hito editorial C18-0.1 — Hablar con la máquina

**Estado:** ocho páginas Word/PDF, cuatro SVG/PNG, catorce OMML, doce ejercicios y **646 verificaciones**. Terminal/teclado y MMIO, `PUTC`/`GETC`/`PUTS` candidatos, eco, variable RAM y cadena terminada en cero. [Manuscrito C18](libro/capitulos/18_hablar_con_la_maquina.md) y [estado editorial](libro/ESTADO_EDITORIAL_C18.md). No hay controlador de terminal ni firmware ejecutable.

## Hito editorial C17-0.1 — Encender una computadora

**Estado:** ocho páginas Word/PDF, cuatro figuras originales, doce OMML y doce ejercicios resueltos. `RESET` lee los bytes candidatos de FFFC–FFFD para iniciar en E000. ROM de 8 KiB, tabla de 32 ranuras con 4 servicios, arranque, monitor hexadecimal y RUN con retorno por RET. **196727 controles de modelo y documento** no validan CPU, firmware ni electrónica.

- [Capítulo 17](libro/capitulos/17_encender_una_computadora.md) y [estado editorial C17](libro/ESTADO_EDITORIAL_C17.md).
- **Entregado después:** capítulo 18 «Hablar con la máquina», terminal, PUTC/GETC/PUTS y eco, todavía a nivel didáctico documentado.

## Hito editorial C16-0.1 — Subrutinas y pila

**Estado:** siete páginas Word/PDF, cuatro diagramas SVG/PNG, doce OMML, doce ejercicios, **184283 controles**. CALL guarda `PC=6003` little-endian, reduce SP de 8000 a 7FFE, ejecuta una rutina en 6010 y RET restaura PC y SP. Anidamiento LIFO y bucles JNZ; **10 lecturas y 2 escrituras** son accesos candidatos, no temporización real.

- [Capítulo 16](libro/capitulos/16_subrutinas_y_pila.md) y [estado editorial C16](libro/ESTADO_EDITORIAL_C16.md).
- **Entregado después:** capítulo 17 «Encender una computadora», vector de reset, ROM, firmware y monitor.

## Hito editorial C15-0.1 — La instrucción en movimiento

**Estado:** capítulo 15 de ocho páginas Word/PDF, cuatro figuras SVG/PNG, doce OMML y doce ejercicios resueltos; **143464 comprobaciones de modelo/documento**. La traza candidata de los ocho bytes muestra PC, MAR, MDR, IR, SEL y TMP; registra ocho lecturas y una escritura, y explica por qué ST debe cargar R0 a MDR **después** de formar la dirección y **antes** del pulso WR. No se afirma medir nueve ciclos ni ejecutar hardware real.

- [Capítulo 15](libro/capitulos/15_la_instruccion_en_movimiento.md) y [estado editorial C15](libro/ESTADO_EDITORIAL_C15.md).
- **Entregado después:** capítulo 16 «Subrutinas y pila», con llamadas, retornos y control de PC.

## Hito editorial C14-0.1 — De números a instrucciones

**Estado:** capítulo 14 de nueve páginas Word/PDF, cuatro figuras SVG/PNG, doce OMML y doce ejercicios con solucionario; **132993 comprobaciones de modelo/documento**. Traduce decimal a bytes y direcciones little-endian, recorre `11 00 2A 13 00 00 6F 01` por las ocho posiciones `6000–6007`, enseña modos absoluto/X/SP y depósito/examen con CPU detenida. Distingue el panel manual del monitor de ROM y HALT de RET; ninguna traza equivale a un bus físico o una CPU funcional.

- [Capítulo 14](libro/capitulos/14_de_numeros_a_instrucciones.md) y [estado editorial C14](libro/ESTADO_EDITORIAL_C14.md).
- **Entregado después:** capítulo 15 «La instrucción en movimiento», con recorrido fetch/decode/execute, PC y efectos candidatos en registros/RAM.

## Hito editorial C13-0.1 — La unidad de control

**Estado:** capítulo 13 en ocho páginas Word/PDF, cuatro figuras SVG/PNG, ocho OMML y doce ejercicios con soluciones; **196771 comprobaciones de modelo/documento**. Diferencia instrucción, microoperación, ROM de control y firmware; desarrolla fetch, despacho candidato, validación de selector LDI y ST absoluto que conserva los bytes de dirección y **prepara MDR antes de WR**. `FAULT` no se confunde con una ruta candidata pendiente. Las 8 lecturas y 1 escritura del ejemplo son **expectativas lógicas**, no ciclos ni pruebas eléctricas.

- [Capítulo 13](libro/capitulos/13_la_unidad_de_control.md) y [estado editorial C13](libro/ESTADO_EDITORIAL_C13.md).
- **Próximo hito:** capítulo 14 «De números a instrucciones»: codificaciones de opcode, operandos y depósito manual de un programa en memoria.

## Hito editorial C12-0.1 — Arquitectura Aula-8

**Estado:** capítulo 12 de nueve páginas Word/PDF, cuatro figuras SVG/PNG, doce OMML, doce ejercicios y 2752599 comprobaciones. Se integran datapath, registros, 16 bits de dirección, bus de 8 bits, MAR/MDR, lectura/escritura con conductor exclusivo, fetch candidato `LDI R0,42` y sumas de dos pasadas con `ADDR_CARRY` invisible. El diseño sigue **sin implementación física, microcódigo aprobado ni ejecución**.

- [Capítulo 12](libro/capitulos/12_arquitectura_aula_8.md) y [estado editorial C12](libro/ESTADO_EDITORIAL_C12.md).
- **Próximo hito:** capítulo 13 «La unidad de control», con estados, selección de microoperaciones y distinción entre ROM de control y firmware.

## Hito editorial C11-0.1 — La unidad aritmético-lógica

**Estado:** capítulo 11 de ocho páginas Word/PDF, cuatro figuras SVG/PNG, 21 ecuaciones, 12 ejercicios con solucionario y 786524 comprobaciones. SUB a través del sumador y complemento a dos; distinción entre `Cout` interno y **C=préstamo** de la ISA candidata; comparación firmada y sin signo, operaciones lógicas y MUX funcional. No existe circuito ALU terminado ni política congelada de flags lógicas.

- [Capítulo 11](libro/capitulos/11_la_unidad_aritmetico_logica.md) y [estado editorial C11](libro/ESTADO_EDITORIAL_C11.md).
- **Próximo hito:** capítulo 12 «Arquitectura Aula-8», integrando registros, ALU, PC, SP y buses sobre el diseño candidato existente.

## Hito editorial C10-0.1 — El circuito que suma

**Estado:** capítulo 10 de ocho páginas Word/PDF, cuatro esquemas propios, diecisiete ecuaciones, doce ejercicios y 786541 controles matemáticos/documentales. Medio sumador, sumador completo, acarreo de ocho bits, desbordamiento sin signo/firmado y referencia a sumadores comerciales. Sin ALU construida ni tiempos medidos.

- [Capítulo 10](libro/capitulos/10_el_circuito_que_suma.md) y [estado editorial C10](libro/ESTADO_EDITORIAL_C10.md).
- **Próximo hito:** capítulo 11 «La unidad aritmético-lógica», enlazando la suma con resta, comparación y banderas.

## Hito editorial C09-0.1 — RAM y ROM reales

**Estado:** capítulo 9 de ocho páginas Word/PDF, cuatro esquemas originales, diez ecuaciones, doce ejercicios y 368752 pruebas matemáticas/documentales. Referencias AS6C62256 y AT28C64B; mapa de SRAM/EEPROM **ilustrativo**, no un sistema físico validado.

- [Capítulo 9](libro/capitulos/09_ram_y_rom_reales.md) y [estado editorial C09](libro/ESTADO_EDITORIAL_C09.md).
- **Próximo hito:** capítulo 10 «El circuito que suma», comenzando por medio sumador, sumador completo y acarreo.

## Hito editorial C08-0.1 — Direcciones y buses

**Estado:** capítulo 8 escrito en Word/PDF de nueve páginas, cuatro esquemas SVG/PNG, doce ecuaciones, doce ejercicios y 459379 controles matemáticos/documentales. Dirección de 16 bits, selección de posiciones y buses Aula-8/Aula-16; memoria real aún no construida.

- [Capítulo 8](libro/capitulos/08_direcciones_y_buses.md) y [estado editorial actualizado](libro/ESTADO_EDITORIAL_C08.md).
- **Próximo hito:** capítulo 9 «RAM y ROM reales», con SRAM/ROM y ampliación de memorias comerciales, antes de ALU y CPU.

## Hito editorial P07B-0.1 — Del bit al significado

**Estado:** interludio ilustrado intercalado entre los capítulos 7 y 8, Word/PDF de ocho páginas, cuatro figuras SVG/PNG, nueve ecuaciones OMML, doce ejercicios y 1383 comprobaciones de codificaciones y estructura de documentos. Explica que la semántica lógica ya opera en hardware y que un byte no lleva un tipo universal grabado. Sin ISA congelada, CPU ni medidas eléctricas.

- [Interludio](libro/capitulos/07b_del_bit_al_significado.md) y [estado editorial actualizado](libro/ESTADO_EDITORIAL_P07B.md).
- **Próximo hito:** capítulo 8 «Direcciones y buses», con direcciones reales, selección y función de los buses; no introducir aún memoria o CPU implementada sin prueba.

## Hito editorial C07-0.1 — Del bit al registro

**Estado:** séptimo capítulo ilustrado, Word/PDF de ocho páginas, cuatro figuras SVG/PNG, nueve ecuaciones OMML, doce ejercicios resueltos y 198502 controles lógicos/documentales. Construye un byte con ocho flip-flops, explica LOAD y OE_n separadamente, la alta impedancia y una transferencia A→B sobre bus sin doble conductor. Sin prueba eléctrica real.

- [Capítulo 7](libro/capitulos/07_del_bit_al_registro.md) y [estado después de C07](libro/ESTADO_EDITORIAL_C07.md).
- **Entregado después:** interludio P07B; sigue capítulo 8, «Direcciones y buses». Su eventual conversión en capítulo numerado sigue pendiente de decisión.

## Hito editorial C06-0.1 — Memorizar en el tiempo

**Estado:** sexto capítulo ilustrado, Word/PDF de ocho páginas, cuatro figuras SVG/PNG, nueve ecuaciones OMML, doce ejercicios resueltos y 171 controles lógicos y documentales. Distingue latch D transparente por nivel, flip-flop D de flanco ascendente, reset asíncrono y setup/hold. Sin medidas físicas.

- [Capítulo 6](libro/capitulos/06_memorizar_en_el_tiempo.md) y [estado después de C06](libro/ESTADO_EDITORIAL_C06.md).
- **Entregado después:** capítulo 7, «Del bit al registro»: bytes, carga, retención y salidas triestado.

## Hito editorial C05-0.1 — La realimentación conserva información

**Estado:** quinto capítulo original, ilustrado y maquetado en Word/PDF: ocho páginas, cuatro figuras propias, once expresiones OMML, doce ejercicios resueltos y 123 controles lógicos/documentales. El latch SR NAND permite conservar un bit si ya tiene estado válido; la entrada simultánea 00 se explica sin atribuir resultados físicos no observados.

- [Capítulo 5](libro/capitulos/05_la_realimentacion_conserva_informacion.md) y [estado después de C05](libro/ESTADO_EDITORIAL_C05.md).
- **Entregado después:** capítulo 6, «Memorizar en el tiempo»: latch D, flip-flop, reloj y reset.
- **Propuesta refinada:** [«Del bit al significado»](libro/PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md), semántica lógica de señales en hardware y significado de datos/software, con POO solo contextual; aún no se suma al total de 24.

## Hito editorial C04-0.1 — Construir funciones con compuertas

**Estado:** cuarto capítulo redactado, ilustrado y maquetado en Word/PDF: nueve páginas, cuatro dibujos propios, trece ecuaciones OMML, doce ejercicios resueltos y 146 controles lógicos y documentales. Se demuestra XOR con cuatro NAND y una simplificación que mantiene su tabla de verdad; no se realizaron prácticas físicas.

- [Capítulo 4](libro/capitulos/04_construir_funciones_con_compuertas.md) y [estado después de C04](libro/ESTADO_EDITORIAL_C04.md).
- **Entregado después:** capítulo 5, «La realimentación conserva información»: latch SR, estados estables y entrada prohibida.
- **Propuesta añadida:** [«Del bit al significado»](libro/PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md), para ubicar tras el capítulo 7 como interludio, sin cambiar todavía el total de 24.

## Hito editorial C03-0.1 — De interruptores a lógica

**Estado:** tercer capítulo escrito, ilustrado y maquetado en Word/PDF: 10 páginas, cuatro dibujos originales, 14 ecuaciones editables, doce ejercicios resueltos y verificación de 132 condiciones documentales y matemáticas. El integrado SN74HCT00 sirve como ejemplo físico de NAND; no hay mediciones eléctricas ni protoboard certificada.

- [Capítulo 3](libro/capitulos/03_de_interruptores_a_logica.md) y [estado después de C03](libro/ESTADO_EDITORIAL_C03.md).
- **Entregado después:** capítulo 4, «Construir funciones con compuertas», con OR/NOR/XOR y simplificación justificada; se mantiene la separación entre lógica abstracta y circuitos físicos.

## Hito editorial C02-0.1 — Transistor como interruptor

**Estado:** segundo capítulo escrito y maquetado en Word/PDF, con dos estados de un interruptor NPN, tres figuras, 12 ejercicios y solucionario. Sus cálculos son estimaciones de un circuito de 5 V y una referencia onsemi 2N3904, no mediciones físicas.

- [Capítulo 2](libro/capitulos/02_el_transistor_como_interruptor.md) y [estado después de C02](libro/ESTADO_EDITORIAL_C02.md).
- **Entregado después:** capítulo 3, «De interruptores a lógica», con condiciones, tabla de verdad, NAND y ejemplo de integrado real.
- No cerrar ni implementar CPU/ISA antes de su proceso R1; el borrador técnico R0.14 continúa independiente.

## Hito editorial C01-0.1 — Primer capítulo

**Estado:** muestra redactada, diagramada, maquetada Word/PDF y verificada documentalmente; pendiente de revisión editorial por Marcos y de cualquier práctica física con componentes específicos.

- [Capítulo 1](libro/capitulos/01_la_corriente_y_sus_caminos.md) y [estado después de C01](libro/ESTADO_EDITORIAL_C01.md).
- **Entregado después:** capítulo 2, transistor como interruptor, con esquemas y hoja de datos de referencia; no exige cerrar ISA R1.
- Mantener la línea técnica R0.14 como línea base aparte: los capítulos 12–24 sí requieren consolidar contratos de CPU, ROM y programación antes de afirmaciones sobre ejecución real.

## R0 — Respaldo del conocimiento

**Estado:** presente en este repositorio.

Entregable: contexto maestro, decisiones, mapa de memoria, editorial, currículo, especificación del taller, pruebas, fuentes, riesgos y reglas para continuar sin el chat.

Condición de salida: todos los vínculos internos y principales restricciones consistentes; ZIP descargable; copia persistente y ruta de publicación GitHub.

## R0.1 — Recorrido de programación y arranque

**Estado:** especificación documental presente; software aún inexistente.

- Diferenciar panel byte a byte, monitor hexadecimal, herramientas nativas y compilación cruzada.
- Registrar dependencia de ROM previamente grabada, arbitraje del bus, persistencia y límites RAM.
- Añadir casos verificables de editor/ensamblador nativos; ningún «compilador» anfitrión oculto debe hacerse pasar por código de Aula.
- Documento de referencia: [programación desde cero](simulador-javafx/PROGRAMACION_DESDE_CERO.md).

## R0.2 — Memoria del software y arranque reproducible

**Estado:** presupuesto y dependencias documentados, sin firmware ejecutable.

- Proponer presupuesto de ROM 8 KiB y partición de RAM 32 KiB, verificando la suma y dejando explícita su naturaleza **candidata**.
- Cargar editor y ensamblador alternativamente en una región *overlay*, manteniendo fuente y binario fuera de ella.
- Diferenciar construcción inicial en anfitrión de ejecución nativa posterior; demostrar bootstrap sin asumir «magia».
- Registrar explícitamente el problema `RUN` / `CALL` / `RET` / `HALT` y su relación con el retorno al monitor.
- Documento: [presupuesto de ROM/RAM y bootstrap](simulador-javafx/PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md).

## R0.3 — ISA Aula-8 candidata y primeros bytes

**Estado:** propuesta documental revisable; **R1 técnico sigue sin cerrar**.

- Diseñar una codificación concreta para discutir tamaños, formas y semántica de operandos de Aula-8.
- Elegir direcciones de programas de ejemplo compatibles con la partición candidata de RAM, sin invadir áreas del monitor.
- Verificar opcodes únicos y decodificación de tres programas de muestra **sin** fingir que se ejecutó una CPU.
- Documentar pila/flags como candidatos y analizar riesgos para microcontrol, memoria y MiniC.
- Materiales: [propuesta de ISA Aula-8](simulador-javafx/ISA_AULA8_CANDIDATA.md), [especificación JSON](simulador-javafx/ISA_AULA8_CANDIDATA.json) y `scripts/verificar_isa_aula8_borrador.py`.

## R0.4 — Datapath y microoperaciones ilustrativas

**Estado:** concepto y traza documental verificables; **no** circuito ni microcontrol codificado.

- Identificar registros internos y control del bus; distinguir datos de 8 bits y direcciones de 16 bits.
- Proponer PC incrementado con lógica propia y X/SP operados por ALU8 serial; analizar la alternativa de reutilizar ALU8.
- Detallar fetch lógico y recorrido LDI/ST/HALT sin asignar falsos ciclos de reloj.
- Conservar separadas las entradas RESET por vector ROM y arranque manual de RAM.
- Verificar consistencia de nueve transacciones esperadas y propiedad del bus sin declarar una CPU simulada.
- Materiales: [microarquitectura](simulador-javafx/MICROARQUITECTURA_AULA8_BORRADOR.md), [microtraza JSON](simulador-javafx/MICROTRAZA_AULA8_BORRADOR.json), `scripts/verificar_microtraza_aula8_borrador.py`.

## R0.5 — Microsecuenciador y flujo lógico de control

**Estado:** propuesta documental verificable; **sin microcódigo binario, reloj físico ni CPU ejecutable**.

- Diferenciar ROM interna de control de la ROM de firmware en `0xE000–0xFFFF`.
- Definir fetch de opcode reutilizable, despacho e ingreso a tres rutas: `LDI`, `ST` absoluto y `HALT`.
- Conservar los dos bytes de dirección de `ST` al seguir usando `MAR/MDR` para fetch; preparar el dato antes de `WR`.
- Distinguir **macroacción lógica** de microinstrucción física o ciclo de reloj.
- Verificar con JSON que las rutas de control implican las nueve transacciones de la traza R0.4 y preservan flags.
- Materiales: [unidad de control candidata](simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md), [microsecuencias JSON](simulador-javafx/MICROSECUENCIAS_AULA8_BORRADOR.json), `scripts/verificar_microsecuencias_aula8_borrador.py`.

## R0.6 — Subrutinas, pila y saltos condicionales

**Estado:** ruta documental verificable; **sin CPU ejecutable, micro-ROM binaria o pila física probada**.

- Respetar la convención candidata de `CALL/RET`: SP descendente, retorno de dos bytes little-endian y reanudación en instrucción siguiente.
- Añadir latches de retorno temporales candidatos; evitar perder destino de salto mientras `MAR/MDR` escriben o leen pila.
- Definir lectura de operandos para JMP/JZ/JNZ/JC/JNC siempre, incluso cuando la condición sea falsa.
- Explicar preservación de flags en flujo de control y la separación entre acarreo de dirección y `C` visible.
- Verificar documentalmente una prueba `CALL→LDI→RET→HALT`: 10 lecturas, 2 escrituras, SP restaurado; contrastar el bucle JNZ de R0.3.
- Materiales: [control de flujo y pila](simulador-javafx/CONTROL_FLUJO_PILA_AULA8_BORRADOR.md), [microflujo JSON](simulador-javafx/MICROFLUJO_AULA8_R0_6_BORRADOR.json), `scripts/verificar_flujo_aula8_r0_6_borrador.py`.

## R0.7 — Pila de datos, INC/DEC y bandera Z/N/C/V

**Estado:** borrador lógico documentado y contrastado con aritmética independiente; **sin CPU, micro-ROM ni montaje físico**.

- Detallar `PUSH/POP` de un byte y `PUSHX/POPX` de dos bytes, conservando la convención little-endian de `CALL/RET`.
- Explicar por qué `POP` lee antes de incrementar SP y por qué no borra la celda de RAM.
- Formalizar resultados de `INC/DEC`, preservación de C y desbordamiento firmado V en `7F→80` y `80→7F`.
- Comprobar matemáticamente Z/N/C/V contra referencia de enteros en operaciones ADD/ADC/SUB/SBC/CMP e INC/DEC.
- Documentar un programa PUSH→POP→DEC y conectar el bucle DEC→JNZ con R0.6; **sin fingir ejecución de CPU**.
- Materiales: [pila y banderas candidata](simulador-javafx/PILA_Y_BANDERAS_AULA8_BORRADOR.md), [modelo JSON](simulador-javafx/MICRODATOS_PILA_FLAGS_AULA8_R0_7_BORRADOR.json), `scripts/verificar_pila_flags_aula8_r0_7_borrador.py`.

## R0.8 — Direccionamiento indexado con X y SP

**Estado:** documentación candidata contrastada por aritmética de referencia; **sin CPU, micro-ROM ni memoria eléctrica ejecutadas**.

- Reutilizar `LD=0x12` y `ST=0x13` con modo X+disp8 (selectores `0x04–0x07`) o SP+disp8 (`0x08–0x0B`). Desplazamientos firmados de −128 a +127.
- Sumar dirección de 16 bits por dos pasadas ALU8, extendiendo signo y aislando `ADDR_CARRY` de las banderas visibles.
- Documentar `SETX` y una prueba de escritura/lectura en `0x6F01`: 14 lecturas y una escritura externas **esperadas**.
- Registrar una futura variable local por `[SP+0]`, sin afirmar que `ADJSP` ni la ABI están implementados.
- Materiales: [direcciones X/SP candidatas](simulador-javafx/DIRECCIONAMIENTO_INDEXADO_AULA8_BORRADOR.md), [rutas JSON](simulador-javafx/MICROINDICES_AULA8_R0_8_BORRADOR.json), `scripts/verificar_indices_aula8_r0_8_borrador.py`.

## R0.9 — Ajustes de X/SP y marcos de función

**Estado:** propuesta documental y aritmética contrastadas; **sin CPU, micro-ROM, ABI final ni hardware**.

- Formalizar `LEAX` (`15`), `ADDXW` (`16`), `SETSP` (`17`), `ADJSP` (`18`) y `XFROMSP` (`19`) reutilizando la codificación candidata R0.3.
- Documentar sumas de 16 bits en dos pasadas ALU8, sin pisar los registros fuente y sin alterar flags visibles.
- Mostrar prólogo y epílogo: `CALL`, `PUSHX`, `XFROMSP`, `ADJSP`, almacenamiento de un byte local, `POPX` y `RET`.
- Contrastar 1572864 casos matemáticos y una traza de 29 lecturas y cinco escrituras **esperadas**, sin atribuir ejecución a la CPU.
- Dejar abiertos la ABI general, parámetros, overflow de pila, latches físicos y tamaño de micro-ROM.
- Materiales: [ajustes y marcos](simulador-javafx/AJUSTES_X_SP_Y_MARCOS_AULA8_BORRADOR.md), [rutas JSON](simulador-javafx/MICROAJUSTES_AULA8_R0_9_BORRADOR.json) y `scripts/verificar_ajustes_aula8_r0_9_borrador.py`.

## R0.10 — ABI candidata de funciones MiniC-Aula8

**Estado:** propuesta contrastada mediante un modelo de escritorio; **no existe CPU, compilador, ABI aprobada ni electrónica**.

- Fijar como propuesta una ranura de dos bytes para argumentos u8/u16, empujar alto antes que bajo y argumentos de derecha a izquierda; limpieza de argumentos a cargo del llamador.
- Establecer prólogo y epílogo de cinco acciones lógicas, guardando X/R2/R3 siempre para estabilizar offsets; retorno u8 en R0, u16 en R1:R0.
- Dejar explícito que los flags son volátiles entre llamadas y que el llamador no debe reutilizar un resultado de comparación anterior al CALL.
- Documentar un programa CALL→SUMAR_UNO→RET de 63 bytes con resultado 0x0200 y traza de 73 lecturas+10 escrituras **esperadas**.
- Probar 640 marcos de 0..4 argumentos y una cuenta matemática de profundidad de recursividad, **sin certificar una pila real**.
- Materiales: [ABI MiniC candidata](simulador-javafx/ABI_MINIC_AULA8_R0_10_BORRADOR.md), [contrato JSON](simulador-javafx/ABI_MINIC_AULA8_R0_10_BORRADOR.json), `scripts/verificar_abi_minic_aula8_r0_10_borrador.py`.

## R0.11 — Tabla ROM y monitor hexadecimal Aula-8 candidatos

**Estado:** contrato documentado y comprobación de sintaxis; **sin ROM compilada, CPU ni controlador terminal/almacenamiento**.

- Reservar como **propuesta** 32 entradas ROM de 4 B en FF00–FF7F; asignar solo PUTC/GETC/PUTS/STATUS, codificadas con JMP absoluto16 little-endian más NOP. No adjudicar aún servicios de bloques ni destinos internos de ejemplo.
- Documentar RESET FFFC–FFFD little-endian: dos bytes `00 E0` apuntarían hipotéticamente a E000; RAM no inicializada y micro-ROM separada.
- Delimitar la ABI ROM frente a MiniC: entrada CALL a ranura, salto interno, salida RET, R2/R3/X preservados y R0/R1/FLAGS volátiles.
- Concretar sintaxis de HELP/MEM/POKE/RUN; proteger provisionalmente POKE y RUN con ventana de práctica `6000–6FFF`, MEM con regiones RAM/ROM; REG/LOAD sin implementación, no ofrecer funcionalidades falsas.
- Ilustrar `RUN 6000` y doble retorno al monitor usando dos CALL/RET; `HALT` requiere reinicio o mecanismo posterior de depuración, **no** restituye el prompt.
- Probar en escritorio cuatro entradas ROM y 40 casos de sintaxis/límites, marcando que esto **no** ejecuta firmware ni demuestra cabida de 8 KiB.
- Materiales: [ROM y monitor](simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.md), [contrato JSON](simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.json), `scripts/verificar_rom_monitor_aula8_r0_11_borrador.py`.

## R0.12 — Registro de bloques y LOAD crudo candidato

**Estado:** contrato MMIO documentado y modelo de persistencia en anfitrión probado; **sin hardware, CPU, ROM, cargador nativo ni archivos nombrados**.

- Respetar el rango de almacenamiento reservado C010–C01F: ocho registros de 8 bits en direcciones pares con COMMAND, STATUS, BLOCK_LO/HI, DATA, ERROR y COUNT_LO/HI.
- Proponer bloques de 256 B, índices little-endian de 16 bits, cuatro comandos NOP/READ/WRITE/RESET y estados BUSY/DRQ/DONE/ERROR con contador 0..256.
- Descartar escrituras incompletas y detectar bloque ausente, acceso a DATA inadecuado, comando nuevo mientras BUSY y error de imagen, sin prometer resistencia real a pérdida de energía.
- Especificar el futuro `LOAD bloque_hex4 destino_hex4 cantidad_hex2` solo para overlay 1000–2FFF o programa 6000–6FFF, límites estrictos/alineación 256 B, sin ejecutar cargas parciales.
- Conservar `LOAD` del monitor R0.11 como **NO DISPONIBLE** hasta implementar registros y secuencias en la CPU; sin asignar ranuras ROM de bloques ni inventar sistema de archivos.
- Ejecutar **20 pruebas de un modelo de referencia Python en anfitrión**, incluyendo reapertura de imagen y fallo inyectado antes de reemplazo, sin atribuirlo al hardware Aula.
- Materiales: [contrato de bloques](simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md), [JSON](simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.json), [modelo Python](scripts/modelo_bloques_aula8_r0_12.py) y `scripts/verificar_bloques_aula8_r0_12_borrador.py`.

## R0.13 — AEX1 de Aula-8, sin cambiar el LOAD crudo

**Estado:** cabecera candidata, packer/inspector y 42 pruebas Python de anfitrión; **NO** loader ROM, CPU ni programas Aula ejecutables.

- Proponer formato **AEX1**, cabecera 32 B en primer bloque crudo R0.12 de 256 B, más payload y relleno a cero. Incluir firma/version/CPU ID 08, origen/entrada/tamaño, CRC16 y sectores necesarios.
- Distinguir tipo `01` de práctica (6000–6FFF) y `02` de herramienta overlay (1000–2FFF); origen alineado 256 B, entrada dentro de bytes útiles, cero en reservas, sin código fuera de RAM autorizada.
- Conservar `LOAD` crudo y proponer comando **separado** `LOADX bloque_hex4`, ambos NO DISPONIBLES hasta firmware/CPU real. No introducir archivos nombrados, bloques con directorio o slots ROM sin especificación.
- La validación completa antes de copiar a RAM se prueba en anfitrión. **Resolver antes de R1** cómo un loader real haría staging/rollback con buffer 3584 B y herramienta de hasta 8160 B: no prometer atomicidad.
- Mantener Aula-16 con bus externo **16 bits** e ISA propia. AEX1 con CPU ID 08 no aplica a Aula-16.
- Materiales: [contrato AEX1](simulador-javafx/EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md), [JSON](simulador-javafx/EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.json), [modelo anfitrión](scripts/modelo_ejecutable_aula8_r0_13.py), [CLI](scripts/empaquetar_aex_aula8_r0_13.py), [42 pruebas](scripts/verificar_ejecutable_aula8_r0_13_borrador.py).

## R0.14 — Verificar y copiar LOADX en dos pasadas de referencia

**Estado:** 30 pruebas Python anfitrión, sin firmware, CPU ni atomicidad de RAM demostrada.

- La primera pasada consume sectores de 256 B y calcula CRC incremental, detectando errores **antes de cualquier copia**.
- La segunda vuelve a leer, compara cabecera y CRC y copia payload en fragmentos de máximo 256 B. Si falla, RAM puede quedar parcialmente actualizada; se cancela toda posibilidad de **entrada supervisada futura** en el modelo, no en ROM real.
- El búfer 0200–0FFF tiene capacidad suficiente para **un bloque** temporal; la verificación completa ya no requiere retener 8160 B de herramienta. Quedan por diseñar mecanismos reales de invalidación, consistencia de lectura y protección ante corte eléctrico.
- Elaborar [auditoría editorial](libro/ESTADO_Y_PENDIENTES_R0_14.md): los 24 capítulos, figuras y pruebas quedan **pendientes**, la portada es una actividad aparte.
- **Cerrar aquí la serie R0 de detalles incrementales**. Ya se puede comenzar el capítulo 1 mientras se prepara R1 en paralelo. No postergar el manuscrito por más formatos.
- Materiales: [LOADX de dos pasadas](simulador-javafx/LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md), [contrato JSON](simulador-javafx/LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.json), [modelo Python](scripts/modelo_loadx_aula8_r0_14.py), [30 pruebas](scripts/verificar_loadx_aula8_r0_14_borrador.py).

## R1 — Contrato técnico de hardware y lenguaje máquina

**Estado:** pendiente. Se realiza al comenzar la fase de contenido del libro.

1. Fichas de hardware con modelos, pinout, tensiones y niveles lógicos verificados.
2. Conjunto completo de opcodes y formatos, Aula-8 y Aula-16.
3. Semántica de flags, pila, endian, traps y lectura/escritura desalineada.
4. Tablas de microoperaciones y señales de control.
5. Vectores de arranque, entradas ROM, puerto terminal y protocolo de bloque.
6. Vectores de prueba para sumadores, registros, memoria y CPU.
7. Propiedad del bus al depositar bytes, semántica de `RUN`/`HALT`, retorno explícito al monitor, política de RAM y tamaño de firmware; prever formato de ejecutables de utilidades.
8. Medir secciones ROM/RAM con mapas de enlace reales. Si el editor o ensamblador no cabe en su *overlay*, ajustar el diseño con pruebas; no presentar el presupuesto de R0.2 como hecho probado.

**No declarar R1 completada sin** casos límite y pruebas de consistencia; si no se dispone de prototipo eléctrico, indicar que esa parte continúa pendiente.

## R2 — Libro, fundamentos físicos

**Estado:** pendiente. Construcción del manual.

- Contrato editorial definitivo y diseño de estilos.
- Electricidad básica, fuente regulada, resistencias, transistor NPN/MOSFET.
- Inversor, NAND, tablas de verdad, símbolos electrónicos.
- Cada circuito: cálculo, esquema, montaje y prueba razonable.
- Word/PDF con figuras originales y revisión visual.

## R3 — Libro, lógica, memoria y ALU

**Estado:** pendiente.

- Biestables, celda SRAM, D latch/flip-flop, byte y registro.
- Decodificadores, buses, triestado, ROM y SRAM comercial.
- Sumadores, resta por complemento, banderas, ALU.
- Comparar simulación lógica y restricciones físicas.

## R4 — Libro, Aula-8 completa

**Estado:** pendiente.

- Datapath, registros, PC/SP/X, control y microoperaciones.
- Fetch, decode, execute; operandos, stack, CALL/RET.
- Ejecución minuciosa de un programa original.
- Ensamblador y memoria de programa.
- Introducción manual de bytes mediante panel detenido; el esquema de bus debe justificar qué conductor tiene el control.

## R5 — Libro, microcomputadora y software

**Estado:** pendiente.

- Arranque, ROM de firmware, terminal, entrada/salida mapeada, monitor.
- Servicios ROM como PUTC, GETC y PUTS.
- Almacenamiento por bloques y programas descargables.
- MiniC-Aula y mini sistema operativo limitado.
- Editor de líneas y ensamblador **nativos de Aula-8**, desde su primera construcción con herramientas cruzadas hasta ejecutarse desde RAM. Diferenciar las fases sin ocultar la necesidad del bootstrap.

## R6 — Libro, Aula-16 y cierre editorial

**Estado:** pendiente.

- Ancho de palabra y bus de 16 bits.
- Banco par/impar, lectura de bytes, alineación y little-endian.
- Compilación para Aula-16, comparación con Aula-8.
- Soluciones separadas, glosario, bibliografía, QA, Word y PDF definitivos.

## R7 — Simulador, núcleo digital verificable

**Estado:** posterior al libro; no iniciar sin mandato de usuario.

- Java 21, Maven, motor lógico sin dependencia de JavaFX.
- Biblioteca acotada de componentes, jerarquía de módulos, netlist único.
- Validador de conexiones, CPU de referencia, ensambladores, firmware y pruebas.
- Prueba de que el ensamblador y editor **nativos** realmente ejecutan código de la CPU Aula y generan bytes iguales al ensamblador cruzado.
- Estado lógico 0/1/Z/X cuando corresponda; temporización simplificada declarada.

## R8 — Simulador, taller 2D y 3D

**Estado:** posterior.

- Vista 2D esquemática, 3D geométrica, selección de componente y estado visible.
- Modo «computadora terminada» y «hazlo tú mismo».
- Guías graduadas, validaciones y mini fichas.
- Panel de depósito manual como lección, terminal de ROM y experiencias de edición nativa; la representación no presupone un panel físico certificado.
- Renderizado jerárquico para evitar millones de nodos 3D.
- Pruebas en Windows del usuario y paquete de retroalimentación.

## R9 — Extensiones opcionales

**No son parte de la primera entrega.** Computadoras históricas adicionales, nuevas CPU, periféricos variados, interrupciones avanzadas, interfaz gráfica retro, almacenamiento físico alternativo, nuevos compiladores o un editor más abierto.

## Cadencia

Trabajar por entregas pequeñas, cada una con objetivo, ejemplos, pruebas, revisión y lista de pendientes. Al terminar una entrega, producir un changelog; no reenviar una solución parcial como si fuera liberación final.

