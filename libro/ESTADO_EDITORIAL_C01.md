# Estado editorial después de C01-0.1

**Fecha de corte:** 5 de noviembre de 2026. Este informe documenta la primera muestra; no declara terminado el libro.

## Lo entregado

- **Capítulo 1, «La corriente y sus caminos»**: manuscrito original de unos 3.700 palabras (fuente Markdown), editable y exportado a Word/PDF.
- **Word DOCX de nueve páginas**, con títulos y estilos, tres figuras PNG con texto alternativo y **13 expresiones OMML** editables.
- **PDF de nueve páginas** con extracción de texto y figuras nítidas. Se inspeccionaron visualmente las páginas renderizadas.
- **Tres figuras originales** disponibles en SVG para edición y PNG para inclusión en documentos: circuito en serie, voltímetro paralelo, amperímetro serie.
- **Doce ejercicios**, solucionario en sección propia, cálculo completo de 5 V/330 Ω/LED rojo (suposición 2 V) y sección de seguridad.
- Referencias primarias para unidades, limitación de corriente y multímetros; **57 controles automáticos** mediante `python3 scripts/verificar_capitulo_01.py`.

## Qué significa el avance

| Concepto | Estado real |
|---|---|
| Plan del libro | 24 capítulos, seis partes definidos |
| Capítulos con borrador escrito | **1 de 24** |
| Capítulos restantes | **23** |
| Capítulo 1 en Word/PDF | **Sí, primera muestra de nueve páginas** |
| Libro Word/PDF maestro | **No existe** |
| Portada | **Actividad independiente, pendiente** |
| Resultados físicos de laboratorio | **No medidos** |
| Certificación DocuPodcast | **No comprobada** |

## Qué falta, sin contar la portada

1. **Leer y corregir el capítulo 1 con Marcos:** voz didáctica, profundidad deseada, formato de ejercicios y claridad de las figuras. Registrar observaciones antes de adoptarlo como plantilla editorial del resto.
2. **Escribir capítulos 2–11**, en orden de prerrequisitos: transistor, compuertas, flip-flops, registros, buses, memoria y ALU; cada uno con circuitos, cálculos, explicación y ejercicios originales.
3. **Cerrar y probar ingeniería R1 para capítulos 12–24:** especificación final Aula-8, CPU lógica ejecutable, ROM y monitor, programación nativa y cargador. Separar código realmente ejecutado de ilustraciones. Definir Aula-16 con su bus externo de 16 bits.
4. **Verificar componentes físicos:** elegir modelos concretos, obtener hojas de datos, revisar límites eléctricos, construir y medir prácticas cuando sea viable. No presentar como físicos resultados que solo se han calculado o simulado.
5. **Completar figuras, solucionario y anexos**: glosario, símbolos de circuitos, guía de instrumentos, documentación de ISA, recorridos de programas y bibliografía consolidada.
6. **Editar la obra completa**: uniformar terminología, nivel de dificultad, numeración de capítulos y figuras; comprobar originalidad, permisos y créditos del manuscrito en coautoría previo.
7. **Integrar Word maestro y PDF maestro**: índice, paginación total, imágenes, enlaces y pruebas de lectura/reflujo; inspeccionar páginas y corregir cortes tras la integración.
8. **Comprobar DocuPodcast con el producto real**, si se dispone de acceso. Hasta entonces solo puede declararse no probado.

## Instrucciones de reproducción (Windows y Linux)

Desde la raíz del repositorio, con Python 3 y `python-docx` instalados, más Inkscape disponible para convertir los SVG:

```bash
python3 scripts/generar_figuras_capitulo_01.py
python3 scripts/generar_capitulo_01.py
```

Después, exportar el DOCX a PDF con Microsoft Word o LibreOffice, guardándolo como `libro/capitulos/01_la_corriente_y_sus_caminos.pdf`. Una vez generado, ejecutar:

```bash
python3 scripts/verificar_capitulo_01.py
```

El verificador de PDF utiliza `pdfinfo` y `pdftotext` (Poppler). El Word y el PDF ya se incluyen en la entrega, de modo que **no hace falta instalar nada para leerlos**.

**Siguiente hito recomendado:** capítulo 2, «El transistor como interruptor», con un NPN de baja corriente y documentación de terminales/valores, sin iniciar una nueva serie R0.
