import unittest

from src.model.errores_gestor_notas import *
from src.model.gestor_notas import GestorNotas, Base, get_engine, get_session, Usuario, Nota

class TestCrearNota(unittest.TestCase):
    def setUp(self):
        engine = get_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.session = get_session(engine)
        self.gestor = GestorNotas(session=self.session)
        self.gestor.registrar_usuario("usuario1", "password1")
        self.usuario = self.gestor.iniciar_sesion("usuario1", "password1")

    # Pruebas normales
    def test_crear_nota_normal_1(self):
        self.gestor.agregar_nota(self.usuario, "Titulo", "Contenido", "Trabajo", [])
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(len(notas), 1)
    
    def test_crear_nota_normal_2(self):
        self.gestor.agregar_nota(self.usuario, "Nota 2", "Texto de prueba", "Personal", [])
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(notas[0].categoria, "Personal")
    
    def test_crear_nota_normal_3(self):
        self.gestor.agregar_nota(self.usuario, "Tarea", "Matematicas", "General", [])
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertTrue(any(n.titulo == "Tarea" for n in notas))
    
    
    # Pruebas extremas
    def test_crear_nota_extremo_1(self):
        self.gestor.agregar_nota(self.usuario, "A" * 200, "B" * 500, "C" * 50, [])
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(len(notas), 1)
    
    def test_crear_nota_extremo_2(self):
        self.gestor.agregar_nota(self.usuario, "", "Contenido sin título", "Trabajo", [])
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(notas[0].titulo, "")
    
    def test_crear_nota_extremo_3(self):
        self.gestor.agregar_nota(self.usuario, "Nota con caracteres especiales!@#$", "Contenido", "General", [])
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertIn("Nota con caracteres especiales!@#$", [n.titulo for n in notas])
    
    
    # Pruebas de error
    def test_crear_nota_error_1(self):
        with self.assertRaises(CamposVaciosError):
            self.gestor.agregar_nota(self.usuario, "", "", "", [])
    
    def test_crear_nota_error_2(self):
        self.gestor.agregar_nota(self.usuario, "Trabajo", "Contenido", "Trabajo", [])
        # Ahora se permiten duplicados, así que no debe lanzar excepción
        self.gestor.agregar_nota(self.usuario, "Trabajo", "Contenido", "Trabajo", [])
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario, titulo="Trabajo").all()
        self.assertEqual(len(notas), 2)
    
    def test_crear_nota_error_3(self):
        with self.assertRaises(CamposVaciosError):
            self.gestor.agregar_nota(None, "Titulo", "Contenido", "Trabajo", [])
            
            
class TestEditarNota(unittest.TestCase):
    def setUp(self):
        engine = get_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.session = get_session(engine)
        self.gestor = GestorNotas(session=self.session)
        self.gestor.registrar_usuario("usuario1", "password1")
        self.usuario = self.gestor.iniciar_sesion("usuario1", "password1")
        self.gestor.agregar_nota(self.usuario, "Titulo", "Contenido", "Trabajo", [])
    
    
    # Pruebas normales
    def test_editar_nota_normal_1(self):
        self.gestor.editar_nota(self.usuario, 0, "Nuevo Titulo", "Nuevo Contenido", "Trabajo")
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(notas[0].titulo, "Nuevo Titulo")
    
    def test_editar_nota_normal_2(self):
        self.gestor.editar_nota(self.usuario, 0, "Actualización", "Texto actualizado", "Trabajo")
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(notas[0].contenido, "Texto actualizado")
    
    def test_editar_nota_normal_3(self):
        self.gestor.editar_nota(self.usuario, 0, "Titulo", "Texto", "Importante")
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(notas[0].categoria, "Importante")
    
    
    # Pruebas extremas
    def test_editar_nota_extremo_1(self):
        self.gestor.editar_nota(self.usuario, 0, "A" * 200, "B" * 500, "C" * 50)
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(notas[0].titulo, "A" * 200)
    
    def test_editar_nota_extremo_2(self):
        self.gestor.editar_nota(self.usuario, 0, "", "Contenido sin título", "Trabajo")
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(notas[0].titulo, "")
    
    def test_editar_nota_extremo_3(self):
        self.gestor.editar_nota(self.usuario, 0, "Nota!@#$", "Contenido especial", "General")
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertIn("Nota!@#$", notas[0].titulo)
    
    
    # Pruebas de error
    def test_editar_nota_error_1(self):
        with self.assertRaises(NotaNoEncontradaError):
            self.gestor.editar_nota(self.usuario, 5, "Nuevo", "Contenido", "Trabajo")
    
    def test_editar_nota_error_2(self):
        with self.assertRaises(EdicionInvalidaError):
            self.gestor.editar_nota(self.usuario, 0, None, None, None)
    
    def test_editar_nota_error_3(self):
        with self.assertRaises(NotaNoEncontradaError):
            self.gestor.editar_nota(None, 0, "Nuevo", "Contenido", "Trabajo")
            
            
