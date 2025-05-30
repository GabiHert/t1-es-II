from flask import jsonify, request
from json.decoder import JSONDecodeError

from config.api.server.server import server
from config.injector.injector import injector
from application.errors.error_handler import JSONValidationError


def get_json_data():
    """Helper function to safely get JSON data from request"""
    if not request.is_json:
        raise JSONValidationError("Request must be JSON")
    try:
        return request.get_json()
    except JSONDecodeError as e:
        raise JSONValidationError(f"Invalid JSON format: {str(e)}")


@server.route("/sync", methods=['GET'])
def sync():
    """
    Endpoint to fetch latest injection and trigger a new extraction.
    Returns the extraction response with HTTP 200 OK status.
    """
    extraction_response = injector.sync_controller.sync()
    return jsonify(extraction_response)


@server.route("/countries", methods=['GET'])
def get_countries():
    countries = injector.country_controller.get_all_countries()
    return jsonify(countries)


@server.route("/countries", methods=['POST'])
def create_country():
    data = get_json_data()
    country = injector.country_controller.create_country(data)
    return jsonify(country), 201


@server.route("/countries/<int:country_id>", methods=['GET'])
def get_country_by_id(country_id):
    country = injector.country_controller.get_country_by_id(country_id)
    return jsonify(country)


@server.route("/currencies", methods=['GET'])
def get_currencies():
    currencies = injector.currency_controller.get_all_currencies()
    return jsonify(currencies)


@server.route("/currencies", methods=['POST'])
def create_currency():
    data = get_json_data()
    currency = injector.currency_controller.create_currency(data)
    return jsonify(currency), 201


@server.route("/currencies/<int:currency_id>", methods=['GET'])
def get_currency_by_id(currency_id):
    currency = injector.currency_controller.get_currency_by_id(currency_id)
    return jsonify(currency)

