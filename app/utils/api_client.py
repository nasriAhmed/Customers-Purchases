import requests
from app.utils.logger import logger


def send_data_to_api(api_url, data):
    """
    Sends data to the specified API URL using an HTTP PUT request.

    Args:
        api_url (str): The URL of the API endpoint to send data to.
        data (dict): The data to be sent to the API in JSON format.

    Returns:
        tuple: A tuple containing the HTTP status code and the response text.
    """
    try:
        response = requests.put(api_url, json=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Erreur de connexion : {e}")
        return 503, None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la requête : {e}")
        return response.status_code if "response" in locals() else 500, None
    except ValueError:
        logger.error("Erreur lors de la récupération des données JSON.")
        return response.status_code, None
