from fastapi import HTTPException
import pytest
from app.services.service_libro import registrar_libro, listar_libros, actualizar_libro
from app.schemas.schema_libro import LibroCreate, LibroUpdate
from pydantic import ValidationError
from app.schemas.schema_usuario import UsuarioCreate
from app.models.usuario import Usuario
from app.models.libro import Libro
from app.services.service_prestamo import (
    realizar_prestamo,
    devolver_libro,
    listar_prestamos_usuario,
    actualizar_estado_prestamo,
)
from app.exceptions.excepciones import UsuarioSuspendidoError, SinStockError


def test_isbn_duplicado(db):
    libro = LibroCreate(
        isbn="572394813657", titulo="Libro 22", autor="Autor", copias_disponibles=2
    )

    registrar_libro(db, libro)

    with pytest.raises(HTTPException):
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

    devolver_libro(db, prestamo["id"])

    libro_actualizado = db.query(Libro).filter(Libro.id == libro.id).first()

    assert libro_actualizado.copias_disponibles == 1


def test_devolver_libro_inexistente(db):
    with pytest.raises(HTTPException):
        devolver_libro(db, prestamo_id=9999)


def test_listar_prestamos_usuario_filtrado(db):
    usuario = Usuario(
        nombre="Listar",
        email="list@test.com",
        contrasenia="123",
        estado="activo",
        prestamos_disponibles=1,
    )
    libro = Libro(
        isbn="1010", titulo="Python Básico", autor="Autor", copias_disponibles=1
    )
    db.add(usuario)
    db.add(libro)
    db.commit()
    realizar_prestamo(db, libro.id, usuario.id)
    result = listar_prestamos_usuario(
        db, usuario.id, search="python", status="activo", page=1, limit=10
    )
    assert result["total"] == 1
    assert result["data"][0]["libro"] == "Python Básico"


def test_actualizar_estado_devuelto_exitoso(db):
    usuario = Usuario(
        nombre="Dev",
        email="dev@test.com",
        contrasenia="123",
        estado="activo",
        prestamos_disponibles=1,
    )
    libro = Libro(isbn="3030", titulo="LibroDev", autor="Autor", copias_disponibles=1)
    db.add(usuario)
    db.add(libro)
    db.commit()
    prestamo = realizar_prestamo(db, libro.id, usuario.id)
    result = actualizar_estado_prestamo(db, prestamo["id"], estado="devuelto")
    assert result["estado"] == "devuelto"
    libro_actualizado = db.query(Libro).filter(Libro.id == libro.id).first()
    assert libro_actualizado.copias_disponibles == 1


def test_listar_libros_por_titulo(db):
    libro1 = Libro(
        isbn="111",
        titulo="Python Básico",
        autor="Autor",
        estado="disponible",
        copias_disponibles=1,
    )
    libro2 = Libro(
        isbn="222",
        titulo="Java Avanzado",
        autor="Autor",
        estado="disponible",
        copias_disponibles=1,
    )
    db.add_all([libro1, libro2])
    db.commit()
    result = listar_libros(db, search="python", status="all", page=1, limit=10)
    assert result["total"] == 1
    assert result["data"][0].titulo == "Python Básico"


def test_actualizar_libro_inexistente(db):
    datos = LibroUpdate(
        isbn="1234",
        titulo="No existe",
        autor="No existe",
        estado="disponible",
        copias_disponibles=3,
    )

    with pytest.raises(HTTPException):
        actualizar_libro(db, libro_id=9999, datos=datos)
