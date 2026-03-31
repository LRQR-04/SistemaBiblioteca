from sqlalchemy.orm import Session
from app.models.libro import Libro
from app.schemas.schema_libro import LibroCreate, LibroUpdate


def registrar_libro(db: Session, libro_data: LibroCreate):
    try:
        nuevo_libro = Libro(**libro_data.model_dump())
        db.add(nuevo_libro)
        db.commit()
        db.refresh(nuevo_libro)
        return nuevo_libro
    except Exception as e:
        db.rollback()  # deshace los cambios si ocurre un error
        raise e


def buscar_libro(db: Session, termino: str):
    return (
        db.query(Libro)
        .filter(
            (Libro.titulo.ilike(f"%{termino}%"))
            | (Libro.autor.ilike(f"%{termino}%"))
            | (Libro.isbn == termino)
        )
        .all()
    )


def actualizar_libro(db: Session, libro_id: int, datos: LibroUpdate):
    try:
        libro = db.query(Libro).filter(Libro.id == libro_id).first()

        if not libro:
            return None

        for key, value in datos.model_dump(exclude_unset=True).items():
            setattr(libro, key, value)

        db.commit()
        db.refresh(libro)
        return libro
    except Exception as e:
        db.rollback()
        raise e
