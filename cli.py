import click
from app.utils.csv_parser import parse_customers, parse_purchases
from app.utils.json_formatter import format_customers_for_api
from app.utils.api_client import send_data_to_api
from config import Config
from app.utils.logger import logger


@click.command()
@click.option(
    "--customers-file",
    default="static/customers.csv",
    help="Path to customers CSV file.",
)
@click.option(
    "--purchases-file",
    default="static/purchases.csv",
    help="Path to purchases CSV file.",
)
@click.option("--api-url", default=Config.API_URL, help="API URL to send data.")
def main(customers_file, purchases_file, api_url):
    """
    Main function to process customer and purchase data, format it, and send it to an API.

    Args:
        customers_file (str): Path to the file containing customer data.
        purchases_file (str): Path to the file containing purchase data.
        api_url (str): URL of the API to send the formatted data to.

    Returns:
        None
    """
    try:
        customers = parse_customers(customers_file)
        logger.info(f"Customers: {customers}")

        purchases = parse_purchases(purchases_file)
        logger.info(f"Purchases: {purchases}")

        formatted_data = format_customers_for_api(customers, purchases)
        logger.info(f"Formatted data: {formatted_data}")

        status_code, response = send_data_to_api(api_url, formatted_data)
        click.echo(f"Response: {status_code} - {response}")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    main()
