from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Prestamo(Base):
    """
    Modelo ORM que representa un préstamo en la base de datos.
    """

    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    libro_id = Column(
        Integer,
        ForeignKey("libros.id"),
        nullable=False,
    )
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
    )
    fecha_prestamo = Column(Date, nullable=False)
    fecha_devolucion = Column(Date, nullable=False)
    estado = Column(String(100), nullable=False, default="activo")

    # Relaciones
    libro = relationship("Libro", back_populates="prestamos")
    usuario = relationship("Usuario", back_populates="prestamos")
