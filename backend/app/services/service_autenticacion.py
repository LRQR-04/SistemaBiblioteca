from sqlalchemy.orm import Session
from app.services.service_usuario import obtener_usuario_por_email
from app.core.security import verificar_contrasenia, crear_token_acceso


def login(db: Session, email: str, password: str):
    usuario = obtener_usuario_por_email(db, email)

    if not usuario:
        return None

    if not verificar_contrasenia(password, usuario.password):
        return None

    token = crear_token_acceso({"sub": usuario.email, "user_id": usuario.id})

    return token
