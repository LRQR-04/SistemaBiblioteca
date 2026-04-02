from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.schema_libro import LibroCreate, LibroResponse, LibroUpdate
from app.services import service_libro
from app.core.database import get_db
from app.middleware.middleware_roles import require_roles

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.post(
    "", response_model=LibroResponse, dependencies=[Depends(require_roles("admin"))]
)
def crear_libro(libro: LibroCreate, db: Session = Depends(get_db)) -> LibroResponse:
    """
    Crea un nuevo libro en el sistema.
    """
    return service_libro.registrar_libro(db, libro)


@router.get("")
def listar_libros(
    search: str = Query("", description="Buscar por nombre o autor"),
    status: str = Query("all", description="Filtrar por estado"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=10),
    db: Session = Depends(get_db),
):
    """
    Lista los libros disponibles en el sistema con filtros opcionales.
    """
    return service_libro.listar_libros(db, search, status, page, limit)


@router.put(
    "/{libro_id}",
    response_model=LibroResponse,
    dependencies=[Depends(require_roles("admin"))],
)
def actualizar_libro(
    libro_id: int, datos: LibroUpdate, db: Session = Depends(get_db)
) -> LibroResponse:
    """
    Actualiza la información de un libro existente.
    """
    return service_libro.actualizar_libro(db, libro_id, datos)
