def validate_side(side: str) -> str:
    """Ensures the side is either BUY or SELL."""
    side_upper = side.upper()
    if side_upper not in ["BUY", "SELL"]:
        raise ValueError("Side must be exactly 'BUY' or 'SELL'.")
    return side_upper

def validate_order_type(order_type: str) -> str:
    """Ensures the order type is either MARKET or LIMIT."""
    type_upper = order_type.upper()
    if type_upper not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be exactly 'MARKET' or 'LIMIT'.")
    return type_upper

def validate_quantity(quantity: float) -> float:
    """Ensures the quantity is a positive number."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")
    return quantity

def validate_price(order_type: str, price: float = None) -> float:
    """Ensures LIMIT orders have a valid positive price."""
    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("A valid positive price is required for LIMIT orders.")
    return price