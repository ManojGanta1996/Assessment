import logging
import os

def setup_logging(log_file="logs/data_pipeline.log"):
    """
    Configures logging for the ETL pipeline.

    Args:
        log_file (str): Path to the log file.

    Returns:
        None
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        filename=log_file,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(console_handler)