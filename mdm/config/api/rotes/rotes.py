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
    return jsonify({"message": "List of currencies"})


@server.route("/currencies", methods=['POST'])
def create_currency():
    data = get_json_data()
    return jsonify(injector.country_controller.create_country(data)), 201


@server.route("/currencies/<int:currency_id>", methods=['GET'])
def get_currency_by_id(currency_id):
    return jsonify({"message": f"Currency with id {currency_id}"})
