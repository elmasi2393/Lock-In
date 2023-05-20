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

## Ejemplo

``` python
from LockIN.LockIn import LockIn
from LockIN.ADC.ADC_USB1408FS import ADC_USB1408FS
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def main():
    #Definicion de los adc usados
    adc_1 = ADC_USB1408FS("014447D8", 10, 1)
    adc_2 = ADC_USB1408FS("014447AC", 10, 3)
    
    # ~ Configuracion del lock-in
    fs = 140
    fr = 4
    lock_in = LockIn(fs=fs, fr=fr, adc_ref=adc_1, adc_med=adc_2)

    #conectamos el lock-in
    lock_in.connect()

    # Apertura del archivo donde se guardan las mediciones
    file = open("mediciones.csv", "a")

    for i in range(3000):
        v1, v2 = lock_in.medir()
        out = lock_in.lock_in(v1, v2)
        file.write(f"{out[0]}, {out[1]}\n")
    
    file.close()

    datos = pd.read_csv("mediciones.csv", header=None, names=['r', 'f'])

    # ~ Graficar los resultados
    plt.plot(datos['r'], label='r')
    plt.plot(datos['f'], label='f')
    plt.grid()
    plt.legend()
    plt.show()
```

## Cómo contribuir

Aportando mediciones en diferentes casos y mejora de la velocidad de lectura de los adc para evitar un timesleep.

## Licencia

Creado por Maximiliano Gatto y Francisco Agretti

## Contacto

Para sugerencias y dudas sobre la implementación, se puede contactar mediante:
- maximiliano.gatto@ib.edu.ar
- francisco.agretti@ib.edu.ar
