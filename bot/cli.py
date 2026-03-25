import os
import typer
from bot.logging_config import setup_logger
from bot.client import BinanceFuturesClient
from bot.orders import place_order
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)

# Initialize the Typer app and our custom logger
app = typer.Typer(help="A Simplified Binance Futures Testnet Trading Bot")
logger = setup_logger()

@app.command()
def trade(
    symbol: str = typer.Argument(..., help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side: BUY or SELL"),
    order_type: str = typer.Argument(..., help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Argument(..., help="Amount to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Price (Required for LIMIT orders)")
):
    """
    Places a MARKET or LIMIT order on the Binance Futures Testnet.
    """
    typer.echo("--- Order Request Summary ---")
    typer.echo(f"Symbol:     {symbol.upper()}")
    typer.echo(f"Side:       {side.upper()}")
    typer.echo(f"Type:       {order_type.upper()}")
    typer.echo(f"Quantity:   {quantity}")
    if price:
        typer.echo(f"Price:      {price}")
    typer.echo("-----------------------------\n")

    try:
        # 1. Validate Inputs
        valid_side = validate_side(side)
        valid_type = validate_order_type(order_type)
        valid_qty = validate_quantity(quantity)
        valid_price = validate_price(valid_type, price)

        # 2. Load API Credentials from Environment Variables (Best Practice)
        api_key = os.getenv("BINANCE_TESTNET_API_KEY")
        api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")

        if not api_key or not api_secret:
            typer.secho(
                "Error: Missing API credentials. Please set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET environment variables.", 
                fg=typer.colors.RED
            )
            raise typer.Exit(code=1)

        # 3. Initialize Client
        typer.echo("Connecting to Binance Testnet...")
        client_wrapper = BinanceFuturesClient(api_key, api_secret)
        
        if not client_wrapper.check_connection():
            typer.secho("Error: Could not connect to the testnet.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        # 4. Place the Order
        typer.echo("Placing order...")
        result = place_order(
            client_wrapper=client_wrapper,
            symbol=symbol,
            side=valid_side,
            order_type=valid_type,
            quantity=valid_qty,
            price=valid_price
        )

        # 5. Output Response Details
        if result:
            typer.secho("\n✅ Order Placed Successfully!", fg=typer.colors.GREEN)
            typer.echo("--- Order Response Details ---")
            typer.echo(f"Order ID:     {result.get('orderId')}")
            typer.echo(f"Status:       {result.get('status')}")
            typer.echo(f"Executed Qty: {result.get('executedQty')}")
            typer.echo(f"Average Price:{result.get('avgPrice')}")
            typer.echo("------------------------------")
        else:
            typer.secho("\n❌ Order Failed. Please check the trading_bot.log file for details.", fg=typer.colors.RED)

    except ValueError as ve:
        typer.secho(f"\n❌ Validation Error: {ve}", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"\n❌ Unexpected Error: {e}", fg=typer.colors.RED)

if __name__ == "__main__":
    app()