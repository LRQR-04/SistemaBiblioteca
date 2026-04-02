from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from fastapi import HTTPException
from app.models.libro import Libro
from app.schemas.schema_libro import LibroCreate, LibroUpdate
from app.utils.logger import get_logger

logger = get_logger(__name__)


def registrar_libro(db: Session, libro_data: LibroCreate) -> Libro:
    """
    Registra un nuevo libro en la base de datos.
    """
    try:
        logger.info(f"Intentando registrar libro con ISBN: {libro_data.isbn}")

        # Validar ISBN único
        existente = (
            db.query(Libro)
            .filter(func.lower(Libro.isbn) == libro_data.isbn.lower())
            .first()
        )

        if existente:
            logger.warning(f"Registro fallido: ISBN duplicado -> {libro_data.isbn}")
            raise HTTPException(status_code=400, detail="El ISBN ya está registrado")

        nuevo_libro = Libro(**libro_data.model_dump())
        db.add(nuevo_libro)
        db.commit()
        db.refresh(nuevo_libro)

        logger.info(
            f"Libro registrado correctamente: ID={nuevo_libro.id}, ISBN={nuevo_libro.isbn}"
        )
        return nuevo_libro

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        logger.error("Error inesperado al registrar libro", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al registrar libro")


# Listar (Búsqueda + filtro + paginación)
def listar_libros(db: Session, search: str, status: str, page: int, limit: int) -> dict:
    """
    Lista libros con búsqueda, filtro por estado y paginación.
    """
    try:
        query = db.query(Libro)

        # Búsqueda (nombre + autor)
        if search:
            query = query.filter(
                or_(
                    func.lower(Libro.titulo).like(f"%{search.lower()}%"),
                    func.lower(Libro.autor).like(f"%{search.lower()}%"),
                )
            )

        # Filtro por estado
        if status != "all":
            query = query.filter(Libro.estado == status)

        total = query.count()

        libros = (
            query.order_by(Libro.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        logger.info(f"Libros encontrados: {total}")

        return {"data": libros, "total": total}

    except Exception:
        logger.error("Error inesperado al listar libros", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al listar libros")


def actualizar_libro(db: Session, libro_id: int, datos: LibroUpdate) -> Libro:
    """
    Actualiza la información de un libro existente.
    """
    try:
        logger.info(f"Intentando actualizar libro ID={libro_id}")
        libro = db.query(Libro).filter(Libro.id == libro_id).first()

        if not libro:
            logger.warning(f"Actualización fallida: libro no encontrado ID={libro_id}")
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        if datos.isbn:
            existente = (
                db.query(Libro)
                .filter(
                    func.lower(Libro.isbn) == datos.isbn.lower(), Libro.id != libro_id
                )
                .first()
            )

            if existente:
                logger.warning(f"Actualización fallida: ISBN duplicado -> {datos.isbn}")
                raise HTTPException(
                    status_code=400, detail="El ISBN ya está registrado"
                )

        for key, value in datos.model_dump(exclude_unset=True).items():
            setattr(libro, key, value)

        db.commit()
        db.refresh(libro)

        logger.info(f"Libro actualizado correctamente: ID={libro.id}")
        return libro

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        logger.error("Error inesperado al actualizar libro", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al actualizar libro")
