from colorlog import ColoredFormatter
import logging
from datetime import datetime

# Configure colored logging with datetime
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Disable propagation to the root logger to avoid duplicate logs
logger.propagate = False

# Create a console handler with colored output
console_handler = logging.StreamHandler()
console_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s %(levelname)-8s%(reset)s %(message)s",  # Added %(asctime)s for datetime
    datefmt="%Y-%m-%d %H:%M:%S",  # Format for the datetime
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    secondary_log_colors={},
    style="%",
)

console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Create a file handler to log only when you want
file_handler = logging.FileHandler(filename=f"app/logs/log_{datetime.now().strftime('%Y_%m_%d')}.log", mode='a')
file_formatter = logging.Formatter('%(asctime)s %(levelname)-8s%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)

# Add the file handler only when you want to log to the file
logger.addHandler(file_handler)

# Optionally, set higher log levels for specific loggers to suppress their logs
# logging.getLogger("watchfiles").setLevel(logging.WARNING)
# logging.getLogger("pymongo").setLevel(logging.WARNING)
# logging.getLogger("uvicorn").setLevel(logging.WARNING)