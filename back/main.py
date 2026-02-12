from data import dataMSCI_WORLD, dataFOND
from analyzer import full_analysis
from metrics import generate_all_metrics
from risk import full_risk_report

# Análisis MSCI World
full_analysis(dataMSCI_WORLD, "MSCI World (EUNL.DE)")
generate_all_metrics(dataMSCI_WORLD, "MSCI World", "msci")
full_risk_report(dataMSCI_WORLD, "MSCI World", investment=150)

# Análisis IBCI
full_analysis(dataFOND, "IBCI (IBCI.DE)")
generate_all_metrics(dataFOND, "IBCI", "ibci")
full_risk_report(dataFOND, "IBCI", investment=100)