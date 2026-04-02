from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import (
    routes_autenticacion,
    routes_libro,
    routes_prestamo,
    routes_usuario,
)
from fastapi.middleware.cors import CORSMiddleware

# Inicialización de la aplicación FastAPI
app = FastAPI(title="Sistema de Biblioteca")

# Crear tablas automáticamente a partir de los modelos ORM
Base.metadata.create_all(bind=engine)

# Configuración de CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registrar routers de la aplicación
app.include_router(routes_autenticacion.router)
app.include_router(routes_libro.router)
app.include_router(routes_prestamo.router)
app.include_router(routes_usuario.router)


@app.get("/")
def root() -> dict[str, str]:
    """
    Endpoint raíz de la API.
    """
    return {"message": "API funcionando correctamente"}
