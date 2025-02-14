"""
Crypto Price Monitor
-------------------
Un bot que monitorea los precios de las principales criptomonedas y analiza sus tendencias.
"""

import os
import time
from datetime import datetime
from threading import Lock
from binance.client import Client
from typing import Optional, Tuple
from colorama import init, Fore, Back, Style
import pandas as pd
import numpy as np

from config.settings import (
    API_KEY, API_SECRET, UPDATE_INTERVAL,
    HISTORY_LIMIT, SUPPORTED_COINS
)
from utils.logger import logger
from database.connection import init_db
from database.operations import save_price, get_price_history
from utils.technical_analysis import generar_recomendacion
from utils.alert_signals import (
    generar_alerta_precio,
    analizar_momentum,
    generar_alerta_tendencia
)

init(autoreset=True)

print_lock = Lock()
client = Client(API_KEY, API_SECRET)

def clear_console():
    """Limpia la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_price(symbol: str) -> Optional[float]:
    """Obtiene el precio actual de una criptomoneda."""
    try:
        ticker = client.get_symbol_ticker(symbol=symbol+"USDT")
        return float(ticker['price'])
    except Exception as e:
        logger.error(f"Error al obtener precio de {symbol}: {e}")
        return None

def mostrar_banner():
    """Muestra el banner inicial del programa."""
    print(Fore.CYAN + """
    ╔═══════════════════════════════════════════════════════════════╗
    ║""" + Fore.YELLOW + """                                                               """ + Fore.CYAN + """║
    ║""" + Fore.GREEN + """   🚀 CRYPTO MONITOR v2.0                                     """ + Fore.CYAN + """║
    ║""" + Fore.WHITE + """   Monitor de Criptomonedas y Análisis Técnico                """ + Fore.CYAN + """║
    ║""" + Fore.YELLOW + """                                                               """ + Fore.CYAN + """║
    ║""" + Fore.WHITE + """   Desarrollado por NightmaresDev                            """ + Fore.CYAN + """║
    ║""" + Fore.WHITE + """   © 2024 - Todos los derechos reservados                    """ + Fore.CYAN + """║
    ║""" + Fore.YELLOW + """                                                               """ + Fore.CYAN + """║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

def update_prices() -> None:
    """Actualiza y muestra los precios con alertas."""
    with print_lock:
        clear_console()
        mostrar_banner()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(Fore.CYAN + "=" * 80)
        print(Fore.CYAN + f"📊 ANÁLISIS DE MERCADO CRYPTO - {Fore.YELLOW}{timestamp}")
        print(Fore.CYAN + "=" * 80)

        for symbol, name in SUPPORTED_COINS.items():
            try:
                price = get_current_price(symbol)
                if price:
                    save_price(timestamp, symbol, price)
                    df = get_price_history(symbol, HISTORY_LIMIT)
                    recomendacion = generar_recomendacion(df)
                    
                    print(f"\n{Fore.WHITE}{'=' * 40}")
                    print(f"{Fore.YELLOW}🪙 {name} ({symbol}/USDT)")
                    print(f"{Fore.WHITE}{'=' * 40}")
                    
                    var_24h = ((price - df['price'].iloc[-1]) / df['price'].iloc[-1]) * 100
                    var_color = Fore.GREEN if var_24h >= 0 else Fore.RED
                    print(f"{Fore.WHITE}💵 Precio: {Fore.GREEN}${price:,.2f} {var_color}({var_24h:+.2f}%)")
                    
                    alertas_precio = generar_alerta_precio(price, recomendacion['niveles'])
                    alertas_momentum = analizar_momentum(recomendacion['indicadores'])
                    alertas_tendencia = generar_alerta_tendencia(df, recomendacion)
                    
                    if alertas_precio or alertas_momentum or alertas_tendencia:
                        print(f"\n{Fore.YELLOW}📢 ALERTAS CRÍTICAS:")
                        print(f"{Fore.WHITE}{'─' * 30}")
                        if alertas_precio:
                            print(alertas_precio)
                        if alertas_momentum:
                            print(alertas_momentum)
                        if alertas_tendencia:
                            print(alertas_tendencia)
                    
                    print(f"\n{Fore.CYAN}📊 ANÁLISIS TÉCNICO:")
                    print(f"{Fore.WHITE}{'─' * 30}")
                    
                    rsi = recomendacion['indicadores']['rsi']
                    rsi_color = (Fore.RED if rsi > 70 else 
                                Fore.GREEN if rsi < 30 else 
                                Fore.YELLOW)
                    rsi_zona = ("SOBRECOMPRA" if rsi > 70 else 
                               "SOBREVENTA" if rsi < 30 else 
                               "NEUTRAL")
                    print(f"RSI (14): {rsi_color}{rsi:.1f} - {rsi_zona}")
                    
                    macd = recomendacion['indicadores']['macd']
                    macd_color = Fore.GREEN if macd > 0 else Fore.RED
                    print(f"MACD: {macd_color}{macd:.8f}")
                    
                    niveles = recomendacion['niveles']
                    print(f"\n{Fore.CYAN}📈 NIVELES CLAVE:")
                    print(f"{Fore.WHITE}{'─' * 30}")
                    print(f"Soporte: {Fore.GREEN}${niveles['soporte']:,.2f} ({niveles['distancia_soporte']:.1f}%)")
                    print(f"Resistencia: {Fore.RED}${niveles['resistencia']:,.2f} ({niveles['distancia_resistencia']:.1f}%)")
                    
                    print(f"\n{Fore.WHITE}🎯 RECOMENDACIÓN FINAL:")
                    print(f"{Fore.WHITE}{'─' * 30}")
                    accion_color = (Fore.GREEN if recomendacion['accion'] == 'COMPRAR' else 
                                  Fore.RED if recomendacion['accion'] == 'VENDER' else 
                                  Fore.YELLOW)
                    print(f"Acción: {accion_color}{recomendacion['accion']}")
                    print(f"Confianza: {accion_color}{abs(recomendacion['confianza'])}/5")

            except Exception as e:
                logger.error(f"Error en el análisis de {symbol}: {e}")
                print(f"{Fore.RED}❌ Error al analizar {symbol}: {str(e)}")

        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.YELLOW}Próxima actualización en {UPDATE_INTERVAL} segundos...")

