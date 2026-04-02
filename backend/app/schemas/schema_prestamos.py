from pydantic import BaseModel
from datetime import date
from typing import Optional


class PrestamoCreate(BaseModel):
    """
    Esquema para la creación de un préstamo.
    """

    libro_id: int


class PrestamoUpdate(BaseModel):
    """
    Esquema para la actualización parcial de un préstamo.
    """

    estado: Optional[str] = None
    fecha_devolucion: Optional[date] = None


class PrestamoResponse(BaseModel):
    """
    Esquema de respuesta para representar un préstamo.
    """

    id: int
    usuario: str
    libro: str
    fecha_prestamo: date
    fecha_devolucion: date
    estado: str

    class Config:
        """
        Configuración para permitir la conversión desde modelos ORM.
        """

        from_attributes = True