class TestEliminarNota(unittest.TestCase):
    def setUp(self):
        engine = get_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.session = get_session(engine)
        self.gestor = GestorNotas(session=self.session)
        self.gestor.registrar_usuario("usuario1", "password1")
        self.usuario = self.gestor.iniciar_sesion("usuario1", "password1")
        self.gestor.agregar_nota(self.usuario, "Titulo", "Contenido", "Trabajo", [])
    
    
    # Pruebas normales
    def test_eliminar_nota_normal_1(self):
        self.gestor.eliminar_nota(self.usuario, 0)
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(len(notas), 0)
    
    def test_eliminar_nota_normal_2(self):
        self.gestor.agregar_nota(self.usuario, "Nota 2", "Texto", "Personal", [])
        self.gestor.eliminar_nota(self.usuario, 0)
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(len(notas), 1)
    
    def test_eliminar_nota_normal_3(self):
        self.gestor.eliminar_nota(self.usuario, 0)
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(len(notas), 0)
    
    
    # Pruebas extremas
    def test_eliminar_nota_extremo_1(self):
        for _ in range(100):
            self.gestor.agregar_nota(self.usuario, "Titulo", "Contenido", "General", [])
        for _ in range(50):
            self.gestor.eliminar_nota(self.usuario, 0)
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(len(notas), 51)
    
    def test_eliminar_nota_extremo_2(self):
        self.gestor.eliminar_nota(self.usuario, 0)
        with self.assertRaises(NotaNoEncontradaError):
            self.gestor.eliminar_nota(self.usuario, 0)
    
    def test_eliminar_nota_extremo_3(self):
        with self.assertRaises(NotaNoEncontradaError):
            self.gestor.eliminar_nota(self.usuario, None)
    
    
    # Pruebas de error
    def test_eliminar_nota_error_1(self):
        with self.assertRaises(NotaNoEncontradaError):
            self.gestor.eliminar_nota(self.usuario, 10)
    
    def test_eliminar_nota_error_2(self):
        with self.assertRaises(EliminacionInvalidaError):
            self.gestor.eliminar_nota(None, 0)
    
    def test_eliminar_nota_error_3(self):
        with self.assertRaises(EliminacionInvalidaError):
            # Crea un usuario de SQLAlchemy, no del modelo antiguo
            otro_usuario = self.session.query(Usuario).filter_by(nombre_usuario="usuario2").first()
            if not otro_usuario:
                self.gestor.registrar_usuario("usuario2", "password2")
                otro_usuario = self.gestor.iniciar_sesion("usuario2", "password2")
            self.gestor.eliminar_nota(otro_usuario, 0)

            
class TestIniciarSesion(unittest.TestCase):
    def setUp(self):
        engine = get_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.session = get_session(engine)
        self.gestor = GestorNotas(session=self.session)
        self.gestor.registrar_usuario("usuario1", "password1")
    
    
    # Pruebas normales
    def test_iniciar_sesion_normal_1(self):
        usuario = self.gestor.iniciar_sesion("usuario1", "password1")
        self.assertEqual(usuario.nombre_usuario, "usuario1")
    
    def test_iniciar_sesion_normal_2(self):
        self.assertIsInstance(self.gestor.iniciar_sesion("usuario1", "password1"), Usuario)
    
    def test_iniciar_sesion_normal_3(self):
        self.assertTrue(self.gestor.iniciar_sesion("usuario1", "password1"))
    
    
    # Pruebas extremas
    def test_iniciar_sesion_extremo_1(self):
        self.gestor.registrar_usuario("a" * 50, "b" * 50)
        self.assertTrue(self.gestor.iniciar_sesion("a" * 50, "b" * 50))
    
    def test_iniciar_sesion_extremo_2(self):
        self.gestor.registrar_usuario("user@#$", "pa$$word!")
        self.assertTrue(self.gestor.iniciar_sesion("user@#$", "pa$$word!"))
    
    def test_iniciar_sesion_extremo_3(self):
        # Ahora se espera que lanzar CamposVaciosError si el nombre de usuario está vacío
        with self.assertRaises(CamposVaciosError):
            self.gestor.registrar_usuario("", "password")
    
    
        # Pruebas de error
    def test_iniciar_sesion_error_1(self):
        with self.assertRaises(CredencialesInvalidasError):
            self.gestor.iniciar_sesion("usuario1", "wrongpassword")
    
    def test_iniciar_sesion_error_2(self):
        with self.assertRaises(UsuarioNoEncontradoError):
            self.gestor.iniciar_sesion("nouser", "password1")
    
    def test_iniciar_sesion_error_3(self):
        with self.assertRaises(CamposVaciosError):
            self.gestor.iniciar_sesion("", "")
            
            
