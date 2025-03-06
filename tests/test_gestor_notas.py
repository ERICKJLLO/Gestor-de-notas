import pytest

from src.model.errores_gestor_notas import *
from src.model.gestor_notas import GestorNotas
from src.model.nota import Nota
from src.model.usuario import Usuario

class TestCrearNota:
    def setUp(self):
        self.gestor = GestorNotas()
        self.gestor.registrar_usuario("usuario1", "password1")
        self.usuario = self.gestor.iniciar_sesion("usuario1", "password1")
    
    # Pruebas normales
    def test_crear_nota_normal_1(self):
        self.gestor.agregar_nota(self.usuario, "Titulo", "Contenido", "Trabajo", [])
        self.assertEqual(len(self.usuario.notas), 1)
    
    def test_crear_nota_normal_2(self):
        self.gestor.agregar_nota(self.usuario, "Nota 2", "Texto de prueba", "Personal", [])
        self.assertEqual(self.usuario.notas[0].categoria, "Personal")
    
    def test_crear_nota_normal_3(self):
        self.gestor.agregar_nota(self.usuario, "Tarea", "Matematicas", "General", [])
        self.assertTrue(any(n.titulo == "Tarea" for n in self.usuario.notas))
    
    # Pruebas extremas
    def test_crear_nota_extremo_1(self):
        self.gestor.agregar_nota(self.usuario, "A" * 200, "B" * 500, "C" * 50, [])
        self.assertEqual(len(self.usuario.notas), 1)
    
    def test_crear_nota_extremo_2(self):
        self.gestor.agregar_nota(self.usuario, "", "Contenido sin título", "Trabajo", [])
        self.assertEqual(self.usuario.notas[0].titulo, "")
    
    def test_crear_nota_extremo_3(self):
        self.gestor.agregar_nota(self.usuario, "Nota con caracteres especiales!@#$", "Contenido", "General", [])
        self.assertIn("Nota con caracteres especiales!@#$", [n.titulo for n in self.usuario.notas])
    
    # Pruebas de error
    def test_crear_nota_error_1(self):
        with self.assertRaises(CamposVaciosError):
            self.gestor.agregar_nota(self.usuario, "", "", "", [])
    
    def test_crear_nota_error_2(self):
        with self.assertRaises(NotaYaExisteError):
            self.gestor.agregar_nota(self.usuario, "Trabajo", "Contenido", "Trabajo", [])
            self.gestor.agregar_nota(self.usuario, "Trabajo", "Contenido", "Trabajo", [])
    
    def test_crear_nota_error_3(self):
        with self.assertRaises(CamposVaciosError):
            self.gestor.agregar_nota(None, "Titulo", "Contenido", "Trabajo", [])
class TestEditarNota:
    def setUp(self):
        self.gestor = GestorNotas()
        self.gestor.registrar_usuario("usuario1", "password1")
        self.usuario = self.gestor.iniciar_sesion("usuario1", "password1")
        self.gestor.agregar_nota(self.usuario, "Titulo", "Contenido", "Trabajo", [])
    
    # Pruebas normales
    def test_editar_nota_normal_1(self):
        self.gestor.editar_nota(self.usuario, 0, "Nuevo Titulo", "Nuevo Contenido", "Trabajo")
        self.assertEqual(self.usuario.notas[0].titulo, "Nuevo Titulo")
    
    def test_editar_nota_normal_2(self):
        self.gestor.editar_nota(self.usuario, 0, "Actualización", "Texto actualizado", "Trabajo")
        self.assertEqual(self.usuario.notas[0].contenido, "Texto actualizado")
    
    def test_editar_nota_normal_3(self):
        self.gestor.editar_nota(self.usuario, 0, "Titulo", "Texto", "Importante")
        self.assertEqual(self.usuario.notas[0].categoria, "Importante")
    
    # Pruebas extremas
    def test_editar_nota_extremo_1(self):
        self.gestor.editar_nota(self.usuario, 0, "A" * 200, "B" * 500, "C" * 50)
        self.assertEqual(self.usuario.notas[0].titulo, "A" * 200)
    
    def test_editar_nota_extremo_2(self):
        self.gestor.editar_nota(self.usuario, 0, "", "Contenido sin título", "Trabajo")
        self.assertEqual(self.usuario.notas[0].titulo, "")
    
    def test_editar_nota_extremo_3(self):
        self.gestor.editar_nota(self.usuario, 0, "Nota!@#$", "Contenido especial", "General")
        self.assertIn("Nota!@#$", self.usuario.notas[0].titulo)
    
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
            
