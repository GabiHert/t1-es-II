from flask import Flask
from routes import api
from config.database import init_db, db_session
from config.logging_config import setup_logging

# Setup logging
logger = setup_logging()

app = Flask(__name__)
app.register_blueprint(api)

@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        logger.error(f"Error during session cleanup: {str(exception)}")
    db_session.remove()

if __name__ == "__main__":
    logger.info("Initializing DEM service...")
    try:
        init_db()
        logger.info("Database initialized successfully")
        logger.info(f"Starting DEM service on port 5001")
        app.run(debug=True, port=5001)
    except Exception as e:
        logger.error(f"Failed to start DEM service: {str(e)}")
        raise