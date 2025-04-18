class Usuario:
    """
    Clase que representa un usuario con nombre, contraseña y una lista de notas.
    """

    def __init__(self, nombre_usuario, contrasena):
        """
        Inicializa un nuevo usuario.

        :param nombre_usuario: Nombre del usuario.
        :param contrasena: Contraseña del usuario.
        """
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.notas = []

    def __str__(self):
        """
        Devuelve una representación en cadena del usuario.

        :return: Cadena que representa al usuario.
        """
        return f"Usuario(nombre_usuario={self.nombre_usuario}, contrasena={self.contrasena}, notas={self.notas})"

    def __eq__(self, other):
        """
        Compara dos usuarios para determinar si son iguales.

        :param other: Otro usuario a comparar.
        :return: True si los usuarios son iguales, False en caso contrario.
        """
        if isinstance(other, Usuario):
            return self.nombre_usuario == other.nombre_usuario and self.contrasena == other.contrasena
        return False
