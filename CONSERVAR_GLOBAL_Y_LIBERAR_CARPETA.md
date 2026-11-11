# Cuando Windows dice que otra aplicación está usando la carpeta

Esta situación no indica necesariamente un error de las pruebas. Windows
puede impedir eliminar un directorio mientras **PowerShell, CMD, VS Code,
Inkscape o una ventana del Explorador** lo están usando como directorio
actual o tienen allí un archivo abierto.

## Antes de borrar la extracción anterior

La carpeta `Aula_Computadora_C28_G_GLOBAL` contiene una versión **global**
del libro/proyecto. El ZIP C28-H es solo un **piloto adicional** y no
contiene por sí solo todo el proyecto anterior. No retires C28-G si no
tienes su ZIP original preservado o si editaste archivos allí sin copiarlos.

## Liberación normal (recomendada)

1. Cierra VS Code o los documentos Inkscape que estén abiertos desde C28-G.
2. En cualquier PowerShell o terminal que muestre una ruta
   `...\Aula_Computadora_C28_G_GLOBAL\...`, ejecuta:

   ```powershell
   Set-Location "$env:USERPROFILE\Downloads"
   ```

3. Cierra ventanas del Explorador que estén dentro de la carpeta antigua.
4. En una ventana independiente del Explorador, intenta mover **solo la
   carpeta extraída** `Aula_Computadora_C28_G_GLOBAL` a la Papelera de
   reciclaje. No elimines el ZIP global original.
5. Si Windows sigue indicando que está en uso, **no finalices a ciegas**
   procesos `python`, `java`, `explorer` o `Code`; podrían tener trabajo
   del usuario abierto. Identifica primero qué ventana o proceso conserva
   el bloqueo y cierra solamente ese proceso tras guardar su trabajo.

## Cómo lanzar las nuevas pruebas sin dejar el terminal dentro

Abre PowerShell directamente en `Descargas`, no en la carpeta del programa:

```powershell
Set-Location "$env:USERPROFILE\Downloads"
$piloto = Join-Path $PWD 'Aula_C28H\Aula_Computadora_C28_H_PILOTO\Aula-Computadora'
Start-Process -FilePath (Join-Path $piloto 'PROBAR_C28H.cmd') -WorkingDirectory $piloto -Wait
```

Al terminar, la ventana del comprobador se cierra automáticamente. Los
resultados permanecen en el ZIP `Retroalimentacion_C28H_*.zip` del piloto.
El PowerShell original sigue en `Descargas`, de modo que no retiene la
carpeta de trabajo del piloto como directorio actual.

## Si hace falta diagnosticar un bloqueo persistente

Windows ofrece herramientas gráficas de Microsoft, como Monitor de recursos
o Process Explorer, para determinar el identificador del proceso que tiene
un archivo abierto. Lo importante es localizar el bloqueo **antes** de
decidir si cerrar una aplicación; no hacer una matanza automática de tareas.
