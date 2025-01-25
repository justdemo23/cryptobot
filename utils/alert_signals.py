"""Sistema de alertas visuales para trading manual."""
from typing import Dict, Any
from colorama import Fore

def generar_alerta_precio(precio_actual: float, niveles: Dict[str, float]) -> str:
    """Genera alertas cuando el precio se acerca a niveles clave."""
    alertas = []
    
    dist_soporte = ((precio_actual - niveles['soporte']) / precio_actual) * 100
    if abs(dist_soporte) < 1.0:  # Precio cerca del soporte (1%)
        alertas.append(f"{Fore.RED}⚠️ PRECIO CERCA DEL SOPORTE")
    
    dist_resistencia = ((niveles['resistencia'] - precio_actual) / precio_actual) * 100
    if abs(dist_resistencia) < 1.0:  # Precio cerca de la resistencia (1%)
        alertas.append(f"{Fore.RED}⚠️ PRECIO CERCA DE LA RESISTENCIA")
    
    return "\n".join(alertas) if alertas else ""

def analizar_momentum(indicadores: Dict[str, float]) -> str:
    """Analiza el momentum y genera alertas."""
    alertas = []
    
    if indicadores['rsi'] < 30:
        alertas.append(f"{Fore.GREEN}🔥 RSI EN SOBREVENTA - Posible rebote alcista")
    elif indicadores['rsi'] > 70:
        alertas.append(f"{Fore.RED}💫 RSI EN SOBRECOMPRA - Posible corrección")
    
    if abs(indicadores['macd']) > indicadores['signal'] * 1.5:
        direccion = "ALCISTA" if indicadores['macd'] > 0 else "BAJISTA"
        alertas.append(f"{Fore.YELLOW}⚡ SEÑAL MACD {direccion} FUERTE")
    
    return "\n".join(alertas) if alertas else ""

def generar_alerta_tendencia(df, recomendacion: Dict[str, Any]) -> str:
    """Genera alertas de cambio de tendencia."""
    alertas = []
    confianza = recomendacion['confianza']
    
    if abs(confianza) >= 4:  # Alta confianza
        if confianza > 0:
            alertas.append(f"{Fore.GREEN}🚀 SEÑAL ALCISTA FUERTE - Considerar compra")
        else:
            alertas.append(f"{Fore.RED}🔻 SEÑAL BAJISTA FUERTE - Considerar venta")
    
    return "\n".join(alertas) if alertas else "" 