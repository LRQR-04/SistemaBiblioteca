from pydantic import BaseModel
from datetime import date
from typing import Optional


class PrestamoBase(BaseModel):
    usuario: str
    libro: str


class PrestamoCreate(PrestamoBase):
    fecha_prestamo: date
    fecha_devolucion: date


class PrestamoUpdate(BaseModel):
    fecha_devolucion: Optional[date]
    estado: Optional[str]


class PrestamoResponse(BaseModel):
    id: int
    usuario: int
    libro: int
    fecha_prestamo: date
    fecha_devolucion: date
    estado: str

    class Config:
        from_attributes = True
