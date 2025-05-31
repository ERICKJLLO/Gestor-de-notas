from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importa tu controlador web (debes crearlo en src/controller/web_controlador.py)
from src.controller.web_controlador import WebControlador

if __name__ == "__main__":
    app = FastAPI()
    web_controlador = WebControlador()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(web_controlador.router)
    # Sirve los archivos estáticos de la carpeta src/view/web
    app.mount("/", StaticFiles(directory="src/view/web", html=True), name="static")
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
