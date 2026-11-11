# Contrato editorial operativo

Derivado del documento del usuario **Estándar editorial para artefactos didácticos v2.0 (4-11-2026)**. Este archivo es una ficha de proyecto, no reproduce el estándar entero.

## Público y finalidad

- **Público:** principiante en electrónica y arquitectura de computadoras; presupone aritmética elemental, pero no experiencia con transistores.
- **Propósito:** entender mecanismos, circuitos, buses, memoria, CPU y software hasta poder explicar y reproducir los ejemplos.
- **Profundidad:** comienzo intuitivo -> mecanismo -> cálculo -> esquema -> práctica -> limitaciones.
- **Voz:** autor experto, cercano, sobrio y paciente. Sin introducciones de video, personaje artificial, elogio de la IA ni tono de ensayo experimental.
- **Género:** manual progresivo con laboratorios y secciones de consulta delimitadas.
- **Contexto:** microcomputadoras 1970–1980, como motivación histórica y cultural; la arquitectura diseñada es original.

## Contenido y exclusiones

- Construcción de Aula-8 y evolución a Aula-16, desde transistores hasta firmware y Mini C.
- Componentes, símbolos, ecuaciones, valores y diagramas deben ser físicamente coherentes.
- Teclado, pantalla, almacenamiento y controladores se tratan a profundidad suficiente para comprender su interfaz, sin derivar a diseño universal de periféricos.
- No narrar herramientas usadas para producir el documento. **No mencionar JavaFX en el cuerpo del libro.**
- No convertirlo en curso general de Python, Java, C++, astronomía o historia enciclopédica.

## Contrato entre prosa y figura

1. Antes de una figura, decir qué debe observarse y por qué.
2. Identificar después los objetos y símbolos efectivamente visibles.
3. Explicar el recorrido de señales en orden espacial o temporal.
4. Derivar la conclusión que el esquema permite comprobar.
5. Si cambia el estado, cambiar la figura o cerrar explícitamente la referencia.

Ningún cable, nodo, dirección, polaridad, estado o flecha puede aparecer solo en el texto o solo en la imagen cuando eso altere el mecanismo.

## Lenguaje y precisión

- Presentar siglas con nombre y función en su primera aparición.
- Conservar números, unidades, direcciones y notaciones técnicas legibles.
- Distinguir simplificaciones pedagógicas de comportamiento real.
- No inventar resultados, modelos comerciales, voltajes, bibliografía ni pruebas.
- Ejercicios apropiados al mecanismo; soluciones separadas del enunciado.
- Usar una analogía solamente cuando se vuelva al mecanismo físico o computacional preciso.

## Entregables

- **Word DOCX** como fuente principal de edición.
- **PDF** derivado y comprobado independientemente.
- Figuras PNG incrustadas en Word, texto alternativo cuando corresponda; SVG permitido como fuente editable fuera del DOCX, nunca embebido directamente en ese perfil.
- PDF con texto seleccionable, ecuaciones legibles y orden lógico de lectura.
- Compatibilidad DocuPodcast **no declarada como certificada** hasta ejecutar prueba real; de no ser posible, informarla como pendiente.

## Bloqueos de publicación

No lanzar un capítulo con fórmula errónea, esquema engañoso, fuente sin derechos de uso, omisión de prerrequisito grave, Word mal renderizado o PDF ilegible. La longitud del capítulo y número de imágenes dependen de la dificultad real, no de una cuota artificial.

