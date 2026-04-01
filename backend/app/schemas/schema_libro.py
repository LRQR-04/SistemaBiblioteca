from pydantic import BaseModel, Field
from typing import Optional, Literal


class LibroBase(BaseModel):
    isbn: str = Field(..., min_length=10, max_length=13)
    titulo: str
    autor: str
    estado: Literal["disponible", "prestado", "reparacion"] = "disponible"
    copias_disponibles: int = Field(..., ge=0)


class LibroCreate(LibroBase):
    pass


class LibroUpdate(BaseModel):
    isbn: Optional[str]
    titulo: Optional[str]
    autor: Optional[str]
    estado: Optional[str]
    copias_disponibles: Optional[int]


class LibroResponse(LibroBase):
    id: int

    class Config:
        from_attributes = True
