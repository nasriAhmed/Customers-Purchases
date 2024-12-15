def format_customers_for_api(customers, purchases):
    """
    Formats customer data for API consumption.

    Args:
        customers (list): A list of dictionaries, where each dictionary contains customer information.
        purchases (dict): A dictionary where keys are customer IDs and values are lists of purchase details.

    Returns:
        list: A list of dictionaries, where each dictionary contains formatted customer information including their purchases.
    """
    formatted_data = []
    for customer in customers:
        customer_id = customer["customer_id"]
        customer_purchases = purchases.get(customer_id, [])
        formatted_data.append(
            {
                "salutation": customer["title"],
                "last_name": customer["last_name"],
                "first_name": customer["first_name"],
                "email": customer["email"],
                "purchases": customer_purchases,
            }
        )
    return formatted_data
