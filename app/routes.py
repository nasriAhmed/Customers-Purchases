from flask import Blueprint, jsonify
from app.utils.csv_parser import parse_customers, parse_purchases
from app.utils.json_formatter import format_customers_for_api
from app.utils.api_client import send_data_to_api
from app.utils.logger import logger
from config import Config

main_bp = Blueprint("main", __name__)

CUSTOMERS_FILE = "static/customers.csv"
PURCHASES_FILE = "static/purchases.csv"


@main_bp.route("/api/customers", methods=["GET"])
def get_customers():
    """
    Retrieves a list of customers from a file and returns it as a JSON response.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
               On success, returns a JSON list of customers and status code 200.
               On failure, returns a JSON error message and status code 500.
    """
    try:
        customers = parse_customers(CUSTOMERS_FILE)
        return jsonify(customers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main_bp.route("/api/purchases", methods=["GET"])
def get_purchases():
    """
    Retrieve and return the list of purchases.

    This function attempts to parse the purchases from a predefined file and
    return them in JSON format with a 200 status code. If an error occurs during
    parsing, it returns an error message in JSON format with a 500 status code.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
    """
    try:
        purchases = parse_purchases(PURCHASES_FILE)
        return jsonify(purchases), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main_bp.route("/api/send", methods=["POST"])
def send_data():
    """
    Endpoint to send customer and purchase data to an external API.

    This function handles POST requests to the '/api/send' route. It performs the following steps:
    1. Parses customer data from a specified file.
    2. Parses purchase data from a specified file.
    3. Formats the parsed data for the API.
    4. Sends the formatted data to an external API.
    5. Returns the status code and response text from the API.

    Returns:
        Response: A JSON response containing the status code and response text from the API,
                or an error message with a 500 status code if an exception occurs.
    """
    try:
        customers = parse_customers(CUSTOMERS_FILE)
        purchases = parse_purchases(PURCHASES_FILE)
        formatted_data = format_customers_for_api(customers, purchases)
        logger.info("Lancer l'envoi des données formatées à l'API.")
        status_code, response_text = send_data_to_api(Config.API_URL, formatted_data)
        return jsonify({"status": status_code, "response": response_text}), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
