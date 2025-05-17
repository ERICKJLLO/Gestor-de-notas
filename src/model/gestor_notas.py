from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session
from src.model.errores_gestor_notas import *

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String, nullable=False, unique=True)
    contrasena = Column(String, nullable=False)
    notas = relationship("Nota", back_populates="usuario", cascade="all, delete-orphan")

class Nota(Base):
    __tablename__ = 'nota'
    id_nota = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    categoria = Column(String, nullable=False)
    enlaces = Column(Text)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    usuario = relationship("Usuario", back_populates="notas")

# Configuración de la base de datos persistente
engine = create_engine('sqlite:///gestor_notas.db', connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))

class GestorNotas:
    """
    Clase que gestiona las operaciones relacionadas con usuarios y notas.
    """

    def __init__(self, session=None):
        """
        Inicializa el gestor de notas con un diccionario vacío de usuarios.
        """
        self.session = session or Session()

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
        if not nombre_usuario:
            raise CamposVaciosError("El nombre de usuario y la contraseña no pueden estar vacíos.")
        if self.session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first():
            raise UsuarioYaExisteError("El usuario ya existe.")
        usuario = Usuario(nombre_usuario=nombre_usuario, contrasena=contraseña)
        self.session.add(usuario)
        self.session.commit()

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
        usuario = self.session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first()
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
        if not usuario or not contenido or not categoria:
            raise CamposVaciosError("El usuario, título, contenido y categoría no pueden estar vacíos.")
        nueva_nota = Nota(
            titulo=titulo,
            contenido=contenido,
            fecha_creacion=datetime.now(),
            categoria=categoria,
            enlaces=",".join(enlaces) if enlaces else "",
            usuario=usuario
        )
        self.session.add(nueva_nota)
        self.session.commit()

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
        if not usuario:
            raise NotaNoEncontradaError("Nota no encontrada.")
        notas = self.session.query(Nota).filter_by(id_usuario=usuario.id_usuario).all()
        if indice < 0 or indice >= len(notas):
            raise NotaNoEncontradaError("Nota no encontrada.")
        nota = notas[indice]
        if nuevo_titulo is None or nuevo_contenido is None or nueva_categoria is None:
            raise EdicionInvalidaError("Los nuevos datos no pueden ser nulos.")
        nota.titulo = nuevo_titulo
        nota.contenido = nuevo_contenido
        nota.categoria = nueva_categoria
        self.session.commit()

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
        notas = self.session.query(Nota).filter_by(id_usuario=usuario.id_usuario).all()
        if indice is None or indice < 0 or indice >= len(notas):
            raise NotaNoEncontradaError("Nota no encontrada.")
        self.session.delete(notas[indice])
        self.session.commit()

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
        self.session.commit()

    def ver_notas(self, usuario):
        """
        Devuelve la lista de notas de un usuario.

        :param usuario: El objeto Usuario cuyas notas se desean ver.
        :return: Lista de notas del usuario o un mensaje indicando que no hay notas.
        :raises UsuarioNoEncontradoError: Si el usuario no existe.
        """
        if not usuario:
            raise UsuarioNoEncontradoError("Usuario no encontrado.")
        notas = self.session.query(Nota).filter_by(id_usuario=usuario.id_usuario).all()
        if not notas:
            return "No hay notas disponibles."
        return [f"Título: {n.titulo}\nContenido: {n.contenido}\nCategoría: {n.categoria}\nFecha: {n.fecha_creacion}\nEnlaces: {n.enlaces}" for n in notas]

    def eliminar_usuario(self, usuario):
        """
        Elimina un usuario y todas sus notas asociadas de la base de datos.

        :param usuario: El objeto Usuario a eliminar.
        :raises UsuarioNoEncontradoError: Si el usuario no existe.
        """
        if not usuario:
            raise UsuarioNoEncontradoError("Usuario no encontrado.")
        usuario_db = self.session.query(Usuario).filter_by(id_usuario=usuario.id_usuario).first()
        if not usuario_db:
            raise UsuarioNoEncontradoError("Usuario no encontrado.")
        self.session.delete(usuario_db)
        self.session.commit()
