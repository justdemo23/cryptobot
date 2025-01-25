import pandas as pd
import numpy as np
from typing import Dict
from dataclasses import dataclass
from enum import Enum
from crypto_monitor import identificar_tendencia
from utils.technical_analysis import analizar_resistencias

class NivelRiesgo(Enum):
    BAJO = "BAJO"
    MEDIO = "MEDIO"
    ALTO = "ALTO"

@dataclass
class Recomendacion:
    accion: str
    razon: str
    riesgo: NivelRiesgo
    precio_objetivo: float
    stop_loss: float

def generar_recomendacion(
    df: pd.DataFrame,
    precio_actual: float,
    analisis_tendencia: Dict,
    analisis_resistencia: Dict
) -> Recomendacion:
    """
    Genera una recomendación clara basada en el análisis técnico
    """
    hay_tendencia = analisis_tendencia['hay_tendencia']
    direccion_tendencia = analisis_tendencia['direccion']
    proxima_resistencia = analisis_resistencia['proxima_resistencia']
    
    distancia_resistencia = ((proxima_resistencia / precio_actual) - 1) * 100 \
        if proxima_resistencia else 0
    
    if hay_tendencia and direccion_tendencia == 'alcista':
        if distancia_resistencia > 5:
            return Recomendacion(
                accion="COMPRAR",
                razon=f"""
                ✅ Tendencia alcista clara
                📈 Potencial de subida: {distancia_resistencia:.2f}%
                🎯 Próxima resistencia: {proxima_resistencia:.2f}
                """,
                riesgo=NivelRiesgo.MEDIO,
                precio_objetivo=proxima_resistencia,
                stop_loss=precio_actual * 0.95
            )
        else:
            return Recomendacion(
                accion="ESPERAR",
                razon="Cerca de resistencia, esperar retroceso",
                riesgo=NivelRiesgo.ALTO,
                precio_objetivo=None,
                stop_loss=None
            )
    
    return Recomendacion(
        accion="MANTENER",
        razon="No hay señales claras en este momento",
        riesgo=NivelRiesgo.BAJO,
        precio_objetivo=None,
        stop_loss=None
    )

def generar_mensaje_usuario(recomendacion: Recomendacion) -> str:
    """
    Genera un mensaje amigable para el usuario
    """
    mensaje = f"""
    🤖 RECOMENDACIÓN DE TRADING:
    
    📊 Acción Sugerida: {recomendacion.accion}
    
    ⚠️ Nivel de Riesgo: {recomendacion.riesgo.value}
    
    📝 Razón: {recomendacion.razon}
    """
    
    if recomendacion.precio_objetivo:
        mensaje += f"\n    🎯 Precio Objetivo: {recomendacion.precio_objetivo:.2f}"
    
    if recomendacion.stop_loss:
        mensaje += f"\n    🛑 Stop Loss Sugerido: {recomendacion.stop_loss:.2f}"
        
    if recomendacion.accion == "COMPRAR":
        mensaje += f"""
        
        ⚠️ Recuerda:
        • No inviertas más de lo que puedas permitirte perder
        • Siempre usa stop loss
        • Diversifica tus inversiones
        """
    
    return mensaje

def analizar_mercado(df: pd.DataFrame):
    """
    Función principal para analizar el mercado y mostrar recomendaciones
    """
    try:
        precio_actual = df['close'].iloc[-1]
        
        hay_tendencia, direccion = identificar_tendencia(df)
        analisis_resistencia = analizar_resistencias(df, precio_actual)
        
        recomendacion = generar_recomendacion(
            df,
            precio_actual,
            {'hay_tendencia': hay_tendencia, 'direccion': direccion},
            analisis_resistencia
        )
        
        print(generar_mensaje_usuario(recomendacion))
        
    except Exception as e:
        print(f"Error en el análisis: {str(e)}") 