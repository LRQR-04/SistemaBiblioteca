from sqlalchemy import Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship


class Usuario(Base):
    """
    Modelo ORM que representa un usuario en la base de datos.
    """

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    contrasenia = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False, default="estudiante")
    prestamos_disponibles = Column(Integer)
    estado = Column(Integer, nullable=False, default=1)

    # Relaciones
    prestamos = relationship("Prestamo", back_populates="usuario")
