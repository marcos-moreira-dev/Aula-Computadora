# Estado editorial después de C02-0.1

**Fecha de corte:** 5 de noviembre de 2026. **Alcance:** manuscritos y maquetación iniciales, no libro completo ni electrónica certificada.

## Lo entregado en esta etapa

- **Capítulo 2, «El transistor como interruptor»**: 4.442 palabras aproximadas en manuscrito Markdown, redactado de manera original y comprensible a partir de la práctica del LED del capítulo 1.
- **DOCX editable** de diez páginas, 13 ecuaciones Office OMML, estilos tipográficos coherentes con el capítulo 1 y tres figuras incrustadas con descripción alternativa.
- **PDF de diez páginas**, con texto seleccionable e inspección visual de todas las páginas. Se corrigieron una tabla que se partía entre páginas y una etiqueta que se acercaba a la figura del LED.
- **Tres figuras originales en SVG y PNG**: terminales de la versión onsemi TO-92 del 2N3904, NPN en conducción con LED encendido y NPN en corte con LED apagado.
- **Ejercicios 1–12 y solucionario independiente**: dos ramas eléctricas, resistencia de LED 330 Ω, resistencia de base 4,7 kΩ, condiciones de saturación, corrientes aproximadas y potencia; advertencias sobre conexiones, tensiones y MOSFET.
- **87 comprobaciones documentales y matemáticas**: fórmulas de corriente y potencia, presencia del solucionario y de advertencias, contenido DOCX, ecuaciones, imágenes y extracción de texto PDF.

El **capítulo 1** conserva su borrador de nueve páginas, tres figuras, 13 ecuaciones y 12 ejercicios, con 57 comprobaciones. Se añadió el segundo verificador al workflow de documentación sin cambiar las propuestas de CPU o firmware de la línea R0.14.

## Resumen verificable

| Indicador | Estado C02-0.1 |
|---|---|
| Capítulos previstos | 24, divididos en seis partes |
| Capítulos con manuscrito, Word y PDF | **2: capítulos 1 y 2** |
| Capítulos restantes | **22** |
| Páginas de las muestras actuales | **19 en total: 9 + 10** |
| Figuras originales | **6 SVG y sus PNG: 3 + 3** |
| Ejercicios con respuestas | **24: 12 + 12** |
| Word/PDF maestro del libro | **No existe** |
| Portada | **Pendiente, independiente del trabajo editorial** |
| Montaje, simulación analógica y mediciones | **No realizados** |
| DocuPodcast | **Sin prueba de interoperabilidad** |
| Simulador JavaFX/CPU Aula | **No implementados** |

## Qué falta para terminar el libro, sin contar la portada

1. **Revisión editorial con Marcos de ambos capítulos**: profundidad didáctica, ritmo de ejemplos, terminología y presentación de las fórmulas. No es necesario detener la redacción del capítulo 3, pero sí registrar sus observaciones antes de fijar el estilo definitivo.
2. **Redacción de los 22 capítulos restantes**: del **3 al 24**, respetando el currículo aprobado y el avance desde transistores hasta lógica, memorias, CPU, periféricos y software. Cada capítulo requiere exposición propia, circuitos, ejemplos y ejercicios, no solo un índice.
3. **Capítulo 3 siguiente: «De interruptores a lógica»**. Introducir 0/1 como niveles interpretados, tablas de verdad, inversor y NAND; conectar el estado anterior con compuertas sin prometer que las tensiones sean ideales para cualquier dispositivo.
4. **Definir y validar electrónica específica**: elegir modelos reales de LED, transistores, familias lógicas, memorias y demás piezas; revisar hojas de datos, márgenes, esquemas, polaridades y disipación. Un cálculo teórico no es una medición ni certifica una placa.
5. **Cerrar la ingeniería que necesitan los capítulos más avanzados**: transformar propuestas R0.14 en decisiones R1 aprobadas antes de presentarlas como implementación; exigir CPU y programas realmente ejecutables para afirmar funcionamiento nativo. Mantener Aula-8 y Aula-16 distintas, y el bus externo de Aula-16 **de 16 bits**.
6. **Producir el aparato pedagógico general**: dibujos eléctricos y conceptuales consistentes, tablas de verdad, glosario, anexos, prácticas, fichas de materiales, listas de comprobación y soluciones; programar verificadores donde sea razonable.
7. **Revisión de fuentes y derechos**: comprobar citas primarias y permiso para cualquier material ajeno o manuscrito coescrito; conservar prosa e ilustraciones originales.
8. **Integrar y corregir el libro maestro**: un solo Word y su PDF con índice, numeración global, referencias cruzadas, texto alternativo, tablas, apéndices y controles visuales página por página.
9. **Comprobar lectura y posible compatibilidad DocuPodcast** sobre el producto real; hasta disponer de pruebas, declarar ese punto pendiente.

## Cómo reproducir el capítulo 2

Desde la raíz del repositorio, con **Python 3**, paquete `python-docx`, Inkscape y LibreOffice o Microsoft Word:

```bash
python3 scripts/generar_figuras_capitulo_02.py
python3 scripts/generar_capitulo_02.py
```

Exportar el archivo `libro/capitulos/02_el_transistor_como_interruptor.docx` a PDF en la misma carpeta mediante Word/LibreOffice. Con Poppler (`pdfinfo` y `pdftotext`) instalado, ejecutar:

```bash
python3 scripts/verificar_capitulo_01.py
python3 scripts/verificar_capitulo_02.py
```

**Próximo entregable recomendado:** redactar y dibujar el capítulo 3, siguiendo el mismo flujo de Markdown original → SVG/PNG → Word editable → PDF inspeccionado → controles documentales → paquete reproducible. No abrir una nueva ronda de diseños de CPU como sustituto de avanzar el libro.
