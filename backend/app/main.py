from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import (
    routes_autenticacion,
    routes_libro,
    routes_prestamo,
    routes_usuario,
)


app = FastAPI(title="Sistema de Biblioteca")

# Crear tablas automaticamente
Base.metadata.create_all(bind=engine)

# Registrar rutas
app.include_router(routes_autenticacion.router)
app.include_router(routes_libro.router)
app.include_router(routes_prestamo.router)
app.include_router(routes_usuario.router)


@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
