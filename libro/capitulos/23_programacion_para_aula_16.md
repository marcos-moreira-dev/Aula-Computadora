# Capítulo 23. Programación para Aula-16

*Parte VI · Aula-16 y comparación · Aula-Computadora*

En Aula-8 aprendimos a mover bytes, construir una suma de dieciséis bits con acarreo y ensamblar un programa de ejemplo en el **equipo anfitrión**. El capítulo 22 nos enseñó a recuperar dos bytes de una RAM dividida en bancos. Ahora toca utilizar esas reglas como programadores. Queremos que Aula-16 pueda resolver el **mismo problema** que Aula-8, pero con sus propias instrucciones, sus registros de dieciséis bits y su convenio de llamadas.

Conviene establecer un límite de honestidad técnica: **todavía no hay una ISA binaria Aula-16 aprobada**. Por eso las sentencias de este capítulo son un **seudolenguaje ensamblador**, con nombres ilustrativos y semántica declarada, no bytes que se puedan cargar y ejecutar en una CPU. No atribuiremos longitudes de instrucción, opcodes, ciclos, frecuencia ni compilador nativo a un hardware inexistente. Sí podemos diseñar modelos matemáticos, comprobar memoria y definir pruebas que servirán cuando esa CPU se construya.

## 1. Qué hereda el programador y qué cambia

Ambas máquinas tienen **cuatro registros generales**, PC, SP y X de dieciséis bits, una memoria de 65536 direcciones de byte y los indicadores Z, C, N y V. Aula-16 hace naturales las operaciones aritméticas sobre **palabras de dieciséis bits** y dispone de bus externo de dieciséis. Los programas de Aula-8 no son binarios compatibles: la ISA y la convención de llamada de Aula-16 serán propias.

| Responsabilidad | Aula-8 | Aula-16 |
| --- | --- | --- |
| Dato natural en R0–R3 | 8 bits | 16 bits |
| Sumar un `u16` | Dos pasos de byte más acarreo | Una suma de palabra conceptual |
| Acceso a memoria | Byte | Byte o palabra alineada |
| Ancho de PC/SP/X | 16 bits | 16 bits |
| Direcciones | Bytes | Bytes |
| Código binario | ISA Aula-8 candidata | **Por definir** |

[[EQ:Valor natural u16 = 0..65535]]

[[EQ:Resultado de suma u16 = (a+b) mod 65536]]

Esta diferencia suele simplificar la descripción de un algoritmo, pero no demuestra que Aula-16 sea más veloz: mover una palabra y realizar su suma involucra camino de datos, bus, control y memoria, cuyo cronometraje no se ha caracterizado.

## 2. Un vocabulario conceptual antes de escribir bytes reales

Usaremos `MOVI16`, `LDW`, `STW`, `LDB`, `STB`, `ADD16`, `CMP16`, `BRANCH`, `CALL`, `RET` y `HALT` como **nombres de acciones**, no opcodes ni propuesta de encoding. En la notación de ejemplos, `LDW R0,[X]` lee una palabra alineada desde la dirección que contiene X; `ADD16 R0,R1` suma los valores de palabra y conserva dieciséis bits. El uso de corchetes indica **acceso a memoria**, no que la máquina tenga ya un modo de direccionamiento aprobado con esa sintaxis.

| Acción ilustrativa | Significado comprobable | Condición previa |
| --- | --- | --- |
| `MOVI16 R0,0200` | R0 toma la palabra `0200` | Literal u16 válido |
| `LDW R0,[X]` | R0 toma RAM[X] y RAM[X+1] | X par, región legible |
| `STW [X],R0` | Escribe R0 little-endian | X par, región escribible |
| `LDB R0,[X]` | Lee un byte a los ocho bits bajos de R0 | Región legible |
| `ADD16 R0,R1` | Suma módulo 65536 | Operandos u16 |
| `CALL objetivo` | Invoca una función | ABI y codificación pendientes |

[[EQ:LDW en dirección a = RAM[a] + (RAM[a+1] × 256)]]

[[EQ:Dirección de palabra alineada ⇔ (a AND 1)=0]]

El modo inmediato significa que una constante viene de la **propia instrucción**; el absoluto nombra una dirección; el indexado construye una dirección con registro base más desplazamiento; y el relativo a pila usa SP o un puntero de marco. Esas son decisiones de la ISA y de la unidad de control. Ninguna se confunde con el modo texto/gráfico de la pantalla, ni permite inferir el número de bytes de su encoding.

