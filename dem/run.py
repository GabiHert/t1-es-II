from config import server, setup_logging
import logging

logger = setup_logging()

if __name__ == "__main__":
    try:
        server.run(debug=True, port=5001)
    except Exception as e:
        logger.error(f"Failed to start DEM service: {str(e)}")
        raise