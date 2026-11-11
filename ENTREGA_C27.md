# Entrega C27-0.1 — Aula Computadora

**Base protegida:** C26-0.1. **Actualización:** 8 de noviembre de 2026.

## Lo que recibes

- `libro/Aula_Computadora_C27_0_1_MAESTRO.pdf`: volumen completo (236 páginas).
- `libro/Aula_Computadora_C27_0_1_MAESTRO.docx`: Word maestro editable,
  ecuaciones OMML e ilustraciones incrustadas.
- `libro/INDICE_C27_0_1.json`: números medidos en el PDF.
- `libro/capitulos/`: 26 fuentes `.md` y sus Word/PDF individuales actualizados.
- `libro/figuras/`: originales SVG, PNG de impresión y portada conceptual.
- `scripts/generar_figuras_construccion_c27.py`: regenera los 9 esquemas.
- `MATRIZ_TRAZABILIDAD_C27.md`: relación capítulo → componente → figura
  → evidencia y límite.
- `FUENTES_CONSULTADAS.txt`: inventario de fuentes externas sin citas
  dispersas innecesarias.
- `libro/ESTADO_EDITORIAL_C27.md`: resultado de pruebas y limitaciones.

## Pruebas de esta versión

En una instalación con Python 3, `python-docx`, Pillow, Inkscape, LibreOffice
y Poppler (`pdfinfo`, `pdftotext`):

```bash
python3 scripts/auditar_revision_c27.py
python3 scripts/verificar_libro_maestro_c27.py
python3 scripts/verificar_capitulos_c27.py
python3 scripts/verificar_isa_aula8_borrador.py
python3 scripts/verificar_contrato_video_aula_v1.py
```

Para regenerar después de cambiar un capítulo:

```bash
python3 scripts/generar_figuras_construccion_c27.py
python3 scripts/generar_libro_maestro_c27.py --pages-json libro/INDICE_C27_0_1.json
soffice --headless --convert-to pdf --outdir libro libro/Aula_Computadora_C27_0_1_MAESTRO.docx
python3 scripts/generar_libro_maestro_c27.py --derive-pages libro/Aula_Computadora_C27_0_1_MAESTRO.pdf
python3 scripts/generar_libro_maestro_c27.py --pages-json libro/INDICE_C27_0_1.json
soffice --headless --convert-to pdf --outdir libro libro/Aula_Computadora_C27_0_1_MAESTRO.docx
python3 scripts/verificar_libro_maestro_c27.py
```

Si necesitas regenerar fascículos, usa los 26 scripts `generar_capitulo_XX.py`,
`generar_puente_07b.py` y `generar_interludio_p23v.py`, y luego exporta sus
DOCX a PDF con LibreOffice. Las comprobaciones revisan el archivo **final**;
generarlo sin mirar sus páginas no basta.

## Paquetes de descarga

El empaquetador `scripts/empaquetar_C27.py` crea:

1. `Aula_Computadora_C27_GLOBAL.zip`: repositorio completo actual de C27,
   sin copias binarias obsoletas de los maestros C25/C26 (esas quedan en la
   base protegida fuera del ZIP).
2. `Aula_Computadora_C27_PATCH_DESDE_C26.zip`: solo los archivos nuevos o
   modificados frente a una base C26 local para actualización conservadora.
3. Doce partes numeradas `Aula_Computadora_C27_GLOBAL.zip.part01` hasta
   `.part12`, y un `MANIFIESTO_ENTREGA_C27.json` con SHA256.

El script `scripts/unir_partes_c27.ps1` une esas partes desde la carpeta
**Descargas** en Windows, muestra su hash y descomprime en una carpeta **nueva**.
No borra el ZIP anterior ni sobrescribe una carpeta existente.

## Lo que esta edición no proclama

Los programas y diagramas de memoria utilizan una **ISA candidata**. No hay
CPU fabricada, compilador nativo ni firmware ejecutable. El patillaje físico
del SN74HCT00N se cotejó con fabricante, pero el latch no está certificado
en una protoboard. Las fotografías históricas con permisos siguen pendientes.
