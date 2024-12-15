import pytest
from app.utils.csv_parser import parse_customers, parse_purchases, validate_purchase_row


@pytest.fixture
def mock_valid_customers_file(tmp_path):
    """
    Créer un fichier temporaire de clients valide.
    """
    file_path = tmp_path / "customers.csv"
    file_path.write_text(
        "customer_id;title;lastname;firstname;email;postal_code;city\n"
        "1;1;Doe;Jane;jane.doe@example.com;12345;Paris\n"
        "2;2;Smith;John;john.smith@example.com;67890;Lyon\n"
    )
    return str(file_path)


@pytest.fixture
def mock_valid_purchases_file(tmp_path):
    """
    Créer un fichier temporaire d'achats valide.
    """
    file_path = tmp_path / "purchases.csv"
    file_path.write_text(
        "customer_id;product_id;quantity;price;currency;date\n"
        "1;P1;2;19.99;EUR;2023-01-01\n"
        "2;P2;1;9.99;USD;2023-01-02\n"
    )
    return str(file_path)


def test_parse_customers_success(mock_valid_customers_file):
    """
    Tester le succès de la fonction "parse_customers" avec un fichier valide.
    """
    customers = parse_customers(mock_valid_customers_file)
    assert len(customers) == 2
    assert customers[0]["customer_id"] == "1"
    assert customers[0]["title"] == "Female"
    assert customers[0]["last_name"] == "Doe"
    assert customers[1]["title"] == "Male"


def test_parse_purchases_success(mock_valid_purchases_file):
    """
    Tester le succès de la fonction "parse_purchases" avec un fichier valide.
    """
    purchases = parse_purchases(mock_valid_purchases_file)
    assert len(purchases) == 2
    assert "1" in purchases
    assert len(purchases["1"]) == 1
    assert purchases["1"][0]["product_id"] == "P1"
    assert purchases["1"][0]["price"] == 19.99
    assert purchases["1"][0]["currency"] == "EUR"


def test_parse_customers_invalid_row(mocker, tmp_path):
    """
    Tester la gestion des lignes invalides dans parse_customers.
    """
    file_path = tmp_path / "invalid_customers.csv"
    file_path.write_text(
        "customer_id;title;lastname;firstname;email\n"
        "1;1;Doe;Jane;\n"
        "2;2;Smith;John;john.smith@example.com\n"
    )

    mock_logger = mocker.patch("app.utils.csv_parser.logger.warning")
    customers = parse_customers(str(file_path))

    assert len(customers) == 1
    mock_logger.assert_called_once_with(
        "Ligne invalide dans le fichier clients : {'customer_id': '1', 'title': '1', 'lastname': 'Doe', 'firstname': 'Jane', 'email': ''}"
    )


def test_parse_purchases_invalid_row(mocker, tmp_path):
    """
    Tester la gestion des lignes invalides dans parse_purchases.
    """
    file_path = tmp_path / "invalid_purchases.csv"
    file_path.write_text(
        "customer_id;product_id;quantity;price;currency;date\n"
        "1;P1;;19.99;EUR;2023-01-01\n"
        "2;P2;1;9.99;USD;2023-01-02\n"
    )

    mock_logger = mocker.patch("app.utils.csv_parser.logger.warning")
    purchases = parse_purchases(str(file_path))

    assert len(purchases) == 1
    mock_logger.assert_called_once_with(
        "Ligne invalide dans le fichier achats : {'customer_id': '1', 'product_id': 'P1', 'quantity': '', 'price': '19.99', 'currency': 'EUR', 'date': '2023-01-01'}"
    )


def test_validate_purchase_row_valid():
    """
    Tester une ligne d'achat valide.
    """
    row = {"purchased_at": "2023-01-01", "price": "19.99", "quantity": "2"}
    validate_purchase_row(row)


def test_validate_purchase_row_invalid():
    """
    Tester une ligne d'achat invalide.
    """
    row = {"purchased_at": "invalid-date", "price": "19.99", "quantity": "2"}
    with pytest.raises(ValueError, match="Invalid purchase row"):
        validate_purchase_row(row)
