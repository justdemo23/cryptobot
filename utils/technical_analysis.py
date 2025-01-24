"""Análisis técnico y señales de trading."""
import pandas as pd
from typing import Dict, Any
from config.settings import RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL
from utils.logger import logger

def calcular_indicadores(precios: pd.Series) -> Dict[str, float]:
    """Calcula indicadores técnicos principales."""
    # RSI
    delta = precios.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=RSI_PERIOD).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=RSI_PERIOD).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # MACD
    ema_fast = precios.ewm(span=MACD_FAST).mean()
    ema_slow = precios.ewm(span=MACD_SLOW).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=MACD_SIGNAL).mean()
    
    return {
        'rsi': rsi.iloc[-1],
        'macd': macd.iloc[-1],
        'signal': signal.iloc[-1]
    }

def analizar_niveles(precios: pd.Series) -> Dict[str, float]:
    """Identifica niveles de soporte y resistencia."""
    maximo = precios.max()
    minimo = precios.min()
    actual = precios.iloc[-1]
    
    resistencia = maximo * 0.95
    soporte = minimo * 1.05
    
    return {
        'soporte': soporte,
        'resistencia': resistencia,
        'distancia_resistencia': ((resistencia - actual) / actual) * 100,
        'distancia_soporte': ((actual - soporte) / actual) * 100
    }

def analizar_resistencias(df: pd.DataFrame, precio_actual: float) -> Dict:
    """Analiza niveles de soporte y resistencia"""
    try:
        # Cálculo simple de niveles usando máximos y mínimos recientes
        max_reciente = df['high'].tail(20).max()
        min_reciente = df['low'].tail(20).min()
        
        return {
            'proxima_resistencia': max_reciente if max_reciente > precio_actual else None,
            'proximo_soporte': min_reciente if min_reciente < precio_actual else None
        }
    except Exception as e:
        logger.error(f"Error analizando resistencias: {e}")
        return {'proxima_resistencia': None, 'proximo_soporte': None}

def generar_recomendacion(df: pd.DataFrame) -> Dict[str, Any]:
    """Genera recomendaciones completas de trading."""
    if len(df) < 2:
        return {
            'señales': ['Datos insuficientes para análisis'],
            'accion': 'ESPERAR ⏳',
            'confianza': 0
        }
    
    precios = df['price']
    indicadores = calcular_indicadores(precios)
    niveles = analizar_niveles(precios)
    señales = []
    confianza = 0
    
    # Análisis RSI
    if indicadores['rsi'] < 30:
        señales.append(f"RSI en sobreventa ({indicadores['rsi']:.1f})")
        confianza += 2
    elif indicadores['rsi'] > 70:
        señales.append(f"RSI en sobrecompra ({indicadores['rsi']:.1f})")
        confianza -= 2
    
    # Análisis MACD
    if indicadores['macd'] > indicadores['signal']:
        señales.append("MACD positivo")
        confianza += 1
    else:
        señales.append("MACD negativo")
        confianza -= 1
    
    # Análisis de Volatilidad
    volatilidad = precios.std() / precios.mean() * 100
    if volatilidad > 5:
        señales.append(f"Volatilidad alta ({volatilidad:.1f}%)")
    
    # Análisis de niveles
    precio_actual = precios.iloc[-1]
    if precio_actual < niveles['soporte']:
        señales.append("Precio bajo soporte")
        confianza += 2
    elif precio_actual > niveles['resistencia']:
        señales.append("Precio sobre resistencia")
        confianza -= 2
    
    # Determinar acción recomendada
    if confianza >= 3:
        accion = "COMPRAR 🟢"
    elif confianza <= -3:
        accion = "VENDER 🔴"
    else:
        accion = "MANTENER ⏺"
    
    return {
        'señales': señales,
        'accion': accion,
        'confianza': confianza,
        'niveles': niveles,
        'indicadores': indicadores
    } 