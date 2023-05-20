import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

class IIR_filtter():
    """IRR_filtter:
        Clase que implementa un filtro IIR de Butterworth.

        Permite la realizacion de un filtro de butterworth de orden n y frecuencia de corte fc por medio de la ecuacion de un filtro IIR:

        y[n] = b[0] * x[n] + b[1] * x[n-1] + ... + b[n] * x[n-n] - a[1] * y[n-1] - ... - a[n] * y[n-n]

        Donde b y a son los coeficientes del filtro y x[n] es la señal de entrada y y[n] la señal de salida. Esto permite filtrar la señal a medida que se obtiene de alguna fuente externa, como puede ser la medición de un instrumento, lo que permite realizar el filtrado en tiempo real.

        ```python
        # probar el filtro
        import numpy as np
        import matplotlib.pyplot as plt
        from filtro_butter.filtro_butter import IRR_filtter
        import time

        Fs = 1000
        f1 = 30
        t = np.arange(0, 1, 1 / Fs)
        noisy_signal = 3*np.sin(2*np.pi*f1*t) + 1*np.sin(2*np.pi*240*t) + 2*np.sin(2*np.pi*280*t) + 3*np.sin(2*np.pi*120*t)

        #Filtrar señal con filtro IIR de orden 2 y frecuencia de corte de 70 Hz
        fc = 40
        orden = 2
        fs = Fs
        iir_filter = IRR_filtter(fc, orden, fs)

        filtered_signal = []
        #medicion de tiempo de filtrado
        t0 = time.time()
        for n in range(len(noisy_signal)):
            filtered_signal.append(iir_filter.filter(noisy_signal[n]))
        print("Tiempo de filtrado: ", time.time() - t0)

        #Gráficos
        plt.figure()
        plt.plot(t, noisy_signal, label='Señal ruidosa')
        plt.plot(t, filtered_signal, label='Señal filtrada')
        plt.legend()
        plt.show()
        ```
    """
    def __init__(self, fc, orden, fs):
        """__init__

        Args:
            fc (float): frecuencia de corte del filtro
            orden (int): orden del filtro
            fs (float): frecuencia de muestreo
        """
        # Chequeo de argumentos
        if not isinstance(orden, int):
            raise TypeError("El orden del filtro debe ser un entero")
        if not isinstance(fc, float) and not isinstance(fc, int):
            raise TypeError("La frecuencia de corte del filtro debe ser un numero")
        if not isinstance(fs, float) and not isinstance(fs, int):
            raise TypeError("La frecuencia de muestreo del filtro debe ser un numero")

        # Parametros del filtro
        self.fc = fc
        self.orden = orden
        self.fs = fs
        self.wn = fc / (fs / 2)
        self.b, self.a = signal.butter(orden, self.wn, 'low')
        self.chunk_size = orden + 1
        # ventana de señales
        self.x_buffer = np.zeros(self.chunk_size)
        self.y_buffer = np.zeros(self.chunk_size)
    
    def set_order(self, orden):
        """set_order
            Cambia el orden del filtro
        Args:
            orden (int): orden del filtro
        """
        # Chequeo de argumentos
        if not isinstance(orden, int):
            raise TypeError("El orden del filtro debe ser un entero")

        self.orden = orden
        self.b, self.a = signal.butter(orden, self.wn, 'low')
        self.chunk_size = orden + 1
        # ventana de señales
        self.x_buffer = np.zeros(self.chunk_size)
        self.y_buffer = np.zeros(self.chunk_size)

    def set_fs(self, fs):
        """set_fs
            Cambia la frecuencia de muestreo del filtro
        Args:
            fs (float): frecuencia de muestreo
        """
        # Chequeo de argumentos
        if not isinstance(fs, float) and not isinstance(fs, int):
            raise TypeError("La frecuencia de muestreo del filtro debe ser un numero")

        self.fs = fs
        self.wn = self.fc / (fs / 2)
        self.b, self.a = signal.butter(self.orden, self.wn, 'low')

    def set_fc(self, fc):
        """set_fc
            Cambia la frecuencia de corte del filtro
        Args:
            fc (float): frecuencia de corte del filtro
        """
        # Chequeo de argumentos
        if not isinstance(fc, float) and not isinstance(fc, int):
            raise TypeError("La frecuencia de corte del filtro debe ser un numero")

        self.fc = fc
        self.wn = fc / (self.fs / 2)
        self.b, self.a = signal.butter(self.orden, self.wn, 'low')
    def get_order(self):
        """get_order
            Devuelve el orden del filtro
        Returns:
            int: orden del filtro
        """
        return self.orden
    def get_fs(self):
        """get_fs
            Devuelve la frecuencia de muestreo del filtro
        Returns:
            float: frecuencia de muestreo del filtro
        """
        return self.fs
    def get_fc(self):
        """get_fc
            Devuelve la frecuencia de corte del filtro
        Returns:
            float: frecuencia de corte del filtro
        """
        return self.fc
    def get_b(self):
        """get_b
            Devuelve los coeficientes b del filtro
        Returns:
            list: coeficientes b del filtro
        """
        return self.b
    def get_a(self):
        """get_a
            Devuelve los coeficientes a del filtro
        Returns:
            list: coeficientes a del filtro
        """
        return self.a
    
    def filter(self, x):
        """filter
            Aplica y[n]= b[0]x[n]+b[1]x[n-1]+ ... +b[N]x[n-N]-a[1]y[n-1]-a[2]y[n-2]- ... -a[M]y[n-M] (1)
        Args:
            x (float): muestra a filtrar

        Returns:
            float: muestra filtrada
        """
        # Chequeo de argumentos
        if not isinstance(x, float) and not isinstance(x, int):
            raise TypeError("La muestra a filtrar debe ser un numero")
        
        # Actualizo la ventana de señales
        self.x_buffer[:-1] = self.x_buffer[1:]
        self.x_buffer[-1] = x
        self.y_buffer[:-1] = self.y_buffer[1:]

        # Actualizo la salida utilizando los valores nuevos de entrada y antigua de salida
        y_out = 0
        for i in range(self.chunk_size):
            y_out += self.b[i] * self.x_buffer[self.chunk_size - i - 1]
        for i in range(1, self.chunk_size):
            y_out -= self.a[i] * self.y_buffer[self.chunk_size - i - 1]

        if np.isinf(y_out):
            raise ValueError("La salida del filtro es infinita")
        if np.isnan(y_out):
            raise ValueError("La salida del filtro es NaN")
        # Actualizo señal actual para la siguiente iteracion
        self.y_buffer[-1] = y_out

        return self.y_buffer[-1]
    def bode(self):
        """bode
            Grafica la respuesta en frecuencia del filtro, tanto en modulo como en fase
        """

        w, h = signal.freqz(self.b, self.a)
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        plt.subplots_adjust(hspace=0.5)

        ax1.semilogx((self.fs * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))
        ax1.set_title('Diagrama de Bode de un filtro pasa bajos Butterworth')
        ax1.set_ylabel('Magnitud (dB)')
        ax1.grid()

        ax2.semilogx((self.fs * 0.5 / np.pi) * w, np.rad2deg(np.unwrap(np.angle(h))))
        ax2.set_xlabel('Frecuencia (Hz)')
        ax2.set_ylabel('Fase (grados)')
        ax2.grid()
