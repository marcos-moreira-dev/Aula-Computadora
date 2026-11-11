# Propuesta de capítulo puente — Del bit al significado

**Estado:** propuesta editorial de Marcos Moreira, registrada el 6 de noviembre de 2026 y **desarrollada como interludio P07B-0.1**. Manuscrito, [Word](capitulos/07b_del_bit_al_significado.docx) y [PDF](capitulos/07b_del_bit_al_significado.pdf) terminados y revisables. **No modifica el total de 24 capítulos numerados.** La eventual renumeración queda pendiente de aprobación durante la integración del índice.

## Tesis didáctica

Un nivel eléctrico real se interpreta dentro de los umbrales de una familia lógica. Un **bit** representa entonces una elección entre los símbolos abstractos 0 y 1. **Ya existe significado en el hardware:** una entrada puede expresar una condición booleana, una NAND calcula una relación lógica, y un latch interpreta su salida como estado retenido. Es una **semántica lógica de circuito**, definida por la función, polaridad y papel de sus señales. No es todavía la semántica de una letra o una estructura de software.

Los mismos símbolos tampoco llevan escrita su interpretación universal: `0` puede indicar «petición activa» en una señal activa en bajo, mientras que `1` indica una petición activa en alto. El circuito y su contrato deciden. Cuando agrupamos bits y los leemos como tipos, caracteres, números, direcciones o instrucciones aparece otra capa de significado; el programa puede construir capas aún más ricas.

Evitar dos confusiones:

1. No afirmar que «0 significa cero voltios» y «1 significa cinco voltios» de forma universal. Los voltajes admisibles dependen de la tecnología.
2. No afirmar «los bits carecen de toda semántica»: **sí tienen semántica lógica cuando los interpreta un circuito**. La afirmación precisa es que un patrón no determina *por sí solo* si representa una letra, una magnitud, una instrucción o un objeto de software.
3. No reducir la semántica informática a la electricidad ni presentar la programación como únicamente semántica: también define operaciones, estado, control y efectos. Sí puede describirse como una manera de **construir y aplicar significados y reglas a representaciones manipulables por una máquina**.

## Ubicación recomendada

**Tras el capítulo 7, «Del bit al registro», y antes del capítulo 8, «Direcciones y buses».** Título realizado: «**Del bit al significado**». Código interno `P07B`, sin renumeración. Si Marcos decide convertirlo en el nuevo capítulo 8, el currículo pasaría a 25 capítulos; esa decisión sigue **pendiente de aprobación editorial**.

El lector habrá conocido señales, compuertas, memoria de un bit y registros de varios bits. En este punto podrá distinguir entre el **patrón almacenado** y las **reglas que lo interpretan** sin necesitar todavía una ISA completa.

## Recorrido de aprendizaje propuesto

1. **Semántica lógica del hardware:** tensión física → umbral bajo/alto → bit 0/1 → condición booleana determinada por función, polaridad y señal. Demostrar con NAND y con una entrada de latch activa en bajo; advertir sobre regiones eléctricas no garantizadas.
2. **Del bit al patrón:** ocho bits forman 256 combinaciones posibles; el patrón no decide qué representa.
3. **Una secuencia, varios significados:** `01000001₂` = `65₁₀` como entero sin signo; `A` como carácter ASCII; ocho indicadores de verdadero/falso; posible opcode solamente si la ISA le asigna ese valor.
4. **El mismo byte, otro número:** `11111111₂` = 255 como entero sin signo de ocho bits y -1 en complemento a dos de ocho bits. Explicar *por qué* al menos con la fórmula valor firmado = valor sin signo - 256 cuando el bit de signo vale 1. Aclarar que un byte no lleva consigo una etiqueta de «entero con signo».
5. **Codificación y contexto:** números, caracteres (ASCII y noción de UTF-8), imágenes como datos de píxeles, y el caso de una dirección que indica dónde leer, sin confundir dirección con contenido.
6. **De dato a operación:** cuando la CPU ejecuta una instrucción, la misma configuración de bits adquiere el papel de opcode, operando o dirección según el formato y la fase de interpretación. Reservar detalles de ISA y *fetch/decode* para capítulos 14–15.
7. **Semántica del software:** variable, tipo, campo, registro/estructura, objeto y función como convenciones y reglas de lenguaje que organizan significados. La programación orientada a objetos aparecerá **como contextualización posterior** sobre la organización de comportamiento y estado; no es requisito del lenguaje MiniC-Aula, ni curso de POO, ni propiedad física del hardware.
8. **Comprobar la interpretación:** un receptor que espera texto no debe leer el mismo byte como tensión; un programa que interpreta longitud o dirección equivocada falla incluso si todos los bits se transmitieron correctamente.

