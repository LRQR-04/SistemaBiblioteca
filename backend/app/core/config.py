from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    url_bd: str
    clave_secreta: str
    algoritmo: str
    expiracion_token: int

    class Config:
        env_file = ".env"


settings = Settings()
