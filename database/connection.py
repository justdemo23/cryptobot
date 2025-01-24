"""Gestión de conexiones a la base de datos."""
import sqlite3
from pathlib import Path
from utils.logger import logger
from config.settings import DB_PATH

def ensure_db_directory():
    """Asegura que existe el directorio para la base de datos."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_db_connection():
    """Retorna una conexión a la base de datos."""
    ensure_db_directory()
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        raise

def init_db():
    """Inicializa la estructura de la base de datos."""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS crypto_precios
                        (timestamp TEXT, symbol TEXT, price REAL)''')
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise 