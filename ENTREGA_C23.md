# Entrega editorial C23-0.1 — dos capítulos adicionales

**Fecha:** 8 de noviembre de 2026. **Base prevista para fusión:** `Aula_Computadora_C21_0_3_GLOBAL.zip`, que incluye los contratos de vídeo Aula V1 congelados por delegación.

Se completaron **exactamente dos capítulos numerados**, con manuscrito Markdown, Word editable, PDF, cuatro diagramas SVG/PNG por capítulo, ecuaciones Word OMML, doce ejercicios y solucionario cada uno.

| Capítulo | Páginas | Ilustraciones | Ecuaciones | Ejercicios | Comprobaciones |
| --- | ---: | ---: | ---: | ---: | ---: |
| 22 — Un bus externo de 16 bits | 8 | 4 | 13 | 12 | 142737 |
| 23 — Programación para Aula-16 | 8 | 4 | 14 | 12 | 77951 |

**Acumulado:** 23 de 24 capítulos numerados más P07B: 201 páginas, 94 figuras, 288 ejercicios y 307 ecuaciones editables. **El capítulo 24 falta**; P23V sobre mapas de caracteres, gráficos, color y fuentes permanece **planificado** y no constituye un capítulo escrito. El libro maestro aún no existe.

## Descargar y fusionar en Windows

Se generan dos paquetes:

- `Aula_Computadora_C23_0_1_GLOBAL.zip` — repositorio entero, autónomo; basta descomprimirlo.
- `Aula_Computadora_C21_0_3_A_C23_0_1_PATCH.zip` — solo los archivos añadidos o modificados comparados **byte a byte** con el C21-0.3; no es autónomo.

Para utilizar el parche, guarda **la base C21-0.3 y el parche C23-0.1** en `Descargas`. Extrae del parche `Aula-Computadora/scripts/fusionar_C21_0_3_C23_0_1.ps1` y ejecútalo desde PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\Aula-Computadora\scripts\fusionar_C21_0_3_C23_0_1.ps1"
```

Se creará `Aula_Computadora_C23_0_1_FUSIONADO.zip`; el script conserva archivos de entrada, evita sobrescribir una salida existente y deja una carpeta temporal para inspección. **Si descargaste el ZIP global, no necesitas fusionar nada**.

## Comprobaciones reproducibles

Descomprime el ZIP global (o el fusionado), abre PowerShell en la carpeta `Aula-Computadora` y ejecuta:

```powershell
py -3 scripts/verificar_contexto.py
py -3 scripts/verificar_contrato_video_aula_v1.py
py -3 scripts/verificar_capitulo_22.py
py -3 scripts/verificar_capitulo_23.py
```

Para que las pruebas inspeccionen los PDF necesitas **Poppler** (`pdfinfo` y `pdftotext`) disponible en `PATH`. Para regenerar los diagramas se requiere **Python e Inkscape**:

```powershell
py -3 scripts/generar_diagramas_capitulos_22_23.py
```

Para reconstruir los Word se necesita `python-docx` y las dependencias ya documentadas en el proyecto. Los Word/PDF del paquete están previamente maquetados; no hace falta regenerarlos para leerlos.

## Fidelidad y límites de esta edición

- Los cálculos de carriles, alineación, Euclides y Fibonacci fueron contrastados en Python **anfitrión**. No se verificaron flancos, señales, retardos, componentes, placa ni osciloscopio.
- El pseudocódigo de Aula-16 **no es lenguaje máquina válido**: faltan opcodes, encoding, ABI, ensamblador cruzado y CPU capaz de ejecutarlo.
- El bus de **direcciones** sigue siendo de 16 bits y cada dirección nombra un byte; el bus **externo de datos** Aula-16 tiene 16 bits y los bancos RAM tienen dos carriles de ocho bits.
- El contrato lógico de vídeo V1, ROM de caracteres, los seis registros MMIO `C020–C02A` y la planificación P23V **no cambian** en este lote.
