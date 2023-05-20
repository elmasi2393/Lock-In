import cmath
from .desfasador_shift.desfasador_shift import desfasador_shift
from .filtro_butter.filtro_butter import IIR_filtter
from .ADC.Driver.Driver import Driver, InvalidDriverError
import time


class LockIn():
    def __init__(self, fr, fs, adc_ref : Driver, adc_med : Driver, sleep = 0.004, orden_filtter=2) -> None:
        if not isinstance(adc_ref, Driver):
            raise InvalidDriverError("El ADC de referencia debe ser una subclase de Driver")
        if not isinstance(adc_med, Driver):
            raise InvalidDriverError("El ADC de medición debe ser una subclase de Driver")
        self.sleep = sleep
        self.adc_ref = adc_ref
        self.adc_med = adc_med
        self.fr = fr
        self.fs = fs
        self.orden_filtter = orden_filtter
        self.desfasador = desfasador_shift(self.fs, self.fr)
        self.filtro_1 = IIR_filtter(self.fr/10, self.orden_filtter, self.fs)
        self.filtro_2 = IIR_filtter(self.fr/10, self.orden_filtter, self.fs)
    
    def connect(self) -> None:
        """connect

            Funcion que conecta los ADC listos para medir, en caso de no encontrarlos, levanta una excepcion.
    
        """
        self.adc_ref.connect()
        self.adc_med.connect()
    
    def set_fs(self, fs: float) -> None:
        """
        Función que setea la frecuencia de muestreo.

        Args:
            fs (float): Frecuencia de muestreo.
        """
        self.fs = fs
        self.desfasador.set_fs(fs)
        self.filtro_1.set_fs(fs)
        self.filtro_2.set_fs(fs)
    
    def set_fr(self, fr: float) -> None:
        """
        Función que setea la frecuencia de referencia.

        Args:
            fr (float): Frecuencia de referencia.
        """
        self.fr = fr
        self.desfasador.set_fr(fr)
        self.filtro_1.set_fr(fr)
        self.filtro_2.set_fr(fr)

    def set_orden_filtro(self, orden: int) -> None:
        """
        Función que setea el orden del filtro.

        Args:
            orden (int): Orden del filtro.
        """
        self.orden_filtter = orden
        self.filtro_1.set_orden(orden)
        self.filtro_2.set_orden(orden)
    
    def medir(self) -> tuple:
        """
        Función que realiza una medición de n_muestras.

        Args:
            n_muestras (int): Cantidad de muestras a medir.

        Returns:
            tuple: Señal de referencia, señal a medir y señal lock-in.
        """
        # Señal de referencia
        ref = self.adc_ref.read()
        # Señal a medir
        med = self.adc_med.read()
        time.sleep(self.sleep)

        return ref, med

    def lock_in(self, ref: float, med: float) -> tuple:
        """
        Función que realiza el lock-in de una señal.

        Args:
            ref : float
                Señal de referencia.
            med : float
                Señal a la cual se le realiza el lock-in.

        Returns:
            tuple: Señal lock-in.
        """
        # Desfasamiento de la señal de referencia
        ref_desf = self.desfasador.desfasing(ref)

        # Obtencion de la parte real e imaginaria de la señal de referencia desfasada
        real = self.filtro_1.filter(med*ref)
        imag = self.filtro_2.filter(med*ref_desf)

        # Devuelve modulo y fase de la señal con funcion de cmath
        return cmath.polar(complex(real, imag))
    

# from ADC.ADC_USB1408FS import ADC_USB1408FS

# adc_ref = ADC_USB1408FS("1212")
# adc_med = ADC_USB1408FS('1212')
# lockin = LockIn(10, 100, adc_ref, adc_med)
# lockin.connect()

# while True:
#     ref, med = lockin.medir()
#     lock = lockin.lock_in(ref, med)
#     print(lock)
