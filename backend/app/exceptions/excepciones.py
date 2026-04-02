class LibroNoEncontradoError(Exception):
    """
    Excepción lanzada cuando un libro no se encuentra en el sistema.
    """

    pass


class UsuarioSuspendidoError(Exception):
    """
    Excepción lanzada cuando un usuario está suspendido y no puede realizar acciones.
    """

    pass


class SinStockError(Exception):
    """
    Excepción lanzada cuando no hay stock disponible de un libro.
    """

    pass


class SinPrestamosDisponiblesError(Exception):
    """
    Excepción lanzada cuando un usuario ya no tiene préstamos disponibles.
    """

    pass
