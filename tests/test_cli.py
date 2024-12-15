import pytest
from click.testing import CliRunner
from cli import main
from app.utils.logger import logger


def test_cli_success(mocker):
    """
    Test the success of the CLI command when everything works correctly.
    This test mocks the following functions:
    - cli.parse_customers: Parses customer data from a CSV file.
    - cli.parse_purchases: Parses purchase data from a CSV file.
    - cli.format_customers_for_api: Formats customer and purchase data for the API.
    - cli.send_data_to_api: Sends formatted data to the API.
    The test then runs the CLI command with specific arguments and verifies:
    - Each mocked function is called with the expected arguments.
    - The CLI command exits with a status code of 0.
    - The output contains the expected success message.
    """

    mock_parse_customers = mocker.patch(
        "cli.parse_customers", return_value=[{"customer_id": "123"}]
    )
    mock_parse_purchases = mocker.patch(
        "cli.parse_purchases", return_value=[{"product_id": "A1"}]
    )
    mock_format_customers = mocker.patch(
        "cli.format_customers_for_api", return_value=[{"formatted_data": "example"}]
    )
    mock_send_data_to_api = mocker.patch(
        "cli.send_data_to_api", return_value=(200, {"message": "success"})
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--customers-file",
            "static/customers.csv",
            "--purchases-file",
            "static/purchases.csv",
            "--api-url",
            "https://httpbin.org/put",
        ],
    )

    logger.info("check the calls of the mocks")
    mock_parse_customers.assert_called_once_with("static/customers.csv")
    mock_parse_purchases.assert_called_once_with("static/purchases.csv")
    mock_format_customers.assert_called_once_with(
        [{"customer_id": "123"}], [{"product_id": "A1"}]
    )
    mock_send_data_to_api.assert_called_once_with(
        "https://httpbin.org/put", [{"formatted_data": "example"}]
    )

    logger.info("check the output")
    assert result.exit_code == 0
    assert "Response: 200 - {'message': 'success'}" in result.output


def test_cli_failure_on_send(mocker):
    """
    Tests the CLI command failure when sending data fails.
    This test mocks the following functions:
    - cli.parse_customers: returns a list with a single customer dictionary.
    - cli.parse_purchases: returns a list with a single purchase dictionary.
    - cli.format_customers_for_api: returns a list with a single formatted data dictionary.
    - cli.send_data_to_api: returns a tuple indicating a failure (status code 500, None).
    The test then invokes the CLI command with specified arguments and checks:
    - The send_data_to_api function is called once with the correct arguments.
    - The CLI command exits with a code of 0.
    - The output contains the expected failure message.
    """

    mocker.patch("cli.parse_customers", return_value=[{"customer_id": "123"}])
    mocker.patch("cli.parse_purchases", return_value=[{"product_id": "A1"}])
    mocker.patch(
        "cli.format_customers_for_api", return_value=[{"formatted_data": "example"}]
    )
    mock_send_data_to_api = mocker.patch(
        "cli.send_data_to_api", return_value=(500, None)
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--customers-file",
            "static/customers.csv",
            "--purchases-file",
            "static/purchases.csv",
            "--api-url",
            "https://httpbin.org/put",
        ],
    )

    logger.info("check the calls of the mocks")
    mock_send_data_to_api.assert_called_once_with(
        "https://httpbin.org/put", [{"formatted_data": "example"}]
    )

    assert result.exit_code == 0
    assert "Response: 500 - None" in result.output
