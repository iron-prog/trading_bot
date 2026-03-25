import logging
import sys

def setup_logger(log_file: str = "trading_bot.log"):
    """
    Configures logging to output to both the console and a file.
    """
    logger = logging.getLogger()
    
    # Prevent adding multiple handlers if setup is called multiple times
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # Format the log output clearly
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler (writes to the log file for your submission)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console Handler (prints to your terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger