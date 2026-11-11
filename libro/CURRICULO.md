# Currículo preliminar — seis partes y 24 capítulos

**Estado:** mapa pedagógico decidido; nombres y numeración pueden refinarse al elaborar el índice, sin alterar objetivos.

## Parte I — Electricidad y electrónica básica (3)

1. **La corriente y sus caminos.** Tensión, corriente, resistencia, potencia y seguridad con 5 V; medir, limitar corriente y encender LED.
2. **El transistor como interruptor.** NPN, MOSFET, terminales, polarización y condiciones de conmutación.
3. **De interruptores a lógica.** Inversor, NAND, operaciones booleanas, niveles y tablas de verdad.

## Parte II — Memoria digital elemental (4)

4. **Construir funciones con compuertas.** AND, OR, NOR, XOR y simplificación justificada.
5. **La realimentación conserva información.** Latch SR y estados prohibidos.
6. **Memorizar en el tiempo.** Latch D, flip-flop, reloj, flancos y reset.
7. **Del bit al registro.** Byte, enable, triestado, carga/retención y pruebas.

**Interludio realizado sin numerar:** [«Del bit al significado: cómo una computadora interpreta datos»](capitulos/07b_del_bit_al_significado.pdf), entre los capítulos 7 y 8. Explica la **semántica lógica del hardware** (función de NAND, polaridad, retención) y la interpretación convencional de un mismo patrón como entero, carácter, máscara o instrucción. Estructuras de datos y POO se mencionan solo como contexto. **No altera el total de 24 capítulos.**

## Parte III — Memoria, buses y aritmética (4)

8. **Direcciones y buses.** Dirección frente a dato, multiplexación, selección y lectura de esquemas.
9. **RAM y ROM reales.** Celda SRAM, decodificación, expansión y memoria comercial.
10. **El circuito que suma.** Half-adder, full-adder, carry, suma de 8 bits.
11. **La unidad aritmético-lógica.** Resta, comparaciones, operaciones lógicas y flags.

## Parte IV — Construir Aula-8 (5)

12. **Arquitectura Aula-8.** Registros R0–R3, PC/SP/X, interconexiones y datapath.
13. **La unidad de control.** Estados, microoperaciones, ROM de control y señales.
14. **De números a instrucciones.** Opcodes, formatos, **modos de direccionamiento (inmediato/absoluto/indexado/pila)**, programa almacenado y primer programa introducido byte a byte con panel detenido. Separar luego el cálculo de dirección efectiva de la decodificación de RAM/ROM/E/S.
15. **La instrucción en movimiento.** Fetch, decode, execute; recorrido completo con registros y señales.
16. **Subrutinas y pila.** CALL/RET, saltos, parámetros, bucles y programa ensamblador comentado.

## Parte V — Microcomputadora y software (4)

17. **Encender una computadora.** Reset, ROM previamente grabada, pila, monitor, mapa de memoria y diferencia entre arranque y depósito manual.
18. **Hablar con la máquina.** Terminal de caracteres, entrada/salida, PUTC/GETC/PUTS, comandos y modificación hexadecimal de RAM.
19. **Guardar y recuperar programas.** Bloques persistentes, imagen de almacenamiento, utilidad cargada a RAM, editor de líneas y progresión hacia archivos.
20. **Programar un pequeño sistema.** Ensamblador nativo, dos pasadas, funciones, mini sistema y MiniC-Aula compilado inicialmente fuera de la máquina; aplicación comprobable de principio a fin.

## Parte VI — Aula-16 y comparación (4)

21. **Qué implica ampliar la palabra.** ALU de 16 bits, comparaciones de capacidad/coste lógico.
22. **Un bus externo de 16 bits.** Dos bancos de 8, direccionamiento por bytes, little-endian, alineación.
23. **Programación para Aula-16.** ISA de palabras, compilación cruzada, ABI y pruebas equivalentes a Aula-8.
24. **Una computadora que podemos explicar.** Integración, límites reales, depuración, proyectos y evolución.

**Interludio redactado y maquetado:** [P23V — «De los mapas de caracteres al escritorio gráfico»](capitulos/23v_de_mapas_de_caracteres_a_escritorio_grafico.md), ubicado entre los capítulos 23 y 24. Trata modo texto, ROM de glifos, mapas de bits, color, fuentes tipográficas y rasterización. El [plan original](PLAN_INTERLUDIO_P23V_TEXTO_GRAFICOS_TIPOGRAFIA.md) permanece como antecedente. **No cambia los 24 capítulos numerados**, ni exige construir una GPU.

**Avance de redacción C24-0.1:** capítulos **1–24** y puentes **P07B/P23V** tienen Word/PDF, figuras y ejercicios. **No faltan capítulos numerados por redactar**, pero el volumen maestro con índice, referencias y revisión cruzada **todavía no se ha compuesto**. Véase el [estado editorial vigente](ESTADO_EDITORIAL_C24.md).

## Tratamiento editorial de cada capítulo

No imponer una extensión fija. Para electrónica y arquitectura:

- Pregunta real y necesidad funcional.
- Prerrequisitos y vocabulario mínimo.
- Mecanismo, circuito/esquema verdadero y tabla de estados.
- Un ejemplo íntegro que pueda comprobarse.
- Criterio de fallo y diagnóstico.
- Ejercicios proporcionados y bibliografía relevante.

### Ejemplos transversales

- Suma de 13 + 9 en binario: corregir índices y propagación del carry del antiguo manuscrito.
- Programa LOAD/ADD/NOT/STORE: ejemplo de máquina heredado como **idea pedagógica**, rediseñado para la ISA nueva.
- Salida de texto «HOLA» vía ROM y terminal.
- Bucle con contador, recorrido de arreglo, función con pila y lectura de un bloque persistente.
- Comparar suma de 16 bits en Aula-8 (dos operaciones con carry) y Aula-16 (una operación natural).
- Sesión completa: introducir un byte, arrancar monitor, escribir líneas de fuente en el editor nativo, ensamblar, guardar, reiniciar, recuperar y ejecutar; separar claramente utilidades que aún no existen en cada etapa.

