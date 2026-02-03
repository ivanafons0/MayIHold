import yfinance as yf
import matplotlib.pyplot as plt

tickers = yf.Tickers('EUNL.DE IBCI.DE DFEN.DE GZURD.XD PPFD.SG')

yf.download(['EUNL.DE', 'IBCI.DE', 'DFEN.DE', 'GZURD.XD', 'PPFD.SG'], period='1mo')

print("Data downloaded successfully.")

# Obtener datos históricos de EUNL.DE
data = tickers.tickers['EUNL.DE'].history(period='1mo')
print(data)

# Crear gráfica
plt.figure(figsize=(30, 10))
plt.plot(data.index, data['Close'], label='Precio de Cierre', color='blue', linewidth=2)
plt.fill_between(data.index, data['Low'], data['High'], alpha=0.3, label='Rango (Low-High)')
plt.title('EUNL.DE - Último Mes', fontsize=18)
plt.xlabel('Fecha')
plt.ylabel('Precio (EUR)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafica_eunl.png', dpi=150)
print("Gráfica guardada en 'grafica_eunl.png'")