def identificar_tendencia(df: pd.DataFrame, 
                         periodo_ema: int = 20,
                         periodo_atr: int = 14,
                         umbral_tendencia: float = 0.02) -> Tuple[bool, str]:
    """
    Identifica si hay una tendencia clara en el mercado
    
    Args:
        df: DataFrame con datos OHLCV
        periodo_ema: Período para la media móvil exponencial
        periodo_atr: Período para el ATR
        umbral_tendencia: Umbral mínimo de pendiente para considerar tendencia
    
    Returns:
        Tuple[bool, str]: (hay_tendencia, dirección)
    """
    
    df['EMA'] = df['close'].ewm(span=periodo_ema, adjust=False).mean()
    
    df['TR'] = np.maximum(
        df['high'] - df['low'],
        np.maximum(
            abs(df['high'] - df['close'].shift(1)),
            abs(df['low'] - df['close'].shift(1))
        )
    )
    df['ATR'] = df['TR'].rolling(window=periodo_atr).mean()
    
    pendiente = (df['EMA'].iloc[-1] - df['EMA'].iloc[-5]) / 5
    pendiente_normalizada = pendiente / df['close'].iloc[-1]
    
    volatilidad = df['ATR'].iloc[-1] / df['close'].iloc[-1]
    
    hay_tendencia = abs(pendiente_normalizada) > umbral_tendencia and \
                    volatilidad < umbral_tendencia * 2
    
    direccion = 'alcista' if pendiente_normalizada > 0 else 'bajista'
    
    return hay_tendencia, direccion

def ejecutar_estrategia(df: pd.DataFrame) -> bool:
    """
    Ejecuta la estrategia solo si hay una tendencia clara
    """
    hay_tendencia, direccion = identificar_tendencia(df)
    
    if not hay_tendencia:
        print("No hay tendencia clara. Esperando mejor momento.")
        return False
    
    print(f"Tendencia {direccion} detectada. Procediendo con la estrategia.")
    return True

def main():
    """Función principal."""
    try:
        init_db()
        logger.info("Iniciando monitor de criptomonedas...")
        
        while True:
            try:
                update_prices()
                time.sleep(UPDATE_INTERVAL)
            except Exception as e:
                logger.error(f"Error en el ciclo de monitoreo: {e}")
                time.sleep(10)

    except KeyboardInterrupt:
        clear_console()
        logger.info("Deteniendo el monitor de criptomonedas...")
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        raise

if __name__ == "__main__":
    main() 

    