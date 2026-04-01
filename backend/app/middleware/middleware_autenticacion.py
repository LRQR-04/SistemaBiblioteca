from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.clave_secreta, algorithms=[settings.algoritmo]
        )
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = db.query(Usuario).filter(Usuario.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