class TestCrearCuenta(unittest.TestCase):
    def setUp(self):
        engine = get_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.session = get_session(engine)
        self.gestor = GestorNotas(session=self.session)
    
    
    # Pruebas normales
    def test_registrar_usuario_normal_1(self):
        self.gestor.registrar_usuario("usuario2", "password2")
        usuario = self.session.query(Usuario).filter_by(nombre_usuario="usuario2").first()
        self.assertIsNotNone(usuario)
    
    def test_registrar_usuario_normal_2(self):
        self.gestor.registrar_usuario("user123", "securepass")
        usuario = self.session.query(Usuario).filter_by(nombre_usuario="user123").first()
        self.assertEqual(usuario.nombre_usuario, "user123")
    
    def test_registrar_usuario_normal_3(self):
        self.gestor.registrar_usuario("testuser", "1234")
        usuario = self.session.query(Usuario).filter_by(nombre_usuario="testuser").first()
        self.assertIsInstance(usuario, Usuario)
    
    
    # Pruebas extremas
    def test_registrar_usuario_extremo_1(self):
        self.gestor.registrar_usuario("a" * 100, "b" * 100)
        usuario = self.session.query(Usuario).filter_by(nombre_usuario="a" * 100).first()
        self.assertIsNotNone(usuario)
    
    def test_registrar_usuario_extremo_2(self):
        with self.assertRaises(CamposVaciosError):
            self.gestor.registrar_usuario("", "password")
    
    def test_registrar_usuario_extremo_3(self):
        self.gestor.registrar_usuario("user@#$", "pa$$word!")
        usuario = self.session.query(Usuario).filter_by(nombre_usuario="user@#$").first()
        self.assertIsNotNone(usuario)
    
    
        # Pruebas de error
    def test_registrar_usuario_error_1(self):
        self.gestor.registrar_usuario("usuario1", "password1")
        with self.assertRaises(UsuarioYaExisteError):
            self.gestor.registrar_usuario("usuario1", "password1")
    
    def test_registrar_usuario_error_2(self):
        with self.assertRaises(CamposVaciosError):
            self.gestor.registrar_usuario("user", "")
    
    def test_registrar_usuario_error_3(self):
        with self.assertRaises(CamposVaciosError):
            self.gestor.registrar_usuario("user", None)


class TestCambiarContrasena(unittest.TestCase):
    def setUp(self):
        engine = get_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.session = get_session(engine)
        self.gestor = GestorNotas(session=self.session)
        self.gestor.registrar_usuario("usuario1", "password1")
        self.usuario = self.gestor.iniciar_sesion("usuario1", "password1")
    
    
    # Pruebas normales
    def test_cambiar_contrasena_normal_1(self):
        self.gestor.cambiar_contraseña(self.usuario, "nueva_password")
        self.assertEqual(self.usuario.contrasena, "nueva_password")
    
    def test_cambiar_contrasena_normal_2(self):
        self.gestor.cambiar_contraseña(self.usuario, "segura123")
        self.assertEqual(self.usuario.contrasena, "segura123")
    
    def test_cambiar_contrasena_normal_3(self):
        self.gestor.cambiar_contraseña(self.usuario, "clave_456")
        self.assertEqual(self.usuario.contrasena, "clave_456")
    
    
    # Pruebas extremas
    def test_cambiar_contrasena_extremo_1(self):
        self.gestor.cambiar_contraseña(self.usuario, "p" * 100)
        self.assertEqual(self.usuario.contrasena, "p" * 100)
    
    def test_cambiar_contrasena_extremo_2(self):
        self.gestor.cambiar_contraseña(self.usuario, "!")
        self.assertEqual(self.usuario.contrasena, "!")
    
    def test_cambiar_contrasena_extremo_3(self):
        self.gestor.cambiar_contraseña(self.usuario, "Pa$$w0rd!@#")
        self.assertEqual(self.usuario.contrasena, "Pa$$w0rd!@#")
    
    
    # Pruebas de error
    def test_cambiar_contrasena_error_1(self):
        with self.assertRaises(ContrasenaInvalidaError):
            self.gestor.cambiar_contraseña(self.usuario, "")

    def test_cambiar_contrasena_error_2(self):
        with self.assertRaises(UsuarioNoEncontradoError):
            self.gestor.cambiar_contraseña(None, "nuevaClave")

    def test_cambiar_contrasena_error_3(self):
        with self.assertRaises(ContrasenaInvalidaError):
            self.gestor.cambiar_contraseña(self.usuario, None)


