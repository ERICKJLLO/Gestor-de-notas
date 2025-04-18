from datetime import datetime
from src.model.usuario import Usuario
from src.model.nota import Nota
from src.model.errores_gestor_notas import *

class GestorNotas:
    """
    Clase que gestiona las operaciones relacionadas con usuarios y notas.
    """

    def __init__(self):
        """
        Inicializa el gestor de notas con un diccionario vacío de usuarios.
        """
        self.usuarios = {}

    def registrar_usuario(self, nombre_usuario, contraseña):
        """
        Registra un nuevo usuario en el sistema.

        :param nombre_usuario: Nombre del usuario.
        :param contraseña: Contraseña del usuario.
        :raises CamposVaciosError: Si el nombre de usuario o la contraseña están vacíos.
        :raises UsuarioYaExisteError: Si el usuario ya está registrado.
        """
        if contraseña is None or contraseña == "":
            raise CamposVaciosError("El nombre de usuario y la contraseña no pueden estar vacíos.")
        if nombre_usuario in self.usuarios:
            raise UsuarioYaExisteError("El usuario ya existe.")
        self.usuarios[nombre_usuario] = Usuario(nombre_usuario, contraseña)

    def iniciar_sesion(self, nombre_usuario, contraseña):
        """
        Inicia sesión con un usuario existente.

        :param nombre_usuario: Nombre del usuario.
        :param contraseña: Contraseña del usuario.
        :return: El objeto Usuario correspondiente.
        :raises CamposVaciosError: Si el nombre de usuario o la contraseña están vacíos.
        :raises UsuarioNoEncontradoError: Si el usuario no existe.
        :raises CredencialesInvalidasError: Si la contraseña es incorrecta.
        """
        if contraseña is None or contraseña == "":
            raise CamposVaciosError("El nombre de usuario y la contraseña no pueden estar vacíos.")
        usuario = self.usuarios.get(nombre_usuario)
        if not usuario:
            raise UsuarioNoEncontradoError("Usuario no encontrado.")
        if usuario.contrasena != contraseña:
            raise CredencialesInvalidasError("Usuario o contraseña incorrectos.")
        return usuario

    def agregar_nota(self, usuario, titulo, contenido, categoria, enlaces=[]):
        """
        Agrega una nueva nota al usuario.

        :param usuario: El objeto Usuario al que se agregará la nota.
        :param titulo: Título de la nota.
        :param contenido: Contenido de la nota.
        :param categoria: Categoría de la nota.
        :param enlaces: Lista de enlaces relacionados con la nota.
        :raises CamposVaciosError: Si algún campo está vacío.
        :raises NotaYaExisteError: Si ya existe una nota con el mismo título.
        """
        if not usuario or not titulo or not contenido or not categoria:
            raise CamposVaciosError("El usuario, título, contenido y categoría no pueden estar vacíos.")
        for nota in usuario.notas:
            if nota.titulo == titulo:
                raise NotaYaExisteError("Ya existe una nota con ese título.")
        nueva_nota = Nota(titulo, contenido, datetime.now(), categoria, enlaces)
        usuario.notas.append(nueva_nota)

    def editar_nota(self, usuario, indice, nuevo_titulo, nuevo_contenido, nueva_categoria):
        """
        Edita una nota existente.

        :param usuario: El objeto Usuario que posee la nota.
        :param indice: Índice de la nota a editar.
        :param nuevo_titulo: Nuevo título de la nota.
        :param nuevo_contenido: Nuevo contenido de la nota.
        :param nueva_categoria: Nueva categoría de la nota.
        :raises NotaNoEncontradaError: Si la nota no existe.
        :raises EdicionInvalidaError: Si los nuevos datos son inválidos.
        """
        if not usuario or indice < 0 or indice >= len(usuario.notas):
            raise NotaNoEncontradaError("Nota no encontrada.")
        if nuevo_titulo is None or nuevo_contenido is None or nueva_categoria is None:
            raise EdicionInvalidaError("Los nuevos datos no pueden ser nulos.")
        nota = usuario.notas[indice]
        nota.titulo = nuevo_titulo
        nota.contenido = nuevo_contenido
        nota.categoria = nueva_categoria

    def eliminar_nota(self, usuario, indice):
        """
        Elimina una nota existente.

        :param usuario: El objeto Usuario que posee la nota.
        :param indice: Índice de la nota a eliminar.
        :raises EliminacionInvalidaError: Si el usuario no existe.
        :raises NotaNoEncontradaError: Si la nota no existe.
        """
        if not usuario:
            raise EliminacionInvalidaError("Usuario no encontrado.")
        if indice is None or indice < 0 or indice >= len(usuario.notas):
            raise NotaNoEncontradaError("Nota no encontrada.")
        usuario.notas.pop(indice)  # Eliminar la nota del índice especificado

    def cambiar_contraseña(self, usuario, nueva_contraseña):
        """
        Cambia la contraseña de un usuario.

        :param usuario: El objeto Usuario cuya contraseña se cambiará.
        :param nueva_contraseña: Nueva contraseña del usuario.
        :raises UsuarioNoEncontradoError: Si el usuario no existe.
        :raises ContrasenaInvalidaError: Si la nueva contraseña está vacía.
        """
        if not usuario:
            raise UsuarioNoEncontradoError("Usuario no encontrado.")
        if not nueva_contraseña:
            raise ContrasenaInvalidaError("La nueva contraseña no puede estar vacía.")
        usuario.contrasena = nueva_contraseña

    def ver_notas(self, usuario):
        """
        Devuelve la lista de notas de un usuario.

        :param usuario: El objeto Usuario cuyas notas se desean ver.
        :return: Lista de notas del usuario o un mensaje indicando que no hay notas.
        :raises UsuarioNoEncontradoError: Si el usuario no existe.
        """
        if not usuario:
            raise UsuarioNoEncontradoError("Usuario no encontrado.")
        if not usuario.notas:
            return "No hay notas disponibles."
        return [str(nota) for nota in usuario.notas]
