# Entrega C25-0.1 — libro maestro de Aula Computadora

Fecha editorial: 8 de noviembre de 2026 (America/Guayaquil).

## Qué se agregó

- `libro/Aula_Computadora_C25_0_1_MAESTRO.docx`: libro editable unificado desde las 26 fuentes Markdown.
- `libro/Aula_Computadora_C25_0_1_MAESTRO.pdf`: el mismo volumen en una secuencia paginada de lectura.
- `libro/INDICE_C25_0_1.json`: índices de página medidos a partir del PDF; el índice del volumen muestra números reales, no marcadores.
- Portada, página de alcance y créditos, índice en dos páginas, guía de lectura y bibliografía con 24 enlaces a documentación primaria.
- `scripts/generar_libro_maestro.py`: recomposición automática de párrafos, imágenes, tablas, ecuaciones editables OMML y fuentes.
- `scripts/verificar_libro_maestro.py`: revisión de títulos, figuras, ecuaciones, referencias, páginas y orden.
- Se regeneró una imagen del capítulo 24 cuyo PNG de la base C24 había quedado truncado; los SVG de origen se conservan.

**Se conserva** cada capítulo e interludio en Markdown, Word y PDF. El libro maestro no cambia el número curricular de capítulos (24), ni convierte las CPU propuestas en aparatos ya construidos.

## Reproducibilidad

Con Python y los paquetes de construcción y documentación del proyecto:

```bash
python3 scripts/generar_libro_maestro.py --pages-json libro/INDICE_C25_0_1.json
python3 scripts/verificar_libro_maestro.py
```

Cuando cambie el manuscrito, la paginación se vuelve a medir sobre una exportación de prueba a PDF:

```bash
python3 scripts/generar_libro_maestro.py
# Exportar el Word recién creado como PDF (por LibreOffice o Word).
python3 scripts/generar_libro_maestro.py --derive-pages libro/Aula_Computadora_C25_0_1_MAESTRO.pdf
python3 scripts/generar_libro_maestro.py --pages-json libro/INDICE_C25_0_1.json
# Exportar de nuevo el Word definitivo y verificar páginas e índice.
```

Las medidas del índice no constituyen un campo Word dinámico: en una modificación que cambie las páginas se debe repetir la secuencia anterior.

## Descargas y parche

La entrega integral se llama `Aula_Computadora_C25_0_1_GLOBAL.zip`. Si ya se dispone de `Aula_Computadora_C24_0_1_GLOBAL.zip`, se puede descargar solo `Aula_Computadora_C24_0_1_A_C25_0_1_PATCH.zip` y ejecutar en PowerShell la secuencia de `scripts/fusionar_C24_0_1_C25_0_1.ps1` desde la carpeta del proyecto; el script busca ambos ZIP en `Descargas` y genera `Aula_Computadora_C25_0_1_FUSIONADO.zip` sin eliminar los originales.

## Qué queda por revisar

1. Corrección humana de voz, ritmo y exactitud línea por línea de toda la obra; se realizó revisión estructural y de maquetación, **no** corrección exhaustiva de cada afirmación.
2. Confirmar permisos de terceros, licencia de distribución, créditos editoriales y datos de publicación, antes de llamar a la edición «final comercial».
3. Decidir si se añaden índice analítico, glosario general, apéndice de códigos y lecturas propuestas; no son condición para que la edición integral sea utilizable para estudio.
4. Los circuitos completos, la ISA final, el firmware ejecutado, el ensamblador nativo y el simulador JavaFX siguen **sin implementarse ni validarse físicamente**.
