from datetime import datetime

class Nota:
    def __init__(self, titulo, contenido, fecha_creacion, categoria, enlaces=[]):
        self.titulo = titulo
        self.contenido = contenido
        self.fecha_creacion = fecha_creacion
        self.categoria = categoria
        self.enlaces = enlaces

    def __eq__(self, other):
        if isinstance(other, Nota):
            return self.titulo == other.titulo and self.contenido == other.contenido and self.fecha_creacion == other.fecha_creacion and self.categoria == other.categoria and self.enlaces == other.enlaces
        return False

    def __str__(self):
        return f"Nota(titulo={self.titulo}, contenido={self.contenido}, fecha_creacion={self.fecha_creacion}, categoria={self.categoria}, enlaces={self.enlaces})"