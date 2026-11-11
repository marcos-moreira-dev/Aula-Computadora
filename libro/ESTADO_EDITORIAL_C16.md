# Estado editorial después de C16-0.1

**Corte:** 8 de noviembre de 2026 (Ecuador). Se encuentran redactados 16 capítulos numerados y el interludio P07B; aún faltan los capítulos 17–24 y la edición maestra.

## Capítulo 16 — Subrutinas y pila

- Siete páginas en Word y PDF; **12 ecuaciones OMML**, **4 figuras SVG/PNG originales** y **12 ejercicios resueltos**.
- `CALL 0x6010` desde `0x6000` preserva la continuación `0x6003` mediante dos bytes little-endian en la pila descendente: `RAM[7FFE]=03`, `RAM[7FFF]=60`, `SP=7FFE`.
- `LDI R0,42`, `RET` y `HALT` dejan R0=`2A`, SP=`8000`, PC=`6004` tras el fetch final; los bytes liberados de RAM permanecen, y FLAGS no se fija artificialmente a cero.
- El ejemplo supone **10 lecturas y 2 escrituras** de memoria externas. Una segunda llamada usa `7FFC–7FFD`; los retornos se recuperan LIFO. `JNZ` consume dos bytes de destino tanto si se toma como si no.
- **184.283 controles lógicos/documentales** recorren estados iniciales, retornos anidados, contador y formatos Word/PDF. No equivalen a CPU real, ciclos de reloj o control eléctrico de límites de pila.

## Acumulado

| Indicador | Valor |
| --- | ---: |
| Capítulos numerados | **16/24** |
| Interludios | **1** (P07B) |
| Capítulos pendientes | **8** |
| Páginas | **144** |
| Figuras | **66** |
| Ejercicios resueltos | **204** |
| Expresiones OMML | **207** |

**Siguiente:** capítulo 17 «Encender una computadora»; la pila del firmware y las rutinas de ROM deben diferenciarse de la micro-ROM y de la ABI MiniC-Aula.

```bash
python3 scripts/generar_figuras_capitulo_16.py
python3 scripts/generar_capitulo_16.py
python3 scripts/verificar_capitulo_16.py
```

**Fuentes candidatas:** `simulador-javafx/MICROFLUJO_AULA8_R0_6_BORRADOR.json`, `simulador-javafx/ISA_AULA8_CANDIDATA.json`. No hay microcódigo ni CPU ejecutados.
