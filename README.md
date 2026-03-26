# 📈 Binance Futures Testnet Trading Bot

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Binance API](https://img.shields.io/badge/api-python--binance-F3BA2F.svg)
![CLI](https://img.shields.io/badge/cli-typer-009688.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A lightweight, robust, and cleanly structured command-line application designed to place Market and Limit orders on the Binance Futures Testnet (USDT-M). Built with a focus on code readability, strict input validation, and comprehensive error handling.

## ✨ Core Features

* **Order Execution:** Seamlessly place both `MARKET` and `LIMIT` orders.
* **Bi-directional Trading:** Full support for `BUY` and `SELL` sides.
* **Strict Validation:** Real-time CLI validation prevents invalid order parameters (e.g., negative quantities, missing prices for limit orders) before hitting the API.
* **Robust Error Handling:** Gracefully catches API exceptions, network failures, and input errors without crashing.
* **Comprehensive Logging:** Automatically outputs execution summaries to the console and detailed logs to `trading_bot.log`.

## 📂 Project Architecture

The application follows a modular, separation-of-concerns architecture to ensure maintainability and testability:

```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py         # Binance API connection wrapper
│   ├── orders.py         # Core execution logic for trades
│   ├── validators.py     # Strict input validation rules
│   ├── logging_config.py # Dual-handler logging setup
│   └── cli.py            # Typer CLI entry point
│
├── requirements.txt      # Project dependencies
├── trading_bot.log       # Execution logs (generated at runtime)
└── README.md
```
## ⚙️ Setup & Installation

* 1. Clone the repo
```
git clone (https://github.com/iron-prog/trading_bot.git)
cd trading_bot
```
* 2. Create a virtual environment
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
* 3. Install dependencies
```
pip install -r requirements.txt
```

* 4. Configure API Credentials
To maintain security, this bot requires your Binance Futures Testnet credentials to be passed via environment variables.
```
export BINANCE_TESTNET_API_KEY="your_api_key_here"
export BINANCE_TESTNET_API_SECRET="your_api_secret_here"
```

## 🚀 Usage Guide
The CLI is built using Typer, providing a clean interface with automatic help generation.
View all available commands and arguments:
```
python -m bot.cli --help
```
**Example 1: Placing a MARKET Order
To buy 0.01 BTC at the current market price:
```
python -m bot.cli BTCUSDT BUY MARKET 0.01
```
**Example 2: Placing a LIMIT Order
To sell 0.01 BTC at a target price (e.g., 75000):
```
python -m bot.cli BTCUSDT SELL LIMIT 0.01 --price 75000
```
## Design Decisions & Assumptions

* Library Selection: The python-binance library was chosen over raw requests/httpx REST calls. It natively handles the complex HMAC SHA256 cryptographic signatures required by Binance, significantly reducing security risks and maintenance overhead.

* CLI Framework: Typer was utilized instead of argparse. Typer offers superior type-hinting integration, automatic help menus, and reduces boilerplate code, resulting in a more maintainable command layer.

* Security Posture: Hardcoding API keys is an anti-pattern. The application strictly enforces the use of environment variables to prevent accidental credential leakage in version control.

* Logging Strategy: A dual-handler logging approach was implemented. High-level summaries are printed to stdout for immediate user feedback, while granular technical details (including raw API responses) are piped to trading_bot.log for debugging and auditing.
