from app import create_app
from app.utils.logger import logger

app = create_app()

if __name__ == "__main__":
    logger.info("Starting the application...")
    app.run(debug=True)
