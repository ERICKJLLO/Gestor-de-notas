import pytest

from src.model.gestor_notas import GestorNotas
from src.model.nota import Nota
from src.model.usuario import Usuario

class TestGestorNotas:
    def setUp(self):
        self.gestor = GestorNotas()
        self.gestor.registrar_usuario("usuario1", "password1")
        self.usuario = self.gestor.iniciar_sesion("usuario1", "password1")
    
    # Crear una nota
    def test_crear_nota_normal_1(self):
        self.gestor.agregar_nota(self.usuario, "Titulo1", "Contenido1", "Trabajo", [])
        self.assertEqual(len(self.usuario.notas), 1)
    
    def test_crear_nota_extremo_1(self):
        self.gestor.agregar_nota(self.usuario, "A" * 200, "B" * 500, "C" * 50, [])
        self.assertEqual(len(self.usuario.notas), 1)
    
    def test_crear_nota_error_1(self):
        with self.assertRaises(ValueError):
            self.gestor.agregar_nota(self.usuario, "", "", "", [])

    # Editar una nota
    def test_editar_nota_normal_1(self):
        nota = self.gestor.agregar_nota(self.usuario, "Titulo1", "Contenido1", "Trabajo", [])
        self.gestor.editar_nota(nota, "Nuevo Titulo", "Nuevo Contenido")
        self.assertEqual(nota.titulo, "Nuevo Titulo")
    
    def test_editar_nota_extremo_1(self):
        nota = self.gestor.agregar_nota(self.usuario, "Titulo1", "Contenido1", "Trabajo", [])
        self.gestor.editar_nota(nota, "A" * 200, "B" * 500)
        self.assertEqual(nota.titulo, "A" * 200)
    
    def test_editar_nota_error_1(self):
        with self.assertRaises(ValueError):
            self.gestor.editar_nota(None, "Nuevo Titulo", "Nuevo Contenido")
    
    # Eliminar una nota
    def test_eliminar_nota_normal_1(self):
        nota = self.gestor.agregar_nota(self.usuario, "Titulo1", "Contenido1", "Trabajo", [])
        self.gestor.eliminar_nota(nota)
        self.assertEqual(len(self.usuario.notas), 0)
    
    def test_eliminar_nota_extremo_1(self):
        nota = self.gestor.agregar_nota(self.usuario, "A" * 200, "B" * 500, "C" * 50, [])
        self.gestor.eliminar_nota(nota)
        self.assertEqual(len(self.usuario.notas), 0)
    
    def test_eliminar_nota_error_1(self):
        with self.assertRaises(ValueError):
            self.gestor.eliminar_nota(None)
    
    # Iniciar sesión
    def test_iniciar_sesion_normal_1(self):
        usuario = self.gestor.iniciar_sesion("usuario1", "password1")
        self.assertEqual(usuario.nombre_usuario, "usuario1")
    
    def test_iniciar_sesion_extremo_1(self):
        self.gestor.registrar_usuario("a" * 50, "b" * 50)
        self.assertTrue(self.gestor.iniciar_sesion("a" * 50, "b" * 50))
    
    def test_iniciar_sesion_error_1(self):
        with self.assertRaises(ValueError):
            self.gestor.iniciar_sesion("usuario1", "wrongpassword")
    
    # Crear cuenta
    def test_registrar_usuario_normal_1(self):
        self.gestor.registrar_usuario("usuario2", "password2")
        self.assertIn("usuario2", self.gestor.usuarios)
    
    def test_registrar_usuario_extremo_1(self):
        self.gestor.registrar_usuario("a" * 100, "b" * 100)
        self.assertIn("a" * 100, self.gestor.usuarios)
    
    def test_registrar_usuario_error_1(self):
        with self.assertRaises(ValueError):
            self.gestor.registrar_usuario("usuario1", "password1")
    
    # Cambiar contraseña
    def test_cambiar_contraseña_normal_1(self):
        self.gestor.cambiar_contraseña(self.usuario, "nueva_password")
        self.assertEqual(self.usuario.contraseña, "nueva_password")
    
    def test_cambiar_contraseña_extremo_1(self):
        self.gestor.cambiar_contraseña(self.usuario, "p" * 100)
        self.assertEqual(self.usuario.contraseña, "p" * 100)
    
    def test_cambiar_contraseña_error_1(self):
        with self.assertRaises(ValueError):
            self.gestor.cambiar_contraseña(self.usuario, "")
    