from fastapi import Depends, HTTPException
from app.middleware.middleware_autenticacion import obtener_usuario_actual
from app.models.usuario import Usuario
from app.utils.logger import get_logger

logger = get_logger(__name__)


def require_roles(*roles: str):
    """
    Genera un verificador de roles para proteger rutas.
    """

    def role_checker(user: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
        try:
            logger.info(
                f"Verificando acceso para usuario: {user.email} con rol: {user.rol}"
            )
            """
            Verifica que el usuario tenga uno de los roles permitidos.
            """
            if user.rol not in roles:
                logger.warning(
                    f"Acceso denegado para usuario: {user.email} | Rol: {user.rol} | Roles requeridos: {roles}"
                )
                raise HTTPException(status_code=403, detail="No autorizado")

            logger.info(f"Acceso permitido para usuario: {user.email}")
            return user

        except HTTPException:
            raise

        except Exception:
            logger.error("Error inesperado en verificación de roles", exc_info=True)
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    return role_checker