class TestEliminarNota:
    def setUp(self):
        self.gestor = GestorNotas()
        self.gestor.registrar_usuario("usuario1", "password1")
        self.usuario = self.gestor.iniciar_sesion("usuario1", "password1")
        self.gestor.agregar_nota(self.usuario, "Titulo", "Contenido", "Trabajo", [])
    
    # Pruebas normales
    def test_eliminar_nota_normal_1(self):
        self.gestor.eliminar_nota(self.usuario, 0)
        self.assertEqual(len(self.usuario.notas), 0)
    
    def test_eliminar_nota_normal_2(self):
        self.gestor.agregar_nota(self.usuario, "Nota 2", "Texto", "Personal", [])
        self.gestor.eliminar_nota(self.usuario, 0)
        self.assertEqual(len(self.usuario.notas), 1)
    
    def test_eliminar_nota_normal_3(self):
        self.gestor.eliminar_nota(self.usuario, 0)
        self.assertEqual(len(self.usuario.notas), -1)
    
    # Pruebas extremas
    def test_eliminar_nota_extremo_1(self):
        for _ in range(100):
            self.gestor.agregar_nota(self.usuario, "Titulo", "Contenido", "General", [])
        for _ in range(50):
            self.gestor.eliminar_nota(self.usuario, 0)
        self.assertEqual(len(self.usuario.notas), 51)
    
    def test_eliminar_nota_extremo_2(self):
        self.gestor.eliminar_nota(self.usuario, 0)
        with self.assertRaises(ValueError):
            self.gestor.eliminar_nota(self.usuario, 0)
    
    def test_eliminar_nota_extremo_3(self):
        with self.assertRaises(ValueError):
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
            otro_usuario = Usuario("usuario2", "password2")
            self.gestor.eliminar_nota(otro_usuario, 0)

            
class TestIniciarSesion:
    def setUp(self):
        self.gestor = GestorNotas()
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
        self.gestor.registrar_usuario("", "password")
        self.assertTrue(self.gestor.iniciar_sesion("", "password"))
    
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
            
class TestCrearCuenta:
    def setUp(self):
        self.gestor = GestorNotas()
    
    # Pruebas normales
    def test_registrar_usuario_normal_1(self):
        self.gestor.registrar_usuario("usuario2", "password2")
        self.assertIn("usuario2", self.gestor.usuarios)
    
    def test_registrar_usuario_normal_2(self):
        self.gestor.registrar_usuario("user123", "securepass")
        self.assertEqual(self.gestor.usuarios["user123"].nombre_usuario, "user123")
    
    def test_registrar_usuario_normal_3(self):
        self.gestor.registrar_usuario("testuser", "1234")
        self.assertTrue(isinstance(self.gestor.usuarios["testuser"], Usuario))
    
    # Pruebas extremas
    def test_registrar_usuario_extremo_1(self):
        self.gestor.registrar_usuario("a" * 100, "b" * 100)
        self.assertIn("a" * 100, self.gestor.usuarios)
    
    def test_registrar_usuario_extremo_2(self):
        self.gestor.registrar_usuario("", "password")
        self.assertIn("", self.gestor.usuarios)
    
    def test_registrar_usuario_extremo_3(self):
        self.gestor.registrar_usuario("user@#$", "pa$$word!")
        self.assertIn("user@#$", self.gestor.usuarios)
    
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

class TestCambiarContrasena:
    def setUp(self):
        self.gestor = GestorNotas()
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
