import pytest
from app.utils.api_client import send_data_to_api
from app.utils.logger import logger


def test_send_data_to_api_success(mocker):
    """
    This test creates a mock response for the `requests.put` method to simulate
    a successful API call with a status code of 200 and a JSON response containing
    a success message.
    Args:
        mocker: A pytest-mock fixture used to create and manage mocks.
    Asserts:
        The status code returned by `send_data_to_api` is 200.
        The response returned by `send_data_to_api` is {"message": "success"}.
    """
    logger.info("Create a mock for the response")
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "success"}

    mocker.patch("requests.put", return_value=mock_response)

    api_url = "https://httpbin.org/put"
    data = [{"key": "value"}]

    logger.info("Call the function")
    status_code, response = send_data_to_api(api_url, data)

    logger.info("Check the results")
    assert status_code == 200
    assert response == {"message": "success"}


def test_send_data_to_api_failure(mocker):
    """
    This test verifies that the `send_data_to_api` function correctly handles
    a failure response from the API. It uses the `mocker` fixture to create a
    mock response object with a status code of 500 and a JSON decoding error.
    Steps:
    1. Create a mock response with a status code of 500 and a JSON decoding error.
    2. Patch the `requests.put` method to return the mock response.
    3. Call the `send_data_to_api` function with a sample API URL and data.
    4. Assert that the status code returned by the function is 500.
    5. Assert that the response returned by the function is `None`.
    Args:
        mocker: The pytest-mock fixture used to mock objects.
    """
    logger.info("Create a mock for the response")
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.json.side_effect = ValueError("No JSON object could be decoded")

    mocker.patch("requests.put", return_value=mock_response)

    api_url = "https://httpbin.org/put"
    data = [{"key": "value"}]

    logger.info("Call function")
    status_code, response = send_data_to_api(api_url, data)

    logger.info("Check the results")
    assert status_code == 500
    assert response is None
