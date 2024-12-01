import pandas as pd
import pytest
from src.data_validation import validate_data

def test_validate_data():
    """
    Test the validate_data function for different validation rules.
    """
    # Create mock enriched dataset
    enriched_df = pd.DataFrame({
        "VIN": ["1", "2", "3", "4", "5"],
        "Options_Code": ["A", "B", None, "C", None],
        "Sales_Price": [100, 200, 0, 150, 50],
        "production_cost": [50, 90, 0, 67.5, 22.5],
        "profit": [50, 110, 0, 82.5, 27.5],
        "Material_Cost": [50, 90, None, None, None]
    })

    # Create mock options dataset
    options_data = pd.DataFrame({
        "Option_Code": ["A", "B", "C"],
        "Material_Cost": [50, 90, 70]
    })

    # Run validation
    validation_summary = validate_data(enriched_df, options_data)

    # Assert Rule 1: Sales_Price <= 0 => Production_Cost = 0
    assert validation_summary["Invalid Zero Costs"] == 0, \
        "All records with Sales_Price <= 0 should have Production_Cost = 0."

    # Assert Rule 2: Exact match in options_data
    assert validation_summary["Invalid Exact Matches"] == 0, \
        "All exact matches should have Production_Cost equal to Material_Cost."

    # Assert Rule 3: Average Material_Cost for unmatched Option_Codes
    assert validation_summary["Invalid Average Costs"] == 2, \
        "Unmatched Option_Codes should use the average Material_Cost."

    # Assert Rule 4: No Option_Code match => 45% of Sales_Price
    assert validation_summary["Invalid Fallback Costs"] == 0, \
        "Unmatched Options_Code should default Production_Cost to 45% of Sales_Price."

    # Assert Rule 5: Validate Profit calculation
    assert validation_summary["Invalid Profits"] == 0, \
        "Profit should equal Sales_Price - Production_Cost."

    # Assert Missing Values
    assert validation_summary["Missing Values"]["Options_Code"] == 2, \
        "There should be 2 missing values in Options_Code."
    assert validation_summary["Missing Values"]["Material_Cost"] == 3, \
        "There should be 3 missing values in Material_Cost."

    print("All validation rules passed successfully!")