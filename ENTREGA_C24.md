# Entrega C24-0.1 — capítulo 24 e interludio P23V

**8 de noviembre de 2026.** Esta entrega añade el **capítulo numerado 24** y el **interludio no numerado P23V**. Con ella se completan los **24 manuscritos numerados**, más dos interludios, en archivos Word/PDF separados. **No está creada todavía la edición maestra del libro**, ni una CPU/firmware/simulador ejecutable.

## Archivos nuevos principales

| Documento | Formatos | Resultado |
| --- | --- | --- |
| P23V — De los mapas de caracteres al escritorio gráfico | `.md`, `.docx`, `.pdf` | 10 páginas, 7 gráficos, 13 OMML, 12 ejercicios |
| C24 — Una computadora que podemos explicar | `.md`, `.docx`, `.pdf` | 9 páginas, 4 gráficos, 13 OMML, 12 ejercicios |
| Diagramas reproducibles | 11 SVG + 11 PNG | Generador Python/Inkscape, sin IA de diagramas |
| Verificador | `scripts/verificar_entrega_c24.py` | 66576 controles anfitriones y documentales |

**Acumulado editorial de archivos individuales:** 220 páginas, 105 figuras originales, 312 ejercicios resueltos y 333 expresiones matemáticas editables, contando los dos interludios. Los programas y el contrato de vídeo **no se han modificado** para agregar opcodes gráficos ni otra pantalla.

## Entrega completa y parche

Hay **dos alternativas**:

- `Aula_Computadora_C24_0_1_GLOBAL.zip`: repositorio completo y autónomo. Si lo descargas, solo necesitas extraerlo.
- `Aula_Computadora_C23_0_1_A_C24_0_1_PATCH.zip`: modificaciones respecto a **`Aula_Computadora_C23_0_1_GLOBAL.zip`**, calculadas por SHA-256. No es autónomo.

Para aplicar el parche en Windows guarda el ZIP base C23 y el parche C24 en **Descargas**. Extrae **únicamente** el script del parche `Aula-Computadora/scripts/fusionar_C23_0_1_C24_0_1.ps1`, conservando esa ruta bajo Descargas, y ejecútalo:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\Aula-Computadora\scripts\fusionar_C23_0_1_C24_0_1.ps1"
```

La salida se llamará `Aula_Computadora_C24_0_1_FUSIONADO.zip`. El script no borra los ZIP originales ni sobrescribe una salida existente. No se requiere fusión si ya tienes el **ZIP GLOBAL C24**.

## Verificación y regeneración

Dentro de la carpeta `Aula-Computadora` descomprimida, ejecuta:

```powershell
py -3 scripts/verificar_contexto.py
py -3 scripts/verificar_contrato_video_aula_v1.py
py -3 scripts/verificar_entrega_c24.py
```

Para inspeccionar PDF en Windows deben existir `pdfinfo` y `pdftotext` en PATH (Poppler). Para **regenerar** figuras necesita Inkscape, y para Word, `python-docx`. Los PDF/Word completos ya están incluidos para leerlos sin regeneración.

## Contrato de fidelidad

- `0x41` es código de A, **no un glifo**; una ROM de ejemplo contiene ocho filas propias `18 24 42 7E 42 42 42 00`.
- El mapa de texto tiene **32×16 códigos**, el gráfico real **256×128 a 2bpp**; el 1bpp es didáctico, no un modo implementado.
- `VIDEO_MODE` usa `C020`; `VRAM_DATA` usa `C028`, y el offset VRAM es un espacio diferente a la dirección CPU. El monitor visible es **una sola pantalla**, no dos periféricos añadidos.
- Las cifras de verificación reproducen **modelos de software**. Ninguna representa ejecución de Aula sobre CPU real, fidelidad eléctrica o certificación de un monitor físico.

**Estado y pendientes:** [libro/ESTADO_EDITORIAL_C24.md](libro/ESTADO_EDITORIAL_C24.md).
