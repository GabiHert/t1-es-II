import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    # Create logger
    logger = logging.getLogger('mdm')
    logger.setLevel(logging.INFO)

    # Create formatters
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')

    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)

    # Create file handlers for INFO and ERROR
    info_handler = RotatingFileHandler('logs/mdm_info.log', maxBytes=10000000, backupCount=5)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(file_formatter)

    error_handler = RotatingFileHandler('logs/mdm_error.log', maxBytes=10000000, backupCount=5)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger 