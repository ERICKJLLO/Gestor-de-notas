from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from src.model.errores_gestor_notas import UsuarioNoEncontradoError
from src.model.gestor_notas import GestorNotas

class MenuNotas(BoxLayout):
    """
    Clase que representa el menú de notas, donde el usuario puede agregar, editar, eliminar y ver notas.
    También permite cerrar sesión.
    """
    def __init__(self, **kwargs):
        """
        Inicializa el menú de notas con botones para las diferentes acciones.
        """
        super().__init__(orientation='vertical', **kwargs)
        self.add_widget(Label(text="Menú de Notas", font_size=24, size_hint=(1, 0.2)))

        self.btn_agregar = Button(text="Agregar Nota", size_hint=(1, 0.2))
        self.btn_agregar.bind(on_press=self.agregar_nota)
        self.add_widget(self.btn_agregar)

        self.btn_editar = Button(text="Editar Nota", size_hint=(1, 0.2))
        self.btn_editar.bind(on_press=self.editar_nota)
        self.add_widget(self.btn_editar)

        self.btn_eliminar = Button(text="Eliminar Nota", size_hint=(1, 0.2))
        self.btn_eliminar.bind(on_press=self.eliminar_nota)
        self.add_widget(self.btn_eliminar)

        self.btn_cerrar_sesion = Button(text="Cerrar Sesión", size_hint=(1, 0.2))
        self.btn_cerrar_sesion.bind(on_press=self.cerrar_sesion)
        self.add_widget(self.btn_cerrar_sesion)

        self.btn_ver_notas = Button(text="Ver Notas", size_hint=(1, 0.2))
        self.btn_ver_notas.bind(on_press=self.ver_notas)
        self.add_widget(self.btn_ver_notas)

    def agregar_nota(self, instance):
        """
        Abre un popup para agregar una nueva nota.
        """
        contenido = BoxLayout(orientation='vertical')
        contenido.add_widget(Label(text="Título de la Nota:"))
        self.input_titulo = TextInput(multiline=False)
        contenido.add_widget(self.input_titulo)

        contenido.add_widget(Label(text="Contenido de la Nota:"))
        self.input_contenido = TextInput(multiline=True)
        contenido.add_widget(self.input_contenido)

        contenido.add_widget(Label(text="Categoría:"))
        self.input_categoria = TextInput(multiline=False)
        contenido.add_widget(self.input_categoria)

        btn_guardar = Button(text="Guardar Nota")
        btn_guardar.bind(on_press=self.guardar_nota)
        contenido.add_widget(btn_guardar)

        self.popup = Popup(title="Agregar Nota", content=contenido, size_hint=(0.8, 0.8))
        self.popup.open()

    def guardar_nota(self, instance):
        """
        Guarda la nota ingresada en el popup.
        """
        titulo = self.input_titulo.text
        contenido = self.input_contenido.text
        categoria = self.input_categoria.text
        try:
            app = App.get_running_app()
            app.gestor.agregar_nota(app.usuario_actual, titulo, contenido, categoria)
            print(f"Nota agregada: Título={titulo}, Contenido={contenido}, Categoría={categoria}")
            self.popup.dismiss()
        except Exception as e:
            print(e)

    def editar_nota(self, instance):
        """
        Abre un popup para editar una nota existente.
        """
        contenido = BoxLayout(orientation='vertical')
        contenido.add_widget(Label(text="Índice de la Nota a Editar:"))
        self.input_indice = TextInput(multiline=False)
        contenido.add_widget(self.input_indice)

        contenido.add_widget(Label(text="Nuevo Título:"))
        self.input_nuevo_titulo = TextInput(multiline=False)
        contenido.add_widget(self.input_nuevo_titulo)

        contenido.add_widget(Label(text="Nuevo Contenido:"))
        self.input_nuevo_contenido = TextInput(multiline=True)
        contenido.add_widget(self.input_nuevo_contenido)

        contenido.add_widget(Label(text="Nueva Categoría:"))
        self.input_nueva_categoria = TextInput(multiline=False)
        contenido.add_widget(self.input_nueva_categoria)

        btn_guardar = Button(text="Guardar Cambios")
        btn_guardar.bind(on_press=self.guardar_cambios)
        contenido.add_widget(btn_guardar)

        self.popup = Popup(title="Editar Nota", content=contenido, size_hint=(0.8, 0.8))
        self.popup.open()

    def guardar_cambios(self, instance):
        """
        Guarda los cambios realizados a una nota existente.
        """
        indice = int(self.input_indice.text)
        nuevo_titulo = self.input_nuevo_titulo.text
        nuevo_contenido = self.input_nuevo_contenido.text
        nueva_categoria = self.input_nueva_categoria.text
        try:
            app = App.get_running_app()
            app.gestor.editar_nota(app.usuario_actual, indice, nuevo_titulo, nuevo_contenido, nueva_categoria)
            print(f"Nota editada: Índice={indice}, Nuevo Título={nuevo_titulo}, Nuevo Contenido={nuevo_contenido}, Nueva Categoría={nueva_categoria}")
            self.popup.dismiss()
        except Exception as e:
            print(e)

    def eliminar_nota(self, instance):
        """
        Abre un popup para eliminar una nota existente.
        """
        contenido = BoxLayout(orientation='vertical')
        contenido.add_widget(Label(text="Índice de la Nota a Eliminar:"))
        self.input_indice_eliminar = TextInput(multiline=False)
        contenido.add_widget(self.input_indice_eliminar)

        btn_eliminar = Button(text="Eliminar Nota")
        btn_eliminar.bind(on_press=self.confirmar_eliminar)
        contenido.add_widget(btn_eliminar)

        self.popup = Popup(title="Eliminar Nota", content=contenido, size_hint=(0.8, 0.8))
        self.popup.open()

    def confirmar_eliminar(self, instance):
        """
        Elimina la nota especificada por el índice ingresado.
        """
        try:
            indice = int(self.input_indice_eliminar.text)
            app = App.get_running_app()
            app.gestor.eliminar_nota(app.usuario_actual, indice)
            print(f"Nota eliminada: Índice={indice}")
            self.popup.dismiss()
        except ValueError:
            print("El índice debe ser un número entero.")
        except Exception as e:
            print(e)

    def cerrar_sesion(self, instance):
        """
        Cierra la sesión del usuario actual y regresa a la pantalla de inicio.
        """
        try:
            app = App.get_running_app()
            app.usuario_actual = None
            self.parent.parent.current = "inicio"
            print("Sesión cerrada.")
        except Exception as e:
            print(f"Error al cerrar sesión: {e}")

    def ver_notas(self, instance):
        """
        Muestra un popup con la lista de notas del usuario actual.
        """
        try:
            app = App.get_running_app()
            notas = app.gestor.ver_notas(app.usuario_actual)
            contenido = BoxLayout(orientation='vertical')
            if isinstance(notas, list):
                for nota in notas:
                    contenido.add_widget(Label(text=nota, size_hint_y=None, height=30))
            else:
                contenido.add_widget(Label(text=notas))
            btn_cerrar = Button(text="Cerrar", size_hint_y=None, height=40)
            btn_cerrar.bind(on_press=lambda x: self.popup.dismiss())
            contenido.add_widget(btn_cerrar)
            self.popup = Popup(title="Notas", content=contenido, size_hint=(0.8, 0.8))
            self.popup.open()
        except Exception as e:
            print(e)

