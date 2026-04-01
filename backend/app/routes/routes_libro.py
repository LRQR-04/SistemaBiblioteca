from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schema_libro import LibroCreate, LibroResponse
from app.services import service_libro
from app.models.libro import Libro
from app.core.database import get_db
from typing import List
from app.middleware.middleware_roles import require_roles

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.post(
    "/", dependencies=[Depends(require_roles("admin"))], response_model=LibroResponse
)
def crear_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    return service_libro.registrar_libro(db, libro)


@router.get("/", response_model=List[LibroResponse])
def listar_libros(db: Session = Depends(get_db)):
    return db.query(Libro).all()
