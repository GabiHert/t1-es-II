from flask import Flask

from config.api.error_handlers import init_error_handlers

server = Flask(__name__)
init_error_handlers(server)

# Import routes to register them with Flask
from config.api.rotes import rotes  # noqa
