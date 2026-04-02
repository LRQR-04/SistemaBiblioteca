from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.service_usuario import obtener_usuario_por_email
from app.core.security import verificar_contrasenia, crear_token_acceso


def login(db: Session, email: str, password: str) -> str:
    """
    Autentica a un usuario y genera un token JWT.
    """
    usuario = obtener_usuario_por_email(db, email)

    if not usuario:
        raise HTTPException(status_code=401, detail="El usuario no esta registrado")

    if usuario.estado != "activo":
        raise HTTPException(status_code=403, detail="Su cuenta se encuentra inactiva")

    if not verificar_contrasenia(password, usuario.contrasenia):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token_acceso(
        {"sub": usuario.email, "user_id": usuario.id, "rol": usuario.rol}
    )
    return token
