from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: Literal["estudiante", "profesor", "admin"] = "estudiante"
    prestamos_disponibles: int = 0
    estado: Literal["activo", "suspendido"] = "activo"


class UsuarioCreate(UsuarioBase):
    contrasenia: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str]
    email: Optional[str]
    rol: Optional[str]


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
