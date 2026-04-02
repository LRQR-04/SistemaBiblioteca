from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schema_autenticacion import LoginRequest, TokenResponse
from app.services.service_autenticacion import login
from app.core.database import get_db
from app.schemas.schema_usuario import UsuarioResponse, UsuarioCreate
from app.services.service_usuario import registrar_usuario

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login_user(data: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Inicia sesión de usuario y genera un token JWT.
    """
    token = login(db, data.email, data.contrasenia)

    if not token:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {"access_token": token}


@router.post("/registro", response_model=UsuarioResponse)
def register_user(
    usuario: UsuarioCreate, db: Session = Depends(get_db)
) -> UsuarioResponse:
    """
    Registra un nuevo usuario en el sistema.
    """
    try:
        return registrar_usuario(db, usuario)

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
