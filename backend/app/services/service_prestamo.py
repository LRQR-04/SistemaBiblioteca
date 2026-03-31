from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.models.prestamo import Prestamo
from app.models.libro import Libro
from app.models.usuario import Usuario
from app.exceptions.excepciones import (
    UsuarioSuspendidoError,
    SinStockError,
    LibroNoEncontradoError,
    SinPrestamosDisponiblesError,
)

DURACION_PRESTAMO = 3  # días


def actualizar_estado_libro(libro: Libro):
    if libro.copias_disponibles <= 0:
        libro.estado = "prestado"
    else:
        libro.estado = "activo"


def realizar_prestamo(db: Session, libro_id: int, usuario_id: int):
    try:
        libro = db.query(Libro).filter(Libro.id == libro_id).with_for_update().first()
        usuario = (
            db.query(Usuario).filter(Usuario.id == usuario_id).with_for_update().first()
        )

        if not usuario or usuario.estado != "activo":
            raise UsuarioSuspendidoError("El usuario no se encuentra activo")

        if usuario.prestamos_disponibles <= 0:
            raise SinPrestamosDisponiblesError("Ya no tienes préstamos disponibles")

        if not libro:
            raise LibroNoEncontradoError("El libro no existe")

        if libro.estado != "disponible":
            raise LibroNoEncontradoError("El libro no está disponible")

        if libro.copias_disponibles <= 0:
            raise SinStockError("No hay copias disponibles")

        # Evitar préstamo duplicado activo
        prestamo_existente = (
            db.query(Prestamo)
            .filter(
                Prestamo.usuario_id == usuario_id,
                Prestamo.libro_id == libro_id,
                Prestamo.estado == "activo",
            )
            .first()
        )

        if prestamo_existente:
            raise Exception("Ya tienes un préstamo correspondiente a este libro")

        # Reducir stock
        libro.copias_disponibles -= 1
        actualizar_estado_libro(libro)

        # Reducir préstamos del usuario
        usuario.prestamos_disponibles -= 1

        prestamo = Prestamo(
            libro_id=libro_id,
            usuario_id=usuario_id,
            fecha_prestamo=date.today(),
            fecha_devolucion=date.today() + timedelta(days=DURACION_PRESTAMO),
            estado="activo",
        )

        db.add(prestamo)
        db.commit()
        db.refresh(prestamo)

        return prestamo
    except Exception as e:
        db.rollback()  # deshace los cambios si ocurre un error
        raise e


def devolver_libro(db: Session, prestamo_id: int):
    try:
        prestamo = (
            db.query(Prestamo)
            .filter(Prestamo.id == prestamo_id)
            .with_for_update()
            .first()
        )

        if not prestamo:
            return None

        if prestamo.estado != "activo":
            raise Exception("El préstamo ya fue procesado")

        libro = (
            db.query(Libro)
            .filter(Libro.id == prestamo.libro_id)
            .with_for_update()
            .first()
        )
        usuario = (
            db.query(Usuario)
            .filter(Usuario.id == prestamo.usuario_id)
            .with_for_update()
            .first()
        )

        if not libro or not usuario:
            raise Exception("Datos inconsistentes en el préstamo")

        # Actualizar datos
        prestamo.estado = (
            "vencido" if date.today() > prestamo.fecha_devolucion else "devuelto"
        )

        libro.estado = "disponible" if libro.copias_disponibles > 0 else "prestado"

        # Actualizar stock
        libro.copias_disponibles += 1
        actualizar_estado_libro(libro)

        # Actualizar préstamos del usuario
        usuario.prestamos_disponibles += 1

        db.commit()
        db.refresh(prestamo)

        return prestamo
    except Exception as e:
        db.rollback()
        raise e
