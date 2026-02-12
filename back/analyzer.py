import pandas as pd
import numpy as np

def analyze_trend(data, name="Activo"):
    """Analiza la tendencia del activo"""
    close = data['Close'].squeeze()
    
    # Calcular medias móviles
    sma_20 = close.rolling(window=20).mean()
    sma_50 = close.rolling(window=50).mean()
    sma_200 = close.rolling(window=200).mean()
    
    # Tendencia actual
    current_price = close.iloc[-1]
    
    analysis = {
        'nombre': name,
        'precio_actual': current_price,
        'sma_20': sma_20.iloc[-1] if len(sma_20) >= 20 else None,
        'sma_50': sma_50.iloc[-1] if len(sma_50) >= 50 else None,
        'sma_200': sma_200.iloc[-1] if len(sma_200) >= 200 else None,
    }
    
    # Determinar tendencia
    if analysis['sma_50'] and analysis['sma_200']:
        if analysis['sma_50'] > analysis['sma_200']:
            analysis['tendencia'] = 'ALCISTA'
        else:
            analysis['tendencia'] = 'BAJISTA'
    else:
        analysis['tendencia'] = 'DATOS INSUFICIENTES'
    
    # Posición respecto a medias
    if analysis['sma_20']:
        analysis['sobre_sma20'] = current_price > analysis['sma_20']
    if analysis['sma_50']:
        analysis['sobre_sma50'] = current_price > analysis['sma_50']
    if analysis['sma_200']:
        analysis['sobre_sma200'] = current_price > analysis['sma_200']
    
    return analysis


def analyze_momentum(data):
    """Calcula indicadores de momentum"""
    close = data['Close'].squeeze()
    
    # RSI (14 períodos)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # MACD
    ema_12 = close.ewm(span=12, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False).mean()
    
    momentum = {
        'rsi': rsi.iloc[-1],
        'rsi_signal': 'SOBRECOMPRA' if rsi.iloc[-1] > 70 else ('SOBREVENTA' if rsi.iloc[-1] < 30 else 'NEUTRAL'),
        'macd': macd.iloc[-1],
        'macd_signal': signal.iloc[-1],
        'macd_histograma': macd.iloc[-1] - signal.iloc[-1],
        'señal_macd': 'COMPRA' if macd.iloc[-1] > signal.iloc[-1] else 'VENTA'
    }
    
    return momentum


def analyze_performance(data):
    """Analiza el rendimiento histórico"""
    close = data['Close'].squeeze()
    
    # Rendimientos por período
    returns = {}
    
    if len(close) >= 5:
        returns['1_semana'] = ((close.iloc[-1] / close.iloc[-5]) - 1) * 100
    if len(close) >= 22:
        returns['1_mes'] = ((close.iloc[-1] / close.iloc[-22]) - 1) * 100
    if len(close) >= 66:
        returns['3_meses'] = ((close.iloc[-1] / close.iloc[-66]) - 1) * 100
    if len(close) >= 252:
        returns['1_año'] = ((close.iloc[-1] / close.iloc[-252]) - 1) * 100
    if len(close) >= 756:
        returns['3_años'] = ((close.iloc[-1] / close.iloc[-756]) - 1) * 100
    if len(close) >= 1260:
        returns['5_años'] = ((close.iloc[-1] / close.iloc[-1260]) - 1) * 100
    
    # Máximos y mínimos
    returns['max_historico'] = close.max()
    returns['min_historico'] = close.min()
    returns['distancia_max'] = ((close.iloc[-1] / close.max()) - 1) * 100
    
    return returns


def full_analysis(data, name="Activo"):
    """Análisis completo del activo"""
    print(f"\n{'='*60}")
    print(f"ANÁLISIS COMPLETO: {name}")
    print('='*60)
    
    # Tendencia
    trend = analyze_trend(data, name)
    print(f"\n TENDENCIA: {trend['tendencia']}")
    print(f"   Precio actual: {trend['precio_actual']:.2f} €")
    if trend.get('sma_20'):
        print(f"   SMA 20: {trend['sma_20']:.2f} {'✅' if trend.get('sobre_sma20') else '❌'}")
    if trend.get('sma_50'):
        print(f"   SMA 50: {trend['sma_50']:.2f} {'✅' if trend.get('sobre_sma50') else '❌'}")
    if trend.get('sma_200'):
        print(f"   SMA 200: {trend['sma_200']:.2f} {'✅' if trend.get('sobre_sma200') else '❌'}")
    
    # Momentum
    momentum = analyze_momentum(data)
    print(f"\n MOMENTUM:")
    print(f"   RSI: {momentum['rsi']:.2f} ({momentum['rsi_signal']})")
    print(f"   MACD: {momentum['señal_macd']}")
    
    # Rendimiento
    perf = analyze_performance(data)
    print(f"\n RENDIMIENTO:")
    for periodo, valor in perf.items():
        if 'max' not in periodo and 'min' not in periodo and 'distancia' not in periodo:
            print(f"   {periodo.replace('_', ' ')}: {valor:+.2f}%")
    print(f"   Distancia al máximo: {perf['distancia_max']:.2f}%")
    
    return {'trend': trend, 'momentum': momentum, 'performance': perf}