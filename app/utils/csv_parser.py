import csv
from datetime import datetime
from app.utils.logger import logger


def parse_customers(file_path):
    """
    Parses a CSV file containing customer information and returns a list of customer dictionaries.

    Args:
        file_path (str): The path to the CSV file to be parsed.

    Returns:
        list: A list of dictionaries, each containing customer information with the following keys:
            - customer_id (str): The ID of the customer.
            - title (str): The title of the customer, either "Female" or "Male".
            - last_name (str): The last name of the customer.
            - first_name (str): The first name of the customer.
            - email (str): The email address of the customer.
    """
    customers = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                if not row.get("customer_id") or not row.get("email"):
                    logger.warning(f"Ligne invalide dans le fichier clients : {row}")
                    continue

                customers.append(
                    {
                        "customer_id": row["customer_id"],
                        "title": "Female" if row["title"] == "1" else "Male",
                        "last_name": row.get("lastname", "").strip(),
                        "first_name": row.get("firstname", "").strip(),
                        "postal_code": row.get("postal_code", "").strip(),
                        "city": row.get("city", "").strip(),
                        "email": row["email"].strip(),
                    }
                )

        logger.info(f"Successfully parsed customers from {file_path}.")
    except Exception as e:
        logger.error(f"Error parsing customers file: {e}")
        raise
    return customers


def parse_purchases(file_path):
    """
    Parses a CSV file containing purchase data and returns a dictionary of purchases grouped by customer ID.

    Args:
        file_path (str): The path to the CSV file containing purchase data.

    Returns:
        dict: A dictionary where the keys are customer IDs and the values are lists of purchase details.
              Each purchase detail is represented as a dictionary with the following keys:
              - "product_id" (str): The ID of the purchased product.
              - "price" (float): The price of the purchased product.
              - "currency" (str): The currency of the price.
              - "quantity" (int): The quantity of the purchased product.
              - "purchased_at" (str): The timestamp of the purchase.
    """
    purchases = {}
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")

            for row in reader:
                required_fields = {
                    "customer_id",
                    "product_id",
                    "quantity",
                    "price",
                    "currency",
                    "date",
                }
                if not required_fields.issubset(row.keys()) or not all(
                    row.get(field) for field in required_fields
                ):
                    logger.warning(f"Ligne invalide dans le fichier achats : {row}")
                    continue

                customer_id = row["customer_id"]
                if customer_id not in purchases:
                    purchases[customer_id] = []

                purchases[customer_id].append(
                    {
                        "product_id": row["product_id"],
                        "quantity": int(row["quantity"]),
                        "price": float(row["price"]),
                        "currency": row["currency"].strip('"'),
                        "purchased_at": row["date"],
                    }
                )

        logger.info(f"Successfully parsed purchases from {file_path}.")
    except Exception as e:
        logger.error(f"Error parsing purchases file: {e}")
        raise
    return purchases


def validate_purchase_row(row):
    """
    This module provides utility functions for parsing and validating CSV data.

    Functions:
        validate_purchase_row(row): Validates a single row of purchase data.
        Args:
            row (dict): A dictionary representing a row of purchase data with keys "purchased_at", "price", and "quantity".
    """
    try:
        datetime.strptime(row["purchased_at"], "%Y-%m-%d")
        float(row["price"])
        int(row["quantity"])
    except Exception as e:
        raise ValueError(f"Invalid purchase row: {row}. Error: {e}")
