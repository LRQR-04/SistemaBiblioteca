from pydantic import BaseModel, Field
from typing import Optional, Literal


class LibroBase(BaseModel):
    """
    Esquema base para representar un libro.
    """

    isbn: str = Field(..., min_length=10, max_length=13)
    titulo: str
    autor: str
    estado: Literal["disponible", "prestado", "reparacion"] = "disponible"
    copias_disponibles: int = Field(..., ge=0)


class LibroCreate(LibroBase):
    """
    Esquema para la creación de un libro.
    """

    pass


class LibroUpdate(BaseModel):
    """
    Esquema para la actualización parcial de un libro.
    """

    isbn: Optional[str]
    titulo: Optional[str]
    autor: Optional[str]
    estado: Optional[str]
    copias_disponibles: Optional[int]


class LibroResponse(LibroBase):
    """
    Esquema de respuesta para un libro.
    """

    id: int

    class Config:
        """
        Configuración para permitir la conversión desde modelos ORM.
        """

        from_attributes = True
