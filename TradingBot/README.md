# TradingBot

Simple Binance Futures Testnet Trading Bot

## Project

Simple Binance Futures Testnet Trading Bot

## Features

- ✔ Market Orders
- ✔ Limit Orders
- ✔ BUY
- ✔ SELL
- ✔ Logging
- ✔ Validation
- ✔ Exception Handling

## Structure

- `bot/` — core trading bot package
- `logs/` — log output directory (trading.log)
- `cli.py` — command-line entry point
- `requirements.txt` — Python dependencies

## Usage

Activate the virtual environment and run examples:

```powershell
.\venv\Scripts\Activate
python TradingBot\cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
python TradingBot\cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 95000
```

## Installation

Install dependencies into your virtual environment:

```bash
pip install -r TradingBot/requirements.txt
```

## Run

Example command to place a market buy:

```bash
python TradingBot/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

## Limit Example

Example command to place a limit sell:

```bash
python TradingBot/cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 105000
```

## Assumptions

- Uses Binance Futures Testnet
- Requires valid API Keys stored in `.env`
- Internet connection required

