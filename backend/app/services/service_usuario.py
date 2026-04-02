from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.usuario import Usuario
from app.schemas.schema_usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import hashear_contrasenia
from app.utils.logger import get_logger

logger = get_logger(__name__)


def registrar_usuario(db: Session, user_data: UsuarioCreate) -> Usuario:
    """
    Registra un nuevo usuario en la base de datos.
    """
    try:
        logger.info(f"Intento de registro de usuario: {user_data.email}")

        existente = (
            db.query(Usuario)
            .filter(func.lower(Usuario.email) == user_data.email.lower())
            .first()
        )

        if existente:
            logger.warning(f"Registro fallido: email duplicado -> {user_data.email}")
            raise HTTPException(status_code=401, detail="El correo ya está registrado")

        hashed_password = hashear_contrasenia(user_data.contrasenia)

        if user_data.rol == "estudiante":
            prestamos_disponibles = 5
        elif user_data.rol == "profesor":
            prestamos_disponibles = 10
        else:
            prestamos_disponibles = 0

        nuevo_usuario = Usuario(
            nombre=user_data.nombre,
            email=user_data.email,
            contrasenia=hashed_password,
            rol=user_data.rol,
            prestamos_disponibles=prestamos_disponibles,
            estado="activo",
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        logger.info(
            f"Usuario registrado correctamente: ID={nuevo_usuario.id}, email={nuevo_usuario.email}"
        )
        return nuevo_usuario

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        logger.error("Error inesperado al registrar usuario", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Listar usuarios (paginación + filtros)
def obtener_usuarios(
    db: Session, search: str = "", status: str = "all", page: int = 1, limit: int = 10
) -> dict:
    """
    Obtiene una lista de usuarios con filtros y paginación.
    """
    try:
        query = db.query(Usuario)

        # Búsqueda por nombre o email
        if search:
            query = query.filter(
                or_(
                    func.lower(Usuario.nombre).like(f"%{search.lower()}%"),
                    func.lower(Usuario.email).like(f"%{search.lower()}%"),
                )
            )

        # Filtro por estado
        if status != "all":
            query = query.filter(Usuario.estado == status)

        total = query.count()

        usuarios = (
            query.order_by(Usuario.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        logger.info(f"Usuarios encontrados: {total}")
        return {"data": usuarios, "total": total}

    except Exception:
        logger.error("Error al obtener usuarios", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al obtener usuarios")


# Actualizar datos del usuario
def actualizar_usuario(
    db: Session, user_id: int, data: UsuarioUpdate, current_user: Usuario
) -> Usuario:
    """
    Actualiza los datos de un usuario existente.
    """
    try:
        logger.info(f"Intento de actualización usuario ID={user_id}")

        usuario = db.query(Usuario).filter(Usuario.id == user_id).first()

        if not usuario:
            logger.warning(f"Usuario no encontrado ID={user_id}")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # El admin no puede editar otros admins
        if usuario.rol == "admin" and usuario.id != current_user.id:
            logger.warning(f"Intento de editar otro admin | usuario_id={user_id}")
            raise HTTPException(
                status_code=403, detail="No es posible editar otro admin"
            )

        # validar email único si se modifica
        if data.email and data.email != usuario.email:
            existente = (
                db.query(Usuario)
                .filter(func.lower(Usuario.email) == data.email.lower())
                .first()
            )
            if existente:
                logger.warning(f"Email duplicado en actualización -> {data.email}")
                raise HTTPException(
                    status_code=400, detail="El correo ya está registrado"
                )

            usuario.email = data.email

        if data.nombre:
            usuario.nombre = data.nombre

        if data.rol:
            usuario.rol = data.rol

        db.commit()
        db.refresh(usuario)

        logger.info(f"Usuario actualizado correctamente ID={usuario.id}")
        return usuario

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        logger.error("Error al actualizar usuario", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al actualizar usuario")


# Cambiar estado del usuario
def cambiar_estado_usuario(db: Session, user_id: int, current_user: Usuario) -> dict:
    """
    Cambia el estado de un usuario (activo/suspendido).
    """
    try:
        logger.info(f"Cambio de estado usuario ID={user_id}")

        usuario = db.query(Usuario).filter(Usuario.id == user_id).first()

        if not usuario:
            logger.warning(f"Usuario no encontrado ID={user_id}")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # El admin no puede modificar otros admins
        if usuario.rol == "admin" and usuario.id != current_user.id:
            logger.warning(f"Intento de modificar otro admin | usuario_id={user_id}")
            raise HTTPException(
                status_code=403, detail="No se puede modificar otro admin"
            )

        usuario.estado = "suspendido" if usuario.estado == "activo" else "activo"

        db.commit()

        logger.info(
            f"Estado actualizado correctamente ID={usuario.id} -> {usuario.estado}"
        )
        return {"message": "Estado actualizado correctamente"}

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        logger.error("Error al cambiar estado de usuario", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al cambiar estado")


def obtener_usuario_por_email(db: Session, email: str) -> Usuario | None:
    """
    Obtiene un usuario por su correo electrónico.
    """
    return db.query(Usuario).filter(func.lower(Usuario.email) == email.lower()).first()


def verificar_usuario_activo(usuario: Usuario) -> bool:
    """
    Verifica si un usuario está activo.
    """
    return usuario.estado == "activo"
