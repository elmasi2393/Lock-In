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
        

