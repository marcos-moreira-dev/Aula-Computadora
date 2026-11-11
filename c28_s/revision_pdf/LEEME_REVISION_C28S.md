# C28-S: recorrido de composición del maestro C28-G

**Fecha:** 9 de noviembre de 2026.
**Archivo examinado:** `libro/ediciones/C28_G/Aula_Computadora_C28_G_MAESTRO.pdf`.

Esta revisión es **local y no destructiva**: no reescribe el Word ni el PDF
maestro. Se usó PyMuPDF para examinar las cajas de texto e imagen de las
248 páginas y crear ocho hojas de contacto JPEG, con 32 miniaturas por hoja
(la última tiene 24 páginas). Las ocho hojas fueron abiertas y repasadas a
escala de composición general; detectan cambios grandes de distribución,
pero no garantizan que todos los rótulos pequeños estén bien a tamaño real.

## Hallazgos comprobables

| Criterio | Resultado |
| --- | ---: |
| Páginas del maestro A4 | 248 |
| Fragmentos de texto obtenidos por el extractor | 17.216 |
| Bloques de imagen encontrados | 127 |
| Cajas de texto o imagen fuera del área de página, tolerancia 1 pt | **0** |
| Páginas sin texto ni imagen | **0** |
| Caracteres de sustitución U+FFFD en texto extraído | **0** |
| Hojas JPEG de contacto conservadas | **8** |
| Entradas de los capítulos en el índice cotejadas con su página real | **26/26** |
| Folios extraídos y comparados con su número físico de página | **247/247** (portada excluida) |

El detalle página por página, SHA-256 del PDF y nombres de las hojas están
en `C28_S_REPORTE_PAGINAS.json`. La prueba Windows
`scripts/c28s_verificar_evidencia_pdf.py` solo coteja su integridad y la
identidad del PDF; la ejecución original de PyMuPDF no se repite en Windows.

## Lo que estas métricas no demuestran

- Un texto o dibujo podría verse demasiado pequeño aunque su caja esté
  dentro de la página.
- No se ha realizado aún una **lectura humana de las 248 páginas a escala
  de lectura** ni una corrección lingüística exhaustiva.
- No se cruzaron automáticamente todos los pies de figuras con sus
  componentes eléctricos, ni se validó una placa física.
- El suplemento secuencial C28-H y el atlas histórico C28-O siguen fuera
  del maestro C28-G: la revisión no los ha integrado.

La auditoría da una evidencia mejor de maquetación global para continuar
sin perder la edición; no significa «libro terminado» ni deja decididas
las alternativas de actualización del PC.
