# MayIHold

Aplicación TUI (Text User Interface) escrita en Python para análisis de inversiones. Permite analizar ETFs, acciones y fondos de inversión, calculando métricas de riesgo y rendimiento basadas en datos históricos.

## Funcionalidades

- Análisis técnico con medias móviles (SMA 20, 50, 200)
- Indicadores de momentum (RSI, MACD)
- Cálculo de rendimientos por período (1 semana a 5 años)
- Análisis de riesgo: volatilidad, VaR, Sharpe Ratio, Max Drawdown
- Generación de gráficas exportadas a PNG
- Recomendaciones basadas en horizonte temporal de inversión
- Compatible con cualquier ticker de Yahoo Finance

## Requisitos

- Python 3.8+
- Entorno virtual (recomendado)

## Instalación

```bash
git clone https://github.com/tu-usuario/MayIHold.git
cd MayIHold
python -m venv quantlab
source quantlab/bin/activate
pip install -r requirements.txt
```

## Dependencias

```
yfinance
matplotlib
pandas
numpy
rich
```

Para instalarlas manualmente:

```bash
pip install yfinance matplotlib pandas numpy rich
```

## Uso

```bash
source quantlab/bin/activate
cd back
python main.py
```

### Flujo de uso

1. Introduce los tickers de Yahoo Finance separados por comas (ej: `AAPL,MSFT,EUNL.DE`)
2. Elige el período de datos históricos (1 mes a máximo disponible)
3. Indica la cantidad de inversión en euros
4. Confirma para iniciar el análisis
5. Revisa los resultados en consola y las gráficas en la carpeta `metrics/`

### Ejemplos de tickers

| Tipo | Ejemplos |
|------|----------|
| Acciones USA | `AAPL`, `MSFT`, `GOOGL`, `TSLA` |
| Acciones Europa | `SAP.DE`, `ASML.AS`, `MC.PA` |
| ETFs | `EUNL.DE`, `VWCE.DE`, `SPY`, `QQQ` |
| Indices | `^GSPC` (S&P 500), `^IXIC` (Nasdaq) |
| Criptomonedas | `BTC-USD`, `ETH-USD` |

## Estructura del proyecto

```
MayIHold/
├── back/
│   ├── main.py        # Interfaz TUI principal
│   ├── analyzer.py    # Análisis técnico y de tendencia
│   ├── metrics.py     # Generación de gráficas
│   └── risk.py        # Cálculo de riesgos
├── metrics/           # Gráficas generadas (PNG)
├── quantlab/          # Entorno virtual
└── README.md
```

## Salida

El programa genera:

- Análisis de tendencia en consola
- Indicadores de momentum (RSI, MACD)
- Rendimientos históricos por período
- Informe de riesgo por horizonte temporal
- Gráficas en `metrics/`:
  - `{ticker}_sma.png` - Precio con medias móviles
  - `{ticker}_rsi.png` - Indicador RSI
  - `{ticker}_returns.png` - Rendimientos por período
  - `{ticker}_drawdown.png` - Drawdown histórico

## Licencia

MIT
