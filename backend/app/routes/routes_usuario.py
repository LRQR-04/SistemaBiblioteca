from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schema_usuario import UsuarioCreate, UsuarioResponse
from app.services.service_usuario import registrar_usuario
from app.core.database import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return registrar_usuario(db, usuario)


# Listar usuarios
