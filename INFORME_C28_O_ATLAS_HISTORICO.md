# C28-O · Cierre de la etapa fotográfica histórica

**Fecha:** 9 de noviembre de 2026. **Alcance:** libro Aula-Computadora.

## Retroalimentación real de Windows

`Retroalimentacion_GLOBAL_C28H_20261109_160251.zip` informó:

- **17 controles aprobados; 0 fallidos; 0 pendientes** en la edición anterior.
- **5/5 fotografías históricas descargadas**, con autores, permisos,
  procedencia y SHA-256 registrados por el recolector C28-N.
- Los datos de prueba lógica/HDL y la recopilación fotográfica son dos
  resultados distintos: descargar una foto no equivale a validar un circuito.

## Trabajo editorial de esta etapa

1. Se conservaron cinco archivos JPEG reales, sin recrear representaciones
   históricas mediante imágenes sintéticas.
2. Se inspeccionó la legibilidad de las cinco fotos y se construyó un
   atlas **de siete páginas**: introducción, cinco fichas y créditos.
3. Cada ficha explica qué se observa, cómo lo relacionamos con una pieza de
   Aula-8/Aula-16, los límites de la comparación y una pregunta práctica.
4. Se añadió una auditoría nueva y offline,
   `scripts/c28o_verificar_atlas_historico.py`, que comprueba los cinco JPEG,
   sus SHA-256, metadatos y la estructura de siete páginas del PDF.
5. No se modificaron los archivos maestros de Word/PDF en
   `libro/ediciones/C28_G/`: sigue pendiente integrar los materiales tras
   la revisión técnica/visual de la totalidad del libro.

### Archivos editoriales

- `libro/figuras_historicas_c28o/`: cinco JPEG.
- `libro/ATLAS_HISTORICO_C28O.md`: texto y notas de rigor.
- `libro/ediciones/C28_O/Aula_Computadora_Atlas_Historico_C28_O.pdf`:
  atlas listo para revisión y futura inserción.
- `libro/ediciones/C28_O/ACTIVOS_FOTOGRAFICOS_VERIFICADOS_C28O.json`:
  créditos, licencias, enlaces a Commons, tamaños y SHA-256.
- `scripts/c28o_generar_atlas_historico.py`: generador con ReportLab y Pillow
  (necesarios **solo para regenerar el atlas**, no para las pruebas Windows).
- `scripts/c28o_verificar_atlas_historico.py`: auditoría offline con Python
  estándar; forma parte del nuevo conjunto global de 18 controles.

## Precauciones históricas

- El Altair 8800 de la foto es un ejemplar conservado, no una foto tomada
  necesariamente en 1975.
- El VT100 es un **terminal**, no una computadora general autónoma completa.
- El Intel 8086 tiene bus externo de datos de 16 bits; el IBM PC 5150
  original incorporaba un Intel **8088**, con bus externo de 8 bits.
- Ninguna de las cinco imágenes certifica conexiones eléctricas de Aula.
- Las fotos tienen licencias Creative Commons diversas: se debe atribuir
  y revisar las condiciones de compartir bajo la misma licencia cuando
  corresponda a adaptaciones. El atlas declara que se redimensionaron.

## Progreso del libro

**Antes:** 80 % de madurez editorial estimada.

**Después:** **82 % de madurez editorial estimada**; avance +2 por estudio
visual, selección, explicación didáctica, autoría/licencias y material
suplementario reproducible, no por declarar terminados capítulos ni circuitos.

**Pendientes principales:** hilo causal y revisión de los 26 capítulos;
figuras de circuitos vinculadas a HDL y tablas; resolución editorial del
suplemento C28-H y políticas de PC; incorporación al maestro Word/PDF;
inspección integral de páginas; publicación con permisos y fuentes completas.

**No se crea repositorio remoto ni se modifica GitHub en esta fase.**
