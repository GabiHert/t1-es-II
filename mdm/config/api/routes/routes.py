from flask import jsonify, request, Blueprint
from json.decoder import JSONDecodeError
import logging

from config.api.server.server import server
from config.injector.injector import injector
from application import JSONValidationError
from infra.entrypoint.controllers import country_controller, currency_controller, sync_controller

# Create a Blueprint for all routes
routes = Blueprint('routes', __name__)
logger = logging.getLogger('mdm')

def get_json_data():
    """Helper function to safely get JSON data from request"""
    if not request.is_json:
        raise JSONValidationError("Request must be JSON")
    try:
        return request.get_json()
    except JSONDecodeError as e:
        raise JSONValidationError(f"Invalid JSON format: {str(e)}")


@routes.route("/sync", methods=['GET'])
def sync():
    """
    Endpoint to fetch latest injection and trigger a new extraction.
    Returns the extraction response with HTTP 200 OK status.
    """
    extraction_response = injector.sync_controller.sync()
    return jsonify(extraction_response)


@routes.route("/countries", methods=['GET'])
def get_countries():
    countries = injector.country_controller.get_all_countries()
    return jsonify(countries)


@routes.route("/countries", methods=['POST'])
def create_country():
    data = get_json_data()
    country = injector.country_controller.create_country(data)
    return jsonify(country), 201


@routes.route("/countries/<int:country_id>", methods=['GET'])
def get_country_by_id(country_id):
    country = injector.country_controller.get_country_by_id(country_id)
    return jsonify(country)


@routes.route("/countries/numeric/<int:numeric_code>", methods=['GET'])
def get_country_by_numeric_code(numeric_code):
    country = injector.country_controller.get_country_by_numeric_code(numeric_code)
    return jsonify(country)


@routes.route("/currencies", methods=['GET'])
def get_currencies():
    currencies = injector.currency_controller.get_all_currencies()
    return jsonify(currencies)


@routes.route("/currencies", methods=['POST'])
def create_currency():
    data = get_json_data()
    currency = injector.currency_controller.create_currency(data)
    return jsonify(currency), 201


@routes.route("/currencies/<int:currency_id>", methods=['GET'])
def get_currency_by_id(currency_id):
    currency = injector.currency_controller.get_currency_by_id(currency_id)
    return jsonify(currency)


@routes.route("/currencies/code/<currency_code>", methods=['GET'])
def get_currency_by_code(currency_code):
    currency = injector.currency_controller.get_currency_by_code(currency_code)
    return jsonify(currency)


@routes.route("/countries/<int:country_id>", methods=['DELETE'])
def delete_country(country_id):
    injector.country_controller.delete_country(country_id)
    return '', 204


@routes.route("/currencies/<int:currency_id>", methods=['DELETE'])
def delete_currency(currency_id):
    injector.currency_controller.delete_currency(currency_id)
    return '', 204


@routes.route("/countries/<int:country_id>", methods=['PATCH'])
def update_country(country_id):
    data = get_json_data()
    country = injector.country_controller.update_country(country_id, data)
    return jsonify(country)


@routes.route("/currencies/<int:currency_id>", methods=['PATCH'])
def update_currency(currency_id):
    data = get_json_data()
    currency = injector.currency_controller.update_currency(currency_id, data)
    return jsonify(currency)


@routes.route('/health', methods=['GET'])
def health_check():
    try:
        # Try to make a simple database query using the injector
        injector.country_controller.get_all_countries()
        logger.info("Health check successful")
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "service": "mdm"
        }), 200
    except Exception as e:
        error_msg = f"Health check failed: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "service": "mdm",
            "error": str(e)
        }), 500

