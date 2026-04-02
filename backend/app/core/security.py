from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# Hash de contraseña
def hashear_contrasenia(password: str) -> str:
    """
    Genera el hash de una contraseña utilizando Argon2.
    """
    return pwd_context.hash(password)


def verificar_contrasenia(password: str, hashed: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    """
    return pwd_context.verify(password, hashed)


# Crear token
def crear_token_acceso(data: dict) -> str:
    """
    Crea un token JWT de acceso con expiración definida.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.expiracion_token)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.clave_secreta, algorithm=settings.algoritmo)
