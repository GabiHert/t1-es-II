from flask import jsonify, request
from pydantic import ValidationError

from config.api.server.server import server
from config.injector.injector import injector


@server.route("/countries", methods=['GET'])
def get_countries():
    return jsonify({"message": "List of countries"})

@server.route("/countries", methods=['POST'])
def create_country():
    data = request.json
    return jsonify({"message": "Country created", "data": data}), 201

@server.route("/countries/<int:country_id>", methods=['GET'])
def get_country_by_id(country_id):
    return jsonify({"message": f"Country with id {country_id}"})

@server.route("/currencies", methods=['GET'])
def get_currencies():
    return jsonify({"message": "List of currencies"})

@server.route("/currencies", methods=['POST'])
def create_currency():
    try:
        data = request.json
        return jsonify(injector.country_controller.create_country(data)), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

@server.route("/currencies/<int:currency_id>", methods=['GET'])
def get_currency_by_id(currency_id):
    return jsonify({"message": f"Currency with id {currency_id}"})
