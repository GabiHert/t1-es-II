from config import server
import os
import logging

# Configure logging
logging.basicConfig(
    filename='logs/dem.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Ensure static directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), 'static'), exist_ok=True)

if __name__ == '__main__':
    server.run(debug=True, port=5001)