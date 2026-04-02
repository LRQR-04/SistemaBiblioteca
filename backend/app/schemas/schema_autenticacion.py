from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """
    Esquema para la solicitud de inicio de sesión.
    """

    email: EmailStr
    contrasenia: str


class TokenResponse(BaseModel):
    """
    Esquema de respuesta con el token de acceso.
    """

    access_token: str
    token_type: str = "bearer"
