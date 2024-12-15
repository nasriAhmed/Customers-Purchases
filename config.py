import os


class Config:
    """
    A class that holds configuration variables for the application.
    Attributes:
        Config.API_URL (str): The base URL for the API. Defaults to "https://myhostname.com/v1/customers" if the environment variable "API_URL" is not set.
        Config.DEBUG (bool): A flag indicating whether debugging is enabled. Defaults to True if the environment variable "DEBUG" is not set.
    """

    # API_URL = os.getenv("API_URL", "https://myhostname.com/v1/customers")
    API_URL = os.getenv("API_URL", "https://httpbin.org/put")  # For testing
    DEBUG = os.getenv("DEBUG", True)  # For debugging
