import logging
from datetime import datetime
import os


def setup_logger():
    """
    Configure un logger pour générer des fichiers de log uniques.
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_filename = os.path.join(
        log_dir, f"app_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    )

    logging.basicConfig(
        level=logging.INFO,
        filename=log_filename,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


logger = setup_logger()
