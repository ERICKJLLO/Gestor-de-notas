from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.model.gestor_notas import GestorNotas
from src.model.errores_gestor_notas import *

router = APIRouter()
gestor = GestorNotas()

@router.post("/register")
async def register(data: dict):
    try:
        gestor.registrar_usuario(data["usuario"], data["contrasena"])
        return {"mensaje": "Usuario registrado exitosamente."}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@router.post("/login")
async def login(data: dict):
    try:
        usuario = gestor.iniciar_sesion(data["usuario"], data["contrasena"])
        return {"mensaje": "Inicio de sesión exitoso.", "usuario": usuario.nombre_usuario}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@router.post("/nota")
async def crear_nota(data: dict):
    try:
        usuario = gestor.iniciar_sesion(data["usuario"], data["contrasena"])
        gestor.agregar_nota(usuario, data["titulo"], data["contenido"], data["categoria"], data.get("enlaces", []))
        return {"mensaje": "Nota creada exitosamente."}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@router.put("/nota/{indice}")
async def editar_nota(indice: int, data: dict):
    try:
        usuario = gestor.iniciar_sesion(data["usuario"], data["contrasena"])
        gestor.editar_nota(usuario, indice, data["titulo"], data["contenido"], data["categoria"])
        return {"mensaje": "Nota editada exitosamente."}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@router.delete("/nota/{indice}")
async def eliminar_nota(indice: int, data: dict):
    try:
        usuario = gestor.iniciar_sesion(data["usuario"], data["contrasena"])
        gestor.eliminar_nota(usuario, indice)
        return {"mensaje": "Nota eliminada exitosamente."}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@router.post("/notas")
async def ver_notas(data: dict):
    try:
        usuario = gestor.iniciar_sesion(data["usuario"], data["contrasena"])
        notas = gestor.ver_notas(usuario)
        return {"notas": notas}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@router.put("/usuario/password")
async def cambiar_contrasena(data: dict):
    try:
        usuario = gestor.iniciar_sesion(data["usuario"], data["contrasena"])
        gestor.cambiar_contraseña(usuario, data["nueva_contrasena"])
        return {"mensaje": "Contraseña cambiada exitosamente."}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@router.delete("/usuario")
async def eliminar_usuario(data: dict):
    try:
        usuario = gestor.iniciar_sesion(data["usuario"], data["contrasena"])
        gestor.eliminar_usuario(usuario)
        return {"mensaje": "Usuario y notas eliminados."}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

class WebControlador:
    def __init__(self):
        self.router = router
