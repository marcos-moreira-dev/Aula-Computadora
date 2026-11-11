# C28-B — Portada aprobada y avance editorial comprobable

Fecha de trabajo: 8 de noviembre de 2026.

## Cambios introducidos

1. Portada de IA aprobada por Marcos, integrada como primera página del Word maestro C28-B. Su dibujo es **arte de ambientación**, no diagrama eléctrico certificable.
2. Capítulo 7 con dos láminas de estudio nuevas: tabla de verdad completa del multiplexor (`LOAD`, `Q_i`, `IN_i`, `D_i`) y tabla combinada del registro/búfer (`CLK`, `LOAD`, `OE_n`, `R0`, `BUS`). Se explican la diferencia entre preparar el dato, capturarlo en el flanco y conducirlo al bus.
3. Ajuste de salida tipográfica de las expresiones que contienen literales hexadecimales `0x...`: dichos literales se componen como código monoespaciado para impedir que Word/LibreOffice los separen en símbolos matemáticos ajenos al valor. Las demás ecuaciones siguen siendo OMML.
4. Capítulo 22: la regla de alineación de palabras se explica como prosa y operación `(dirección AND 1) = 0`, evitando la expresión matemática anterior formada por un identificador largo con subrayados. Se conserva la restricción adicional de región y permisos.
5. Los archivos de C27 **no se sobrescriben**. Las fuentes revisadas quedan en `libro/revisiones_c28b`, el constructor en `scripts/generar_libro_maestro_c28b.py`, y la nueva edición en `libro/ediciones/C28_B`.

## Prueba de la lógica y límites de su interpretación

- `python scripts/c28_verificar_piloto.py`: **509.268 comparaciones correctas**, cubriendo NAND, flancos, LOAD, HOLD, Z y estado inicial X.
- El Word C28-B contiene **118 imágenes insertadas**: la portada, las 115 figuras heredadas del volumen y las dos nuevas láminas del registro R0.
- Esta prueba es de **modelo lógico en Python**. No se ha ejecutado el testbench Verilog ni se han comprobado retardos, niveles eléctricos, integrados reales o protoboard.
- Las láminas del capítulo 7 son ayudas didácticas diseñadas a partir del mismo contrato lógico, no capturas de un circuito construido.

## Estado de revisión

- Word maestro editable regenerado: **118 imágenes insertadas**, incluida la portada.
- PDF C28-B final de esta tanda: **238 páginas A4**. El índice se recalculó a partir de la nueva paginación y los 26 títulos se ubicaron en orden.
- Verificación visual de la portada, las dos nuevas láminas y las páginas físicas 120 (`0x12FF`) y 207 (alineación de palabra): realizada en PDF; sin colisiones visibles en esas muestras.
- Ninguna de las 238 páginas resultó aparentemente vacía según el control automático de texto/imágenes.
- No se afirma auditoría al 100 % de las **115 figuras previas**: algunas contienen texto rasterizado y requieren inspección a tamaño real, no solamente comprobaciones automáticas.

## Trabajo siguiente, en orden

1. Concluir auditoría visual transversal de las 115 figuras, empezando por esquemas con cables y etiquetas y verificando texto/ecuaciones en el PDF renderizado.
2. Pasar de diagramas funcionales a **esquemas de compuertas/celdas verificables**, con fuente única de conexiones y simulación digital automatizada. Separar el dibujo funcional, lógico y la futura versión de montaje eléctrico.
3. Continuar el itinerario de construcción de Aula-8: reloj, registro R0, bus, ALU, control, RAM/ROM, ejecución de programas cortos y mapas de memoria contiguos con flechas de saltos. Los contratos de ISA y microarquitectura siguen candidatos.
4. Tras estabilizar la especificación lógica, implementar el taller guiado de JavaFX y volver al libro para insertar capturas reales del simulador, manteniendo las ilustraciones históricas separadas de los diagramas técnicos.
5. Validación final editorial: tablas y soluciones necesarias, naturalidad pedagógica, referencias consolidadas, licencias y revisión de todas las páginas.

No confundir **una edición de trabajo C28-B** con una publicación final «de oro».
