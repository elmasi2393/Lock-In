from .Driver.Driver import Driver
from .usb_1408FS.usb_1408FS import *

class ADC_USB1408FS(Driver):
    """ADC
    Clase para el manejo de ADC para leer la 
    señal de entrada de un sensor

    Args:
        Driver (_type_): _description_
    """

    #ganancias posibles segun libreria
    ganancias = [1.0, 1.25, 2.0, 2.0, 2.50, 4.0, 5.0, 10.0, 20.0]

    #canales disponibles (Fijarse bien los canales)
    canales = [0, 1, 2, 3, 4, 5, 6, 7]

    def __init__(self, serial, gain, chan):
        self.serial = serial
        self.set_gain(gain)
        self.set_chanel(chan)

    def set_gain(self, gain):
        """set_gain
        Método para setear la ganancia del ADC correspondiente a sus valores permitidos

        Args:
            gain (float): ganancia del ADC correspondiente

        Raises:
            Exception: ganancia no soportada
        """

        #elijo la ganancia que mas se ajuste
        self.gain = -1

        for g in self.ganancias:
            if gain  <= g:
                if((g%1) > 0.1):
                    self.gain = f"BP_{int(g)}__{int((g%1)*100)}V"
                else:
                    self.gain = f"BP_{int(g)}_00V"
                break
        if self.gain == -1:
            raise Exception("Ganancia no soportada")
        
    def set_chanel(self, chanel):
        """set_chanel
        Método para setear el canal del ADC correspondiente a sus valores permitidos

        Args:
            chanel (int): canal del ADC correspondiente

        Raises:
            Exception: canal no soportado
        """

        if chanel in self.canales:
            self.chanel = chanel
        else:
            raise Exception("Canal no soportado")
        
    def connect(self):
        self.adc = usb_1408FS(self.serial)

    def read(self):
        v = self.adc.AIn(self.chanel, self.gain)
        return float (format(self.adc.volts(self.gain, v)))