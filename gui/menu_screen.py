from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from src.model.errores_gestor_notas import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class MenuScreen(Screen):
    """
    Clase que representa la pantalla del menú principal para gestionar notas.
    Permite ver, editar, eliminar y crear notas, así como cerrar sesión.
    """

    def ver_notas(self):
        """
        Muestra un popup con la lista de notas del usuario actual.
        """
        gestor = App.get_running_app().gestor
        usuario_actual = App.get_running_app().usuario_actual
        try:
            notas = gestor.ver_notas(usuario_actual)
            contenido = BoxLayout(orientation='vertical')

            if isinstance(notas, list):
                scrollview = ScrollView(size_hint=(1, 0.8))
                grid = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
                grid.bind(minimum_height=grid.setter('height'))

                for nota in notas:
                    nota_box = BoxLayout(orientation='vertical', padding=10, spacing=5, size_hint_y=None, height=150)
                    nota_box.add_widget(Label(text=f"Título: {nota.titulo}", bold=True, font_size=16, size_hint_y=None, height=30))
                    nota_box.add_widget(Label(text=f"Contenido: {nota.contenido}", size_hint_y=None, height=50))
                    nota_box.add_widget(Label(text=f"Categoría: {nota.categoria}", italic=True, size_hint_y=None, height=20))
                    nota_box.add_widget(Label(text=f"Fecha: {nota.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}", size_hint_y=None, height=20))
                    grid.add_widget(nota_box)

                scrollview.add_widget(grid)
                contenido.add_widget(scrollview)
            else:
                contenido.add_widget(Label(text=notas))

            btn_cerrar = Button(text="Cerrar", size_hint_y=None, height=40)
            btn_cerrar.bind(on_press=lambda x: self.popup.dismiss())
            contenido.add_widget(btn_cerrar)

            self.popup = Popup(title="Notas", content=contenido, size_hint=(0.9, 0.9))
            self.popup.open()
        except UsuarioNoEncontradoError as e:
            self.mostrar_error(str(e))

    def editar_notas(self):
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

        :param instance: Instancia del botón que activó el evento.
        """
        gestor = App.get_running_app().gestor
        usuario_actual = App.get_running_app().usuario_actual
        try:
            indice = int(self.input_indice.text)
            nuevo_titulo = self.input_nuevo_titulo.text
            nuevo_contenido = self.input_nuevo_contenido.text
            nueva_categoria = self.input_nueva_categoria.text
            gestor.editar_nota(usuario_actual, indice, nuevo_titulo, nuevo_contenido, nueva_categoria)
            print("Nota editada exitosamente.")
            self.popup.dismiss()
        except Exception as e:
            self.mostrar_error(str(e))

    def eliminar_notas(self):
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

        :param instance: Instancia del botón que activó el evento.
        """
        gestor = App.get_running_app().gestor
        usuario_actual = App.get_running_app().usuario_actual
        try:
            indice = int(self.input_indice_eliminar.text)
            gestor.eliminar_nota(usuario_actual, indice)
            print("Nota eliminada exitosamente.")
            self.popup.dismiss()
        except Exception as e:
            self.mostrar_error(str(e))

    def crear_nota(self):
        """
        Abre un popup para crear una nueva nota.
        """
        # Crear el formulario para ingresar los datos de la nota
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

        self.popup = Popup(title="Crear Nota", content=contenido, size_hint=(0.8, 0.8))
        self.popup.open()

    def guardar_nota(self, instance):
        """
        Guarda la nota ingresada en el popup.

        :param instance: Instancia del botón que activó el evento.
        """
        gestor = App.get_running_app().gestor
        usuario_actual = App.get_running_app().usuario_actual

        try:
            # Obtener y limpiar los valores de los campos
            titulo = self.input_titulo.text.strip()
            contenido = self.input_contenido.text.strip()
            categoria = self.input_categoria.text.strip()

            # Validar que los campos no estén vacíos
            if not titulo or not contenido or not categoria:
                raise CamposVaciosError("Todos los campos son obligatorios.")

            # Agregar la nota al gestor
            gestor.agregar_nota(usuario_actual, titulo, contenido, categoria)
            print("Nota creada exitosamente.")
            self.popup.dismiss()
        except CamposVaciosError as e:
            self.mostrar_error(str(e))
        except NotaYaExisteError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def cerrar_sesion(self):
        """
        Cambia a la pantalla principal y cierra la sesión del usuario actual.
        """
        self.manager.current = "main"

    def mostrar_error(self, mensaje):
        """
        Muestra un popup con un mensaje de error.

        :param mensaje: Mensaje de error a mostrar.
        """
        # Mostrar un popup con el mensaje de error
        popup = Popup(title="Error", content=Label(text=mensaje), size_hint=(0.8, 0.4))
        popup.open()
