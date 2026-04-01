from fastapi import Depends, HTTPException
from app.middleware.middleware_autenticacion import obtener_usuario_actual


def require_roles(*roles):
    def role_checker(user=Depends(obtener_usuario_actual)):
        if user.rol not in roles:
            raise HTTPException(status_code=403, detail="No autorizado")
        return user

    return role_checker
