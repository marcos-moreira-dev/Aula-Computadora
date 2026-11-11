# Publicación inicial de Aula-Computadora en GitHub

Este repositorio **público** reúne el proyecto educativo original de Marcos Moreira. Contiene fuentes del libro, scripts, modelos digitales y documentación de una futura aplicación JavaFX. **No supone que exista una CPU completa ejecutable ni una aplicación terminada.**

## Qué se publica primero

- Documentación de arquitectura, decisiones, capítulo y verificaciones de contenido.
- Código de pruebas y modelos lógicos/RTL, con sus límites explícitos.
- SVG y recursos originales de circuitos y las propuestas de UX, incluidos C28-AC/C28-AD, cuando provienen de generadores propios.
- Boceto del taller JavaFX y su fuente generadora, claramente etiquetados como **maquetas**, no capturas del programa.

## Qué no se incluye todavía

1. **Fotografías históricas de terceros** y documentos binarios que las incorporen, hasta confirmar atribución, licencia y compatibilidad de redistribución. La existencia de una imagen en una carpeta de trabajo no demuestra permiso de publicación.
2. Ediciones Word/PDF históricas redundantes o candidatas con contenido todavía no revisado. No están perdidas: permanecen en las entregas de trabajo originales y se incorporarán una vez superada la revisión editorial y de derechos.
3. ZIP de retroalimentación, pruebas Windows efímeras y paquetes grandes de intercambio; el repositorio conserva fuentes reproducibles siempre que existan.

## Fuentes de verdad

- `AGENTS.md`, `DECISIONES.md`, `ARQUITECTURA.md` establecen acuerdos y niveles de evidencia.
- `simulador-javafx/CONTRATO_VIDEO_AULA_V1.md` describe el periférico lógico compartido por ambas CPU, no un controlador fabricado.
- `c28_ac/` y `c28_ad/` contienen **activos candidatos y comprobados por etapa**, no un netlist total del sistema.
- `simulador-javafx/CONTRATO_UX_COMANDOS_Y_CAPTURAS_V1_PROPUESTA.md` recoge la gramática operativa y las capturas propuestas.
- `docs/ux/` conserva los análisis de preproducción, separados del libro.

## Responsabilidad de licencias

No se adjudica una licencia abierta al conjunto por defecto. Antes de añadir una licencia o liberar fotografías y traducciones de terceros, el autor debe verificar derechos, atribuciones y coautorías (D-033). No se copia código de `djhworld/simple-computer` ni ilustraciones de otros simuladores.

## Aviso técnico

Los vectores de prueba verifican funciones **del modelo que se probó**: no son certificación de temporización, placa física, consumo o software final de Aula-8/Aula-16. La ISA Aula-8 sigue candidata; la ISA binaria Aula-16 no está congelada.
