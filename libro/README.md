# Libro — una computadora desde sus transistores

**Estado editorial C27-0.1:** la edición reúne **26 capítulos**, los 24 troncales más **7B «Del bit al significado»** y **23B «De los mapas de caracteres al escritorio gráfico»**. El [volumen maestro C27](Aula_Computadora_C27_0_1_MAESTRO.pdf) y su [Word editable](Aula_Computadora_C27_0_1_MAESTRO.docx) tienen **236 páginas, 115 figuras y 110 ejercicios esenciales con solución**. Los 26 fascículos conservan sus 312 actividades originales. C27 añade etapas de construcción de la CPU, memoria contigua y portada conceptual. El [estado C27](ESTADO_EDITORIAL_C27.md) distingue qué está probado y qué no; las referencias C26 de más abajo se conservan como historial de la edición anterior.

El libro será una obra original en español que lleve al lector de la electrónica elemental a una microcomputadora funcional. La máquina central del relato es **Aula-8**; **Aula-16** sirve para comprender una arquitectura más amplia, incluyendo su bus externo de datos de 16 bits.

**Capítulo 23B ya realizado:** [«De los mapas de caracteres al escritorio gráfico»](capitulos/23v_de_mapas_de_caracteres_a_escritorio_grafico.md) conecta ROM de glifos, texto, píxeles, color y tipografía hasta ventanas, con **siete esquemas reproducibles**. No exige construir todavía un controlador gráfico.

## Documentos de trabajo

- **[Libro C27 (PDF)](Aula_Computadora_C27_0_1_MAESTRO.pdf)** — edición actual con ejemplos de memoria, buses y construcción progresiva.
- **[Libro C27 (Word)](Aula_Computadora_C27_0_1_MAESTRO.docx)** — original editable con ecuaciones OfficeMath.
- **[Índice C27 (JSON)](INDICE_C27_0_1.json)** — paginación medida en el volumen.
- **[Estado C27](ESTADO_EDITORIAL_C27.md)** — auditorías, mejoras y límites.

### Referencias y fichas históricas de la edición C26

- **[Libro completo (PDF)](Aula_Computadora_C26_0_1_MAESTRO.pdf)** — edición maestra C26 de lectura, con índice paginado, esquemas corregidos, solucionarios y bibliografía final.
- **[Libro completo (Word)](Aula_Computadora_C26_0_1_MAESTRO.docx)** — volumen editable con ecuaciones OMML.
- **[Índice de páginas (JSON)](INDICE_C26_0_1.json)** — inicios reales de los 26 capítulos.
- **[Estado editorial C26](ESTADO_EDITORIAL_C26.md)** — cambios y revisión humana pendiente.

