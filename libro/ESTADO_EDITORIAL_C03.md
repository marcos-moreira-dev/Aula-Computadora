# Estado editorial después de C03-0.1

**Fecha de corte:** 6 de noviembre de 2026. **Alcance:** tres capítulos didácticos iniciales, revisables. La línea de diseño R0.14 de Aula-8/Aula-16 sigue en estado teórico. No existe un libro maestro terminado ni hardware certificado.

## Qué entrega el capítulo 3

- «**De interruptores a lógica**»: manuscrito original de unas **4.070 palabras**, desde las condiciones 0/1 y las tablas de verdad hasta el inversor, AND y NAND.
- Demostración de que una NAND permite construir NOT, AND y OR; la operación de una compuerta aislada **no conserva memoria**.
- Ejemplo documentado con el **SN74HCT00N PDIP-14** de Texas Instruments: cuatro NAND independientes, pines 1/2/3, alimentación 14/7, tensión recomendada 4,5–5,5 V, VIL ≤ 0,8 V y VIH ≥ 2,0 V.
- **Cuatro diagramas propios SVG y PNG**: interruptores ideales en serie; símbolo NAND y tabla; patillaje PDIP-14; LED activo en bajo con resistor de 1 kΩ y desacoplo de 100 nF.
- **Word editable de diez páginas**, 14 ecuaciones OMML y cuatro figuras incrustadas con texto alternativo; **PDF de diez páginas**, texto seleccionable e inspección visual de todas las páginas.
- **Doce ejercicios más solucionario**: combinaciones, interpretación de filas, realización de funciones con NAND, umbrales, patillaje y cálculos del LED.
- **132 comprobaciones automáticas**: tabla completa y síntesis NAND, clasificación de entradas respecto a umbrales, 2,7 mA, 7,29 mW, presencia de fórmulas y figuras, integridad de DOCX y extracción de PDF. CI actualizado.

Los cálculos de LED usan **VLED ≈ 2,0 V, VOL ≈ 0,3 V y 5 V de alimentación** como hipótesis didácticas. No son lecturas de multímetro ni valores que deban extrapolarse a otra familia de circuitos. El ensayo de protoboard se propone como práctica opcional, pero **no se realizó**.

## Estado acumulado comprobable

| Indicador | Estado C03-0.1 |
| --- | --- |
| Capítulos previstos | 24, divididos en seis partes |
| Capítulos con manuscrito, Word y PDF | **3: 1, 2 y 3** |
| Capítulos por redactar | **21: del 4 al 24** |
| Páginas de los borradores | **29: 9 + 10 + 10** |
| Figuras propias | **10 SVG + 10 PNG** |
| Ejercicios con solución | **36: 12 por capítulo** |
| Ecuaciones Word OMML | **40: 13 + 13 + 14** |
| Controles por capítulo | C01: 57; C02: 87; C03: **132** |
| Libro maestro DOCX/PDF con índice global | **Pendiente** |
| Portada | **Pendiente, etapa separada** |
| Prácticas eléctricas medidas | **No realizadas** |
| Compatibilidad DocuPodcast | **Sin prueba real** |
| CPU, firmware y simulador de Aula | **Sin implementación** |

## Qué falta para completar el libro (sin contar la portada)

1. **Redactar los capítulos 4–24.** El siguiente es «Construir funciones con compuertas» (AND, OR, NOR, XOR y simplificación justificada). Continuar según los prerrequisitos de `CURRICULO.md`, no saltar a CPU/ensamblador sin haber explicado los bloques anteriores.
2. **Revisar con Marcos los capítulos 1–3.** Confirmar profundidad, vocabulario, ejemplos manuales, claridad de ecuaciones y diseño gráfico antes de fijar la versión editorial de referencia.
3. **Elegir y verificar componentes para prácticas físicas.** El LED aún se modela con su caída supuesta; distinguir versiones de encapsulado, ratings, corrientes, márgenes de ruido, cargas, protecciones y lista de compra. Obtener resultados físicos solamente si se realiza montaje y medición, no por analogía con las tablas ideales.
4. **Resolver las decisiones técnicas abiertas del prototipo de computadora.** Las propuestas R0.14 no son especificación R1 aprobada ni CPU probada. Verificar CPU, firmware, buses y memoria antes de afirmar en el libro que sus programas se ejecutan. Mantener Aula-16 con bus de datos externo de **16 bits**.
5. **Completar figuras y aparato de aprendizaje.** Diagramas eléctricos legibles, componentes, tablas, ejercicios, soluciones, prácticas guiadas, glosario, anexos y fichas con procedencia de cada número.
6. **Cerrar fuentes y originalidad.** Citas de normas y fabricantes, revisión de derechos de manuscritos coescritos y cualquier imagen ajena; textos y gráficos nuevos salvo materiales expresamente autorizados.
7. **Integrar un solo documento maestro.** Componer Word y PDF completos con estilos uniformes, índice, numeración continua, referencias cruzadas, pies de figura, texto alternativo y revisión visual página por página.
8. **Probar el producto final en Word, PDF y, si interesa, DocuPodcast.** Verificar legibilidad de fórmulas, accesibilidad básica, impresión, exportaciones y posible interoperabilidad. Ninguna de esas pruebas finales se considera aprobada todavía.

## Reproducibilidad del capítulo 3

Desde la raíz del repositorio se requieren **Python 3, `python-docx` e Inkscape** para generar las imágenes y el Word:

```bash
python3 scripts/generar_figuras_capitulo_03.py
python3 scripts/generar_capitulo_03.py
```

Exportar `libro/capitulos/03_de_interruptores_a_logica.docx` a PDF con Word o LibreOffice, conservando la ruta `libro/capitulos/03_de_interruptores_a_logica.pdf`. Después instalar Poppler (`pdfinfo`, `pdftotext`) y ejecutar:

```bash
python3 scripts/verificar_capitulo_01.py
python3 scripts/verificar_capitulo_02.py
python3 scripts/verificar_capitulo_03.py
python3 scripts/verificar_contexto.py
```

**Próximo paso recomendado:** producir el capítulo 4 con el mismo contrato editorial; no abrir otra serie de diseños de CPU ni comenzar el simulador mientras la prioridad sea terminar el libro.
