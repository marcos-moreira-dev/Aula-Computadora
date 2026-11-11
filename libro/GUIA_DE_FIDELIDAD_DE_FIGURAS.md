# Guía de fidelidad y reproducción de figuras técnicas

Esta guía evita que una figura atractiva enseñe un mecanismo falso. Los diagramas de C18–C21 son **vectores SVG generados a partir de contratos y ejemplos verificables**: etiquetas, offsets, anchos de registros/buses y direcciones se comprueban antes de exportar PNG. **No son netlists eléctricos, oscilogramas medidos, simulaciones físicas ni pruebas de una CPU.**

## Qué distingue cada clase de dibujo

| Tipo | Qué se puede afirmar | Qué no se puede afirmar con solo un SVG |
| --- | --- | --- |
| Diagrama funcional | Quién produce y consume un dato; qué valor u operación representa | Polaridad eléctrica, selección de pines, tiempos reales |
| Diagrama lógico | Tabla de verdad, señales de entrada/salida, ecuación y estados discretos definidos | Retardos de propagación, metastabilidad, integridad de señal |
| Flip-flop | Diferencia entre flanco y nivel; D, Q, reloj, reset y secuencia de estados **según componente elegido** | Que una representación genérica sirve para cualquier chip real |
| RAM/bus | Direcciones, CE/OE/WE cuando existan en una hoja de datos, direcciones válidas y sentido de lectura/escritura | Que cualquier RAM física cumpla la temporización propuesta |
| Protocolo de periférico | Registros MMIO, transiciones de estado, conteos y casos de error acordados | Que el periférico y su firmware existan físicamente |

## Contrato editorial de un esquema

1. Identificar **el origen de cada dirección, byte, bandera y estado**. El programa de dibujo usa los JSON `ROM_MONITOR_AULA8_R0_11_BORRADOR.json` y `CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.json` y falla si cambian las constantes principales.
2. Etiquetar el **sentido de cada transferencia**. Una flecha de datos no es una pista eléctrica ni implica tiempo de propagación cero.
3. Distinguir números en hexadecimal de números decimales, en particular `0x10=16`, `0x0100=256` y little-endian.
4. Para una figura de RAM y bus, no dibujar simultáneamente dos salidas activas si no hay arbitraje; para una de flip-flops, no mezclar transparencia por nivel con captura por flanco.
5. No asignar **pines, tensión, reloj ni ancho de bus de Aula-16** copiándolos de Aula-8. Aula-16 conserva su bus externo **de 16 bits**.
6. Inspeccionar el SVG en tamaño real, el PNG rasterizado y su inclusión en Word/PDF. Verificar legibilidad de etiquetas, texto alternativo y que el cuerpo del libro explique antes el mecanismo.
7. Ante una corrección técnica, editar primero el contrato o los datos y **regenerar**; no retocar a mano una imagen PNG de forma que se desincronice de su SVG.

## Reproducir en Windows

Descomprime el ZIP global en `Descargas`, instala Python 3, `python-docx` e [Inkscape](https://inkscape.org/) para exportar PNG. Abre PowerShell dentro de la carpeta `Aula-Computadora` que hayas extraído:

```powershell
py -3 -m pip install python-docx
py -3 scripts/generar_diagramas_tecnicos_aula8.py
py -3 scripts/generar_diagramas_capitulos_20_21.py
py -3 scripts/generar_capitulo_18.py
py -3 scripts/generar_capitulo_19.py
py -3 scripts/generar_capitulo_20.py
py -3 scripts/generar_capitulo_21.py
py -3 scripts/verificar_capitulo_18.py
py -3 scripts/verificar_capitulo_19.py
py -3 scripts/verificar_capitulo_20.py
py -3 scripts/verificar_capitulo_21.py
explorer.exe libro\figuras
```

En Linux, sustituye `py -3` por `python3`. Si no se detecta Inkscape, el script informa cómo instalarlo y no declara haber producido el PNG. Los SVG son **editables** en programas vectoriales; los PNG quedan incrustados en los DOCX. Para convertir los Word a PDF y revisar cada página se usa la herramienta de renderizado de documentos del entorno de desarrollo o LibreOffice. El script C20/C21 produce **8 figuras** y comprueba símbolos (`BUCLE`, `RESTAR_A`, `FIN`) y bus externo de Aula-16 de **16 bits** antes de dibujar.

## Puerta de calidad para los capítulos posteriores

Los dibujos de los futuros capítulos sobre CPU, control, memorias y buses deben poder rastrearse a **un netlist o una tabla de señales** cuando tales objetos ya existan. Antes de eso, el título y la leyenda deben indicar que el esquema es **conceptual o candidato**. Para probar física real hacen falta fichas de componentes, análisis eléctrico, validación de temporización y ensayos, no una ilustración.