- [Capítulo 1: La corriente y sus caminos (Word)](capitulos/01_la_corriente_y_sus_caminos.docx) — texto y ecuaciones editables, 4 diagramas, incluida una protoboard.
- [Capítulo 1: La corriente y sus caminos (PDF)](capitulos/01_la_corriente_y_sus_caminos.pdf) — diez páginas con texto seleccionable y esquema de conexiones en protoboard.
- [Capítulo 2: El transistor como interruptor (Word)](capitulos/02_el_transistor_como_interruptor.docx) — diez páginas, 13 expresiones editables, tres diagramas incrustados.
- [Capítulo 2: El transistor como interruptor (PDF)](capitulos/02_el_transistor_como_interruptor.pdf) — diez páginas con texto seleccionable, cálculos del NPN 2N3904 y ejercicios.
- [Capítulo 3: De interruptores a lógica (Word)](capitulos/03_de_interruptores_a_logica.docx) — diez páginas, 14 ecuaciones editables y cuatro figuras.
- [Capítulo 3: De interruptores a lógica (PDF)](capitulos/03_de_interruptores_a_logica.pdf) — diez páginas con texto seleccionable, tablas de verdad, NAND SN74HCT00, LED y ejercicios.
- [Capítulo 4: Construir funciones con compuertas (Word)](capitulos/04_construir_funciones_con_compuertas.docx) — nueve páginas, trece ecuaciones editables, cuatro figuras y doce ejercicios.
- [Capítulo 4: Construir funciones con compuertas (PDF)](capitulos/04_construir_funciones_con_compuertas.pdf) — nueve páginas con OR, NOR, XOR, síntesis de XOR con NAND y simplificación explicada.
- [Capítulo 5: La realimentación conserva información (Word)](capitulos/05_la_realimentacion_conserva_informacion.docx) — ocho páginas, once ecuaciones editables, cuatro figuras y doce ejercicios.
- [Capítulo 5: La realimentación conserva información (PDF)](capitulos/05_la_realimentacion_conserva_informacion.pdf) — estados SET, RESET, HOLD, entrada prohibida y secuencia resuelta.
- [Capítulo 6: Memorizar en el tiempo (Word)](capitulos/06_memorizar_en_el_tiempo.docx) — ocho páginas, nueve ecuaciones, cuatro diagramas y doce ejercicios.
- [Capítulo 6: Memorizar en el tiempo (PDF)](capitulos/06_memorizar_en_el_tiempo.pdf) — latch D, flip-flop D, reloj, reset y requisitos temporales.
- [Capítulo 7: Del bit al registro (Word)](capitulos/07_del_bit_al_registro.docx) — ocho páginas, nueve ecuaciones editables, cuatro esquemas y doce ejercicios.
- [Capítulo 7: Del bit al registro (PDF)](capitulos/07_del_bit_al_registro.pdf) — byte, LOAD, multiplexor, alta impedancia y transferencia A→B.
- [Capítulo 7B: Del bit al significado (Word)](capitulos/07b_del_bit_al_significado.docx) — señales lógicas, máscaras, enteros firmados, ASCII/UTF-8 y tipos del programa.
- [Capítulo 7B: Del bit al significado (PDF)](capitulos/07b_del_bit_al_significado.pdf) — puente entre representación de bits y significado del programa.
- [Capítulo 8: Direcciones y buses (Word)](capitulos/08_direcciones_y_buses.docx) — nueve páginas; conversión de direcciones, cuatro diagramas, doce ecuaciones y ejercicios.
- [Capítulo 8: Direcciones y buses (PDF)](capitulos/08_direcciones_y_buses.pdf) — decodificador, buses, lectura/escritura, 16 bits de direcciones y bancos little-endian.
- [Capítulo 9: RAM y ROM reales (Word)](capitulos/09_ram_y_rom_reales.docx) — ocho páginas, cuatro diagramas y 12 ejercicios resueltos.
- [Capítulo 9: RAM y ROM reales (PDF)](capitulos/09_ram_y_rom_reales.pdf) — SRAM/EEPROM comerciales, señales, mapa ilustrativo y expansión de memoria.
- [Capítulo 10: El circuito que suma (Word)](capitulos/10_el_circuito_que_suma.docx) — ocho páginas, 17 ecuaciones, cuatro ilustraciones y doce ejercicios.
- [Capítulo 10: El circuito que suma (PDF)](capitulos/10_el_circuito_que_suma.pdf) — medio sumador, sumador completo, 13 + 9, acarreo, desbordamiento y suma de dos bytes.
- [Capítulo 11: La unidad aritmético-lógica (Word)](capitulos/11_la_unidad_aritmetico_logica.docx) — ocho páginas, 21 ecuaciones, cuatro figuras y doce ejercicios con soluciones.
- [Capítulo 11: La unidad aritmético-lógica (PDF)](capitulos/11_la_unidad_aritmetico_logica.pdf) — resta, comparaciones con/sin signo, lógica bit a bit y MUX de ALU.
- [Capítulo 12: Arquitectura Aula-8 (Word)](capitulos/12_arquitectura_aula_8.docx) — nueve páginas, 12 ecuaciones, cuatro figuras y 12 ejercicios resueltos.
- [Capítulo 12: Arquitectura Aula-8 (PDF)](capitulos/12_arquitectura_aula_8.pdf) — camino de datos, registros, MAR/MDR, buses, traza LDI candidata y dirección de 16 bits con ALU8.
- [Capítulo 13: La unidad de control (Word)](capitulos/13_la_unidad_de_control.docx) — ocho páginas, ocho expresiones editables, cuatro figuras y doce ejercicios.
- [Capítulo 13: La unidad de control (PDF)](capitulos/13_la_unidad_de_control.pdf) — lectura de opcodes, secuenciador, despacho, LDI/ST/HALT y distinción entre acciones lógicas y ciclos físicos.
- [Capítulo 14: De números a instrucciones (Word)](capitulos/14_de_numeros_a_instrucciones.docx) — nueve páginas, 12 OMML, cuatro ilustraciones y doce ejercicios resueltos.
- [Capítulo 14: De números a instrucciones (PDF)](capitulos/14_de_numeros_a_instrucciones.pdf) — hexadecimal, opcode, selector, direccionamiento, panel detenido y monitor ROM propuesto.
- [Capítulo 15: La instrucción en movimiento (Word)](capitulos/15_la_instruccion_en_movimiento.docx) — ocho páginas, doce OMML, cuatro diagramas y doce ejercicios con soluciones.
- [Capítulo 15: La instrucción en movimiento (PDF)](capitulos/15_la_instruccion_en_movimiento.pdf) — fetch/decode/execute, registros PC/MAR/MDR/IR, LDI/ST/HALT y nueve transacciones externas esperadas.
- [Capítulo 16: Subrutinas y pila (Word)](capitulos/16_subrutinas_y_pila.docx) — siete páginas, doce OMML, cuatro diagramas y doce ejercicios con soluciones.
- [Capítulo 16: Subrutinas y pila (PDF)](capitulos/16_subrutinas_y_pila.pdf) — CALL/RET, pila descendente, retornos anidados, saltos y bucles.
- [Capítulo 17: Encender una computadora (Word)](capitulos/17_encender_una_computadora.docx) — ocho páginas, doce OMML, cuatro figuras y doce ejercicios resueltos.
- [Capítulo 17: Encender una computadora (PDF)](capitulos/17_encender_una_computadora.pdf) — vector de reset, ROM, tabla pública, monitor hexadecimal y RUN/RET/HALT.
- [Capítulo 18: Hablar con la máquina (Word)](capitulos/18_hablar_con_la_maquina.docx) — ocho páginas, 14 OMML, cuatro diagramas y doce ejercicios con soluciones.
- [Capítulo 18: Hablar con la máquina (PDF)](capitulos/18_hablar_con_la_maquina.pdf) — terminal, memoria de E/S, servicios candidatos de ROM, eco y variable en RAM.
- [Capítulo 19: Guardar y recuperar programas (Word)](capitulos/19_guardar_y_recuperar_programas.docx) — ocho páginas, 15 OMML, cuatro diagramas y doce ejercicios con soluciones.
- [Capítulo 19: Guardar y recuperar programas (PDF)](capitulos/19_guardar_y_recuperar_programas.pdf) — bloques de 256 B, controlador candidato, persistencia y LOAD/LOADX propuestos.
- [Capítulo 20: Programar un pequeño sistema (Word)](capitulos/20_programar_un_pequeno_sistema.docx) — 9 páginas, 14 OMML, cuatro diagramas y doce ejercicios con soluciones.
- [Capítulo 20: Programar un pequeño sistema (PDF)](capitulos/20_programar_un_pequeno_sistema.pdf) — dos pasadas, suma, Euclides, Fibonacci y monitor propuesto.
- [Capítulo 21: Qué implica ampliar la palabra (Word)](capitulos/21_que_implica_ampliar_la_palabra.docx) — 8 páginas, 18 OMML, cuatro diagramas y doce ejercicios con soluciones.
- [Capítulo 21: Qué implica ampliar la palabra (PDF)](capitulos/21_que_implica_ampliar_la_palabra.pdf) — datos de 16 bits, banderas, sumador y RAM direccionada por bytes.
- [Capítulo 22: Un bus externo de 16 bits (Word)](capitulos/22_un_bus_externo_de_16_bits.docx) — 8 páginas, 13 OMML, cuatro figuras, dos carriles y 12 ejercicios resueltos.
- [Capítulo 22: Un bus externo de 16 bits (PDF)](capitulos/22_un_bus_externo_de_16_bits.pdf) — bancos de 8 bits, byte par/impar, little-endian, alineación y memoria mapeada.
- [Capítulo 23: Programación para Aula-16 (Word)](capitulos/23_programacion_para_aula_16.docx) — 8 páginas, 14 OMML, cuatro figuras y 12 ejercicios resueltos.
- [Capítulo 23: Programación para Aula-16 (PDF)](capitulos/23_programacion_para_aula_16.pdf) — recorrido de palabras en RAM, suma, Euclides, Fibonacci y ABI pendiente.
- [Capítulo 23B: De los mapas de caracteres al escritorio gráfico (Word)](capitulos/23v_de_mapas_de_caracteres_a_escritorio_grafico.docx) — 7 ilustraciones; ROM de glifos, VRAM, colores y tipografía.
- [Capítulo 23B: De los mapas de caracteres al escritorio gráfico (PDF)](capitulos/23v_de_mapas_de_caracteres_a_escritorio_grafico.pdf) — caracteres y glifos 8×8, matriz de texto 32×16, bitmap 2bpp, MMIO, fuentes vectoriales y escritorios.
- [Capítulo 24: Una computadora que podemos explicar (Word)](capitulos/24_una_computadora_que_podemos_explicar.docx) — 9 páginas, 4 figuras, 13 OMML, 12 ejercicios con soluciones.
- [Capítulo 24: Una computadora que podemos explicar (PDF)](capitulos/24_una_computadora_que_podemos_explicar.pdf) — mapa completo, escalera de algoritmos, Aula-8/Aula-16 y criterios de implementación real.
- [Programas ASM del capítulo 20](programas/) y [ensamblador educativo de anfitrión](../scripts/ensamblador_dos_pasadas_aula8_educativo.py): bytes de referencia reproducibles; **no** ejecutan Aula-8.
- Manuscritos editables en Markdown de los [capítulos 1](capitulos/01_la_corriente_y_sus_caminos.md), [2](capitulos/02_el_transistor_como_interruptor.md), [3](capitulos/03_de_interruptores_a_logica.md), [4](capitulos/04_construir_funciones_con_compuertas.md), [5](capitulos/05_la_realimentacion_conserva_informacion.md), [6](capitulos/06_memorizar_en_el_tiempo.md), [7](capitulos/07_del_bit_al_registro.md), [8](capitulos/08_direcciones_y_buses.md), [9](capitulos/09_ram_y_rom_reales.md), [10](capitulos/10_el_circuito_que_suma.md), [11](capitulos/11_la_unidad_aritmetico_logica.md), [12](capitulos/12_arquitectura_aula_8.md), [13](capitulos/13_la_unidad_de_control.md), [14](capitulos/14_de_numeros_a_instrucciones.md), [15](capitulos/15_la_instruccion_en_movimiento.md), [16](capitulos/16_subrutinas_y_pila.md), [17](capitulos/17_encender_una_computadora.md), [18](capitulos/18_hablar_con_la_maquina.md) y [19](capitulos/19_guardar_y_recuperar_programas.md); [figuras originales](figuras/) en SVG/PNG.
- [Estado editorial después del capítulo 1](ESTADO_EDITORIAL_C01.md): alcance, controles y próximos pasos.
- [Estado editorial después del capítulo 2](ESTADO_EDITORIAL_C02.md): lo entregado, límites y el orden restante.
- [Estado editorial después del capítulo 3](ESTADO_EDITORIAL_C03.md): revisión de las diez páginas, 132 controles y 21 capítulos pendientes.
- [Estado editorial después del capítulo 4](ESTADO_EDITORIAL_C04.md): revisión de nueve páginas, 146 controles y 20 capítulos pendientes.
- [Estado editorial después del capítulo 5](ESTADO_EDITORIAL_C05.md): revisión de ocho páginas, 123 controles y 19 capítulos pendientes.
- [Estado editorial después del capítulo 6](ESTADO_EDITORIAL_C06.md): revisión de ocho páginas, 171 controles y 18 capítulos pendientes.
- [Estado editorial después del capítulo 7](ESTADO_EDITORIAL_C07.md): ocho páginas, 198502 controles lógicos/documentales y 17 capítulos pendientes.
- [Estado editorial después del interludio P07B](ESTADO_EDITORIAL_P07B.md): ocho páginas adicionales, 1383 controles y 17 capítulos numerados pendientes.
- [Estado editorial después del capítulo 8](ESTADO_EDITORIAL_C08.md): nueve páginas nuevas, 459379 controles matemáticos/documentales y 16 capítulos numerados pendientes.
- [Estado editorial después del capítulo 9](ESTADO_EDITORIAL_C09.md): ocho páginas nuevas, 368752 controles matemáticos/documentales y 15 capítulos numerados pendientes.
- [Estado editorial después del capítulo 10](ESTADO_EDITORIAL_C10.md): ocho páginas, 786541 controles matemáticos/documentales y 14 capítulos numerados pendientes.
- [Estado editorial después del capítulo 11](ESTADO_EDITORIAL_C11.md): ocho páginas, 786524 controles matemáticos/documentales y 13 capítulos numerados pendientes.
- [Estado editorial después del capítulo 12](ESTADO_EDITORIAL_C12.md): nueve páginas, 2752599 controles matemáticos/documentales y 12 capítulos numerados pendientes.
- [Estado editorial después del capítulo 13](ESTADO_EDITORIAL_C13.md): ocho páginas, 196771 controles de modelo/documento y 11 capítulos numerados pendientes.
- [Estado editorial después del capítulo 14](ESTADO_EDITORIAL_C14.md): nueve páginas, 132993 controles de modelo/documento y 10 capítulos numerados pendientes.
- [Estado editorial después del capítulo 15](ESTADO_EDITORIAL_C15.md): ocho páginas, 143464 controles de modelo/documento y 9 capítulos numerados pendientes.
- [Estado editorial después del capítulo 16](ESTADO_EDITORIAL_C16.md): siete páginas, 184283 controles de modelo/documento y 8 capítulos numerados pendientes.
- [Estado editorial después del capítulo 17](ESTADO_EDITORIAL_C17.md): ocho páginas, 196727 controles de modelo/documento y 7 capítulos numerados pendientes.
- [Estado editorial después del capítulo 18](ESTADO_EDITORIAL_C18.md): ocho páginas, 646 controles de contratos/archivos y 6 capítulos numerados pendientes.
- [Estado editorial después del capítulo 19](ESTADO_EDITORIAL_C19.md): ocho páginas, 205037 controles de contratos/modelo/archivos y 5 capítulos numerados pendientes.
- [Estado editorial después del capítulo 20](ESTADO_EDITORIAL_C20.md): nueve páginas, 130685 controles de ensamblador/modelo/archivos.
- [Estado editorial después del capítulo 21](ESTADO_EDITORIAL_C21.md): ocho páginas, 126921 controles de palabras de 16 bits/modelo/archivos; faltan 3 capítulos numerados.
- [Estado editorial después de los capítulos 22 y 23](ESTADO_EDITORIAL_C23.md): 16 páginas, ocho figuras y modelos de memoria y algoritmos; solo queda el capítulo 24 numerado.
- [Estado editorial después de capítulo 24 e interludio P23V](ESTADO_EDITORIAL_C24.md): 24/24 manuscritos numerados más dos interludios, 220 páginas, 105 esquemas, edición maestra pendiente.
- [Escalera de programas Aula-8](ESCALERA_DE_PROGRAMAS_AULA8.md): de almacenar un byte a sumar, usar CALL/RET, trabajar con terminal, guardar, calcular MCD y Fibonacci hasta un mini sistema; cada paso señala lo que aún no puede ejecutarse en Aula-8.
- [Fidelidad y regeneración de figuras](GUIA_DE_FIDELIDAD_DE_FIGURAS.md): cómo reproducir diagramas SVG/PNG con Python/Inkscape y qué falta para validar circuitos a nivel eléctrico.
- [Propuesta original: Del bit al significado](PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md): desarrollada como interludio tras capítulo 7; no altera el total numerado.

