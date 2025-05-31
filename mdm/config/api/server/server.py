from flask import Flask, request
from config.api.error_handlers import init_error_handlers
from config.logging_config import setup_logging

# Setup logging
logger = setup_logging()

server = Flask(__name__)
init_error_handlers(server)

# Import routes to register them with Flask
logger.info("Initializing MDM service and registering routes...")
try:
    from config.api.rotes import rotes  # noqa
    logger.info("Routes registered successfully")
except Exception as e:
    logger.error(f"Failed to register routes: {str(e)}")
    raise

@server.before_request
def log_request():
    logger.info(f"Incoming request: {request.method} {request.path}")

@server.after_request
def log_response(response):
    logger.info(f"Response status: {response.status}")
    return response
