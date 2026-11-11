# Publicar este mismo repositorio en GitHub

Esta carpeta está pensada para vivir íntegra en **un único repositorio**. No habrá un GitHub distinto para el libro y otro para JavaFX.

## Antes de publicar

1. Elegir nombre remoto (propuesta: **Aula-Computadora**).
2. Elegir visibilidad. **Privado inicialmente** es prudente mientras se revisan licencias, coautorías y fuentes.
3. Crear un repositorio GitHub vacío, sin README ni licencia predeterminada para evitar conflictos con esta base.
4. No cargar los PDFs de Scott o el manuscrito coescrito por error: solo se incluyen aquí descripciones y referencias.

## Desde Git Bash en Windows

El paquete R0 se distribuye **con la carpeta .git y un commit inicial**, de modo que al descomprimirlo ya existe un repositorio local. Abrir Git Bash dentro de Aula-Computadora y ejecutar:

~~~bash
git status --short
git log -1 --oneline
git remote add origin https://github.com/TU_USUARIO/Aula-Computadora.git
git push -u origin main
~~~

Sustituir **TU_USUARIO** y el nombre del repositorio si se elige otro. No ejecutar el comando de push sin haber creado el remoto y comprobado que pertenece al usuario correcto.

Si un extractor o sistema de transporte ha omitido la carpeta .git, inicializar una sola vez y generar el commit desde Git Bash antes de añadir origin:

~~~bash
git init -b main
git add .
git commit -m "docs: respaldo inicial Aula-8 y Aula-16"
~~~

## Comprobar publicación

~~~bash
git status --short
git remote -v
git log -1 --oneline
~~~

El repositorio remoto debería mostrar tanto **libro/** como **simulador-javafx/** y todos los documentos raíz. En este primer estado ambas carpetas contienen especificaciones, no el libro o programa final.

## Próximas entregas

- Crear ramas o PR para cambios importantes y preservar historial.
- Incorporar el Word/PDF completo bajo libro/ cuando exista y se haya revisado.
- Incorporar después el código JavaFX bajo simulador-javafx/.
- Mantener los enlaces de documentos y estado en README.md.
- Nunca subir credenciales, tokens, datos personales o material de terceros sin autorización.

