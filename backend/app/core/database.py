from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Motor de conexión a la base de datos
engine = create_engine(settings.url_bd, connect_args={"check_same_thread": False})

# Sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos ORM
Base = declarative_base()


def get_db():
    """
    Proporciona una sesión de base de datos.

    Genera una sesión de SQLAlchemy que se cierra automáticamente
    al finalizar el uso.

    Yields:
        SessionLocal: Sesión activa de la base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