[[FIG:c23_fig01_niveles_de_programa|Figura 1. Un problema pasa por fuente, ensamblador, binario y CPU cuando todas esas piezas existan.|El programa Aula-16 actual es semántica conceptual comprobada en anfitrión; el ensamblador binario, el cargador y la ejecución sobre CPU Aula-16 todavía no existen.]]

## 3. El primer programa útil: sumar tres palabras en RAM

Reservemos una tabla de tres palabras en la RAM de ejemplo, empezando en `0x2200`. La primera es `0x01FF` (511); la segunda, `0x0001` (1); la tercera, `0x0002` (2). Como cada palabra ocupa dos direcciones de byte, sus comienzos son `2200`, `2202` y `2204`. El resultado debe guardarse en `0x2210`.

[[EQ:Dirección_del_elemento_i = 0x2200 + 2i]]

[[EQ:0x01FF + 0x0001 + 0x0002 = 0x0202 = 514]]

| Dirección | Bytes little-endian | Valor lógico |
| --- | --- | --- |
| `2200–2201` | `FF 01` | `01FF` |
| `2202–2203` | `01 00` | `0001` |
| `2204–2205` | `02 00` | `0002` |
| `2210–2211` | `02 02` al finalizar | `0202` |

Una receta de ensamblador conceptual sería: preparar R0=`0`, X=`2200` y R2=`3`; repetir `LDW R1,[X]`, sumar R1 a R0, avanzar X en **dos bytes** y disminuir R2; cuando el contador llega a cero, escribir R0 en `[2210]`. En la máquina real habrá que diseñar **qué instrucciones concretas** realizan cada paso, cómo afectan los indicadores y cómo se codifica el salto del bucle. En el modelo anfitrión sí podemos contrastar el resultado calculado por iteración con la suma directa.

[[FIG:c23_fig02_sumar_arreglo|Figura 2. Tres palabras consecutivas se recorren avanzando dos direcciones de byte por elemento.|X toma 2200, 2202 y 2204; acumula 01FF más 0001 más 0002; escribe 0202 como bytes 02 02 en 2210 y 2211.]]

**¿Y si el arreglo empezara en `2201`?** Su dirección inicial sería impar. Aula-16 V1 no permite `LDW` desde esa dirección; el programa debe validar la alineación antes de entrar al bucle. Esa restricción es observable en el modelo aunque todavía no contemos con circuitos de excepción ni un conjunto aprobado de instrucciones.

## 4. Direccionamiento y cálculo de direcciones efectivas

El direccionamiento indexado ayuda a recorrer arreglos, estructuras y marcos de pila. Si X=`0x2200` y un desplazamiento expresado en **bytes** vale `4`, la dirección efectiva es `0x2204`. Si el elemento ocupa dos bytes, el índice lógico `i=2` se escala por dos antes de llegar a la dirección.

[[EQ:EA = (X + desplazamiento_en_bytes) mod 65536]]

[[EQ:EA_del_elemento_2 = 0x2200 + (2 × 2) = 0x2204]]

**Importante:** el desplazamiento de una instrucción podría codificarse con signo en ocho bits, dieciséis u otra forma; eso **no se ha aprobado para Aula-16**. La fórmula de dirección es útil, pero no fija el campo binario ni garantiza que una instrucción acepte cualquier desplazamiento. También hay que comprobar que una palabra no cruce una frontera prohibida ni acceda a un periférico que solo permite bytes.

## 5. Euclides: reutilizar las pruebas, no los opcodes

El algoritmo de Euclides por restas calcula el máximo común divisor de dos enteros **positivos**. Para `48` y `18`, si el primero es mayor, le restamos el segundo; si el segundo es mayor, le restamos el primero. Cuando ambos son iguales, ese valor es el MCD. En la explicación del capítulo 20 lo representamos mediante operaciones de byte de Aula-8; aquí los registros naturalmente conservan enteros de palabra.

| Iteración | a | b | Decisión |
| --- | ---: | ---: | --- |
| Inicial | 48 | 18 | `a>b`, restar b a a |
| 1 | 30 | 18 | `a>b`, restar b a a |
| 2 | 12 | 18 | `b>a`, restar a a b |
| 3 | 12 | 6 | `a>b`, restar b a a |
| Final | 6 | 6 | Iguales: terminar |

[[EQ:MCD(48,18)=6]]

[[FIG:c23_fig03_euclides_dos_maquinas|Figura 3. El mismo algoritmo y sus pruebas sirven para Aula-8 y Aula-16, aunque cambie la representación en instrucciones.|Estados 48,18 a 30,18 a 12,18 a 12,6 a 6,6; Aula-16 usa palabras conceptuales y Aula-8 bytes, sin compatibilidad de binarios.]]

