import logging
from typing import Optional, Dict, Any
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger(__name__)

def place_order(
    client_wrapper,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None
) -> Optional[Dict[str, Any]]:
    """
    Places a futures order (MARKET or LIMIT) and logs the outcome.
    """
    try:
        # Standard parameters required by the Binance API
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }
        
        # Limit orders require a price and a timeInForce parameter
        if order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("Price must be provided for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good Till Canceled

        logger.info(f"Sending {order_type.upper()} order request: {params}")
        
        # Access the raw python-binance client from our wrapper
        raw_client = client_wrapper.get_client()
        response = raw_client.futures_create_order(**params)
        
        logger.info(f"Raw API Response: {response}")
        
        # Extract the specific fields the assignment requested
        summary = {
            "orderId": response.get("orderId"),
            "status": response.get("status"),
            "executedQty": response.get("executedQty"),
            "avgPrice": response.get("avgPrice", "0.0") 
        }
        return summary

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Binance API Error during order placement: {e}")
        return None
    except ValueError as ve:
        logger.error(f"Input Validation Error: {ve}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error placing order: {e}")
        return None