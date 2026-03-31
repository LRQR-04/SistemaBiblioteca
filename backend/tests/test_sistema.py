import pytest
from app.services.service_libro import registrar_libro
from app.schemas.schema_libro import LibroCreate
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from app.schemas.schema_usuario import UsuarioCreate
from app.models.usuario import Usuario
from app.models.libro import Libro
from app.services.service_prestamo import realizar_prestamo, devolver_libro
from app.exceptions.excepciones import UsuarioSuspendidoError, SinStockError


def test_isbn_duplicado(db):
    libro = LibroCreate(
        isbn="1234567890", titulo="Libro 1", autor="Autor", copias_disponibles=2
    )

    registrar_libro(db, libro)

    with pytest.raises(IntegrityError):
        registrar_libro(db, libro)


def test_email_invalido():
    with pytest.raises(ValidationError):
        UsuarioCreate(
            nombre="Juan",
            email="correo_invalido",
            contrasenia="123456",
            tipo="estudiante",
            prestamos_disponibles=5,
        )


def test_usuario_suspendido_no_presta(db):
    usuario = Usuario(
        nombre="Test",
        email="test@test.com",
        contrasenia="123",
        estado="suspendido",
        prestamos_disponibles=5,
    )
    libro = Libro(isbn="111", titulo="Libro", autor="Autor", copias_disponibles=1)

    db.add(usuario)
    db.add(libro)
    db.commit()

    with pytest.raises(UsuarioSuspendidoError):
        realizar_prestamo(db, libro.id, usuario.id)


def test_sin_stock(db):
    usuario = Usuario(
        nombre="Test",
        email="test2@test.com",
        contrasenia="123",
        estado="activo",
        prestamos_disponibles=5,
    )
    libro = Libro(isbn="222", titulo="Libro", autor="Autor", copias_disponibles=0)

    db.add(usuario)
    db.add(libro)
    db.commit()

    with pytest.raises(SinStockError):
        realizar_prestamo(db, libro.id, usuario.id)


def test_aumenta_stock_devolucion(db):
    usuario = Usuario(
        nombre="Test",
        email="test4@test.com",
        contrasenia="123",
        estado="activo",
        prestamos_disponibles=5,
    )
    libro = Libro(isbn="444", titulo="Libro", autor="Autor", copias_disponibles=1)

    db.add(usuario)
    db.add(libro)
    db.commit()

    prestamo = realizar_prestamo(db, libro.id, usuario.id)

    devolver_libro(db, prestamo.id)

    libro_actualizado = db.query(Libro).filter(Libro.id == libro.id).first()

    assert libro_actualizado.copias_disponibles == 1
