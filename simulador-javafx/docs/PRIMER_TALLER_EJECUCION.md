# Primera aplicación Aula Computadora — taller NAND2 ejecutable

**Estado (11-nov-2026, R0.6):** implementación JavaFX revisada con
retroalimentación visual de Windows. No es una CPU ni una simulación eléctrica.
Hay placa 2D y **primera placa 3D conceptual**, ninguna es una PCB fabricable.
Las imágenes IA son referencias; **el estado real se dibuja desde Java**.

## Qué puedes hacer ahora

1. Abrir la ventana clásica: menú, barra de herramientas con iconos
   vectoriales, kit, workspace, inspector, dock de pruebas y barra de estado;
   controles rectangulares, cabeceras laterales de ancho completo y
   triángulos para plegar o desplegar Recorrido e Inspector.
2. Elegir una pieza `PMOS` o `NMOS` y pulsar uno de los cuatro huecos, o
   arrastrarla al molde. Las piezas colocadas se vuelven opacas. Cada
   transistor presenta tres contactos salientes en 2D y 3D; no es un
   integrado digital de ocho pines.
3. Colocar piezas de tipo incorrecto; el molde las admite sin afirmar que
   el circuito funciona. El inventario total sigue limitado a 2+2.
4. Seleccionar un hueco y abrir el **interior blanco de la cucarachita**
   con doble clic, clic derecho o toolbar. Los terminales externos A, B, Y,
   VDD y GND conducen al esquema CMOS interno. No hay pinout comercial.
5. Quitar/deshacer, guardar automáticamente, reabrir el programa y retomar.
6. Panear y ampliar Montaje 2D/Interior con rueda y `Shift + arrastrar`,
   o la barra de herramientas. En Placa 3D, arrastrar el fondo orbita,
   `Shift + arrastrar` desplaza y la rueda cambia la distancia.
7. Cuando haya cuatro piezas, probar cuatro vectores `00/01/10/11`.
   El resultado observado puede ser 0, 1, X (contención ideal) o Z
   (salida flotante ideal). La prueba muestra discrepancias, no adivina causas.
8. Ver las redes educativas VDD, A, B, Y, MID y GND sobre el molde de
   montaje 2D y la placa 3D. Se basan en el **mismo trazado normalizado**,
   sin atribuir al NAND2 un bus de datos o una PCB fabricable.
9. En el Inspector, pulsar los conmutadores `A = 0/1` y `B = 0/1` para
   observar la salida `Y` en vivo. Con cuatro piezas instaladas, el interior
   resalta en verde los MOS que conducen idealmente y en gris los que no.
   Antes de completar el molde, `Y` permanece sin evaluar.
10. Las vistas Montaje 2D y Placa 3D reflejan las mismas entradas y salida
    en el propio objeto: se colorean las pistas A, B e Y según la señal
    digital. VDD y GND mantienen sus colores de red; MID es neutra porque
    no existe un cálculo eléctrico de su tensión. Los bordes de los MOS
    correctos activos se iluminan de forma conceptual.

La topología es la NAND2 CMOS de C28-AC: dos ramas PMOS paralelas entre
`VDD` y `Y`; dos NMOS en serie entre `Y` y `GND`. Cada pieza discreta se
representa con tres terminales conceptuales. Ni los huecos de la placa ni
la silueta de un chip fijan una huella, un encapsulado comercial o su pinout.

## Ejecutar en Windows

Si ya clonaste el repositorio, actualizar es tan sencillo como abrir
Git Bash en su carpeta y ejecutar:

```bash
git pull --ff-only origin main
```

La compilación y las pruebas JUnit se ejecutan también automáticamente
en **GitHub Actions → Java 21 · NAND2** al subir cambios en `main` o
proponer un pull request. No hace falta que Marcos ejecute una revisión
manual por cada commit; las pruebas visuales de JavaFX siguen siendo
necesarias cuando se modifica el aspecto de la interfaz.

Requisitos: **JDK 21** (con `javac`), **Maven 3.9+** e Internet la primera
vez para resolver las dependencias oficiales de JavaFX y JUnit.

1. Descarga el repositorio completo y extráelo manteniendo las carpetas.
2. Entra en `simulador-javafx`.
3. Haz doble clic en **`EJECUTAR_Y_CAPTURAR.cmd`**. Este ejecuta primero las
   pruebas y abre la GUI solo si pasan.
4. Explora las tres pestañas y pulsa **F12** cada vez que quieras una captura
   de la ventana. Después cierra Aula y espera: se generará automáticamente
   `Retroalimentacion_AULA_GUI_FECHA.zip` con logs y capturas.

También puedes abrir PowerShell o Git Bash en esa carpeta y escribir:

```powershell
mvn clean test
mvn javafx:run
```

Para comprobar las versiones:

```powershell
java -version
javac -version
mvn -version
```

Si prefieres iniciar sin recogida automática, sigue disponible
`INICIAR_AULA.cmd`. Si ya la cerraste y solo necesitas generar un informe,
puedes ejecutar `GENERAR_RETROALIMENTACION.cmd`.

**El nuevo procedimiento nunca transmite el ZIP automáticamente**, ni toma
capturas del escritorio completo por iniciativa propia: F12 lo activas tú.
Recuerda revisar las capturas antes de compartirlas.

### Descomprimir y ejecutar desde PowerShell (copia el bloque completo)

Si descargaste el archivo `AULA_PRIMER_TALLER_JAVAFX_R04.zip` en Descargas:

```powershell
$aulaZip = Join-Path $env:USERPROFILE 'Downloads\AULA_PRIMER_TALLER_JAVAFX_R04.zip'
$aulaDir = Join-Path $env:USERPROFILE 'Downloads\AULA_PRIMER_TALLER_R04'
Expand-Archive -LiteralPath $aulaZip -DestinationPath $aulaDir
& (Join-Path $aulaDir 'simulador-javafx\EJECUTAR_Y_CAPTURAR.cmd')
```

Al finalizar, adjúntame el ZIP `Retroalimentacion_AULA_GUI_*.zip` que quedó
en la carpeta `simulador-javafx`. Si prefieres puedes ejecutar la prueba
mediante un doble clic en lugar de PowerShell.

## Comprobación sin GUI en Linux

Desde la raíz del repositorio:

```bash
bash scripts/verificar_primer_taller_java.sh
```

Esta prueba compila y ejecuta el **modelo independiente de JavaFX**.
La verificación completa (`mvn test` y `mvn javafx:run`) requiere Maven,
JavaFX y un entorno gráfico; los controles del modelo no sustituyen
la observación de la GUI en Windows.

## Próxima iteración

- Ajustes de escala y estilos de la ventana en la Dell G3/Windows.
- Mejorar el gesto de encaje y el resaltado de destino si el uso real lo pide.
- Evaluar el rendimiento 3D y las interacciones de cámara con ratón/touchpad.
- Ampliar el netlist digital y conexiones explícitas solo desde datos
  verificables, evitando duplicar circuitos en las vistas.
- Refinar las posiciones, la iluminación y los gestos de la placa 3D
  conceptual de acuerdo con las capturas reales, sin tratarla como PCB validada.

No se han cambiado el código de instrucciones, el mapa MMIO, la ABI,
el firmware ni la topología completa de las CPU Aula-8/Aula-16.
