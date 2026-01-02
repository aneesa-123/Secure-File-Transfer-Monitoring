import logging
import os

def setup_logger(log_file):
    """Setup logger to log file events."""
    logger = logging.getLogger("FileMonitor")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Avoid adding multiple handlers if logger is reused
    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger

