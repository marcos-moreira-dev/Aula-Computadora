# C28-M · Revisión dirigida del hilo de construcción, capítulos 8–14

**9 de noviembre de 2026.** Los hallazgos se refieren al libro y sus
contratos didácticos; no a una CPU Aula construida. Se inspeccionaron los
pasajes que definen cada paso, sus ejemplos cuantitativos y cuatro de las
figuras centrales. No sustituye una lectura de corrección de estilo completa
de cada página ni el cotejo eléctrico de cada diagrama.

## Qué pieza añadimos después de cada explicación

| Capítulo | Conocimiento previo que reaprovecha | Pieza o capacidad conceptual nueva | Qué no debe afirmarse |
| --- | --- | --- | --- |
| 8. Buses y direcciones | Registro de 8 bits y significado de los bits | MAR, MDR, 16 líneas de dirección, bus de datos bidireccional y selección | El dibujo no garantiza arbitraje eléctrico. |
| 9. RAM y ROM | Decodificación y protocolos de lectura/escritura | Mapa ilustrativo SRAM 32 KiB + EEPROM 8 KiB + ventana sin asignación | No es el mapa de memoria físico aprobado. |
| 10. Sumador | XOR/AND, acarreo y bits | Medio sumador, sumador completo y cadena de ocho etapas | No hay temporización ni chips de CPU medidos. |
| 11. ALU | Sumador y registros | ADD/SUB con XOR condicional, lógica bit a bit, flags y selector de resultado | La política de flags de operaciones lógicas sigue sin cerrarse. |
| 12. Arquitectura | Buses, almacenamiento y ALU | Rutas de datos y responsabilidad diferenciada de PC, MAR, MDR y control | Un diagrama de bloques no es plano de cableado. |
| 13. Control | Camino de datos | Orden lógico de `LDI`, `ST` y `HALT`, permisos de bus y captura | Los 36 opcodes propuestos no tienen 36 microsecuencias implementadas. |
| 14. Programa | Control y memoria direccionable | Conversión a bytes y depósito manual hipotético; `LDI / ST / HALT` | No hay CPU o monitor real que ejecute esos bytes. |

## Comprobaciones numéricas realizadas

El nuevo script `scripts/c28m_verificar_alu_mapa_y_programa.py` utiliza
solo la biblioteca estándar de Python. Construye un **sumador por acarreo
propagado** de ocho etapas y comprueba sus salidas contra el resultado
aritmético esperado, incluidos los flags. El mapa de memoria se evalúa por
señales de selección y por límites de dirección, sin afirmar que existan
los chips montados.

| Familia | Vectores de entrada |
| --- | ---: |
| Mapa de 16 bits: SRAM, ROM y región libre | 65.536 |
| ADD de ocho bits, acarreo y overflow firmado | 65.536 |
| SUB de ocho bits, préstamo, overflow y comparaciones | 65.536 |
| Tabla del medio sumador | 4 |
| Tabla del sumador completo | 8 |
| **Total de vectores verificados** | **196.620** |

También se cotejaron las tablas impresas de los capítulos 8–11 y los
ejemplos `13 + 9`, `250 + 10`, `127 + 1`, `13 − 9`, `9 − 13`,
`0x80 − 0x01` y máscaras lógicas. Las figuras inspeccionadas visualmente
incluyeron el mapa 64 KiB, los acarreos de 13+9, la ruta ADD/SUB y el
mapa de bytes `6000–6007`.

En la referencia de papel `11 00 2A 13 00 00 6F 01`, un pequeño
**intérprete deliberadamente limitado a tres instrucciones** obtuvo:

- `R0 = 0x2A` y `RAM[0x6F00] = 0x2A`.
- Ocho lecturas de bytes y una escritura.
- `PC` lógico después de consumir HALT: `0x6008`.
- Los ocho bytes del programa conservan sus posiciones originales.

Esas propiedades contrastan los capítulos 13 y 14 con
`simulador-javafx/ISA_AULA8_CANDIDATA.json`. **No equivalen a ejecutar
microcódigo, un HDL completo ni firmware de Aula-8.**

El verificador ya existente `scripts/verificar_isa_aula8_borrador.py` pasó
también: 36 opcodes candidatos sin colisión, tres programas ejemplo y
12 instrucciones documentales decodificadas. Se incorporó por primera
vez al comprobador global como control separado.

## Qué está validado y qué sigue abierto

| Afirmación | Estado |
| --- | --- |
| Las fórmulas y tablas ejemplares de este tramo son matemáticamente coherentes con los modelos probados | **Contrastado** en las rutas indicadas |
| El mapa ilustrativo 32 + 24 + 8 KiB evita ventanas superpuestas | **Contrastado** en sus 65.536 direcciones |
| La descripción de ocho bytes del ejemplo coincide con el borrador ISA | **Contrastado** como contrato documental |
| Los PNG seleccionados muestran con claridad los ejemplos trabajados | **Inspección visual parcial** |
| Cada cable de todos los SVG/PNG coincide con una netlist y con pines físicos | **Pendiente** |
| La ALU completa fue simulada en Verilog y medida con retardos | **Pendiente** |
| El microsecuenciador ejecuta físicamente los 36 opcodes | **No implementado** |
| Word/PDF maestro ya incluye C28-L/M y el suplemento C28-H | **No; sigue maestro C28-G** |

## Próximo tramo prioritario

1. Cotejar diagramas y nodos reales de sumador, ALU, memorias y control
   (no únicamente sus operaciones matemáticas).
2. Continuar los capítulos 15–24: búsqueda/ejecución, saltos, pila,
   periféricos, programación y conclusión del aprendizaje.
3. Elegir y documentar política del PC solo cuando la comparación sea
   suficiente; mantener las dos propuestas mientras tanto.
4. Integrar el texto consolidado, sus figuras y los pilotos al maestro
   Word/PDF; actualizar índice y referencias cruzadas.
5. Revisión de todas las páginas, permisos de figuras y entrega final.

**Resultado global de Windows previo a esta auditoría:** 15/15 controles
aprobados en `Retroalimentacion_GLOBAL_C28H_20261109_152420.zip`.
Con los dos controles C28-M e ISA incluidos ahora, el siguiente Windows
podrá reportar **17 controles**, pendientes de ejecutar efectivamente.
