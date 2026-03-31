from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.schema_usuario import UsuarioCreate
from app.core.security import hashear_contrasenia


def registrar_usuario(db: Session, user_data: UsuarioCreate):
    try:
        hashed_password = hashear_contrasenia(user_data.contrasenia)

        if user_data.tipo == "estudiante":
            prestamos_disponibles = 5
        elif user_data.tipo == "profesor":
            prestamos_disponibles = 10
        else:
            prestamos_disponibles = 0

        nuevo_usuario = Usuario(
            nombre=user_data.nombre,
            email=user_data.email,
            contrasenia=hashed_password,
            rol=user_data.tipo,
            prestamos_disponibles=prestamos_disponibles,
            estado="activo",
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    except Exception as e:
        db.rollback()
        raise e


def obtener_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def verificar_usuario_activo(usuario: Usuario):
    return usuario.estado == "activo"
