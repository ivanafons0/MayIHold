from analyzer import full_analysis
from metrics import generate_all_metrics
from risk import full_risk_report
import yfinance as yf

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()


PERIODOS = {
    "1": {"valor": "1mo", "nombre": "1 mes"},
    "2": {"valor": "3mo", "nombre": "3 meses"},
    "3": {"valor": "6mo", "nombre": "6 meses"},
    "4": {"valor": "1y", "nombre": "1 año"},
    "5": {"valor": "2y", "nombre": "2 años"},
    "6": {"valor": "5y", "nombre": "5 años"},
    "7": {"valor": "10y", "nombre": "10 años"},
    "8": {"valor": "max", "nombre": "Máximo disponible"},
}


def mostrar_banner():
    """Muestra el banner de bienvenida"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║   ███╗   ███╗ █████╗ ██╗   ██╗    ██╗    ██╗  ██╗  ██████╗  ██╗      ██████╗ ║
    ║   ████╗ ████║██╔══██╗╚██╗ ██╔╝    ██║    ██║  ██║ ██╔═══██╗ ██║      ██╔══██╗║
    ║   ██╔████╔██║███████║ ╚████╔╝     ██║    ███████║ ██║   ██║ ██║      ██║  ██║║
    ║   ██║╚██╔╝██║██╔══██║  ╚██╔╝      ██║    ██╔══██║ ██║   ██║ ██║      ██║  ██║║
    ║   ██║ ╚═╝ ██║██║  ██║   ██║       ██║    ██║  ██║ ╚██████╔╝ ███████╗ ██████╔╝║
    ║   ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═╝    ╚═╝  ╚═╝  ╚═════╝  ╚══════╝ ╚═════╝ ║
    ║                                                                              ║
    ║                          ANALIZADOR DE ETFs                                  ║                             
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="white")


def mostrar_catalogo():
    """Muestra el catálogo de ETFs en una tabla"""
    table = Table(
        title="CATÁLOGO DE ETFs DISPONIBLES",
        box=box.DOUBLE_EDGE,
        show_header=True,
        header_style="bold magenta",
    )

    table.add_column("#", style="cyan", justify="center", width=4)
    table.add_column("Ticker", style="yellow", width=12)
    table.add_column("Nombre", style="green", width=35)
    table.add_column("Descripción", style="white")

    for num, etf in ETF_CATALOG.items():
        table.add_row(num, etf["ticker"], etf["nombre"], etf["descripcion"])

    console.print(table)


def mostrar_periodos():
    """Muestra los períodos disponibles en una tabla"""
    table = Table(
        title=" PERÍODOS DISPONIBLES",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold blue",
    )

    table.add_column("#", style="cyan", justify="center", width=4)
    table.add_column("Período", style="green", width=20)

    for num, periodo in PERIODOS.items():
        table.add_row(num, periodo["nombre"])

    console.print(table)


def seleccionar_etfs():
    """Permite al usuario introducir los tickers que quiera"""
    console.print("\n[bold yellow] INSTRUCCIONES:[/bold yellow]")
    console.print(
        "   • Escribe los tickers separados por comas (ej: [cyan]AAPL, MSFT, EUNL.DE[/cyan])"
    )
    console.print("   • Escribe [cyan]q[/cyan] para salir\n")

    seleccion = (
        Prompt.ask("[bold green] Introduce los tickers[/bold green]").strip().lower()
    )

    if seleccion == "q":
        console.print("[yellow]Bye![/yellow]")
        return []

    etfs_seleccionados = []
    tickers = [t.strip().upper() for t in seleccion.split(",")]

    for ticker in tickers:
        if ticker:
            etfs_seleccionados.append(
                {
                    "ticker": ticker,
                    "nombre": ticker,
                }
            )
            console.print(f"   [green]✓[/green] {ticker} añadido")

    return etfs_seleccionados


def solicitar_periodo():
    """Solicita el período de datos a descargar"""
    mostrar_periodos()

    seleccion = Prompt.ask(
        "\n[bold green] Selecciona período (1-8)[/bold green]", default="6"
    )
    periodo = PERIODOS.get(seleccion, PERIODOS["6"])
    console.print(f"[green]Período seleccionado: {periodo['nombre']}[/green]")
    return periodo["valor"]


def solicitar_inversion():
    """Solicita la cantidad a invertir"""
    inversion = FloatPrompt.ask(
        "\n[bold green] ¿Cuánto quieres invertir? (€)[/bold green]", default=10000.0
    )
    console.print(f"[green] Inversión: {inversion:,.2f} €[/green]")
    return inversion


def analizar_etf(etf, periodo, inversion):
    """Descarga y analiza un ETF"""
    nombre_completo = f"{etf['nombre']} ({etf['ticker']})"

    console.print(Panel(f"[bold]Analizando: {nombre_completo}[/bold]", style="blue"))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        task = progress.add_task(
            f"[cyan]Descargando datos de {etf['ticker']}...", total=None
        )

        try:
            data = yf.download(etf["ticker"], period=periodo, progress=False)

            if data.empty:
                console.print(
                    f"[red] No se pudieron obtener datos para {etf['ticker']}[/red]"
                )
                return

            progress.update(task, description=f"[cyan]Ejecutando análisis técnico...")
            prefix = etf["ticker"].replace(".", "_").lower()

            full_analysis(data, nombre_completo)

            progress.update(task, description=f"[cyan]Generando métricas visuales...")
            generate_all_metrics(data, nombre_completo, prefix)

            progress.update(task, description=f"[cyan]Calculando análisis de riesgo...")
            full_risk_report(data, nombre_completo, investment=inversion)

            progress.update(task, description=f"[green]Completado!")

        except Exception as e:
            console.print(f"[red] Error analizando {etf['ticker']}: {e}[/red]")


def mostrar_resumen(etfs, periodo, inversion):
    """Muestra un resumen de la configuración seleccionada"""
    table = Table(
        title=" RESUMEN DE ANÁLISIS",
        box=box.DOUBLE,
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Parámetro", style="yellow", width=20)
    table.add_column("Valor", style="green")

    table.add_row("ETFs seleccionados", str(len(etfs)))
    table.add_row("Período", periodo)
    table.add_row("Inversión", f"{inversion:,.2f} €")

    console.print(table)

    # Lista de ETFs
    console.print("\n[bold]ETFs a analizar:[/bold]")
    for etf in etfs:
        console.print(f"   • [cyan]{etf['ticker']}[/cyan] - {etf['nombre']}")


def main():
    """Función principal"""
    console.clear()
    mostrar_banner()

    etfs = seleccionar_etfs()

    if not etfs:
        console.print("[yellow]No se seleccionaron ETFs. Saliendo...[/yellow]")
        return

    periodo = solicitar_periodo()

    inversion = solicitar_inversion()

    console.print()
    mostrar_resumen(etfs, periodo, inversion)

    if not Confirm.ask(
        "\n[bold yellow]¿Deseas continuar con el análisis?[/bold yellow]"
    ):
        console.print("[yellow]Análisis cancelado.[/yellow]")
        return

    console.print("\n" + "=" * 70)

    for i, etf in enumerate(etfs, 1):
        console.print(f"\n[bold cyan] Procesando {i}/{len(etfs)}[/bold cyan]")
        analizar_etf(etf, periodo, inversion)

    console.print()
    console.print(
        Panel(
            "[bold green]ANÁLISIS COMPLETADO[/bold green]\n\n"
            " Las gráficas se han guardado en la carpeta [cyan]'metrics/'[/cyan]\n"
            " Revisa los informes en la consola arriba",
            title=" Finalizado",
            style="green",
        )
    )


if __name__ == "__main__":
    main()
