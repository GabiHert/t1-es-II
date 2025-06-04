from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from infra.entrypoint.routes import api
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='logs/dem.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "DEM API Documentation"
    }
)

# Ensure static directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), 'static'), exist_ok=True)

# Register blueprints
app.register_blueprint(api)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)