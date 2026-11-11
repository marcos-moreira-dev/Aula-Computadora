# ISA, ensamblador, MiniC y convención de llamadas

**Estado:** especificación funcional de lenguaje; codificación máquina final es un hito R1 pendiente.

**Candidato concreto (NO aprobado):** [ISA_AULA8_CANDIDATA.md](ISA_AULA8_CANDIDATA.md) y [su JSON](ISA_AULA8_CANDIDATA.json), con opcodes provisionales y ejemplos byte por byte. La validación documental de encodings no equivale a ejecución de la CPU ni congela el ABI. Los modos X/SP se proponen como variantes de `LD`/`ST`, manteniendo posibles alias `LDX`/`STX`.

## Invariantes

- Dos binarios de destino diferentes: Aula-8 y Aula-16.
- Conjunto de instrucciones lo más uniforme posible en nombres/semántica.
- Aula-8: opcode en bytes y operandos de 8/16 según formato.
- Aula-16: instrucción inicial de 16 bits en dirección par, con palabra inmediata opcional.
- Dirección de datos por byte, little-endian en valores multibyte.

## Familias previstas

| Familia | Operaciones |
| --- | --- |
| Movimientos | MOV, LDI, LD, ST |
| Indirectas / indexadas | LDX, STX y formas con X + desplazamiento |
| Aritmética | ADD, ADC, SUB, SBC, INC, DEC, CMP |
| Lógica | AND, OR, XOR, NOT, SHL, SHR |
| Saltos | JMP, JZ, JNZ, JC, JNC |
| Subrutinas / pila | CALL, RET, PUSH, POP |
| Control | NOP, HALT |

Reservar direccionamiento relativo a SP o mecanismo equivalente que permita acceder a parámetros y variables locales. Un Mini C con funciones y arreglos no puede depender exclusivamente de direcciones absolutas.

## Banderas

- Z: resultado igual a cero.
- N: bit alto de resultado.
- C: carry en suma / borrow en resta.
- V: overflow aritmético con signo.
- Debe definirse por **cada opcode** qué flags cambia y cuáles conserva.
- Tests obligatorios: 0xFF + 1 en Aula-8, 0xFFFF + 1 en Aula-16; comparación con/sin préstamo, números negativos en complemento a dos.

## ABI provisional

- CALL deposita retorno de 16 bits, RET lo recupera.
- SP de 16 bits, pila descendente y delimitada a RAM.
- Parámetros de programas MiniC inicialmente en ranuras de 2 bytes, preservando alineación Aula-16.
- Retorno u8: R0.
- Retorno u16: Aula-8 R0 como byte bajo y R1 como alto; Aula-16 R0 de 16 bits.
- R0/R1: volátiles; R2/R3 y X conservados por la función llamada cuando se utilicen, sujeto a especificación por opcode.
- Se especificarán los desplazamientos de argumentos, prólogo/epílogo y preservación de flags antes de generar código.

**Avance R0.10 sin aprobación:** el [borrador de ABI MiniC-Aula8](ABI_MINIC_AULA8_R0_10_BORRADOR.md) ya propone desplazamientos concretos desde X: retorno en X+4/5, argumento0 X+6/7 y los posteriores en ranuras de 2 B. Se guarda X/R2/R3 con prólogo fijo y el llamador limpia argumentos. R0/R1/FLAGS son volátiles, y este contrato **no se aplica automáticamente a servicios ROM**. Falta contrastarlo con una CPU y un compilador reales en R1.

## Ensambladores

- Un ensamblador **cruzado** por destino, sintaxis compartida donde sea posible.
- Etiquetas, bytes, palabras, cadenas, literales, origen, alineación y direcciones simbólicas.
- Archivo binario más listado desensamblado y mapa de símbolos.
- Errores explícitos de opcode desconocido, tamaño de operando, salto fuera de ROM/RAM, alineación y etiqueta no resuelta.
- V1 puede compilar una unidad de traducción por archivo sin exigir un enlazador general completo.

### Ensamblador y editor nativos

También se planifica un **ensamblador nativo de Aula-8** cargado en RAM, acompañado de editor de líneas ASCII. Un subconjunto de la sintaxis del ensamblador cruzado será común; usar dos pasadas y comparar bytes generados por ambos para los mismos programas y direcciones. Sin enlazador completo, macros ni optimizaciones en esta primera utilidad. Su instalación inicial se realiza con binarios generados fuera de la microcomputadora; luego sus instrucciones corren efectivamente **sobre Aula**. Ver [PROGRAMACION_DESDE_CERO.md](PROGRAMACION_DESDE_CERO.md).

## MiniC-Aula

Lenguaje **parecido a C**, deliberadamente distinto de ISO C completo:

- u8, u16, char y arreglos de tamaño fijo.
- Asignación, suma, resta, comparaciones, lógica bit a bit y condicionales.
- if/else, while, for; funciones, parámetros y variables locales.
- Literales de cadenas y biblioteca de funciones de ROM/terminal.
- Sin float, malloc, clases, hilos, librería estándar C completa ni optimizaciones complejas en V1.
- En Aula-8, aritmética u16 se compone de operaciones de 8 bits con carry; en Aula-16 puede operar con palabras nativas.

Pipeline previsto: **fuente MiniC -> análisis léxico/sintáctico -> AST tipado -> código intermedio simple -> ensamblador de destino -> binario -> CPU**. Compilación cruzada en la computadora anfitriona, no autoalojada en V1.

El requisito del **ensamblador nativo** no implica exigir un **compilador MiniC nativo**. Este último queda fuera de V1 por límites de RAM, tamaño de herramientas y esfuerzo de desarrollo.

## Vectores de prueba irrenunciables

1. Programas binarios sencillos escritos a mano y codificados por ensamblador deben coincidir.
2. CALL/RET con pila anidada, R2/R3 conservados, X preservado.
3. Arreglos de bytes con acceso a dirección impar en Aula-16.
4. Comparar resultados u16 en Aula-8 y Aula-16.
5. Aritmética con carry/borrow, saltos condicionales y flags.
6. Programa que llama PUTC/GETC por tabla pública de ROM.
7. Programa compilado de MiniC que realiza bucles, funciones, arreglos y terminal.

