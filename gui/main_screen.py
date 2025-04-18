from kivy.uix.screenmanager import Screen
from kivy.app import App

class MainScreen(Screen):
    """
    Clase que representa la pantalla principal de la aplicación.
    Permite al usuario registrar una cuenta, iniciar sesión o salir de la aplicación.
    """

    def registrar_usuario(self):
        """
        Cambia a la pantalla de registro de usuario.
        """
        self.manager.current = "register"

    def iniciar_sesion(self):
        """
        Cambia a la pantalla de inicio de sesión.
        """
        self.manager.current = "login"

    def salir(self):
        """
        Cierra la aplicación.
        """
        App.get_running_app().stop()
