"""Configuración del sistema de logging."""
import logging
from pathlib import Path

def setup_logger():
    """Configura y retorna el logger global."""
    # Asegurar que existe el directorio de logs
    Path('logs').mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/crypto_monitor.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger() 