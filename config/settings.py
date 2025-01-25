"""Configuración global del monitor de criptomonedas."""
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

DB_PATH = Path('data/precios_historicos.db')

UPDATE_INTERVAL = 60  # segundos
HISTORY_LIMIT = 50   # Aumentado para mejor análisis técnico

RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

SUPPORTED_COINS = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'BNB': 'Binance Coin',
    'SOL': 'Solana',
    'XRP': 'Ripple',
    'USDC': 'USD Coin',
    'ADA': 'Cardano',
    'AVAX': 'Avalanche',
    'DOGE': 'Dogecoin',
    'TRX': 'TRON',
    'LTC': 'Litecoin'
} 