No debemos escoger una instrucción de salto `JG` y su código sin definir antes **cómo `CMP16` actualiza C, Z, N y V**. Para comparar sin signo, una arquitectura puede adoptar una bandera de préstamo; para comparar con signo se necesita considerar `N XOR V`. Esa semántica se revisará junto con la ISA. Mientras tanto, un verificador anfitrión calcula las comparaciones como enteros y evita inferir banderas inexistentes.

## 6. Fibonacci enseña los límites del ancho de palabra

Fibonacci permite estudiar estado, iteración y límites aritméticos. Comenzando por `F0=0`, `F1=1`, cada término es la suma de los dos anteriores. El término `F10` vale 55, que cabe en un byte; `F14` vale 377, que **requiere más de ocho bits** pero cabe en una palabra Aula-16. `F24=46368` todavía cabe como `u16`, aunque **ya no** como entero firmado `i16` positivo. `F25=75025` excede incluso el máximo `u16`.

[[EQ:F(n+2) = F(n+1) + F(n)]]

[[EQ:F14 = 377 = 0x0179]]

[[EQ:F25 = 75025; 75025 mod 65536 = 9489 = 0x2511]]

Si una suma `u16` guarda solo 16 bits, calcular `F25` sin política de error devuelve `9489` y genera acarreo, lo cual **no es el Fibonacci matemático correcto**. Un programa serio debe documentar si interrumpe por desbordamiento, usa enteros más grandes o acepta aritmética modular. La misma prueba revela por qué los indicadores de estado son relevantes.

## 7. Funciones y ABI: un acuerdo necesario que aún debemos diseñar

Una función no solo necesita `CALL` y `RET`; también hay que saber **dónde llegan sus argumentos**, en qué registro regresa el resultado, quién preserva cada registro y cómo se organiza la pila. Ese contrato se llama **interfaz binaria de aplicación** o ABI. Aula-8 tiene un borrador de ABI para MiniC; **no debemos trasladarlo en silencio a Aula-16**.

Como práctica conceptual, imaginemos una función `SUMAR_DOS(u16 a, u16 b) -> u16`. El llamador debe entregar `a` y `b` de alguna forma; el cuerpo calcula `(a+b) mod 65536`; el llamador recibe el resultado. Podemos **ilustrar** argumentos en dos posiciones contiguas de memoria y devolver el valor en R0, pero esa distribución todavía **no constituye un ABI adoptado**.

| Pregunta de ABI | Opciones que deberá resolver la ISA Aula-16 |
| --- | --- |
| Entrega de argumentos | Registros, pila o mezcla |
| Valor de retorno | R0, par de registros o memoria |
| Registros preservados | Decisión de llamador o llamado |
| Pila | Orden y alineación de elementos |
| Datos grandes | Referencias, copias o ubicación en memoria |
| Llamadas recursivas | Marco independiente por activación |

[[EQ:SUMAR_DOS(0x01FF, 0x0001) = 0x0200]]

El puntero SP sigue teniendo dieciséis bits. Un retorno de dos bytes debe respetar el orden de almacenamiento y las condiciones de la pila; sin embargo, **no fijaremos offsets de marcos, orden de PUSH ni código de CALL** hasta validar el control de flujo de Aula-16. No confundamos el esquema de la función con una pila que la máquina ya sepa manipular.

## 8. Compilación cruzada y MiniC-Aula

Para aprender a programar una computadora nueva es habitual **crear herramientas en una máquina que ya funciona**. Un ensamblador cruzado recibe texto fuente Aula-16 y, cuando exista su ISA, emitirá bytes Aula-16. Un compilador MiniC-Aula transforma un subconjunto de C educativo en una representación adecuada, pero dependerá tanto de la ISA como de la ABI. La máquina de destino no necesita ejecutar el compilador para ejecutar el resultado compilado.

[[FIG:c23_fig04_compilacion_y_pruebas|Figura 4. La compilación cruzada necesita ISA, ABI, ensamblador y cargador antes de producir programas Aula-16 ejecutables.|Se distingue una referencia matemática anfitriona de un ensamblador binario futuro y de una CPU aún no implementada.]]

Una cadena de herramientas completa incluirá análisis de sintaxis y tipos, elección de instrucciones, ensamblado de etiquetas, comprobación de memoria y permisos, una imagen de carga y pruebas de ejecución. Las rutinas ROM de Aula-8 como `FW_PUTC` no deben declararse automáticamente compatibles con Aula-16: el contrato del firmware público y sus llamadas requieren adaptación explícita.

## 9. Contrato de prueba antes de construir el procesador

