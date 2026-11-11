# C28-T · Mapa de inserción editorial sin modificar el libro maestro

**Estado:** propuesta de integración para una revisión futura.
**Maestro protegido:** edición C28-G de 248 páginas, Word y PDF, sin cambios.

## Dónde encajan las láminas nuevas

| Lugar actual en C28-G | Material complementario | Función precisa |
| --- | --- | --- |
| Capítulo 4, páginas 35–43 | Recordatorio de XOR con cuatro NAND (figura original C04) | Preparar la síntesis de NAND antes de hablar de memoria |
| Capítulo 10, páginas 97–105, sección de sumador completo | C28-T figura 1 y secciones 1–2 del suplemento | Identificar **las nueve puertas** y cada señal de un sumador completo |
| Capítulo 10, sección de ocho sumadores en cadena | C28-T sección 3 | Aclarar C0…C8 y el recorrido del acarreo, sin confundirlo con ocho ciclos |
| Capítulo 11, páginas 106–114, sección ADD/SUB | C28-T figura 2 y secciones 4–5 | Mostrar ocho XOR condicionales, ocho sumadores y banderas, hasta **134 NAND** |
| Final del capítulo 11 | C28-T secciones 6–8, como apéndice opcional | Distinguir netlist digital, diseño eléctrico y decisión posterior de ISA |

La figura 1 muestra las operaciones `N1...N9` de un sumador completo y
su correspondencia exacta con los nombres `an`, `au`, `av`, `P`, `cn`,
`su`, `sv`, `S` y `C` de cada bit en la red C28-R. La figura 2 muestra
el presupuesto **32+72+4+4+22=134 NAND**. Ambas son ilustraciones
didácticas funcionales, **no pinouts de componentes comerciales**.

## Cambios que una futura edición maestra requeriría

1. Elegir si el suplemento entra como apéndice al final del capítulo 11,
   o se distribuye como dos recuadros en las secciones correspondientes.
2. Insertar las dos figuras con pies diferenciados: *topología de puertas*
   para N1…N9 y *bloques de ocho bits* para la ruta de 134 NAND.
3. Rehacer índice y numeración real de páginas del maestro Word/PDF,
   pues la inserción puede desplazar desde el capítulo 11 al final.
4. Verificar que las referencias C4 → C10 → C11 → C12 siguen apareciendo
   después de explicar sus requisitos previos.
5. Inspeccionar a escala de lectura todo el maestro regenerado, incluyendo
   ecuaciones, figuras, tablas, paginación y créditos.

Estas acciones están registradas, **no ejecutadas**. Mantener los fascículos
históricos C28-G recuperables y conservar cualquier versión previa para
comparación.

## Separación respecto a otras piezas pendientes

- **C28-H:** su suplemento sobre lectura secuencial y políticas de PC
  anticipado/diferido **no se inserta** hasta que Marcos decida esa política
  y se compruebe que el relato representa los estados correctos.
- **C28-O:** el atlas histórico de siete páginas requiere ubicarlo sin
  romper el hilo didáctico, confirmar licencias/créditos y actualizar el
  índice y la bibliografía. No mezclar esa tarea con la red NAND de C28-T.
- **Aula-16:** preservar su bus externo de 16 bits y sus dos carriles de ocho.
  El ejemplo de suma en dos pasadas de C28-T es **solo una explicación de
  una ruta de ocho bits**, no una aprobación de microarquitectura Aula-16.
- **ISA y firmware:** el suplemento no asigna opcodes ni congela el
  comportamiento de flags para AND/OR/XOR/NOT.

## Estado al cerrar C28-T

Con las figuras, el suplemento y este mapa, hay una propuesta didáctica
concreta para insertar la ruta aritmética en el libro. **No hay todavía
edición C28-T del maestro**. La siguiente decisión editorial podría
concentrarse en integración/lectura exhaustiva, sin perder el contenido
vigente ni exigir pruebas de hardware.