- [CONTRATO_EDITORIAL.md](CONTRATO_EDITORIAL.md): compromiso de calidad y voz didáctica.
- [CURRICULO.md](CURRICULO.md): seis partes, 24 capítulos previstos y prerrequisitos.
- [PLANTILLA_CAPITULO.md](PLANTILLA_CAPITULO.md): método para convertir un tema en conocimiento.
- [DIAGRAMAS_Y_COMPONENTES.md](DIAGRAMAS_Y_COMPONENTES.md): tipos de diagramas, esquemas y fichas.
- [FUENTES_Y_ORIGINALIDAD.md](FUENTES_Y_ORIGINALIDAD.md): uso correcto de la obra de Scott y del manuscrito del usuario.
- [VALIDACION_EDITORIAL.md](VALIDACION_EDITORIAL.md): revisiones Word, PDF, contenidos y pruebas.
- [ESTADO_Y_PENDIENTES_R0_14.md](ESTADO_Y_PENDIENTES_R0_14.md): auditoría de los **24 capítulos pendientes** y ruta real para escribir, ilustrar y verificar la obra, excluida la portada.

El producto final se entregará en **Word editable + PDF**, tras comprobar ambos. La obra debe permitir estudiar sus ejercicios y comprender los circuitos sin depender de una aplicación externa.

## Principio narrativo

Cada nueva capacidad aparece porque resuelve una necesidad comprensible:

1. Un transistor permite controlar una corriente.
2. Varias conexiones permiten representar condiciones lógicas.
3. La realimentación permite conservar un bit.
4. Muchos bits permiten almacenar datos.
5. Una ALU permite operar con esos datos.
6. Una unidad de control permite ejecutar instrucciones.
7. RAM, ROM y periféricos forman una computadora.
8. El software permite aprovecharla.

No será una simple reseña histórica ni un catálogo de tecnologías.

