from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.service_usuario import obtener_usuario_por_email
from app.core.security import verificar_contrasenia, crear_token_acceso
from app.utils.logger import get_logger

logger = get_logger(__name__)


def login(db: Session, email: str, password: str) -> str:
    """
    Autentica a un usuario y genera un token JWT.
    """
    logger.info(f"Intento de login para: {email}")
    usuario = obtener_usuario_por_email(db, email)

    if not usuario:
        logger.warning(f"Usuario no registrado: {email}")
        raise HTTPException(status_code=401, detail="El usuario no esta registrado")

    if usuario.estado != "activo":
        logger.warning(f"Usuario inactivo: {email}")
        raise HTTPException(status_code=403, detail="Su cuenta se encuentra inactiva")

    if not verificar_contrasenia(password, usuario.contrasenia):
        logger.warning(f"Contraseña incorrecta: {email}")
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token_acceso(
        {"sub": usuario.email, "user_id": usuario.id, "rol": usuario.rol}
    )

    logger.info(f"Login exitoso: {email}")
    return token
