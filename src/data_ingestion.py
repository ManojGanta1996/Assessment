import os
import pandas as pd
import logging

def load_data(data_folder):
    """
    Automatically fetch and load data from a local folder.

    Args:
        data_folder (str): Path to the folder containing the datasets.

    Returns:
        tuple: base_data (DataFrame), options_data (DataFrame)
    """
    try:
        # Define file paths
        base_path = os.path.join(data_folder, "base_data.csv")
        options_path = os.path.join(data_folder, "options_data.csv")

        # Check if files exist
        if not os.path.exists(base_path):
            raise FileNotFoundError(f"File not found: {base_path}")
        if not os.path.exists(options_path):
            raise FileNotFoundError(f"File not found: {options_path}")

        # Load datasets
        logging.info(f"Loading base dataset from {base_path}...")
        base_data = pd.read_csv(base_path)

        logging.info(f"Loading options dataset from {options_path}...")
        options_data = pd.read_csv(options_path)

        logging.info("Data ingestion completed successfully.")
        return base_data, options_data
    except Exception as e:
        logging.error(f"Data ingestion failed: {str(e)}")
        raise