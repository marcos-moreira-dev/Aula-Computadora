# C28-M · Cierre de etapa: madurez editorial estimada 80 %

**Fecha:** 9 de noviembre de 2026. **Formato:** nueva versión del mismo
ZIP GLOBAL; no parche y sin eliminar ediciones antiguas del libro.

## Retroalimentación de Marcos

`Retroalimentacion_GLOBAL_C28H_20261109_152420.zip`:

- **15 APROBADOS; 0 FALLIDOS; 0 PENDIENTES** en Windows.
- Incluye las simulaciones con Icarus Verilog y los renderizados de PNG.
- No demuestra que todos los circuitos del libro estén construidos.

## Trabajo realizado ahora

1. Lectura técnica dirigida del hilo de capítulos 8–14, desde el bus hasta
   el pequeño programa almacenado en RAM.
2. Inspección visual de cuatro láminas especialmente ligadas a esas cuentas:
   mapa de 64 KiB, 13 + 9, selección ADD/SUB y bytes `6000–6007`.
3. Auditoría matemática nueva de **196.620 vectores** de entrada y
   cotejo de tablas/ejemplos del libro.
4. Modelo **documental** de `LDI R0,42 / ST [6F00],R0 / HALT`, que verifica
   ocho lecturas, una escritura, R0=0x2A y PC final=0x6008.
5. Activación en la suite global del verificador ya existente de ISA:
   36 opcodes candidatos sin colisiones y tres ejemplos decodificados.

Los dos controles nuevos son `LIBRO_C28M_ALU_MEMORIA_ISA` e
`ISA_AULA8_BORRADOR`, por lo que el siguiente Windows puede arrojar **17/17**.

## Porcentaje explicado

**Antes: 77 %. Ahora: 80 %.** Incrementos: +1,5 puntos de hilo
didáctico, +1 punto de pruebas de lógica, +0,5 puntos de lectura y
figuras. La suma se explica en `libro/PLAN_CIERRE_EDITORIAL_C28I.md`.

**El Word y PDF maestros siguen siendo C28-G.** Los informes C28-J/L/M y
el suplemento C28-H son materiales de trabajo aparte hasta su integración
editorial; no se anuncia una edición final actualizada inexistente.

**Próximo:** capítulos 15–24, correspondencia entre dibujos y netlists,
contratos de PC y microcontrol, edición maestra, revisión de páginas y
fuentes/licencias. GitHub, branches y pull requests quedan para la etapa
posterior, por decisión de Marcos.

## Pruebas

Ejecutar el bloque PowerShell **completo** de
`LEEME_C28_H_GLOBAL_COMPLETO.md`, desde Descargas; no cambia política de
ejecución ni deja la consola dentro de una carpeta que luego se quiera
eliminar. Enviar el nuevo ZIP `Retroalimentacion_GLOBAL_C28H_*.zip`.
