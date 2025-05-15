from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from src.model.errores_gestor_notas import CamposVaciosError, UsuarioNoEncontradoError, CredencialesInvalidasError

class GameScreen(Screen):
    """
    Clase que representa la pantalla del juego.
    Permite al usuario volver a la pantalla principal.
    """
    pass

class LoginScreen(Screen):
    """
    Clase que representa la pantalla de inicio de sesión.
    Permite al usuario ingresar un nombre de usuario y contraseña para iniciar sesión.
    """

    def continuar(self):
        """
        Maneja la acción de continuar después de ingresar los datos de inicio de sesión.
        """
        usuario = self.ids.usuario.text.strip()
        contrasena = self.ids.contrasena.text.strip()
        gestor = App.get_running_app().gestor

        try:
            if not usuario or not contrasena:
                raise CamposVaciosError("El nombre de usuario y la contraseña no pueden estar vacíos.")
            usuario_actual = gestor.iniciar_sesion(usuario, contrasena)
            App.get_running_app().usuario_actual = usuario_actual
            print(f"Inicio de sesión: {usuario}")
            self.manager.current = "menu"
        except CamposVaciosError as e:
            self.mostrar_error(str(e))
        except UsuarioNoEncontradoError as e:
            self.mostrar_error(str(e))
        except CredencialesInvalidasError as e:
            self.mostrar_error(str(e))

    def mostrar_error(self, mensaje):
        popup = Popup(title="Error", content=Label(text=mensaje), size_hint=(0.8, 0.4))
        popup.open()
