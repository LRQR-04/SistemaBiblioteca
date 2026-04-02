from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from datetime import date, timedelta
from fastapi import HTTPException

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


def actualizar_estado_libro(libro: Libro) -> None:
    """
    Actualiza el estado de un libro según sus copias disponibles..
    """
    libro.estado = "disponible" if libro.copias_disponibles > 0 else "prestado"


def map_prestamo_response(p: Prestamo) -> dict:
    """
    Mapea un objeto Prestamo a un diccionario de respuesta.
    """
    return {
        "id": p.id,
        "usuario": p.usuario.email,
        "libro": p.libro.titulo,
        "fecha_prestamo": p.fecha_prestamo,
        "fecha_devolucion": p.fecha_devolucion,
        "estado": p.estado,
    }


def realizar_prestamo(db: Session, libro_id: int, usuario_id: int) -> dict:
    """
    Realiza un préstamo de un libro para un usuario.
    """
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
                Prestamo.estado.in_(["activo", "vencido"]),
            )
            .first()
        )

        if prestamo_existente:
            raise HTTPException(
                status_code=400, detail="Ya existe un préstamo de este libro"
            )

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

        return map_prestamo_response(prestamo)
    except Exception as e:
        db.rollback()  # deshace los cambios si ocurre un error
        raise e


def devolver_libro(db: Session, prestamo_id: int) -> dict:
    """
    Devuelve un libro prestado y actualiza el estado del préstamo.
    """
    try:
        prestamo = (
            db.query(Prestamo)
            .filter(Prestamo.id == prestamo_id)
            .with_for_update()
            .first()
        )

        if not prestamo:
            raise HTTPException(status_code=404, detail="Préstamo no encontrado")

        if prestamo.estado == "devuelto":
            raise HTTPException(status_code=400, detail="El préstamo ya fue devuelto")

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
            raise HTTPException(status_code=500, detail="Los datos son inconsistentes")

        # Actualizar datos
        prestamo.estado = "devuelto"

        # Actualizar stock
        libro.copias_disponibles += 1
        actualizar_estado_libro(libro)

        # Actualizar préstamos del usuario
        usuario.prestamos_disponibles += 1

        db.commit()
        db.refresh(prestamo)

        return map_prestamo_response(prestamo)

    except Exception as e:
        db.rollback()
        raise e


def listar_prestamos_usuario(
    db: Session, usuario_id: int, search: str, status: str, page: int, limit: int
) -> dict:
    """
    Lista los préstamos de un usuario con filtros y paginación.
    """
    try:
        query = db.query(Prestamo).join(Libro).filter(Prestamo.usuario_id == usuario_id)

        if search:
            query = query.filter(func.lower(Libro.titulo).like(f"%{search.lower()}%"))

        if status != "all":
            query = query.filter(Prestamo.estado == status)

        total = query.count()

        prestamos = (
            query.order_by(Prestamo.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "data": [
                {
                    "id": p.id,
                    "libro": p.libro.titulo,
                    "estado": p.estado,
                    "fecha_prestamo": p.fecha_prestamo,
                    "fecha_devolucion": p.fecha_devolucion,
                }
                for p in prestamos
            ],
            "total": total,
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Error al listar préstamos")


def listar_prestamos(
    db: Session, search: str, status: str, page: int, limit: int
) -> dict:
    """
    Lista todos los préstamos del sistema con filtros y paginación.
    """
    try:
        query = db.query(Prestamo).options(
            joinedload(Prestamo.usuario), joinedload(Prestamo.libro)
        )

        if search:
            query = (
                query.join(Usuario)
                .join(Libro)
                .filter(
                    or_(
                        func.lower(Usuario.email).like(f"%{search.lower()}%"),
                        func.lower(Libro.titulo).like(f"%{search.lower()}%"),
                    )
                )
            )

        if status != "all":
            query = query.filter(Prestamo.estado == status)

        total = query.count()

        prestamos = (
            query.order_by(Prestamo.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "data": [map_prestamo_response(p) for p in prestamos],
            "total": total,
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Error al listar préstamos")


def actualizar_estado_prestamo(
    db: Session, prestamo_id: int, estado: str, fecha_devolucion=None
) -> dict:
    """
    Actualiza el estado de un préstamo existente.
    """
    try:
        prestamo = (
            db.query(Prestamo)
            .options(joinedload(Prestamo.usuario), joinedload(Prestamo.libro))
            .filter(Prestamo.id == prestamo_id)
            .with_for_update()
            .first()
        )

        if not prestamo:
            raise HTTPException(status_code=404, detail="Préstamo no encontrado")

        estados_validos = ["activo", "devuelto", "vencido"]

        if estado and estado not in estados_validos:
            raise HTTPException(status_code=400, detail="Estado inválido")

        # Validar fecha
        if fecha_devolucion:
            if fecha_devolucion <= prestamo.fecha_prestamo:
                raise HTTPException(
                    status_code=400,
                    detail="La fecha de devolución debe ser mayor a la fecha de préstamo",
                )

            prestamo.fecha_devolucion = fecha_devolucion

        # Cambio de estado
        if estado and estado != prestamo.estado:

            # Solo si estaba activo
            if prestamo.estado != "activo":
                raise HTTPException(
                    status_code=400,
                    detail="El préstamo ya fue procesado",
                )

            # Devolución
            if estado == "devuelto":
                libro = prestamo.libro
                usuario = prestamo.usuario

                # Actualizar stock
                libro.copias_disponibles += 1
                actualizar_estado_libro(libro)

                # Devolver préstamo al usuario
                usuario.prestamos_disponibles += 1

            prestamo.estado = estado

        db.commit()
        db.refresh(prestamo)

        return {
            "id": prestamo.id,
            "usuario": prestamo.usuario.email,
            "libro": prestamo.libro.titulo,
            "fecha_prestamo": prestamo.fecha_prestamo,
            "fecha_devolucion": prestamo.fecha_devolucion,
            "estado": prestamo.estado,
        }

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar estado")
