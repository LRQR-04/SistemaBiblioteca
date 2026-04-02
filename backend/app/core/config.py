from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración principal de la aplicación.

    Contiene parámetros de conexión y seguridad
    obtenidos desde variables de entorno.
    """

    url_bd: str
    clave_secreta: str
    algoritmo: str
    expiracion_token: int

    class Config:
        """
        Configuración interna de Pydantic.

        Define el archivo de entorno desde el cual
        se cargarán las variables.
        """

        env_file = ".env"


settings = Settings()
