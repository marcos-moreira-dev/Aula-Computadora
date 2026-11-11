# Estado editorial después de C20-0.1

**Corte:** 8 de noviembre de 2026, Ecuador. El capítulo 20 «Programar un pequeño sistema» se encuentra redactado y maquetado en **9 páginas Word/PDF**, con **4 figuras SVG/PNG originales**, **14 ecuaciones editables OMML** y **12 ejercicios resueltos**.

## Qué enseña y qué se comprobó

- Del texto del editor a bytes y direcciones; primera pasada para etiquetas, segunda para emisión; ejemplos con símbolos adelantados.
- Archivo ejecutable en el **anfitrión** `scripts/ensamblador_dos_pasadas_aula8_educativo.py`; **no** es ensamblador nativo ni emulador de CPU. Limita entradas y devuelve errores explícitos.
- Código completo y reproducible de suma `13+9=22` (13 bytes) y Euclides `mcd(48,18)=6` (29 bytes), en `libro/programas/c20_*.asm`, con tabla de direcciones/bytes y resultado previsto para `RAM[6F00]`.
- Fibonacci iterativo y recursivo como referencia matemática: `F(6)=8`, 25 llamadas recursivas ingenuas, `F(14)=377` supera el rango `u8`.
- Papel del monitor ROM, del cargador y de la ABI; un pequeño sistema **no se considera construido** por escribir sus comandos en un capítulo.

Las **130.685 comprobaciones** de `python3 scripts/verificar_capitulo_20.py` contrastan opcodes, etiquetas, errores de ensamblado, todas las sumas de dos bytes, 65.025 pares positivos para Euclides, Fibonacci y el contenido/maquetación de Word/PDF. El programa por restas exige entradas positivas: no trata `mcd(a,0)`.

Las cuatro figuras originales se regeneran con `python3 scripts/generar_diagramas_capitulos_20_21.py`. Son diagramas funcionales **no** netlists eléctricos ni trazas obtenidas de una CPU real.

**Siguiente capítulo:** 21, «Qué implica ampliar la palabra». En esta entrega ya se incluye y documenta por separado.
