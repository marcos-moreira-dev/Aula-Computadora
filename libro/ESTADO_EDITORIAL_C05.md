# Estado editorial después de C05-0.1

**Fecha de corte:** 6 de noviembre de 2026. **Alcance:** cinco capítulos del currículo redactados y maquetados. La arquitectura R0.14 continúa en fase de propuesta; no hay CPU física o virtual ejecutable.

## Entrega del capítulo 5

- **«La realimentación conserva información»**: desarrollo paso a paso de un latch SR elemental con **dos NAND**, controles activos en bajo, ecuaciones cruzadas, operaciones SET/RESET/HOLD y condición prohibida.
- Se muestra por qué **las mismas entradas 11** permiten conservar Q = 0 o Q = 1 dependiendo de un estado válido anterior; no se presume que un dispositivo arranque en un valor determinado.
- Se distingue entre el caso **00 aplicado**, que fuerza las dos salidas a 1, y su **liberación casi simultánea**, cuyo resultado final no puede garantizarse desde la lógica ideal.
- Cuatro diagramas originales en SVG/PNG: combinacional frente a realimentación, esquema NAND cruzado, estados y secuencia de cinco pasos.
- **Word editable y PDF de ocho páginas**, 11 ecuaciones OMML, cuatro figuras con texto alternativo y **12 ejercicios resueltos**.
- **123 controles automáticos**: soluciones estables de las ecuaciones cruzadas, secuencia, presencia de contenido, archivos SVG/PNG, estructura DOCX y contenido del PDF. Incorporados a CI.
- Referencia concreta de pines y alimentación SN74HCT00N de Texas Instruments. **Sin montaje físico, cronometraje, simulación de transistores ni mediciones de metastabilidad**.

## Alcance preciso de la semántica

Se ajustó [la propuesta de capítulo puente](PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md) según las observaciones de Marcos:

1. La **semántica lógica del hardware** existe cuando un circuito interpreta niveles digitales de acuerdo con su función y polaridad; por ejemplo, una señal activa en bajo asigna la orden de SET al valor 0.
2. Un patrón de bits **no determina por sí solo** si es un número, carácter, dirección, instrucción o campo de software: falta especificar cómo se interpreta.
3. Variables, tipos, estructuras de datos y comportamiento del software construyen otras reglas de interpretación. La **programación orientada a objetos** será solo un ejemplo contextualizador posterior, no una exigencia de MiniC-Aula ni una propiedad del circuito.

El puente sigue siendo **propuesta no redactada**, recomendado tras el capítulo 7 y antes del 8. No se ha agregado ni renumerado ningún capítulo.

## Estado acumulado

| Indicador | C05-0.1 |
| --- | --- |
| Capítulos del currículo numerado | **24** |
| Capítulos con manuscrito, Word y PDF | **5** (1–5) |
| Capítulos numerados aún pendientes | **19** (6–24) |
| Páginas acumuladas | **46** (9 + 10 + 10 + 9 + 8) |
| Figuras originales | **18 SVG + 18 PNG** |
| Ejercicios con respuestas | **60** |
| Expresiones OMML | **64** (13 + 13 + 14 + 13 + 11) |
| Verificación específica C05 | **123 controles** |
| Puente de semántica de bits | Propuesto, no redactado |
| Portada y libro maestro completo | Pendientes |
| CPU, firmware, simulador, hardware físico | No implementados |

## Qué falta para terminar el libro (sin contar portada)

1. Redactar, ilustrar, calcular y verificar los **19 capítulos numerados** restantes. El inmediato es **capítulo 6, «Memorizar en el tiempo»**: latch D, flip-flop, reloj, habilitación y reset.
2. Después del capítulo 7, decidir con Marcos si el puente se integra como interludio sin numeración o como capítulo adicional. Si se incorpora numerado, el total subiría a 25 y habría un capítulo adicional pendiente.
3. Realizar revisión pedagógica transversal de capítulos 1–5: dificultad creciente, continuidad de ejemplos, lectura de esquemas y precisión de terminología.
4. Verificar referencias de componentes y cálculos; incorporar **medidas reales** solamente si algún circuito se construye y ensaya de verdad, distinguiendo su alcance de las demostraciones ideales.
5. Consolidar la arquitectura, la codificación de instrucciones, el firmware y la metodología de pruebas antes de presentar ejecución real de los programas de capítulos posteriores.
6. Compilar el **Word maestro y PDF maestro**, con índice, glosario, bibliografía unificada, créditos, referencias cruzadas, números de página y revisión visual completa.
7. Revisar ortografía, tipografía, accesibilidad, derechos de materiales y fidelidad de exportación para lectura en pantalla e impresión. Probar DocuPodcast solamente si se añade ese destino.

## Reproducir la entrega

En un entorno con Python 3, `python-docx`, Inkscape, LibreOffice y Poppler:

```bash
python3 scripts/generar_figuras_capitulo_05.py
python3 scripts/generar_capitulo_05.py
# Exportar el DOCX como libro/capitulos/05_la_realimentacion_conserva_informacion.pdf
python3 scripts/verificar_capitulo_05.py
```

**Próximo paso:** capítulo 6. El capítulo puente no sustituye la secuencia constructiva de memoria y registros.
