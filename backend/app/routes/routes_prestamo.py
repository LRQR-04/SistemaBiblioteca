from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.schema_prestamos import (
    PrestamoCreate,
    PrestamoResponse,
    PrestamoUpdate,
)
from app.services.service_prestamo import (
    realizar_prestamo,
    devolver_libro,
    listar_prestamos_usuario,
    actualizar_estado_prestamo,
    listar_prestamos as listar_prestamos_service,
)
from app.core.database import get_db
from app.middleware.middleware_autenticacion import obtener_usuario_actual
from app.middleware.middleware_roles import require_roles


router = APIRouter(prefix="/prestamos", tags=["Prestamos"])


@router.post("/mis", response_model=PrestamoResponse)
def crear_prestamo(
    data: PrestamoCreate,
    db: Session = Depends(get_db),
    user=Depends(obtener_usuario_actual),
) -> PrestamoResponse:
    """
    Crea un nuevo préstamo para el usuario autenticado.
    """
    try:
        return realizar_prestamo(db, data.libro_id, user.id)

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mis")
def mis_prestamos(
    search: str = Query(""),
    status: str = Query("all"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=10),
    db: Session = Depends(get_db),
    user=Depends(obtener_usuario_actual),
):
    """
    Lista los préstamos del usuario autenticado.
    """
    return listar_prestamos_usuario(
        db,
        user.id,
        search,
        status,
        page,
        limit,
    )


@router.get("", dependencies=[Depends(require_roles("admin"))])
def listar_prestamos(
    search: str = Query(""),
    status: str = Query("all"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=10),
    db: Session = Depends(get_db),
):
    """
    Lista todos los préstamos del sistema (solo admin).
    """
    return listar_prestamos_service(
        db,
        search,
        status,
        page,
        limit,
    )


@router.put("/devolver/{prestamo_id}", response_model=PrestamoResponse)
def devolver(
    prestamo_id: int,
    db: Session = Depends(get_db),
    user=Depends(obtener_usuario_actual),
) -> PrestamoResponse:
    """
    Devuelve un libro prestado.
    """
    prestamo = devolver_libro(db, prestamo_id)

    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    return prestamo


@router.patch("/{prestamo_id}", dependencies=[Depends(require_roles("admin"))])
def actualizar_estado(
    prestamo_id: int,
    data: PrestamoUpdate,
    db: Session = Depends(get_db),
) -> PrestamoResponse:
    """
    Actualiza el estado de un préstamo (solo admin).
    """
    return actualizar_estado_prestamo(
        db, prestamo_id, data.estado, data.fecha_devolucion
    )
