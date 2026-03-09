import yfinance as yf

yf.download(['EUNL.DE', 'IBCI.DE', 'DFEN.DE', 'GZURD.XD', 'PPFD.SG'], period='1mo')

tickers = yf.Tickers('EUNL.DE IBCI.DE DFEN.DE GZURD.XD PPFD.SG')

print("Data downloaded successfully.")

dataMSCI_WORLD = tickers.tickers['EUNL.DE'].history(period='10y')
dataFOND = tickers.tickers['IBCI.DE'].history(period='10y')
