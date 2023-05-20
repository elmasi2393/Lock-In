import numpy as np

class desfasador_shift():
    """
    Clase que implementa un desfasador de 90 grados para una señal sinusoidal o cosenoidal.

    Almacena la señal de entrada en un buffer y dependiendo de la frecuencia de refrenecia y la de muestreo, se obtiene el desfasaje dentro del buffer para ontener una señal desfasada 90 grados.

    Permite desfasar una señal en tiempo real, para una determinada frecuencia de muestreo y de referencia constante. El desafasaje funciona mejor una vez que el buffer se llene con mediciones, por lo que demora aproximadamente (fs/fr)/4 segundos en comenzar a desfasar correctamente.

    Ejemplo de utilizacion
    ```python
    import numpy as np
    import matplotlib.pyplot as plt
    from desfasador_shift.desfasador_shift import desfasador_shift

    # Crear una señal
    fs = 130
    fr = 2

    t = np.linspace(0, 10, 10*fs)
    signal = np.sin(2*np.pi*fr*t)

    desf = desfasador_shift(fs, fr, 100)

    out = []

    for i in range(len(signal)):
        out.append(desf.desfasing(signal[i]))

    out = np.array(out)

    # Graficar los resultados
    plt.plot(t, signal, label='signal')
    plt.plot(t, out, label='new signal')
    plt.grid()
    plt.legend()
    plt.show()
    ```
    """

    def __init__(self, fs: float, fr: float, nysquit = 4) -> None:
        """
        Constructor de la clase Desfasador_Shift.

        Args:
            fs : float
                Frecuencia de muestreo de la señal.
            fr : float
                Frecuencia de referencia de la señal.

        Atributos:
            fs : float
                Frecuencia de muestreo de la señal.
            fr : float
                Frecuencia de referencia de la señal.
            shift : int
                Cantidad de muestras necesarias para desfasar en 90 grados.
            chunk_size : int
                Tamaño de la ventana utilizada para el desfasamiento.
            x_buffer : numpy array
                Buffer utilizado para almacenar las muestras anteriores de la señal y realizar el desfasamiento.
        """
        if nysquit < 2:
            raise ValueError("La cantidad de muestras de desfasaje debe ser al menos 2")
        self.nysquit = nysquit
        self.set_fs(fs)
        self.set_fr(fr)

    def set_fr(self, fr):
        """
        Función que setea la frecuencia de referencia.

        Args:
            fr : float
                Frecuencia de referencia.
        """
        if fr <= 0:
            raise ValueError("La frecuencia de referencia debe ser mayor a cero")
        self.fr = fr
    def set_fs(self, fs):
        """
        Función que setea la frecuencia de muestreo.

        Args:
            fs : float
                Frecuencia de muestreo.
        """
        if fs <= 0:
            raise ValueError("La frecuencia de muestreo debe ser mayor a cero")
        if fs < self.nysquit * self.fr:
            raise ValueError(f"La frecuencia de muestreo debe ser al menos {self.nysquit} veces mayor a la frecuencia de referencia")
        self.fs = fs
        self.shift = int(self.fs/self.fr/4)
        self.chunk_size = int(self.fs/self.fr/2)
        self.x_buffer = np.zeros(self.chunk_size)

    def desfasing(self, x: float) -> float:
        """
        Función que realiza el desfasamiento en tiempo real.

        Args:
            x: float
                Última muestra de la señal a procesar.

        Returns:
            float
                Muestra de la señal desfasada en 90 grados.
        """

        # Actualizar buffer de muestras anteriores
        self.x_buffer[:-1] = self.x_buffer[1:]
        
        # Agregar la última muestra al buffer
        self.x_buffer[-1] = x

        # Devolver la muestra desfasada en 90 grados
        return self.x_buffer[-self.shift]
