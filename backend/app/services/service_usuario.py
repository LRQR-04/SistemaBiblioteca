from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.usuario import Usuario
from app.schemas.schema_usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import hashear_contrasenia


def registrar_usuario(db: Session, user_data: UsuarioCreate):
    try:
        existente = (
            db.query(Usuario)
            .filter(func.lower(Usuario.email) == user_data.email.lower())
            .first()
        )

        if existente:
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
        return nuevo_usuario

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Listar usuarios (paginación + filtros)
def obtener_usuarios(
    db: Session, search: str = "", status: str = "all", page: int = 1, limit: int = 10
):
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

        return {"data": usuarios, "total": total}

    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener usuarios")


# Actualizar datos del usuario
def actualizar_usuario(
    db: Session, user_id: int, data: UsuarioUpdate, current_user: Usuario
):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == user_id).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # El admin no puede editar otros admins
        if usuario.rol == "admin" and usuario.id != current_user.id:
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

        return usuario

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar usuario")


# Cambiar estado del usuario
def cambiar_estado_usuario(db: Session, user_id: int, current_user: Usuario):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == user_id).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # El admin no puede modificar otros admins
        if usuario.rol == "admin" and usuario.id != current_user.id:
            raise HTTPException(
                status_code=403, detail="No se puede modificar otro admin"
            )

        usuario.estado = "suspendido" if usuario.estado == "activo" else "activo"

        db.commit()

        return {"message": "Estado actualizado correctamente"}

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al cambiar estado")


def obtener_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(func.lower(Usuario.email) == email.lower()).first()


def verificar_usuario_activo(usuario: Usuario):
    return usuario.estado == "activo"
