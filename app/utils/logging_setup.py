import logging
from logging.handlers import RotatingFileHandler
import os

class CustomFormatter(logging.Formatter):
    """Custom formatter for coloring log level and timestamp."""

    COLORS = {
        logging.DEBUG: "\033[90m",  # Grey for DEBUG
        logging.INFO: "\033[92m",   # Green for INFO
        logging.WARNING: "\033[93m", # Yellow for WARNING
        logging.ERROR: "\033[91m",  # Red for ERROR
        logging.CRITICAL: "\033[95m", # Magenta for CRITICAL
    }
    RESET = "\033[0m"  # Reset color

    def format(self, record):
        # Get color for the log level
        level_color = self.COLORS.get(record.levelno, self.RESET)
        
        # Apply color only to the levelname and asctime
        record.levelname = f"{level_color}{record.levelname}{self.RESET}"
        record.asctime = f"{level_color}{self.formatTime(record)}{self.RESET}"
        
        # Format the log message
        return super().format(record)

# Create a "logs" directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Define file paths
INFO_LOG_FILE = os.path.join(LOG_DIR, "info.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

# Create a custom logger
logger = logging.getLogger("system_logger")
logger.setLevel(logging.DEBUG)  # or INFO, but we’ll handle levels per handler

# Common formatter
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
color_formatter = CustomFormatter(
    fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 1) Handler for INFO and higher-level logs -> info.log
info_handler = RotatingFileHandler(INFO_LOG_FILE, maxBytes=5_000_000, backupCount=3)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)
logger.addHandler(info_handler)

# 2) Handler for ERROR and higher-level logs -> error.log
error_handler = RotatingFileHandler(ERROR_LOG_FILE, maxBytes=5_000_000, backupCount=3)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

# You can optionally add a console handler (useful while debugging locally).
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
console_handler.setFormatter(color_formatter)
logger.addHandler(console_handler)

def GetLogger():
    """Return the custom system logger."""
    return logger