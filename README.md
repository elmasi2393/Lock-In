# Lock-In

Implementación de un Lock-In digital en Python para efectuar mediciones en tiempo real realizado en la catedra de Experimantal II en el instituto Balseiro en el año 2023.

La señal de referencia y la señal a medir se obtiene mediante dos modulos de ADC. Para ello, se creo la clase abstracta ADC con el objetivo de que la librería del Lock-In funcione siempre que se implementen las funciones necesaris. Para este caso, se encuentra implementado para un ADC MS 1408FS.

## Requerimientos del Sistema

Lista los requerimientos necesarios para poder ejecutar el programa. Ejemplos:

- Python 3.x
- Bibliotecas adicionales:
  - pip install pandas
  - pip install numpy
  - pip install matplotlib
  - bibliotecas necesarias para el ADC 
- Sistema operativo: Windows, Linux y MacOS

## Uso

1. Asegurarse de cumplir con los requerimientos previos descritos anteriormente.
2. Utilizar la clase Lock-In y definir los ADC utilizados para la implementacion.
3. Utilizar la función connect() para asegurarse de que se pueda establecer la comunicación con los ADC.

## Cómo contribuir

Aportando mediciones en diferentes casos y mejora de la velocidad de lectura de los adc para evitar un timesleep.

## Licencia

Creado por Maximiliano Gatto y Francisco Agretti