## Ejemplo principal listo para desarrollar

Una pequeña máquina Aula almacena `01000001` en una ubicación de RAM. Tres ejercicios observan exactamente esos ocho bits:

| Interpretación acordada | Resultado |
| --- | --- |
| Entero sin signo de ocho bits | 65 |
| Carácter ASCII (byte cuyo valor es 65) | `A` |
| Máscara de ocho indicadores | Indicadores 6 y 0 activos, si numeramos de 7 a 0 |
| Entero con signo de ocho bits, complemento a dos | +65 |
| Instrucción en una ISA inventada | No se puede determinar sin una tabla de opcodes definida |

La interpretación de la máscara usa bits `b7…b0 = 0 1 0 0 0 0 0 1`, por lo que los unos están en `b6` y `b0`.

**Otro ejemplo importante:** `11111111` significa 255 sin signo, pero -1 en complemento a dos de ocho bits. La memoria no cambia; cambia la interpretación.

## Ilustraciones sugeridas

- **Diagrama de niveles:** señal eléctrica real → reconocimiento lógico → función o estado de circuito → interpretación codificada de datos → significado de software. Mostrar que el primer paso exige especificaciones eléctricas y que una señal activa en bajo invierte el significado de «activo» respecto a `1`.
- **Cuatro lecturas de un byte:** el patrón `01000001` en el centro, y sus lecturas como entero, carácter, máscara y posible instrucción condicionada por una ISA.
- **Escalera de significado:** bit lógico de hardware → señal de control/estado → valor codificado → variable tipada → estructura de datos → comportamiento de programa → objeto como ejemplo contextual; aclarar que esas etapas no son capas físicas necesariamente independientes.

## Ejercicios que debe contener

- Convertir `01000001` manualmente a decimal mediante potencias de dos.
- Interpretar `11111111` como entero sin signo y entero con signo de ocho bits, explicando la diferencia.
- Identificar los indicadores activos en una máscara de bits con índices explícitos.
- Explicar qué información adicional se necesita para leer un byte como carácter, número o instrucción.
- Comparar «valor almacenado», «dirección del valor» y «tipo que espera el programa».
- Relacionar una lectura equivocada con un fallo realista de sistema, sin atribuir al hardware una intención semántica.

## Dependencias y límites editoriales

- El capítulo 7 debe explicar retención, bytes y registros; el puente añade **interpretación**, sin reexplicar circuitos de compuertas.
- Capítulos 14–15 retomarán estos conceptos desde opcodes y formatos de instrucción.
- Capítulo 20 los retomará desde variables, estructuras y funciones de MiniC-Aula.
- No es requisito enseñar POO íntegra para comprender una computadora Aula; hablar de objetos solo como ampliación conceptual.
- No afirmar que los bytes en RAM guardan su propio tipo, ni que la CPU general sabe «qué significa una letra» sin programas, dispositivos y convenciones.

## Decisión pendiente

La propuesta se desarrolló como interludio de ocho páginas, con cuatro diagramas y doce ejercicios resueltos. **Se registra como pieza adicional redactada, no como octavo capítulo numerado**. El siguiente trabajo editorial corresponde al capítulo 8, «Direcciones y buses». Ver [estado P07B](ESTADO_EDITORIAL_P07B.md).
