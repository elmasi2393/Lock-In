from abc import ABC, abstractmethod

class Driver(ABC):
    """Driver
    Clase abstracta para el manejo de Driver para leer una señal mediante un ADC implementado en un LockIn.

    Cada subclase debe implementar los métodos connect, read y identify para el correcto funcionamiento de un LockIn

    Args:
        ABC (_type_): _description_
    """
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def read(self):
        pass
    
    @abstractmethod
    def identify(self):
        pass

class InvalidDriverError(Exception):
    """InvalidDriverError
    Excepción para el manejo de errores de Driver no implementado en LockIn

    Args:
        Exception (Any): excepción genérica de Python
    """
    
    pass