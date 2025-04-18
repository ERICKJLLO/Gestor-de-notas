from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from gui.main_screen import MainScreen
from gui.config_screen import RegisterScreen
from gui.game_screen import LoginScreen
from gui.menu_screen import MenuScreen
from src.model.gestor_notas import GestorNotas

class GestorNotasApp(App):
    """
    Clase principal de la aplicación que inicializa el gestor de notas y configura las pantallas.
    """

    def __init__(self, **kwargs):
        """
        Inicializa la aplicación y configura el gestor de notas y el usuario actual.
        """
        super().__init__(**kwargs)
        self.gestor = GestorNotas()
        self.usuario_actual = None

    def build(self):
        """
        Construye la aplicación cargando los archivos .kv y configurando el ScreenManager.
        """
        # Cargar manualmente los archivos .kv
        Builder.load_file("gui/kv/main_screen.kv")
        Builder.load_file("gui/kv/config_screen.kv")
        Builder.load_file("gui/kv/game_screen.kv")
        Builder.load_file("gui/kv/menu_screen.kv")

        # Configurar el ScreenManager
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MenuScreen(name="menu"))
        return sm

if __name__ == "__main__":
    GestorNotasApp().run()
