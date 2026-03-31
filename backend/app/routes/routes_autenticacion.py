from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schema_autenticacion import LoginRequest, TokenResponse
from app.services.service_autenticacion import login
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    token = login(db, data.email, data.contrasenia)

    if not token:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {"access_token": token}
