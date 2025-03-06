class UsuarioNoEncontradoError(Exception):
    """Se lanza cuando un usuario no se encuentra en el sistema."""
    def __init__(self, mensaje="El usuario no existe."):
        super().__init__(mensaje)

class UsuarioYaExisteError(Exception):
    """Se lanza cuando se intenta registrar un usuario que ya existe."""
    def __init__(self, mensaje="El usuario ya está registrado."):
        super().__init__(mensaje)

class ContrasenaInvalidaError(Exception):
    """Se lanza cuando la contraseña proporcionada es inválida."""
    def __init__(self, mensaje="La contraseña es inválida."):
        super().__init__(mensaje)

class CredencialesInvalidasError(Exception):
    """Se lanza cuando las credenciales de inicio de sesión son incorrectas."""
    def __init__(self, mensaje="Usuario o contraseña incorrectos."):
        super().__init__(mensaje)

class CamposVaciosError(Exception):
    """Se lanza cuando se intenta ingresar datos vacíos en el sistema."""
    def __init__(self, mensaje="No se permiten campos vacíos."):
        super().__init__(mensaje)

class NotaNoEncontradaError(Exception):
    """Se lanza cuando se intenta acceder a una nota que no existe."""
    def __init__(self, mensaje="La nota no fue encontrada."):
        super().__init__(mensaje)

class NotaYaExisteError(Exception):
    """Se lanza cuando se intenta crear una nota con un título ya existente."""
    def __init__(self, mensaje="Ya existe una nota con este título."):
        super().__init__(mensaje)

class EdicionInvalidaError(Exception):
    """Se lanza cuando se intenta editar una nota con datos inválidos."""
    def __init__(self, mensaje="Los datos proporcionados para la edición son inválidos."):
        super().__init__(mensaje)

class EliminacionInvalidaError(Exception):
    """Se lanza cuando se intenta eliminar una nota de manera incorrecta."""
    def __init__(self, mensaje="No se puede eliminar la nota especificada."):
        super().__init__(mensaje)