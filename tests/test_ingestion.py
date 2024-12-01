import pytest
from src.data_ingestion import load_data

def test_load_data():
    data_folder = "data"

    # Call the load_data function
    base_data, options_data = load_data(data_folder)

    # Assertions to verify data was loaded correctly
    assert not base_data.empty, "Base data should not be empty"
    assert not options_data.empty, "Options data should not be empty"