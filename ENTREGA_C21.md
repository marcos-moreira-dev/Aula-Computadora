# Entrega C21-0.1 — dos capítulos más

**Fecha:** 8 de noviembre de 2026 (Ecuador).

Esta entrega continúa la C19-0.1 y desarrolla **exactamente los capítulos numerados 20 y 21**. No renumera el interludio P07B ni sustituye el trabajo anterior. Las fuentes de texto están en Markdown; cada capítulo tiene Word editable y PDF, ecuaciones Word OMML, cuatro figuras SVG/PNG con texto alternativo y doce ejercicios con solucionario.

Se entrega un **ZIP global autónomo**, un **ZIP pequeño solo de Word/PDF**, un **ZIP de diagramas y código** y un **parche para la C19 original**. Para fusionar el parche con `Aula_Computadora_C19_0_1_GLOBAL.zip`, descarga los dos archivos en `Descargas` y ejecuta el script `scripts/fusionar_C19_C21.ps1` incluido en el parche (desde PowerShell). El script no elimina los originales, no sobrescribe un destino existente y conserva la carpeta temporal para inspección.

| Capítulo | Páginas | Figuras | OMML | Ejercicios | Verificador |
| --- | ---: | ---: | ---: | ---: | --- |
| 20 — Programar un pequeño sistema | 9 | 4 | 14 | 12 | `scripts/verificar_capitulo_20.py`: 130.685 comprobaciones |
| 21 — Qué implica ampliar la palabra | 8 | 4 | 18 | 12 | `scripts/verificar_capitulo_21.py`: 126.921 comprobaciones |

**Acumulado editorial:** 21/24 capítulos más P07B, 185 páginas, 86 figuras, 264 ejercicios y 280 ecuaciones OMML. **Pendientes:** capítulos 22–24; libro maestro integral con portada, índice, glosario y auditoría final.

## Reproducir los ejemplos en Windows

Después de descomprimir `Aula_Computadora_C21_0_1_GLOBAL.zip` en `Descargas`, abre PowerShell dentro de la carpeta `Aula-Computadora` y utiliza:

```powershell
py -3 scripts/ensamblador_dos_pasadas_aula8_educativo.py libro/programas/c20_suma_aula8.asm
py -3 scripts/ensamblador_dos_pasadas_aula8_educativo.py libro/programas/c20_euclides_aula8.asm
```

La primera orden produce **13 bytes** para `13+9=22` y la segunda **29 bytes** y etiquetas `BUCLE=6006`, `RESTAR_A=6013`, `FIN=6018` para `mcd(48,18)=6`.

Para regenerar las ocho figuras se necesita Python e Inkscape. Para reconstruir Word se necesita también `python-docx`:

```powershell
py -3 -m pip install python-docx
py -3 scripts/generar_diagramas_capitulos_20_21.py
py -3 scripts/generar_capitulo_20.py
py -3 scripts/generar_capitulo_21.py
```

Para probar también estructura DOCX/PDF y cálculos, ejecuta `py -3 scripts/verificar_capitulo_20.py` y `py -3 scripts/verificar_capitulo_21.py`. **Estas dos auditorías requieren las utilidades Poppler `pdfinfo` y `pdftotext` disponibles en PATH**. La reproducción del PDF a partir de Word requiere LibreOffice u otro conversor equivalente.

## Límite técnico

- No hay CPU Aula-8 o Aula-16 implementada, ni firmware/monitor/binario nativo ejecutados.
- El ensamblador educativo corre **en tu PC**, no en Aula-8.
- Los diagramas de compuertas/registros/RAM y ALU son representaciones **funcionales**. No se debe declarar fidelidad eléctrica o tiempos reales sin netlists, fichas de componentes, simulación y ensayos.
- Aula-16 conserva dirección de 16 bits (**64 KiB direccionados por byte**) y se proyecta con bus **externo de datos de 16 bits**. El capítulo 22 profundizará en los bancos/carriles de memoria.

La verificación automática de los capítulos 1–21 y P07B, y de los contratos Aula-8 R0.14, terminó correctamente en el entorno de preparación de esta entrega.
