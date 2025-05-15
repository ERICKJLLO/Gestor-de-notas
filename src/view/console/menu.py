from src.model.gestor_notas import GestorNotas
from src.model.errores_gestor_notas import *

def mostrar_menu():
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Salir")

def mostrar_menu_usuario():
    print("1. Agregar nota")
    print("2. Editar nota")
    print("3. Eliminar nota")
    print("4. Cambiar contraseña")
    print("5. Cerrar sesión")
    print("6. Ver notas")

def consola():
    gestor = GestorNotas()
    usuario_actual = None

    while True:
        if usuario_actual is None:
            mostrar_menu()
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                nombre_usuario = input("Nombre de usuario: ")
                contraseña = input("Contraseña: ")
                try:
                    gestor.registrar_usuario(nombre_usuario, contraseña)
                    print("Usuario registrado exitosamente.")
                except CamposVaciosError as e:
                    print(e)
                except UsuarioYaExisteError as e:
                    print(e)
            elif opcion == "2":
                nombre_usuario = input("Nombre de usuario: ")
                contraseña = input("Contraseña: ")
                try:
                    usuario_actual = gestor.iniciar_sesion(nombre_usuario, contraseña)
                    print("Sesión iniciada exitosamente.")
                except CamposVaciosError as e:
                    print(e)
                except UsuarioNoEncontradoError as e:
                    print(e)
                except CredencialesInvalidasError as e:
                    print(e)
            elif opcion == "3":
                break
            else:
                print("Opción no válida.")
        else:
            mostrar_menu_usuario()
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                titulo = input("Título de la nota: ")
                contenido = input("Contenido de la nota: ")
                categoria = input("Categoría de la nota: ")
                enlaces = input("Enlaces (separados por comas): ").split(",")
                try:
                    gestor.agregar_nota(usuario_actual, titulo, contenido, categoria, enlaces)
                    print("Nota agregada exitosamente.")
                except CamposVaciosError as e:
                    print(e)
                except NotaYaExisteError as e:
                    print(e)
            elif opcion == "2":
                indice = int(input("Índice de la nota a editar: "))
                nuevo_titulo = input("Nuevo título: ")
                nuevo_contenido = input("Nuevo contenido: ")
                nueva_categoria = input("Nueva categoría: ")
                try:
                    gestor.editar_nota(usuario_actual, indice, nuevo_titulo, nuevo_contenido, nueva_categoria)
                    print("Nota editada exitosamente.")
                except NotaNoEncontradaError as e:
                    print(e)
                except EdicionInvalidaError as e:
                    print(e)
            elif opcion == "3":
                indice = int(input("Índice de la nota a eliminar: "))
                try:
                    gestor.eliminar_nota(usuario_actual, indice)
                    print("Nota eliminada exitosamente.")
                except NotaNoEncontradaError as e:
                    print(e)
                except EliminacionInvalidaError as e:
                    print(e)
            elif opcion == "4":
                nueva_contraseña = input("Nueva contraseña: ")
                try:
                    gestor.cambiar_contraseña(usuario_actual, nueva_contraseña)
                    print("Contraseña cambiada exitosamente.")
                except ContrasenaInvalidaError as e:
                    print(e)
            elif opcion == "5":
                usuario_actual = None
                print("Sesión cerrada.")
            elif opcion == "6":
                try:
                    notas = gestor.ver_notas(usuario_actual)
                    if isinstance(notas, list):
                        print("Notas:")
                        for i, nota in enumerate(notas):
                            print(f"{i}. {nota}")
                    else:
                        print(notas)
                except UsuarioNoEncontradoError as e:
                    print(e)
            else:
                print("Opción no válida.")
