# R0.4 — encapsulados y terminales visibles

## Evidencia Windows de R0.3 (11-nov-2026)

Marcos adjuntó captura `imagen(20261111-160604).png` y el paquete de
retroalimentación `Retroalimentacion_AULA_GUI_20261111_110505.zip`.

- `mvn clean test`: **BUILD SUCCESS; 8 pruebas JUnit, 0 fallos y 0 errores**.
- `mvn javafx:run`: **BUILD SUCCESS**, la aplicación abrió y cerró normalmente.
- Captura: las leyendas de las cuatro piezas 3D aparecían **espejadas**;
  apenas se distinguían los contactos, aunque las rutas de placa sí eran visibles.

## Cambios en R0.4

1. El texto del encapsulado 3D utiliza la cara frontal hacia la superficie
   superior de la placa; antes se leía desde la espalda del plano de texto.
2. Tres contactos por componente, con pies y codos metálicos salientes 3D:
   fuente, drenador y compuerta. No reutilizar un mismo tipo de terminal como
   si fuera un circuito integrado DIP de ocho o catorce patas.
3. El molde 2D representa los mismos tres contactos mediante rectángulos
   metálicos visibles fuera del borde del encapsulado.
4. Se conserva el modelo de redes de un bit y las posiciones P1/P2/N1/N2.

Los contactos de este modelo son **educativos**, con orientación ilustrativa:
no fijan número de patilla, huella, paquete SOT/TO/DIP ni conexión física
certificada. Escoger un encapsulado específico requerirá seleccionar y
verificar una hoja de datos comercial.

## Próxima comprobación

- Verificar que las leyendas P1/P2/N1/N2 y PMOS/NMOS **no se reflejen**
  al abrir la vista 3D ni al orbitar unos grados.
- Comprobar patas salientes en la vista 2D y desde una cámara oblicua en 3D.
- Confirmar que arrastrar, seleccionar, retirar, guardar y probar siguen
  funcionando y que el plegado de paneles no afecta el área de trabajo.
- Usar F12 y adjuntar el ZIP de la siguiente ejecución de Windows.

**Estado:** implementación R0.4 lista para prueba de interfaz; no certificada
visualmente hasta recibir una captura de la nueva versión.