class TestEliminarUsuario(unittest.TestCase):
    def setUp(self):
        engine = get_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.session = get_session(engine)
        self.gestor = GestorNotas(session=self.session)
        self.gestor.registrar_usuario("usuario1", "password1")
        self.usuario = self.gestor.iniciar_sesion("usuario1", "password1")
        self.gestor.agregar_nota(self.usuario, "Nota1", "Contenido1", "General", [])
        self.gestor.agregar_nota(self.usuario, "Nota2", "Contenido2", "Trabajo", [])

    # Pruebas normales
    def test_eliminar_usuario_normal(self):
        self.gestor.eliminar_usuario(self.usuario)
        usuario_db = self.session.query(Usuario).filter_by(nombre_usuario="usuario1").first()
        self.assertIsNone(usuario_db)
        notas = self.session.query(Nota).filter_by(id_usuario=self.usuario.id_usuario).all()
        self.assertEqual(len(notas), 0)

    # Pruebas de error
    def test_eliminar_usuario_error(self):
        with self.assertRaises(UsuarioNoEncontradoError):
            self.gestor.eliminar_usuario(None)

    def test_eliminar_usuario_no_existente(self):
        self.gestor.eliminar_usuario(self.usuario)
        with self.assertRaises(UsuarioNoEncontradoError):
            self.gestor.eliminar_usuario(self.usuario)

class TestVerNotas(unittest.TestCase):
    def setUp(self):
        engine = get_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.session = get_session(engine)
        self.gestor = GestorNotas(session=self.session)
        self.gestor.registrar_usuario("usuario1", "password1")
        self.usuario = self.gestor.iniciar_sesion("usuario1", "password1")

    # Pruebas normales
    def test_ver_notas_lista(self):
        self.gestor.agregar_nota(self.usuario, "Nota1", "Contenido1", "General", [])
        self.gestor.agregar_nota(self.usuario, "Nota2", "Contenido2", "Trabajo", [])
        resultado = self.gestor.ver_notas(self.usuario)
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(any("Nota1" in n for n in resultado))
        self.assertTrue(any("Nota2" in n for n in resultado))

    # Pruebas extremas
    def test_ver_notas_vacio(self):
        resultado = self.gestor.ver_notas(self.usuario)
        self.assertEqual(resultado, "No hay notas disponibles.")

    # Pruebas de error
    def test_ver_notas_usuario_no_existente(self):
        with self.assertRaises(UsuarioNoEncontradoError):
            self.gestor.ver_notas(None)

class TestNotasPorUsuario(unittest.TestCase):
    def setUp(self):
        engine = get_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.session = get_session(engine)
        self.gestor = GestorNotas(session=self.session)
        self.gestor.registrar_usuario("usuario1", "password1")
        self.gestor.registrar_usuario("usuario2", "password2")
        self.usuario1 = self.gestor.iniciar_sesion("usuario1", "password1")
        self.usuario2 = self.gestor.iniciar_sesion("usuario2", "password2")
        self.gestor.agregar_nota(self.usuario1, "Nota1", "Contenido1", "General", [])
        self.gestor.agregar_nota(self.usuario2, "Nota2", "Contenido2", "Trabajo", [])

    # Pruebas normales
    def test_notas_solo_usuario_actual(self):
        notas1 = self.gestor.ver_notas(self.usuario1)
        notas2 = self.gestor.ver_notas(self.usuario2)
        self.assertTrue(any("Nota1" in n for n in notas1))
        self.assertFalse(any("Nota2" in n for n in notas1))
        self.assertTrue(any("Nota2" in n for n in notas2))
        self.assertFalse(any("Nota1" in n for n in notas2))
