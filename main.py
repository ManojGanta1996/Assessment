from src.utils import setup_logging
from src.data_ingestion import load_data
from src.data_enrichment import enrich_data
from src.data_validation import validate_data
import logging
import os

def main():
    """
    Main function to execute the ETL pipeline.
    """
    setup_logging()
    try:
        # Define paths
        data_folder = "data/"  # Folder containing the datasets
        output_path = os.path.join("output", "enriched_data.parquet")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Load data
        logging.info("Starting data ingestion...")
        base_data, options_data = load_data(data_folder)

        # Enrich data
        logging.info("Starting data enrichment...")
        enriched_data = enrich_data(base_data, options_data)

        # Validate data
        logging.info("Validating enriched data...")
        validate_data(enriched_data, options_data)

        # Save the enriched data
        logging.info(f"Saving enriched data to {output_path}...")
        enriched_data.to_parquet(output_path, index=False)
        logging.info("ETL pipeline completed successfully.")
    except Exception as e:
        logging.error(f"ETL pipeline failed: {str(e)}")

if __name__ == "__main__":
    main()