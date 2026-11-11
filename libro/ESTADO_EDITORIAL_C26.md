# Estado editorial C26-0.1 — revisión de lectura y figuras

**Fecha:** 8 de noviembre de 2026.

## Resultado

- El **libro maestro** reúne 26 capítulos: los 24 troncales más **7B** y **23B**.
- El Word/PDF maestro tiene **228 páginas** y los 26 fascículos individuales suman **221 páginas** (se paginan por separado).
- Hay **332 ecuaciones OfficeMath** en el libro maestro, incluidas 28 potencias con representación matemática específica.
- Las fuentes Markdown mantienen **312 ejercicios resueltos** (12 por capítulo). Para la edición maestra se seleccionaron **156 ejercicios** (6 por capítulo), conservando los fascículos individuales íntegros.
- Se añadió la cuarta figura de C01 (protoboard); por tanto, la obra utiliza **106 figuras originales** en el conjunto de capítulos.
- Se corrigieron posiciones de etiquetas en C01 y C13 y la expresión hexadecimal de C08; se generaron las potencias matemáticas con elementos OfficeMath.
- La primera inspección de miniaturas abarcó la colección completa de figuras; la revisión focalizada del PDF comprueba las tres incidencias visibles comunicadas por el autor.
- Bibliografía agrupada al final, con inventario externo en `FUENTES_CONSULTADAS.txt`; se redujo la repetición de referencias al final de los capítulos introductorios.

## Cómo se usa el contenido en otros componentes

El material que enseña un concepto y termina allí puede permanecer como explicación o ejercicio. Las partes **reutilizables en el simulador futuro** son los nodos del circuito introductorio, los flujos de datos, habilitaciones de bancos de RAM, registros y decodificadores, y el contrato lógico V1 de texto/bitmap. Las figuras actuales no representan todavía una única netlist validada ni son pruebas físicas.

## Pendientes reales

1. Lectura humana integral para detectar fragmentos escuetos, reiteraciones locales o pasajes que necesiten más ejemplos narrativos. La inspección técnica de maquetación no equivale a una corrección literaria profesional.
2. Selección y derechos de imágenes históricas; portada ilustrativa y fotografías/ilustraciones de contexto **pospuestas** por decisión del autor.
3. Definir licencia, permisos y créditos finales antes de publicar para distribución comercial o abierta.
4. Implementar y verificar hardware, CPU, firmware, ensambladores nativos y simulador; el manuscrito solo enseña contratos y modelos hasta que haya código/circuitos ejecutables.

**Contrato intacto:** Aula-8 usa bus externo de ocho bits; Aula-16, bus externo de dieciséis y dos bancos de ocho. El controlador V1 mantiene pantalla única con modos alternativos, seis registros en direcciones pares `C020–C02A`, VRAM indirecta y ROM de glifos de 2 KiB. No se cambió ninguna de estas decisiones.
