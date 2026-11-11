# Aula-Computadora | C28-H, piloto de lectura secuencial

Este paquete **no reemplaza al global C28-G** y no contiene una CPU terminada.
Sirve como piloto independiente para comparar dos convenciones candidatas de
avance del PC mientras se solicita y acepta un byte de memoria.

La matriz `AUDITORIA_CIRCUITOS_Y_RUTA_FX.md` distingue qué piezas de la
computadora tienen evidencia digital y qué falta comprobar o dibujar antes
de discutir la interfaz JavaFX.

## El problema que construimos

La red de 177 NAND de C28-F ya calculaba PC+1, la seleccion de salto y MAR_D.
Un circuito combinacional entrega valores candidatos; **un registro decide
cuándo guardarlos**. Durante una lectura necesitamos conservar una dirección
hasta que el dispositivo indique que el dato esta disponible. En C28-G se
explico la abstraccion READY; C28-H materializa esa regla con flip-flops
ideales en un modulo Verilog secuencial.

No se altera la ISA candidata, la ROM, el mapa de memoria ni los buses.

| Alternativa | En la solicitud FETCH | Al aceptar el byte | Riesgo docente |
| --- | --- | --- | --- |
| A: C28-F | PC incrementa; MAR retiene PC anterior | MDR captura | Hay dos direcciones distintas durante espera |
| B: C28-G | PC espera; MAR retiene PC anterior | MDR captura y PC incrementa | Menos solapamiento, pero mas latencia |

**Ambas siguen candidatas.** El autor debe aprobar una antes de integrar
microsecuencias o prometer ciclos de CPU.

## Contrato del piloto

- `req=1`: solicita lectura en un flanco si el controlador esta libre.
- `fetch=1`: usa PC para MAR; `fetch=0`: usa `data_addr`.
- `ready=0`: retiene PC/MAR/MDR durante una lectura pendiente (salvo que
  la alternativa A ya incremento PC al solicitarla).
- `ready=1` con lectura pendiente: captura `data_in` en MDR, emite `accepted`
  un ciclo, quita `rd` y `busy`. La entrada READY en reposo se ignora.
- `mdr_valid`: se mantiene tras una lectura aceptada, hasta una nueva lectura
  o RESET; es validez del ultimo dato, **no** un pulso de control.
- `pc_write`: carga un destino en reposo (para comparar preparacion de salto).
- `req+pc_write` simultaneos o nuevos mandatos con `busy=1` producen
  `rejected` un ciclo; durante busy el dato READY puede aceptarse incluso
  si se rechazo otra orden en ese mismo flanco.
- `rst_n=0`: reinicio ideal asíncrono de registros; PC toma `0x6000` como
  **valor didactico**, no como vector ROM implementado.
- En este piloto, una solicitud ocupa al menos un ciclo antes de ser aceptada.

No hay señal WR, bus triestado, arbitro, ROM real, micro-ROM ni temporizacion
electrica. READY es un estímulo **del banco de pruebas**.

## Ejecutar en Windows

Descomprime el ZIP completo dentro de `Descargas`, abre PowerShell en la
carpeta `Aula-Computadora` del piloto y ejecuta:

```powershell
py .\scripts\c28h_piloto.py
```

Esto necesita solo Python 3. Genera una traza JSON, los vectores de referencia,
una tabla de estados y dos diagramas SVG. Si encuentra Inkscape también
genera los PNG; **no falla por falta de Inkscape**.

Para probar realmente el HDL, instala Icarus Verilog (ya presente en el
equipo de Marcos) y ejecuta:

```powershell
iverilog -g2012 -s tb_lectura_c28h -o .\c28_h\piloto\c28h.vvp `
    .\c28_h\rtl\lectura_c28h.v .\c28_h\rtl\tb_lectura_c28h.v
vvp .\c28_h\piloto\c28h.vvp
```

Tambien se incluye `PROBAR_C28H.cmd` para ejecutar las pruebas y recoger
la evidencia ZIP con doble clic, sin requerir un archivo `.ps1`. **Esta
versión se cierra automáticamente** al finalizar: no mantiene una ventana
de pruebas abierta con el directorio de trabajo bloqueado. Conserva los
resultados en archivos `RESULTADO_*.txt` dentro del ZIP de retroalimentación,
incluidos errores de Python o Icarus.

Si lanzaste la prueba desde una ventana PowerShell abierta **dentro** de la
carpeta antigua, esa ventana es otro proceso y debe salir de allí por su
cuenta con `Set-Location "$env:USERPROFILE\Downloads"` o cerrarse.

**C28-H no sustituye C28-G:** antes de eliminar la carpeta extraída de C28-G,
guarda su ZIP global original y comprueba que no contiene cambios locales
únicos. Véase `CONSERVAR_GLOBAL_Y_LIBERAR_CARPETA.md`.

## Lectura correcta de la evidencia

El Python verifica el modelo y genera **salidas esperadas independientes**
para el HDL. La simulacion Icarus, si se ejecuta, contrasta todas las señales
en cada ciclo, para **ambas** alternativas. El VCD puede abrirse con GTKWave.
Un SVG funcional no demuestra que las conexiones electricas esten completas.
Un netlist sintetizado por Yosys y el esquema de pines/consumo se incorporaran
en otra fase. No presentar este piloto como CPU funcional o hardware validado.
