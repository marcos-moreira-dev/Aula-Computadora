# Estado editorial después de C21-0.1

**Corte:** 8 de noviembre de 2026, Ecuador. El capítulo 21 «Qué implica ampliar la palabra» está redactado y maquetado en **8 páginas Word/PDF**, con **4 figuras SVG/PNG originales**, **18 ecuaciones OMML editables** y **12 ejercicios resueltos**.

## Qué enseña y qué se comprobó

- Diferencia precisa entre registros/ALU de **8 o 16 bits**, bus externo de **8 o 16 bits**, y **16 líneas de dirección** conservadas en ambas máquinas: 65.536 direcciones de **bytes** (=64 KiB), no 128 KiB.
- Extensión de cuatro registros generales de 32 a 64 bits de almacenamiento funcional: no equivale a duplicar todos los flip-flops ni permite deducir cantidades de encapsulados/transistores.
- Propagación de acarreo entre dos grupos de ocho bits, `0x01FF+1=0x0200`, banderas C/V/Z/N y límites de signo `−32768..32767` frente a `u16=0..65535`.
- Escritura de la palabra `0x1234` en direcciones `2000:34` y `2001:12`; alineación par; dos carriles de memoria de ocho bits explicados **con detalle en el futuro capítulo 22**.
- Diferencia entre compatibilidad de ejercicios y compatibilidad de binarios: Aula-16 aún no tiene ISA de opcodes aprobada.

`python3 scripts/verificar_capitulo_21.py` superó **126.921 comprobaciones** matemáticas/de límites/documentales: comparación de suma directa de 16 bits con suma por bytes, banderas con referencia firmada, alineación, little-endian, XML Word y lectura de PDF. **Son verificaciones del modelo**, no mediciones de temporización o pruebas de bus físico.

## Auditoría acumulada

| Indicador | Estado tras C21 |
| --- | ---: |
| Capítulos numerados redactados | **21/24** |
| Interludios | **1 (P07B)** |
| Capítulos por redactar | **3 (22–24)** |
| Páginas Word/PDF | **185** |
| Figuras técnicas originales | **86** |
| Ejercicios resueltos | **264** |
| Ecuaciones editables OMML | **280** |
| Word/PDF maestro, índice y auditoría integral | Pendientes |
| CPU física, firmware y simulador JavaFX | Sin implementar |

**Próximo:** capítulo 22 «El bus de memoria de dieciséis bits», de acuerdo con `CURRICULO.md`, y luego capítulos 23 y 24. Los dibujos siguen siendo **funcionales** hasta contar con netlists, temporizaciones y ensayos de componentes.
