from sqlalchemy import Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship


class Libro(Base):
    """
    Modelo ORM que representa un libro en la base de datos.
    """

    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(150), unique=True, nullable=False, index=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(String(150), nullable=False)
    estado = Column(String, default="disponible", nullable=False)
    copias_disponibles = Column(Integer, default=1, nullable=False)

    # Relaciones
    prestamos = relationship("Prestamo", back_populates="libro")
