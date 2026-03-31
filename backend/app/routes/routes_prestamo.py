from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schema_prestamos import PrestamoCreate, PrestamoResponse
from app.services.service_prestamo import realizar_prestamo, devolver_libro
from app.core.database import get_db
from app.middleware.middleware_autenticacion import obtener_usuario_actual
from app.exceptions.excepciones import UsuarioSuspendidoError, SinStockError

router = APIRouter(prefix="/prestamos", tags=["Prestamos"])


@router.post("/", response_model=PrestamoResponse)
def crear_prestamo(
    data: PrestamoCreate,
    db: Session = Depends(get_db),
    user=Depends(obtener_usuario_actual),
):
    try:
        return realizar_prestamo(db, data.libro_id, data.usuario_id)
    except UsuarioSuspendidoError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SinStockError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/devolver/{prestamo_id}", response_model=PrestamoResponse)
def devolver(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = devolver_libro(db, prestamo_id)

    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    return prestamo


# Listar préstamos
