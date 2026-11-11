# Conservación del libro y aprendizaje con GitHub — plan FUTURO

**Estado:** PLAN, no ejecución. No se ha creado repositorio ni conectado
ninguna cuenta. Este documento se aplica cuando Marcos declare terminada
la edición del libro y decida iniciar el código.

## Preservar el libro antes del primer cambio de programación

1. Conservar las fuentes Markdown y Word, PDF maestro, figuras SVG/PNG,
   scripts de generación, pruebas y licencias. Evitar archivar solo un PDF.
2. Identificar una **versión editorial cerrada** (`libro-v1.0.0`) mediante
   etiqueta Git y un artefacto ZIP íntegro, además de su suma SHA-256.
3. Mantener esos archivos dentro de `libro/` en el **mismo repositorio**
   futuro que incluirá el código, como ya se acordó.
4. No borrar el historial del manuscrito al introducir proyectos nuevos.
   Los cambios posteriores del libro serían solo erratas o nuevas ediciones
   trazables, no reescrituras silenciosas.
5. Antes de iniciar el código, documentar qué nombre/ubicación se elige
   para los módulos sin mover ni renombrar el libro ya publicado.

## Flujo para que Marcos practique desarrollo colaborativo

1. Marcos autoriza expresamente la conexión con GitHub **cuando llegue el
   momento**; comprobar entonces qué mecanismos y permisos están disponibles.
2. Partir de una rama de trabajo pequeña, por ejemplo `feature/registro8`.
3. Crear un cambio limitado y pruebas automáticas reproducibles.
4. Abrir un **pull request** con explicación de qué cambió, por qué y cómo
   se comprobó; aprender a interpretar la diferencia de archivos.
5. Hacer revisión de código con comentarios, petición de ajustes y
   respuesta a los comentarios. Marcos mantiene el control sobre la aprobación.
6. Fusionar después de pasar los controles; dejar un historial legible y
   vincular el código con su explicación en el libro.

Se podrá utilizar la interfaz de GitHub, herramientas Git autorizadas o
integraciones disponibles en ese momento. No se presupone acceso hoy.

## Barreras para proteger el material editorial

- Cambios propuestos en `libro/` exigirán revisión explícita y motivo.
- Definir, si conviene, reglas de protección de rama, checks automáticos y
  responsables de revisión (`CODEOWNERS`) en el repositorio real.
- No prometer que `CODEOWNERS` por sí solo impida cambios: dependerá de
  las reglas y permisos efectivos configurados.
- Las pruebas del software futuro no cambiarán retrospectivamente la
  evidencia disponible para la edición publicada.

**No iniciar esta fase antes del cierre del libro y del visto bueno de Marcos.**
