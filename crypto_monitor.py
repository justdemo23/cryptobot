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
from typing import Optional
from colorama import init, Fore, Back, Style

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

# Inicializar colorama
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
                    
                    # Cabecera de la moneda
                    print(f"\n{Fore.WHITE}{'=' * 40}")
                    print(f"{Fore.YELLOW}🪙 {name} ({symbol}/USDT)")
                    print(f"{Fore.WHITE}{'=' * 40}")
                    
                    # Precio y variación
                    var_24h = ((price - df['price'].iloc[-1]) / df['price'].iloc[-1]) * 100
                    var_color = Fore.GREEN if var_24h >= 0 else Fore.RED
                    print(f"{Fore.WHITE}💵 Precio: {Fore.GREEN}${price:,.2f} {var_color}({var_24h:+.2f}%)")
                    
                    # Alertas importantes en un cuadro
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
                    
                    # Análisis técnico en formato tabla
                    print(f"\n{Fore.CYAN}📊 ANÁLISIS TÉCNICO:")
                    print(f"{Fore.WHITE}{'─' * 30}")
                    
                    # RSI con zonas
                    rsi = recomendacion['indicadores']['rsi']
                    rsi_color = (Fore.RED if rsi > 70 else 
                                Fore.GREEN if rsi < 30 else 
                                Fore.YELLOW)
                    rsi_zona = ("SOBRECOMPRA" if rsi > 70 else 
                               "SOBREVENTA" if rsi < 30 else 
                               "NEUTRAL")
                    print(f"RSI (14): {rsi_color}{rsi:.1f} - {rsi_zona}")
                    
                    # MACD con señal
                    macd = recomendacion['indicadores']['macd']
                    macd_color = Fore.GREEN if macd > 0 else Fore.RED
                    print(f"MACD: {macd_color}{macd:.8f}")
                    
                    # Niveles clave
                    niveles = recomendacion['niveles']
                    print(f"\n{Fore.CYAN}📈 NIVELES CLAVE:")
                    print(f"{Fore.WHITE}{'─' * 30}")
                    print(f"Soporte: {Fore.GREEN}${niveles['soporte']:,.2f} ({niveles['distancia_soporte']:.1f}%)")
                    print(f"Resistencia: {Fore.RED}${niveles['resistencia']:,.2f} ({niveles['distancia_resistencia']:.1f}%)")
                    
                    # Recomendación final
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

    