Un buen conjunto de pruebas separa **semántica** de **implementación**. Podemos verificar hoy que `0x2200`, `0x2202` y `0x2204` son direcciones pares; que sus bytes forman `01FF`, `0001` y `0002`; que el resultado esperado es `0202`; que Euclides acaba en seis; y que `F25` rebasa u16. No podemos verificar hoy que `LDW` decodifique, que `CALL` preserve un registro o que una RAM física cumpla un tiempo eléctrico.

| Capa de prueba | Qué demuestra | Qué no demuestra |
| --- | --- | --- |
| Referencia Python | Aritmética, bancos y casos límite | CPU ejecutando instrucciones |
| Ensamblador Aula-16 futuro | Codificación y resolución de símbolos | Corrección eléctrica |
| Emulador de ISA futuro | Semántica de instrucciones definidas | Temporización física |
| Circuito/prototipo futuro | Señales y acceso a chips medidos | Corrección de todo el software |

[[EQ:Resultado esperado en RAM[0x2210..0x2211] = [0x02,0x02]]]

Antes del capítulo final nos detendremos en el capítulo 23B para comprender los mapas de caracteres, la tipografía y los modos gráficos sin introducir una tarjeta gráfica imaginaria ni instrucciones de CPU especiales. El capítulo 24 reunirá después los recorridos aprendidos, desde una señal física hasta una imagen en pantalla.

[[PAGEBREAK]]
## Ejercicios del capítulo 23

**Ejercicio 1 — Capacidades.** ¿Por qué Aula-16 no dispone de 128 KiB de espacio direccionable por tener bus de datos de 16 bits?

**Ejercicio 2 — Dos bytes.** ¿Qué valor obtiene `LDW` desde `[2200]` si los bytes son `FF 01`?

**Ejercicio 3 — Índices.** Enumera los comienzos de tres palabras en un arreglo desde `2200`.

**Ejercicio 4 — Acumulador.** Calcula `01FF+0001+0002` en 16 bits.

**Ejercicio 5 — Destino.** ¿Qué bytes se almacenan en `2210` y `2211` para ese resultado?

**Ejercicio 6 — Alineación.** ¿Por qué `LDW` desde `2201` se rechaza en el contrato V1?

**Ejercicio 7 — Direccionamiento.** Calcula `EA` para `X=2200` y desplazamiento de 4 bytes.

**Ejercicio 8 — Euclides.** ¿Cuál es el MCD de 48 y 18 y cuántos estados sucesivos aparecen en la tabla?

**Ejercicio 9 — Fibonacci.** ¿Qué término entre F10 y F14 demuestra la necesidad de más de ocho bits en el ejemplo?

**Ejercicio 10 — Overflow.** ¿Qué valor deja una suma modular de 16 bits al producir F25?

**Ejercicio 11 — ABI.** Cita cuatro acuerdos que debe tener un convenio de llamadas Aula-16 antes de afirmar que una función es ejecutable.

**Ejercicio 12 — Herramientas.** ¿Es posible reutilizar el código máquina de Euclides Aula-8 directamente en Aula-16? ¿Qué puede reutilizarse?

[[PAGEBREAK]]
## Solucionario del capítulo 23

**1.** Mantiene 16 líneas de dirección y direcciones de byte: `2^16=65536 bytes=64 KiB`.

**2.** `0x01FF` por little-endian.

**3.** `2200`, `2202` y `2204`.

**4.** `0x0202`, equivalente a 514 decimal.

**5.** Byte bajo `02` en `2210` y byte alto `02` en `2211`.

**6.** Es una dirección impar; las palabras deben comenzar en pares en Aula-16 V1.

**7.** `0x2204`.

**8.** MCD `6`; la tabla contiene cinco estados incluyendo inicial y final.

**9.** `F14=377` (también los términos posteriores a F13 requieren más de ocho bits); supera 255.

**10.** `75025 mod 65536 = 9489 = 0x2511` y debe marcarse el desbordamiento sin signo.

**11.** Entrega de argumentos, retorno, registros preservados y orden/alineación de pila; también responsabilidad por limpieza.

**12.** No: la ISA binaria Aula-16 aún no existe. Sí pueden reutilizarse el algoritmo, las entradas, salidas esperadas y los casos de prueba.

## Para continuar

El capítulo 24 hará un inventario honesto de lo que sabemos demostrar, de los componentes que falta diseñar y de las pruebas necesarias para convertir nuestras explicaciones en una computadora construible. Los mapas de caracteres y los gráficos seguirán una línea didáctica complementaria, sin sustituir ese cierre de arquitectura.
