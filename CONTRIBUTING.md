# Contribuciones y ciclo profesional

## Por cada cambio

1. Consultar AGENTS.md y decisiones relevantes.
2. Documentar objetivo, especificación afectada y pruebas previstas.
3. Implementar por módulos, sin expandir alcance incidentalmente.
4. Añadir casos positivos, negativos y límites.
5. Verificar resultados y registrar incertidumbres.
6. Actualizar documentación y HOJA_DE_RUTA.md al mismo tiempo.

## Línea base R0

Esta es una entrega **solo documental**. Existe un verificador de integridad y un workflow GitHub para los documentos, pero **no** existe todavía un POM de aplicación compilable ni se anuncian pruebas Maven superadas. Los scripts de compilación y test del producto se crearán cuando haya código real.

## Revisión de diseño

Se requiere especial revisión cuando cambien:

- Buses, instrucciones, endian y mapa de memoria.
- Convención de llamadas y formato binario.
- Definición de componentes, pines y unidad de control.
- Ejemplos explicados en el libro que deban coincidir con simulación.
- Afirmaciones de validez física o seguridad.

## Convenciones de Git

Mensajes breves: docs:, feat:, fix:, test:, refactor:. No reescribir historial compartido ni borrar pruebas o material sin permiso.

