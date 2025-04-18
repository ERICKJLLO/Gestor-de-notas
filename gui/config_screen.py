from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from src.model.errores_gestor_notas import CamposVaciosError, UsuarioYaExisteError

class ConfigScreen(Screen):
    """
    Clase que representa la pantalla de configuración de la aplicación.
    Permite al usuario volver a la pantalla principal.
    """
    pass

class RegisterScreen(Screen):
    """
    Clase que representa la pantalla de registro de usuario.
    Permite al usuario ingresar un nombre de usuario y contraseña para registrarse.
    """

    def continuar(self):
        """
        Maneja la acción de continuar después de ingresar los datos de registro.
        """
        usuario = self.ids.usuario.text.strip()
        contrasena = self.ids.contrasena.text.strip()
        gestor = App.get_running_app().gestor

        try:
            if not usuario or not contrasena:
                raise CamposVaciosError("El nombre de usuario y la contraseña no pueden estar vacíos.")
            gestor.registrar_usuario(usuario, contrasena)
            print(f"Usuario registrado: {usuario}")
            self.manager.current = "menu"
        except CamposVaciosError as e:
            self.mostrar_error(str(e))
        except UsuarioYaExisteError as e:
            self.mostrar_error(str(e))

    def mostrar_error(self, mensaje):
        """
        Muestra un popup de error con el mensaje proporcionado.
        """
        popup = Popup(title="Error", content=Label(text=mensaje), size_hint=(0.8, 0.4))
        popup.open()
