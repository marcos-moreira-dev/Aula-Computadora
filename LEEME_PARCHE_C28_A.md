# Parche C28-A — instrucciones rápidas

Este paquete **no reemplaza C27** ni contiene todavía un nuevo PDF maestro.
Incluye los nuevos archivos de `c28_a/` y dos scripts de `scripts/`.

## Probarlo sin descomprimir el proyecto C27

Guardar el ZIP de este parche en Descargas. Abrir PowerShell y ejecutar:

```powershell
Set-Location "$env:USERPROFILE\Downloads"
Expand-Archive .\Aula_Computadora_C28_A_PILOTO_Y_AUDITORIA.zip -DestinationPath .\Aula_C28_A_PILOTO -Force
Set-Location .\Aula_C28_A_PILOTO
py .\scripts\c28_verificar_piloto.py
Invoke-Item .\c28_a\piloto_registro8\c28a_registro8_celda.png
```

El resultado esperado son **509268 comparaciones correctas**. La figura PNG
del registro ya está incluida: no hace falta instalar un CAD para verla.

## Incorporarlo a una copia de C27

Si tienes el ZIP global C27 descargado y quieres unirlo con este parche,
ejecuta en PowerShell:

```powershell
Set-Location "$env:USERPROFILE\Downloads"
Expand-Archive .\Aula_Computadora_C27_GLOBAL.zip -DestinationPath .\C28_FUSION -Force
Expand-Archive .\Aula_Computadora_C28_A_PILOTO_Y_AUDITORIA.zip -DestinationPath .\C28_PARCHE -Force
Copy-Item .\C28_PARCHE\c28_a .\C28_FUSION\Aula-Computadora\ -Recurse -Force
Copy-Item .\C28_PARCHE\scripts\* .\C28_FUSION\Aula-Computadora\scripts\ -Force
Copy-Item .\C28_PARCHE\LEEME_PARCHE_C28_A.md .\C28_FUSION\Aula-Computadora\ -Force
Set-Location .\C28_FUSION\Aula-Computadora
py .\scripts\c28_verificar_piloto.py
```

El generador de figuras del piloto requiere **Inkscape** si deseas regenerar
los PNG. El auditor de las 115 figuras requiere la carpeta `libro/figuras`
del C27 global, y **no** funciona en la carpeta aislada del parche.

El banco de pruebas Verilog incluido necesita Icarus Verilog para ejecutarse.
**La prueba Verilog no se ha ejecutado todavía** en la infraestructura usada
para esta entrega; solo se han ejecutado las verificaciones Python.
