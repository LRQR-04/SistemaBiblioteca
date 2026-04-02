from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.usuario import Usuario
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Esquema de seguridad OAuth2 para autenticación con tokens JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtiene el usuario actual a partir de un token JWT.
    """
    try:
        logger.info("Validando token de acceso")

        payload = jwt.decode(
            token, settings.clave_secreta, algorithms=[settings.algoritmo]
        )
        user_id = payload.get("user_id")

        if user_id is None:
            logger.warning("Token inválido: no contiene user_id")
            raise HTTPException(status_code=401, detail="Token inválido")

        user = db.query(Usuario).filter(Usuario.id == user_id).first()

        if not user:
            logger.warning(f"Token válido pero usuario no existe: user_id={user_id}")
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        logger.info(
            f"Usuario autenticado correctamente: id={user.id}, email={user.email}"
        )
        return user

    except JWTError:
        logger.warning("Error al decodificar token JWT")
        raise HTTPException(status_code=401, detail="Token inválido")

    except Exception:
        logger.error("Error inesperado en autenticación JWT", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
