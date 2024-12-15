import pytest
from app.utils.json_formatter import format_customers_for_api
from app.utils.logger import logger


def test_format_customers_for_api_success():
    """
    Tester le formatage des données clients avec des achats associés.
    """
    logger.info("Prapare the data")
    customers = [
        {
            "customer_id": "1",
            "title": "Female",
            "last_name": "Doe",
            "first_name": "Jane",
            "email": "jane.doe@example.com",
        },
        {
            "customer_id": "2",
            "title": "Male",
            "last_name": "Smith",
            "first_name": "John",
            "email": "john.smith@example.com",
        },
    ]
    purchases = {
        "1": [
            {
                "product_id": "P1",
                "price": 19.99,
                "currency": "EUR",
                "quantity": 2,
                "purchased_at": "2023-01-01",
            }
        ],
        "2": [
            {
                "product_id": "P2",
                "price": 9.99,
                "currency": "USD",
                "quantity": 1,
                "purchased_at": "2023-01-02",
            }
        ],
    }

    logger.info("Call the function")
    result = format_customers_for_api(customers, purchases)

    logger.info("Check the results")
    assert len(result) == 2
    assert result[0]["salutation"] == "Female"
    assert result[0]["last_name"] == "Doe"
    assert len(result[0]["purchases"]) == 1
    assert result[0]["purchases"][0]["product_id"] == "P1"
    assert result[1]["salutation"] == "Male"
    assert result[1]["purchases"][0]["currency"] == "USD"


def test_format_customers_for_api_no_purchases():
    """
    Tester le formatage des données clients lorsque les clients n'ont pas d'achats associés.
    """
    customers = [
        {
            "customer_id": "1",
            "title": "Female",
            "last_name": "Doe",
            "first_name": "Jane",
            "email": "jane.doe@example.com",
        }
    ]
    purchases = {}

    result = format_customers_for_api(customers, purchases)

    assert len(result) == 1
    assert result[0]["salutation"] == "Female"
    assert result[0]["last_name"] == "Doe"
    assert result[0]["purchases"] == []


def test_format_customers_for_api_empty_customers():
    """
    Teste le formatage lorsque la liste des clients est vide.
    """
    customers = []
    purchases = {
        "1": [
            {
                "product_id": "P1",
                "price": 19.99,
                "currency": "EUR",
                "quantity": 2,
                "purchased_at": "2023-01-01",
            }
        ]
    }

    result = format_customers_for_api(customers, purchases)

    assert result == []


def test_format_customers_for_api_invalid_purchase_key():
    """
    Tester le formatage des données clients avec un ID client inexistant dans les achats.
    """
    customers = [
        {
            "customer_id": "1",
            "title": "Female",
            "last_name": "Doe",
            "first_name": "Jane",
            "email": "jane.doe@example.com",
        }
    ]
    purchases = {
        "2": [
            {
                "product_id": "P2",
                "price": 9.99,
                "currency": "USD",
                "quantity": 1,
                "purchased_at": "2023-01-02",
            }
        ]
    }

    result = format_customers_for_api(customers, purchases)

    assert len(result) == 1
    assert result[0]["salutation"] == "Female"
    assert result[0]["purchases"] == []
