from fastapi import Depends, HTTPException
from app.middleware.middleware_autenticacion import obtener_usuario_actual
from app.models.usuario import Usuario


def require_roles(*roles: str):
    """
    Genera un verificador de roles para proteger rutas.
    """

    def role_checker(user: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
        try:
            """
            Verifica que el usuario tenga uno de los roles permitidos.
            """
            if user.rol not in roles:
                raise HTTPException(status_code=403, detail="No autorizado")

            return user

        except HTTPException:
            raise

        except Exception:
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    return role_checker
