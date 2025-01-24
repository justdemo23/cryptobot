"""Análisis de tendencias de precios."""
import pandas as pd
from typing import Dict, Any

def analyze_trend(df: pd.DataFrame) -> Dict[str, Any]:
    """Analiza la tendencia de precios y retorna estadísticas."""
    if len(df) < 2:
        return {"status": "Insuficientes datos", "cambio": 0.0, "tendencia": "→"}

    ultimo_precio = df['price'].iloc[0]
    precio_anterior = df['price'].iloc[-1]
    cambio_porcentual = ((ultimo_precio - precio_anterior) / precio_anterior) * 100

    if cambio_porcentual > 1:
        tendencia = "ALZA SIGNIFICATIVA 📈"
    elif cambio_porcentual > 0:
        tendencia = "Ligera alza ↗"
    elif cambio_porcentual < -1:
        tendencia = "BAJA SIGNIFICATIVA 📉"
    elif cambio_porcentual < 0:
        tendencia = "Ligera baja ↘"
    else:
        tendencia = "Estable →"

    return {
        "status": tendencia,
        "cambio": cambio_porcentual,
        "ultimo_precio": ultimo_precio,
        "precio_anterior": precio_anterior
    } 