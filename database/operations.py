"""Operaciones de la base de datos."""
import pandas as pd
import sqlite3
from utils.logger import logger
from database.connection import get_db_connection

def save_price(timestamp: str, symbol: str, price: float) -> None:
    """Guarda un nuevo precio en la base de datos."""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute('INSERT INTO crypto_precios VALUES (?, ?, ?)',
                     (timestamp, symbol, price))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error al guardar precio para {symbol}: {e}")

def get_price_history(symbol: str, limit: int = 30) -> pd.DataFrame:
    """Obtiene el historial de precios para un símbolo."""
    try:
        with get_db_connection() as conn:
            query = '''SELECT timestamp, price FROM crypto_precios 
                      WHERE symbol = ? ORDER BY timestamp DESC LIMIT ?'''
            return pd.read_sql_query(query, conn, params=(symbol, limit))
    except sqlite3.Error as e:
        logger.error(f"Error al obtener historial para {symbol}: {e}")
        return pd.DataFrame() 