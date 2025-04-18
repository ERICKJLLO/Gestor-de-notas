from datetime import datetime

class Nota:
    """
    Clase que representa una nota con título, contenido, fecha de creación, categoría y enlaces relacionados.
    """

    def __init__(self, titulo, contenido, fecha_creacion, categoria, enlaces=[]):
        """
        Inicializa una nueva nota.

        :param titulo: Título de la nota.
        :param contenido: Contenido de la nota.
        :param fecha_creacion: Fecha de creación de la nota.
        :param categoria: Categoría de la nota.
        :param enlaces: Lista de enlaces relacionados con la nota.
        """
        self.titulo = titulo
        self.contenido = contenido
        self.fecha_creacion = fecha_creacion
        self.categoria = categoria
        self.enlaces = enlaces

    def __eq__(self, other):
        """
        Compara dos notas para determinar si son iguales.

        :param other: Otra nota a comparar.
        :return: True si las notas son iguales, False en caso contrario.
        """
        if isinstance(other, Nota):
            return self.titulo == other.titulo and self.contenido == other.contenido and self.fecha_creacion == other.fecha_creacion and self.categoria == other.categoria and self.enlaces == other.enlaces
        return False

    def __str__(self):
        """
        Devuelve una representación en cadena de la nota.

        :return: Cadena que representa la nota.
        """
        return f"Nota(titulo={self.titulo}, contenido={self.contenido}, fecha_creacion={self.fecha_creacion}, categoria={self.categoria}, enlaces={self.enlaces})"