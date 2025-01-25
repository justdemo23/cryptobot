# Documentación Técnica - Crypto Monitor v2.0

## 1. Requisitos del Sistema

### 1.1 Software Necesario
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### 1.2 Dependencias Python

pip install python-binance==1.0.16
pip install pandas==1.5.3
pip install colorama==0.4.6
pip install python-dotenv==1.0.0


## 2. Estructura del Proyecto

crypto-monitor/
├── config/
│   └── settings.py         # usa: python-dotenv
├── utils/
│   ├── technical_analysis.py  # usa: pandas, numpy
│   ├── alert_signals.py    # usa: colorama
│   ├── trend_analyzer.py   # usa: pandas, numpy
│   ├── trading_signals.py  # usa: pandas
│   └── logger.py          # usa: logging
├── crypto_monitor.py      # usa: python-binance, colorama
└── recomendaciones.py     # usa: pandas

## 3. Configuración Inicial

### 3.1 Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
env
BINANCE_API_KEY=tu_api_key_aqui
BINANCE_API_SECRET=tu_api_secret_aqui


### 3.2 Base de Datos
La aplicación usa SQLite3. La base de datos se creará automáticamente en:

## 4. Ejecución del Proyecto

### 4.1 Preparación
1. Clonar/descargar el proyecto
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar `.env` con tus credenciales de Binance

### 4.2 Iniciar la Aplicación



## 5. Componentes Principales

### 5.1 Análisis Técnico
- RSI (Relative Strength Index)
  - Período: 14
  - Zonas: <30 (sobreventa), >70 (sobrecompra)

- MACD
  - EMA Rápida: 12 períodos
  - EMA Lenta: 26 períodos
  - Señal: 9 períodos

### 5.2 Sistema de Alertas
- Alertas de precio (±1% de S/R)
- Alertas de momentum (RSI + MACD)
- Alertas de tendencia
- Sistema de confianza (1-5)

## 6. Archivos Principales

### 6.1 crypto_monitor.py
- Archivo principal
- Gestiona la interfaz de usuario
- Coordina todos los componentes

### 6.2 technical_analysis.py
- Cálculo de indicadores técnicos
- Análisis de tendencias
- Generación de recomendaciones

### 6.3 alert_signals.py
- Sistema de alertas
- Análisis de momentum
- Señales de trading

## 7. Base de Datos

### 7.1 Estructura


### 7.2 Operaciones Principales
- Guardar precios
- Obtener historial
- Análisis de tendencias

## 8. Mantenimiento

### 8.1 Logs
- Ubicación: `logs/crypto_monitor.log`
- Nivel: INFO
- Formato: timestamp - nombre - nivel - mensaje

### 8.2 Respaldo
- Base de datos: Hacer backup periódico de `precios_historicos.db`
- Configuración: Mantener copia segura del `.env`

## 9. Solución de Problemas

### 9.1 Errores Comunes
1. Error de API Binance
   - Verificar credenciales en `.env`
   - Comprobar límites de API

2. Error de Base de Datos
   - Verificar permisos de escritura
   - Comprobar espacio en disco

3. Error de Red
   - Verificar conexión a internet
   - Comprobar firewall

### 9.2 Contacto
Para soporte técnico o reportar problemas:
- Email: rdemetrio72@yahoo.com

## 10. Actualizaciones Futuras
- Integración con más exchanges
- Análisis técnico avanzado
- Interfaz gráfica
- Sistema de backtesting
- Alertas por email/telegram

## 11. Notas Adicionales
- Actualizar regularmente las dependencias
- Mantener backups de la base de datos
- Revisar periódicamente los logs
- Monitorear el uso de recursos