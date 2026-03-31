from pydantic import BaseModel
from datetime import date
from typing import Optional


class PrestamoBase(BaseModel):
    libro_id: int
    usuario_id: int


class PrestamoCreate(PrestamoBase):
    fecha_prestamo: date
    fecha_devolucion: date


class PrestamoUpdate(BaseModel):
    fecha_devolucion: Optional[date]
    estado: Optional[str]


class PrestamoResponse(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    fecha_prestamo: date
    fecha_devolucion: Optional[date]
    estado: str

    class Config:
        from_attributes = True
