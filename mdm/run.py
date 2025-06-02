from config.api.server.server import server
import logging

logger = logging.getLogger('mdm')

if __name__ == "__main__":
    logger.info("Starting MDM service on port 5002")
    try:
        server.run(debug=True, port=5002)
    except Exception as e:
        logger.error(f"Failed to start MDM service: {str(e)}")
        raise