from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


class UsuarioBase(BaseModel):
    """
    Esquema base para representar un usuario.
    """

    nombre: str
    email: EmailStr
    rol: Literal["estudiante", "profesor", "admin"] = "estudiante"
    prestamos_disponibles: int = 0
    estado: Literal["activo", "suspendido"] = "activo"


class UsuarioCreate(UsuarioBase):
    """
    Esquema para la creación de un usuario.
    """

    contrasenia: str


class UsuarioUpdate(BaseModel):
    """
    Esquema para la actualización parcial de un usuario.
    """

    nombre: Optional[str]
    email: Optional[str]
    rol: Optional[str]


class UsuarioResponse(UsuarioBase):
    """
    Esquema de respuesta para representar un usuario.
    """

    id: int

    class Config:
        """
        Configuración para permitir la conversión desde modelos ORM.
        """

        from_attributes = True
