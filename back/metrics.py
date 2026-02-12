import matplotlib.pyplot as plt
import numpy as np

def plot_price_with_sma(data, name="Activo", save_path=None):
    """Gráfica de precio con medias móviles"""
    close = data['Close'].squeeze()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Precio
    ax.plot(close.index, close, label='Precio', color='blue', linewidth=1.5)
    
    # Medias móviles
    if len(close) >= 20:
        sma_20 = close.rolling(window=20).mean()
        ax.plot(close.index, sma_20, label='SMA 20', color='orange', linewidth=1)
    if len(close) >= 50:
        sma_50 = close.rolling(window=50).mean()
        ax.plot(close.index, sma_50, label='SMA 50', color='green', linewidth=1)
    if len(close) >= 200:
        sma_200 = close.rolling(window=200).mean()
        ax.plot(close.index, sma_200, label='SMA 200', color='red', linewidth=1.5)
    
    ax.set_title(f'{name} - Precio con Medias Móviles', fontsize=14)
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precio (€)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Gráfica guardada en '{save_path}'")
    
    return fig


def plot_rsi(data, name="Activo", save_path=None):
    """Gráfica del RSI"""
    close = data['Close'].squeeze()
    
    # Calcular RSI
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[2, 1])
    
    # Precio
    ax1.plot(close.index, close, label='Precio', color='blue')
    ax1.set_title(f'{name} - Precio y RSI', fontsize=14)
    ax1.set_ylabel('Precio (€)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # RSI
    ax2.plot(rsi.index, rsi, label='RSI (14)', color='purple')
    ax2.axhline(y=70, color='red', linestyle='--', label='Sobrecompra (70)')
    ax2.axhline(y=30, color='green', linestyle='--', label='Sobreventa (30)')
    ax2.fill_between(rsi.index, 70, 100, alpha=0.2, color='red')
    ax2.fill_between(rsi.index, 0, 30, alpha=0.2, color='green')
    ax2.set_ylabel('RSI')
    ax2.set_ylim(0, 100)
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Gráfica guardada en '{save_path}'")
    
    return fig


def plot_returns_comparison(data, name="Activo", save_path=None):
    """Gráfica de rendimientos por período"""
    close = data['Close'].squeeze()
    
    periods = {}
    labels = []
    values = []
    colors = []
    
    if len(close) >= 5:
        val = ((close.iloc[-1] / close.iloc[-5]) - 1) * 100
        labels.append('1 Semana')
        values.append(val)
    if len(close) >= 22:
        val = ((close.iloc[-1] / close.iloc[-22]) - 1) * 100
        labels.append('1 Mes')
        values.append(val)
    if len(close) >= 66:
        val = ((close.iloc[-1] / close.iloc[-66]) - 1) * 100
        labels.append('3 Meses')
        values.append(val)
    if len(close) >= 132:
        val = ((close.iloc[-1] / close.iloc[-132]) - 1) * 100
        labels.append('6 Meses')
        values.append(val)
    if len(close) >= 252:
        val = ((close.iloc[-1] / close.iloc[-252]) - 1) * 100
        labels.append('1 Año')
        values.append(val)
    if len(close) >= 756:
        val = ((close.iloc[-1] / close.iloc[-756]) - 1) * 100
        labels.append('3 Años')
        values.append(val)
    if len(close) >= 1260:
        val = ((close.iloc[-1] / close.iloc[-1260]) - 1) * 100
        labels.append('5 Años')
        values.append(val)
    
    colors = ['green' if v >= 0 else 'red' for v in values]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color=colors, edgecolor='black')
    
    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.set_title(f'{name} - Rendimientos por Período', fontsize=14)
    ax.set_ylabel('Rendimiento (%)')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores sobre las barras
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.annotate(f'{val:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3 if height >= 0 else -15),
                    textcoords="offset points",
                    ha='center', fontsize=10, fontweight='bold')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Gráfica guardada en '{save_path}'")
    
    return fig


def plot_drawdown(data, name="Activo", save_path=None):
    """Gráfica de drawdown (caída desde máximos)"""
    close = data['Close'].squeeze()
    
    # Calcular drawdown
    rolling_max = close.cummax()
    drawdown = (close - rolling_max) / rolling_max * 100
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[2, 1])
    
    # Precio
    ax1.plot(close.index, close, label='Precio', color='blue')
    ax1.plot(close.index, rolling_max, label='Máximo histórico', color='green', linestyle='--', alpha=0.7)
    ax1.set_title(f'{name} - Drawdown', fontsize=14)
    ax1.set_ylabel('Precio (€)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Drawdown
    ax2.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.5)
    ax2.set_ylabel('Drawdown (%)')
    ax2.set_xlabel('Fecha')
    ax2.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Gráfica guardada en '{save_path}'")
    
    return fig


def generate_all_metrics(data, name="Activo", prefix=""):
    """Genera todas las gráficas de métricas"""
    prefix = prefix or name.lower().replace(" ", "_")
    
    plot_price_with_sma(data, name, f'{prefix}_sma.png')
    plot_rsi(data, name, f'{prefix}_rsi.png')
    plot_returns_comparison(data, name, f'{prefix}_returns.png')
    plot_drawdown(data, name, f'{prefix}_drawdown.png')
    
    print(f"\n✅ Todas las métricas visuales generadas para {name}")