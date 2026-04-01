from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.usuario import Usuario
from app.schemas.schema_usuario import UsuarioCreate
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


def obtener_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(func.lower(Usuario.email) == email.lower()).first()


def verificar_usuario_activo(usuario: Usuario):
    return usuario.estado == "activo"
