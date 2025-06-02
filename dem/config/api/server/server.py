from flask import Flask
from infra.entrypoint.routes import api
from config.database import init_db, db_session
import logging

logger = logging.getLogger('dem')

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(api)
        
        @self.app.teardown_appcontext
        def shutdown_session(exception=None):
            if exception:
                logger.error(f"Error during session cleanup: {str(exception)}")
            db_session.remove()
            
    def initialize(self):
        """Initialize server dependencies"""
        logger.info("Initializing DEM service...")
        try:
            init_db()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise
            
    def run(self, debug=False, port=5001):
        """Run the server"""
        self.initialize()
        logger.info(f"Starting DEM service on port {port}")
        self.app.run(debug=debug, port=port)

server = Server() 