import yfinance as yf
import matplotlib.pyplot as plt

tickers = yf.Tickers('EUNL.DE IBCI.DE DFEN.DE GZURD.XD PPFD.SG')

yf.download(['EUNL.DE', 'IBCI.DE', 'DFEN.DE', 'GZURD.XD', 'PPFD.SG'], period='1mo')

print("Data downloaded successfully.")

dataMSCI_WORLD = tickers.tickers['EUNL.DE'].history(period='10y')
dataFOND = tickers.tickers['IBCI.DE'].history(period='10y')
print(dataMSCI_WORLD)

# Crear gráfica
plt.figure(figsize=(30, 10))
plt.plot(dataMSCI_WORLD.index, dataMSCI_WORLD['Close'], label='Precio de Cierre', color='blue', linewidth=2)
plt.fill_between(dataMSCI_WORLD.index, dataMSCI_WORLD['Low'], dataMSCI_WORLD['High'], alpha=0.3, label='Rango (Low-High)')
plt.title('MSCI_World - Últimos 10 años', fontsize=18)
plt.xlabel('Fecha')
plt.ylabel('Precio (EUR)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafica_msci_world.png', dpi=150)
print("Gráfica guardada en 'grafica_msci_world.png'")

# Gráfica para IBCI.DE
plt.figure(figsize=(30, 10))
plt.plot(dataFOND.index, dataFOND['Close'], label='Precio de Cierre', color='blue', linewidth=2)
plt.fill_between(dataFOND.index, dataFOND['Low'], dataFOND['High'], alpha=0.3, label='Rango (Low-High)')
plt.title('IBCI - Último Mes', fontsize=18)
plt.xlabel('Fecha')
plt.ylabel('Precio (EUR)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)