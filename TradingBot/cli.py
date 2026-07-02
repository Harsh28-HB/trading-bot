"""Command-line interface for TradingBot."""

import logging
from typing import Optional

import typer
from rich import print as rprint

from bot.logging_config import configure_logging
from bot.orders import place_limit_order, place_market_order

app = typer.Typer()
logger = logging.getLogger(__name__)


def print_order_summary(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]) -> None:
    rprint("-----------------------")
    rprint("[bold]ORDER SUMMARY[/bold]")
    rprint("-----------------------")
    rprint(f"\nSymbol : {symbol}\n")
    rprint(f"Side : {side}\n")
    rprint(f"Type : {order_type}\n")
    rprint(f"Quantity : {quantity}")
    if order_type == "LIMIT" and price is not None:
        rprint(f"\nPrice : {price}")


def print_order_response(response: dict) -> None:
    status = response.get("status") or response.get("orderStatus") or "UNKNOWN"
    executed_qty = response.get("executedQty") or response.get("cumQuote") or "0"
    average_price = response.get("avgPrice") or response.get("averagePrice") or "0"

    rprint("-----------------------")
    rprint("\n[bold]ORDER RESPONSE[/bold]")
    rprint("-----------------------")
    rprint(f"\nOrder ID : {response.get('orderId', response.get('order_id', 'N/A'))}\n")
    rprint(f"Status : {status}\n")
    rprint(f"Executed Qty : {executed_qty}\n")
    rprint(f"Average Price : {average_price}\n")
    rprint("[green]SUCCESS[/green]")


@app.command()
def run(
    symbol: str = typer.Option(..., help="Trading symbol, e.g. BTCUSDT"),
    side: str = typer.Option(..., case_sensitive=False, help="Trade side: BUY or SELL"),
    order_type: str = typer.Option(..., "--type", case_sensitive=False, help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Option(..., help="Order quantity"),
    price: Optional[float] = typer.Option(None, help="Order price for LIMIT orders"),
) -> None:
    """Place an order on Binance Futures Testnet."""
    configure_logging()

    side_u = side.strip().upper()
    order_type_u = order_type.strip().upper()

    if order_type_u == "LIMIT" and price is None:
        logger.error("Price missing for LIMIT order.")
        rprint("[red]ERROR[/red]\n\nPrice missing for LIMIT order.")
        raise typer.Exit(code=1)

    print_order_summary(symbol, side_u, order_type_u, quantity, price)

    try:
        if order_type_u == "MARKET":
            result = place_market_order(symbol, side_u, quantity)
        else:
            result = place_limit_order(symbol, side_u, quantity, price)

        print_order_response(result)
    except Exception:
        logger.exception("Order execution failed")
        rprint("[red]Something went wrong\n\nSee trading.log[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
