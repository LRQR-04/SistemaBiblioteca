from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.schema_usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.services.service_usuario import (
    registrar_usuario,
    obtener_usuarios,
    actualizar_usuario,
    cambiar_estado_usuario,
)
from app.core.database import get_db
from app.middleware.middleware_roles import require_roles
from app.middleware.middleware_autenticacion import obtener_usuario_actual
from app.models.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", dependencies=[Depends(require_roles("admin"))])
def listar_usuarios(
    search: str = Query("", description="Buscar por nombre o correo"),
    status: str = Query("all", description="Filtrar por estado"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=10),
    db: Session = Depends(get_db),
):
    return obtener_usuarios(db, search, status, page, limit)


@router.post(
    "", dependencies=[Depends(require_roles("admin"))], response_model=UsuarioResponse
)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return registrar_usuario(db, usuario)


@router.put(
    "/{user_id}",
    dependencies=[Depends(require_roles("admin"))],
    response_model=UsuarioResponse,
)
def editar_usuario(
    user_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(obtener_usuario_actual),
):
    return actualizar_usuario(db, user_id, data, current_user)


@router.patch("/{user_id}/estado", dependencies=[Depends(require_roles("admin"))])
def cambiar_estado(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(obtener_usuario_actual),
):
    return cambiar_estado_usuario(db, user_id, current_user)
