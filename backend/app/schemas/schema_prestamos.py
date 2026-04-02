from pydantic import BaseModel
from datetime import date
from typing import Optional


class PrestamoCreate(BaseModel):
    libro_id: int


class PrestamoUpdate(BaseModel):
    estado: Optional[str] = None
    fecha_devolucion: Optional[date] = None


class PrestamoResponse(BaseModel):
    id: int
    usuario: str
    libro: str
    fecha_prestamo: date
    fecha_devolucion: date
    estado: str

    class Config:
        from_attributes = True
