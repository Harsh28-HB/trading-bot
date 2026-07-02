"""Binance Futures testnet client loader."""

import os
from pathlib import Path
from typing import Tuple

from binance.client import Client
from dotenv import load_dotenv


def _find_env_path() -> Path:
    """Search upward for the nearest .env file."""
    current = Path(__file__).resolve()
    for parent in (current.parent, current.parent.parent, current.parent.parent.parent):
        env_path = parent / ".env"
        if env_path.exists():
            return env_path
    raise FileNotFoundError(".env file not found in project hierarchy")


def load_api_keys() -> Tuple[str, str]:
    """Load Binance API credentials from the nearest .env file."""
    env_path = _find_env_path()
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("API_KEY", "")
    api_secret = os.getenv("API_SECRET", "")

    if not api_key or not api_secret:
        raise RuntimeError("API_KEY and API_SECRET must be set in .env")

    return api_key, api_secret


def create_binance_client() -> Client:
    """Create and return a Binance futures testnet client."""
    api_key, api_secret = load_api_keys()
    client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
    client.FUTURES_URL = Client.FUTURES_TESTNET_URL
    client.FUTURES_DATA_URL = Client.FUTURES_DATA_TESTNET_URL
    client.FUTURES_COIN_URL = Client.FUTURES_COIN_TESTNET_URL
    return client
