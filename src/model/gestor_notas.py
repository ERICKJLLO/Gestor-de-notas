from datetime import datetime
from src.model.usuario import Usuario
from src.model.nota import Nota
from src.model.errores_gestor_notas import *

class GestorNotas:
    def __init__(self):
        self.usuarios = {}

    def registrar_usuario(self, nombre_usuario, contraseña):
        if contraseña is None or contraseña == "":
            raise CamposVaciosError("El nombre de usuario y la contraseña no pueden estar vacíos.")
        if nombre_usuario in self.usuarios:
            raise UsuarioYaExisteError("El usuario ya existe.")
        self.usuarios[nombre_usuario] = Usuario(nombre_usuario, contraseña)

    def iniciar_sesion(self, nombre_usuario, contraseña):
        if contraseña is None or contraseña == "":
            raise CamposVaciosError("El nombre de usuario y la contraseña no pueden estar vacíos.")
        usuario = self.usuarios.get(nombre_usuario)
        if not usuario:
            raise UsuarioNoEncontradoError("Usuario no encontrado.")
        if usuario.contrasena != contraseña:
            raise CredencialesInvalidasError("Usuario o contraseña incorrectos.")
        return usuario

    def agregar_nota(self, usuario, titulo, contenido, categoria, enlaces=[]):
        if not usuario or titulo is None or contenido is None or categoria is None:
            raise CamposVaciosError("El usuario, título, contenido y categoría no pueden estar vacíos.")
        for nota in usuario.notas:
            if nota.titulo == titulo:
                raise NotaYaExisteError("Ya existe una nota con ese título.")
        nueva_nota = Nota(titulo, contenido, datetime.now(), categoria, enlaces)
        usuario.notas.append(nueva_nota)

    def editar_nota(self, usuario, indice, nuevo_titulo, nuevo_contenido, nueva_categoria):
        if not usuario or indice < 0 or indice >= len(usuario.notas):
            raise NotaNoEncontradaError("Nota no encontrada.")
        if nuevo_titulo is None or nuevo_contenido is None or nueva_categoria is None:
            raise EdicionInvalidaError("Los nuevos datos no pueden ser nulos.")
        nota = usuario.notas[indice]
        nota.titulo = nuevo_titulo
        nota.contenido = nuevo_contenido
        nota.categoria = nueva_categoria

    def eliminar_nota(self, usuario, indice):
        if not usuario:
            raise EliminacionInvalidaError("Usuario no encontrado.")
        if indice is None or indice < 0 or indice >= len(usuario.notas):
            raise NotaNoEncontradaError("Nota no encontrada.")
        del usuario.notas[indice]

    def cambiar_contraseña(self, usuario, nueva_contraseña):
        if not usuario:
            raise UsuarioNoEncontradoError("Usuario no encontrado.")
        if not nueva_contraseña:
            raise ContrasenaInvalidaError("La nueva contraseña no puede estar vacía.")
        usuario.contrasena = nueva_contraseña
