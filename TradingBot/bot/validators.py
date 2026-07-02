"""Validation helpers for TradingBot."""

from typing import Any, Optional


def validate_symbol(symbol: str) -> bool:
    """Validate symbol format. Must end with USDT."""
    if not isinstance(symbol, str):
        return False
    symbol = symbol.strip().upper()
    if not symbol.endswith("USDT"):
        return False
    base_asset = symbol[: -len("USDT")]
    return len(base_asset) > 0 and base_asset.isalpha()


def validate_side(side: str) -> bool:
    """Validate trade side. Allowed values: BUY, SELL."""
    if not isinstance(side, str):
        return False
    return side.strip().upper() in {"BUY", "SELL"}


def validate_order_type(order_type: str) -> bool:
    """Validate order type. Allowed values: MARKET, LIMIT."""
    if not isinstance(order_type, str):
        return False
    return order_type.strip().upper() in {"MARKET", "LIMIT"}


def validate_quantity(quantity: Any) -> bool:
    """Validate quantity. Must be greater than zero."""
    try:
        return float(quantity) > 0
    except (TypeError, ValueError):
        return False


def validate_price(price: Optional[Any], order_type: str) -> bool:
    """Validate price. Required for LIMIT orders, optional otherwise."""
    if not validate_order_type(order_type):
        return False

    if order_type.strip().upper() == "LIMIT":
        if price is None:
            return False
        try:
            return float(price) > 0
        except (TypeError, ValueError):
            return False

    return True
