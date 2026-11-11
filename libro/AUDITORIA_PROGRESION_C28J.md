# Auditoría de progresión editorial C28-J — 26 capítulos

**Método:** inventario automático de fuentes Markdown, fascículos
Word/PDF, referencias a PNG/SVG, ecuaciones y encabezados de
construcción. **No** constituye lectura semántica certificada.

- Capítulos: **26** (objetivo: 26).
- Bloques explícitos «Construimos Aula…»: **20**.
- Referencias a ilustraciones: **115**.
- Diagramas SVG adicionales de pilotos fuera de los 26 capítulos: **9**.
- Problemas estructurales detectados: **0**.

| Cap. | Qué aporta a la computadora | «Construimos» | Figuras | Fórmulas | Estructura |
| --- | --- | --- | ---: | ---: | --- |
| 01 | corriente, resistencia y alimentación de una práctica | No (revisar narrativa) | 4 | 13 | OK |
| 02 | transistor usado como interruptor controlado | No (revisar narrativa) | 3 | 13 | OK |
| 03 | tabla de verdad, NAND y señal de habilitación | Sí | 4 | 14 | OK |
| 04 | funciones combinacionales y XOR con NAND | No (revisar narrativa) | 4 | 13 | OK |
| 05 | realimentación y almacenamiento de un bit | Sí | 5 | 11 | OK |
| 06 | biestable D y control de carga mediante reloj | Sí | 4 | 9 | OK |
| 07 | ocho biestables forman el registro R0 de Aula-8 | Sí | 5 | 8 | OK |
| 07B | significado de un byte, números, texto e instrucciones | No (revisar narrativa) | 4 | 8 | OK |
| 08 | buses de 16 direcciones y 8 datos; acceso a memoria | Sí | 5 | 11 | OK |
| 09 | transferencias entre registros, RAM y ROM | Sí | 4 | 10 | OK |
| 10 | sumador y cambio del estado aritmético | Sí | 4 | 17 | OK |
| 11 | selección de operaciones de una ALU de 8 bits | Sí | 4 | 21 | OK |
| 12 | integración del datapath de Aula-8 | Sí | 5 | 11 | OK |
| 13 | señales que coordinan las microacciones | Sí | 4 | 8 | OK |
| 14 | bytes de programa y flujo de lectura del panel | Sí | 6 | 11 | OK |
| 15 | trayecto PC/MAR/MDR/IR y acceso a instrucciones | Sí | 4 | 10 | OK |
| 16 | pila, SP, saltos, CALL y RET | Sí | 6 | 11 | OK |
| 17 | vector de reset y arranque desde ROM | Sí | 4 | 11 | OK |
| 18 | terminal y periféricos en mapa de memoria | Sí | 4 | 14 | OK |
| 19 | bloques de almacenamiento y recuperación de programas | Sí | 4 | 15 | OK |
| 20 | programas y ensamblado en el anfitrión | Sí | 4 | 14 | OK |
| 21 | operaciones de 16 bits sin alterar 16 bits de dirección | Sí | 4 | 17 | OK |
| 22 | bus externo Aula-16 de 16 bits y bancos bajo/alto | Sí | 5 | 11 | OK |
| 23 | algoritmos Aula-16 con ISA aún candidata | No (revisar narrativa) | 4 | 12 | OK |
| 23B | periférico de vídeo V1 en texto y gráficos | Sí | 7 | 13 | OK |
| 24 | integración didáctica y límites del prototipo | No (revisar narrativa) | 4 | 13 | OK |

## Capítulos sin encabezado «Construimos»

**01**, **02**, **04**, **07B**, **23**, **24**

**Interpretación:** la ausencia de ese título NO significa que falte
una explicación constructiva. Revisar especialmente el salto de
conceptos a piezas en C04 y 07B, el carácter provisional de C23
y la síntesis final de C24. C01/C02 incluyen prácticas propias y
tampoco requieren una sección con ese nombre para ser correctos.

## Próximos controles manuales (todavía no certificados)

1. Leer todos los cierres y aperturas de capítulo como una secuencia continua.
2. Comprobar que diagramas 2D, tablas y nombres de señales coinciden con su modelo.
3. Añadir un anclaje de construcción solo cuando mejore la comprensión.
4. Distinguir pruebas digitales de documentación y de montajes físicos.
5. Integrar el suplemento C28-H únicamente tras revisar el capítulo 15 y la política del PC.
6. Revisar cuáles diagramas adicionales de los pilotos merecen entrar en una futura edición maestra.

El progreso editorial global previo (77 %) **no se modifica solo por
pasar esta auditoría estructural**. Su objetivo es localizar el trabajo
real, no producir un porcentaje artificial.
