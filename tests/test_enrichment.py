import pandas as pd
from src.data_enrichment import enrich_data

def test_exact_match():
    """
    Test that exact matches in Options_Code and Model_Text correctly assign Material_cost.
    """
    base_df = pd.DataFrame({
        "VIN": ["1", "2"],
        "Options_Code": ["A", "B"],
        "Model_Text": ["ModelX", "ModelY"],
        "Sales_Price": [100, 200]
    })
    options_df = pd.DataFrame({
        "Option_Code": ["A", "B"],
        "Model": ["ModelX", "ModelY"],
        "Material_Cost": [50, 80]
    })
    enriched_df = enrich_data(base_df, options_df)
    assert enriched_df.loc[0, "production_cost"] == 50, "Exact match should assign Material_cost of 50."
    assert enriched_df.loc[1, "production_cost"] == 80, "Exact match should assign Material_cost of 80."

def test_missing_option_code():
    """
    Test that missing Options_Code assigns the average Material_cost.
    """
    base_df = pd.DataFrame({
        "VIN": ["1", "2"],
        "Options_Code": ["C", "D"],
        "Model_Text": ["ModelZ", "ModelW"],
        "Sales_Price": [150, 250]
    })
    options_df = pd.DataFrame({
        "Option_Code": ["C"],
        "Model": ["ModelZ"],
        "Material_Cost": [70]
    })
    enriched_df = enrich_data(base_df, options_df)
    assert round(enriched_df.loc[0, "production_cost"], 2) == 70.00, "Assign average Material_cost of 70."
    assert round(enriched_df.loc[1, "production_cost"], 2) == 112.5, "Default 45% Sales_Price for unmatched record."

def test_sales_price_zero():
    """
    Test that Sales_Price of zero assigns production_cost as 0.
    """
    base_df = pd.DataFrame({
        "VIN": ["1"],
        "Options_Code": ["A"],
        "Model_Text": ["ModelX"],
        "Sales_Price": [0]
    })
    options_df = pd.DataFrame({
        "Option_Code": ["A"],
        "Model": ["ModelX"],
        "Material_Cost": [50]
    })
    enriched_df = enrich_data(base_df, options_df)
    assert enriched_df.loc[0, "production_cost"] == 0, "Sales_Price of zero should result in production_cost of 0."

def test_default_45_percent_sales_price():
    """
    Test that unmatched records use 45% of Sales_Price as production_cost.
    """
    base_df = pd.DataFrame({
        "VIN": ["1"],
        "Options_Code": ["X"],
        "Model_Text": ["ModelY"],
        "Sales_Price": [100]
    })
    options_df = pd.DataFrame({
        "Option_Code": ["A"],
        "Model": ["ModelX"],
        "Material_Cost": [50]
    })
    enriched_df = enrich_data(base_df, options_df)
    assert enriched_df.loc[0, "production_cost"] == 45, "Default to 45% of Sales_Price when no match exists."