class InterfazInicio(BoxLayout):
    """
    Clase que representa la pantalla inicial, donde el usuario puede registrarse, iniciar sesión o salir.
    """
    def __init__(self, **kwargs):
        """
        Inicializa la pantalla inicial con botones para las diferentes acciones.
        """
        super().__init__(orientation='vertical', **kwargs)
        self.add_widget(Label(text="Gestor de Notas", font_size=24, size_hint=(1, 0.2)))

        self.btn_registrar = Button(text="Registrar Usuario", size_hint=(1, 0.2))
        self.btn_registrar.bind(on_press=self.mostrar_registro)
        self.add_widget(self.btn_registrar)

        self.btn_iniciar_sesion = Button(text="Iniciar Sesión", size_hint=(1, 0.2))
        self.btn_iniciar_sesion.bind(on_press=self.mostrar_inicio_sesion)
        self.add_widget(self.btn_iniciar_sesion)

        self.btn_salir = Button(text="Salir", size_hint=(1, 0.2))
        self.btn_salir.bind(on_press=self.salir)
        self.add_widget(self.btn_salir)

    def mostrar_registro(self, instance):
        """
        Abre un popup para registrar un nuevo usuario.
        """
        contenido = BoxLayout(orientation='vertical')
        contenido.add_widget(Label(text="Nombre de Usuario:"))
        self.input_usuario = TextInput(multiline=False)
        contenido.add_widget(self.input_usuario)

        contenido.add_widget(Label(text="Contraseña:"))
        self.input_contrasena = TextInput(multiline=False, password=True)
        contenido.add_widget(self.input_contrasena)

        btn_guardar = Button(text="Registrar")
        btn_guardar.bind(on_press=self.registrar_usuario)
        contenido.add_widget(btn_guardar)

        self.popup = Popup(title="Registrar Usuario", content=contenido, size_hint=(0.8, 0.8))
        self.popup.open()

    def registrar_usuario(self, instance):
        """
        Registra un nuevo usuario con los datos ingresados en el popup.
        """
        usuario = self.input_usuario.text
        contrasena = self.input_contrasena.text
        try:
            app = App.get_running_app()
            app.gestor.registrar_usuario(usuario, contrasena)
            app.usuario_actual = app.gestor.iniciar_sesion(usuario, contrasena)
            print(f"Usuario registrado: {usuario}, Contraseña: {contrasena}")
            self.popup.dismiss()
            self.parent.parent.current = "menu_notas"
        except Exception as e:
            print(e)

    def mostrar_inicio_sesion(self, instance):
        """
        Abre un popup para iniciar sesión con un usuario existente.
        """
        contenido = BoxLayout(orientation='vertical')
        contenido.add_widget(Label(text="Nombre de Usuario:"))
        self.input_usuario_login = TextInput(multiline=False)
        contenido.add_widget(self.input_usuario_login)

        contenido.add_widget(Label(text="Contraseña:"))
        self.input_contrasena_login = TextInput(multiline=False, password=True)
        contenido.add_widget(self.input_contrasena_login)

        btn_iniciar = Button(text="Iniciar Sesión")
        btn_iniciar.bind(on_press=self.iniciar_sesion)
        contenido.add_widget(btn_iniciar)

        self.popup = Popup(title="Iniciar Sesión", content=contenido, size_hint=(0.8, 0.8))
        self.popup.open()

    def iniciar_sesion(self, instance):
        """
        Inicia sesión con los datos ingresados en el popup.
        """
        usuario = self.input_usuario_login.text
        contrasena = self.input_contrasena_login.text
        try:
            app = App.get_running_app()
            app.usuario_actual = app.gestor.iniciar_sesion(usuario, contrasena)
            print(f"Inicio de sesión: {usuario}, Contraseña: {contrasena}")
            self.popup.dismiss()
            self.parent.parent.current = "menu_notas"
        except Exception as e:
            print(e)

    def salir(self, instance):
        """
        Cierra la aplicación.
        """
        App.get_running_app().stop()

class GestorNotasApp(App):
    """
    Clase principal de la aplicación que inicializa el gestor de notas y configura las pantallas.
    """
    def build(self):
        """
        Construye la aplicación configurando el ScreenManager con las pantallas disponibles.
        """
        self.gestor = GestorNotas()
        self.usuario_actual = None
        sm = ScreenManager()

        pantalla_inicio = Screen(name="inicio")
        pantalla_inicio.add_widget(InterfazInicio())
        sm.add_widget(pantalla_inicio)

        pantalla_menu_notas = Screen(name="menu_notas")
        pantalla_menu_notas.add_widget(MenuNotas())
        sm.add_widget(pantalla_menu_notas)

        return sm
