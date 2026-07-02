"""Logging configuration for TradingBot."""

import logging
from pathlib import Path


def configure_logging(level: int = logging.INFO) -> None:
    """Configure logging for the application.

    Logs are written to logs/trading.log and also emitted to the console.
    """
    project_root = Path(__file__).resolve().parents[1]
    log_directory = project_root / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)
    log_file = log_directory / "trading.log"

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
