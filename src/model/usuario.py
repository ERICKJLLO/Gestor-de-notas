class Usuario:
    def __init__(self, nombre_usuario, contrasena):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.notas = []

    def __str__(self):
        return f"Usuario(nombre_usuario={self.nombre_usuario}, contrasena={self.contrasena}, notas={self.notas})"

    def __eq__(self, other):
        if isinstance(other, Usuario):
            return self.nombre_usuario == other.nombre_usuario and self.contrasena == other.contrasena
        return False
