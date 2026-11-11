# Escalera didáctica de programas verificables

Este plan convierte la sugerencia del lector en una **secuencia creciente de capacidades**, sin atribuirlas a una computadora que todavía no se ha construido. **No reemplaza el currículo de 24 capítulos ni añade capítulos.** Cada peldaño tiene entradas, un estado observable y condiciones de aprobación. Los capítulos 18–20 desarrollan el camino desde la E/S hasta el ensamblador de referencia del anfitrión.

| Peldaño | Programa o tarea | Entrada | Resultado comprobable | Prerrequisitos | Estado actual |
| --- | --- | --- | --- | --- | --- |
| 1 | Guardar una variable | `42` en R0 | RAM[`6F00`]=`2A` | `LDI`, `ST`, buses, RAM | Traza documental C14–C15 |
| 2 | Sumar dos números | `13`, `9` | R0=`22` decimal, RAM[`6F00`]=`16` hexadecimal | ALU, flags, `ADD` | C20: 13 bytes ensamblados en anfitrión; no ejecución CPU |
| 3 | Llamar y regresar | `CALL 6010` | R0=`2A`, SP vuelve a `8000`, PC sigue en `6003` | Pila, `RET` | Traza documental C16 |
| 4 | Mostrar un carácter | `0x41` | Salida `A`, luego prompt por `RET` | ROM/terminal, ABI | C18, todavía no ejecutable |
| 5 | Eco con variable | Byte ASCII `B` (`42`) | RAM[`6F00`]=`42` y salida `B` | `GETC`, `ST`, `PUTC` | C18, todavía no ejecutable |
| 6 | Guardar y recuperar | 256 bytes en bloque `0001` | Misma secuencia tras READ/LOAD y verificación | Controlador de bloques, imagen persistente, firmware | Modelo anfitrión R0.12; LOAD no disponible |
| 7 | Euclides | `mcd(48,18)` | `6`; termina sin desbordar | Comparaciones sin signo, bucles, resta; **no existe DIV/MOD** | C20: 29 bytes en anfitrión y modelo semántico contrastado con `math.gcd`; no CPU |
| 8 | Fibonacci iterativo | `F(6)` | `8`, con límite de byte y pruebas de casos base | Variables, suma, bucles | C20: modelo matemático anfitrión; falta binario Aula-8 |
| 9 | Fibonacci recursivo | `F(6)` | `8`; pila equilibrada y llamadas anidadas | ABI, pila, funciones, límites | C20: 25 llamadas modelo anfitrión; falta validación de pila CPU |
| 10 | Herramienta nativa y mini sistema | Código fuente con etiquetas | Bytes ensamblados, carga, entrada, salida y retorno | Editor, ensamblador de dos pasadas, almacenamiento | C20: ensamblador Python de dos pasadas; la herramienta nativa y el sistema son futuros |

Los puntos 7–9 tienen **referencias matemáticas y archivos fuente en el anfitrión**, pero la puerta de ejecución de CPU sigue cerrada. El algoritmo de Euclides puede expresarse por restas sucesivas porque el juego candidato de Aula-8 no contiene una instrucción de módulo/división. El Fibonacci recursivo es una prueba especialmente útil para **pila y convención de llamadas**; no es conveniente como primer programa.

## Qué cuenta como prueba de cada peldaño

1. **Cálculo independiente:** confirmar el resultado con aritmética manual o un modelo Python que no se limite a repetir la misma lógica de implementación.
2. **Bytes y direcciones:** comparar opcodes, selectores, little-endian, ubicación de variables y longitud del programa con la ISA aprobada o la propuesta explícitamente indicada.
3. **Rastro de estado:** observar valores antes/después de PC, SP, R0–R3, X, RAM, flags y salidas relevantes; identificar cada condición de parada.
4. **Memoria y pila:** comprobar regiones válidas, pila equilibrada, salida ante error y ausencia de colisiones con la ROM, MMIO y el monitor.
5. **Ejecución real:** solo declarar «funciona en Aula-8» cuando una CPU implementada ejecute esos bytes, en un simulador digital fiel o hardware validado, y se compare con la referencia.

## Ejemplo de referencia numérica independiente

| Ejercicio | Entrada | Salida |
| --- | --- | --- |
| Suma | 13 + 9 | 22 decimal, `0x16` |
| Euclides | (48, 18) → (30, 18) → (12, 18) → (12, 6) → (6, 6) | `mcd=6` |
| Fibonacci | `F(0)=0`, `F(1)=1`, `F(n)=F(n−1)+F(n−2)` | `F(6)=8` |

Para los ejemplos recursivos se deberá presupuestar el peor caso de pila **con la ABI que finalmente se apruebe**. No presentar un número de ciclos, bytes de pila o frecuencia máxima antes de definir el prólogo, los parámetros y el control de memoria.
