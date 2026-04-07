# BTC Pattern Detector

Aplicación web para visualizar gráficos de Bitcoin en tiempo real y detectar automáticamente patrones chartistas usando Python, Flask y Plotly.

## Requisitos

- Python 3.8+
- Windows/Mac/Linux

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/ilangraterol/patron-detector.git
cd patron-detector
```

2. Crear entorno virtual:
```bash
python -m venv venv
```

3. Activar entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

Abrir en el navegador: http://localhost:5000

## Estructura del Proyecto

```
btc_pattern_app/
├── main.py                 # Servidor Flask
├── requirements.txt       # Dependencias
├── data/
│   └── data_fetcher.py    # Obtención de datos de Binance (CCXT)
├── patterns/
│   ├── detector.py        # Detector principal
│   ├── continuation_patterns.py  # Patrones de continuación
│   └── reversal_patterns.py     # Patrones de reversión
├── visualization/
│   └── chart.py          # Gráfico interactivo con Plotly
├── analysis/
│   └── predictor.py      # Análisis predictivo de patrones
├── utils/
│   └── helpers.py        # Utilidades
└── templates/
    └── index.html       # Interfaz web
```

## API Endpoints

- `GET /` - Página principal
- `GET /api/data` - Obtiene datos OHLCV, precio actual y patrones detectados
- `GET /api/ticker` - Obtiene precio actual de BTC/USDT

### Parámetros

- `timeframe` (opcional): Intervalo de tiempo (1m, 5m, 15m, 30m, 1h, 4h, 1d). Por defecto: 1h

## Patrones Detectados

### Patrones de Continuación
- Triángulo Ascendente
- Triángulo Descendente
- Triángulo Simétrico
- Banderas (Flags)
- Banderines (Pennants)

### Patrones de Reversión
- Doble Techo (Double Top)
- Doble Suelo (Double Bottom)
- Hombro-Cabeza-Hombro (HCH)
- HCH Invertido
- Triple Techo / Suelo

## Características

- Datos en tiempo real de Binance
- Visualización interactiva con Plotly
- Detección automática de patrones chartistas
- Múltiples timeframes
- Actualización automática cada 10 segundos
- Interfaz web moderna y responsiva

## Tecnologías

- **Backend**: Flask (Python)
- **Datos**: CCXT (Binance API)
- **Visualización**: Plotly
- **Frontend**: HTML5, CSS3, JavaScript

## Licencia

MIT
