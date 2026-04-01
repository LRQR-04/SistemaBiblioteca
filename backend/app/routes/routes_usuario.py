from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schema_usuario import UsuarioCreate, UsuarioResponse
from app.services.service_usuario import registrar_usuario
from app.core.database import get_db
from app.middleware.middleware_roles import require_roles
from app.models.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# @router.post(
#     "", dependencies=[Depends(require_roles("admin"))], response_model=UsuarioResponse
# )
# def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
#     return registrar_usuario(db, usuario)


@router.get("", dependencies=[Depends(require_roles("admin"))])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()
