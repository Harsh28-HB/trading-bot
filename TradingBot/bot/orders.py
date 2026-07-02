"""Order management helpers for TradingBot."""

import logging
from typing import Any

import requests
from binance.exceptions import (
    BinanceAPIException,
    BinanceOrderException,
    BinanceRequestException,
)

from bot.client import create_binance_client
from bot.validators import validate_price, validate_quantity, validate_side, validate_symbol

logger = logging.getLogger(__name__)


def _raise_logged_error(exc: Exception) -> None:
    if isinstance(exc, BinanceRequestException) or isinstance(exc, requests.RequestException):
        logger.error("Network error: %s", exc)
    elif isinstance(exc, requests.Timeout):
        logger.error("Connection timeout: %s", exc)
    elif isinstance(exc, BinanceOrderException):
        logger.error("Binance order exception: %s", exc)
    elif isinstance(exc, BinanceAPIException):
        logger.error("Binance API exception: %s", exc)
    else:
        logger.error("Unexpected error: %s", exc, exc_info=True)
    raise RuntimeError("Trading operation failed") from exc


def place_market_order(symbol: str, side: str, quantity: Any) -> dict:
    """Place a market order using Binance Futures testnet."""
    if not validate_symbol(symbol):
        raise ValueError("Invalid symbol. Must end with USDT.")
    if not validate_side(side):
        raise ValueError("Invalid side. Allowed values: BUY, SELL.")
    if not validate_quantity(quantity):
        raise ValueError("Invalid quantity. Must be greater than zero.")

    symbol = symbol.strip().upper()
    side = side.strip().upper()
    quantity = float(quantity)

    logger.info("Sending MARKET %s %s Qty=%s", side, symbol, quantity)
    client = create_binance_client()

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        logger.info("SUCCESS OrderID=%s", response.get("orderId"))
        return response
    except Exception as exc:
        _raise_logged_error(exc)


def place_limit_order(symbol: str, side: str, quantity: Any, price: Any) -> dict:
    """Place a limit order using Binance Futures testnet."""
    if not validate_symbol(symbol):
        raise ValueError("Invalid symbol. Must end with USDT.")
    if not validate_side(side):
        raise ValueError("Invalid side. Allowed values: BUY, SELL.")
    if not validate_quantity(quantity):
        raise ValueError("Invalid quantity. Must be greater than zero.")
    if not validate_price(price, "LIMIT"):
        raise ValueError("Invalid price. LIMIT orders require a positive price.")

    symbol = symbol.strip().upper()
    side = side.strip().upper()
    quantity = float(quantity)
    price = str(float(price))

    logger.info("Sending LIMIT %s %s Qty=%s Price=%s", side, symbol, quantity, price)
    client = create_binance_client()

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price,
        )
        logger.info("SUCCESS OrderID=%s", response.get("orderId"))
        return response
    except Exception as exc:
        _raise_logged_error(exc)
