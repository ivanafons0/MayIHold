import numpy as np
import pandas as pd

def calculate_volatility(data, periods=[22, 66, 252]):
    """Calcula la volatilidad anualizada para diferentes períodos"""
    close = data['Close'].squeeze()
    daily_returns = close.pct_change().dropna()
    
    volatility = {}
    
    for p in periods:
        if len(daily_returns) >= p:
            vol = daily_returns.tail(p).std() * np.sqrt(252) * 100
            period_name = {22: '1_mes', 66: '3_meses', 252: '1_año'}.get(p, f'{p}_dias')
            volatility[period_name] = vol
    
    return volatility


def calculate_var(data, confidence_levels=[0.95, 0.99], investment=10000):
    """Calcula el Value at Risk (VaR) para diferentes niveles de confianza"""
    close = data['Close'].squeeze()
    daily_returns = close.pct_change().dropna()
    
    var_results = {}
    
    for conf in confidence_levels:
        var_pct = np.percentile(daily_returns, (1 - conf) * 100)
        var_results[f'VaR_{int(conf*100)}%'] = {
            'porcentaje': var_pct * 100,
            'cantidad': investment * abs(var_pct)
        }
    
    return var_results


def calculate_max_drawdown(data):
    """Calcula el máximo drawdown histórico"""
    close = data['Close'].squeeze()
    
    rolling_max = close.cummax()
    drawdown = (close - rolling_max) / rolling_max * 100
    
    max_dd = drawdown.min()
    max_dd_date = drawdown.idxmin()
    
    # Encontrar fecha del pico anterior
    peak_date = close[:max_dd_date].idxmax()
    
    return {
        'max_drawdown': max_dd,
        'fecha_minimo': max_dd_date,
        'fecha_pico': peak_date,
        'dias_recuperacion': None  # Calcular si se recuperó
    }


def calculate_risk_by_timeframe(data, investment=10000):
    """Calcula riesgos para diferentes horizontes de inversión"""
    close = data['Close'].squeeze()
    daily_returns = close.pct_change().dropna()
    
    timeframes = {
        '1_mes': 22,
        '3_meses': 66,
        '6_meses': 132,
        '1_año': 252,
        '3_años': 756,
        '5_años': 1260
    }
    
    risk_analysis = {}
    
    for name, days in timeframes.items():
        if len(close) < days:
            continue
            
        period_data = close.tail(days)
        period_returns = daily_returns.tail(days)
        
        # Rendimiento del período
        total_return = ((period_data.iloc[-1] / period_data.iloc[0]) - 1) * 100
        
        # Volatilidad anualizada
        volatility = period_returns.std() * np.sqrt(252) * 100
        
        # Sharpe Ratio (asumiendo tasa libre de riesgo del 3%)
        risk_free_rate = 0.03
        annual_return = total_return * (252 / days)
        sharpe = (annual_return - risk_free_rate * 100) / volatility if volatility > 0 else 0
        
        # Peor caída en el período
        rolling_max = period_data.cummax()
        drawdown = (period_data - rolling_max) / rolling_max * 100
        max_dd = drawdown.min()
        
        # Probabilidad de pérdida (basada en datos históricos)
        negative_days = (period_returns < 0).sum()
        prob_loss = negative_days / len(period_returns) * 100
        
        # VaR 95% para el período
        var_95 = np.percentile(period_returns, 5) * 100
        
        risk_analysis[name] = {
            'rendimiento_total': total_return,
            'volatilidad_anualizada': volatility,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_dd,
            'prob_dia_negativo': prob_loss,
            'var_95_diario': var_95,
            'peor_escenario': investment * (1 + max_dd / 100),
            'ganancia_esperada': investment * (1 + total_return / 100)
        }
    
    return risk_analysis


def risk_rating(volatility):
    """Clasifica el riesgo basado en la volatilidad"""
    if volatility < 10:
        return 'BAJO', '🟢'
    elif volatility < 20:
        return 'MODERADO', '🟡'
    elif volatility < 30:
        return 'ALTO', '🟠'
    else:
        return 'MUY ALTO', '🔴'


def full_risk_report(data, name="Activo", investment=10000):
    """Genera un informe completo de riesgos"""
    print(f"\n{'='*60}")
    print(f" ANÁLISIS DE RIESGO: {name}")
    print(f" Inversión analizada: {investment:,.0f} €")
    print('='*60)
    
    # Volatilidad
    vol = calculate_volatility(data)
    print(f"\n VOLATILIDAD ANUALIZADA:")
    for periodo, valor in vol.items():
        rating, emoji = risk_rating(valor)
        print(f"   {periodo.replace('_', ' ')}: {valor:.2f}% {emoji} ({rating})")
    
    # VaR
    var = calculate_var(data, investment=investment)
    print(f"\n  VALUE AT RISK (pérdida máxima diaria esperada):")
    for nivel, valores in var.items():
        print(f"   {nivel}: {valores['porcentaje']:.2f}% ({valores['cantidad']:.2f} €)")
    
    # Max Drawdown
    dd = calculate_max_drawdown(data)
    print(f"\n MÁXIMO DRAWDOWN HISTÓRICO:")
    print(f"   Caída máxima: {dd['max_drawdown']:.2f}%")
    print(f"   Fecha del mínimo: {dd['fecha_minimo']}")
    print(f"   Fecha del pico anterior: {dd['fecha_pico']}")
    
    # Análisis por horizonte temporal
    risk_by_time = calculate_risk_by_timeframe(data, investment)
    print(f"\n⏱ RIESGO POR HORIZONTE TEMPORAL:")
    print("-" * 60)
    
    for periodo, metrics in risk_by_time.items():
        rating, emoji = risk_rating(metrics['volatilidad_anualizada'])
        print(f"\n    {periodo.replace('_', ' ').upper()}:")
        print(f"      Rendimiento: {metrics['rendimiento_total']:+.2f}%")
        print(f"      Volatilidad: {metrics['volatilidad_anualizada']:.2f}% {emoji}")
        print(f"      Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        print(f"      Max Drawdown: {metrics['max_drawdown']:.2f}%")
        print(f"      Peor escenario: {metrics['peor_escenario']:,.2f} €")
        print(f"      Valor esperado: {metrics['ganancia_esperada']:,.2f} €")
    
    # Recomendación
    print(f"\n{'='*60}")
    print(" RECOMENDACIÓN:")
    
    if len(risk_by_time) >= 3:
        vol_1y = risk_by_time.get('1_año', {}).get('volatilidad_anualizada', 20)
        sharpe_1y = risk_by_time.get('1_año', {}).get('sharpe_ratio', 0)
        
        if vol_1y < 15 and sharpe_1y > 0.5:
            print("    Activo apto para inversores conservadores")
            print("    Horizonte mínimo recomendado: 1 año")
        elif vol_1y < 25 and sharpe_1y > 0:
            print("    Activo apto para inversores moderados")
            print("    Horizonte mínimo recomendado: 3 años")
        else:
            print("    Activo para inversores agresivos")
            print("    Horizonte mínimo recomendado: 5+ años")
    
    print('='*60)
    
    return {
        'volatility': vol,
        'var': var,
        'max_drawdown': dd,
        'risk_by_timeframe': risk_by_time
    }