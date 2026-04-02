import logging
import os

# Crear carpeta logs si no existe
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "errors.log")


# Configuración global
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


# Función para obtener logger por módulo
def get_logger(nombre: str):
    return logging.getLogger(nombre)
