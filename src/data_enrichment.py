import pandas as pd
import numpy as np
import logging

def enrich_data(base_df, options_df):
    """
    Enriches the base dataset with production cost and profit calculations.

    Args:
        base_df (pd.DataFrame): The base dataset.
        options_df (pd.DataFrame): The options dataset.

    Returns:
        pd.DataFrame: The enriched dataset.
    """
    try:
        # Handle sales price <= 0
        base_df["production_cost"] = np.where(base_df["Sales_Price"] <= 0, 0, np.nan)
        logging.debug("Step 1: Set production cost to 0 for sales price <= 0.")

        # Merge with options dataset
        merged_df = base_df.merge(
            options_df,
            left_on=["Options_Code", "Model_Text"],
            right_on=["Option_Code", "Model"],
            how="left"
        )
        # Use material cost where exact match exists
        merged_df["production_cost"] = np.where(
            merged_df["production_cost"].isnull(),
            merged_df["Material_Cost"],
            merged_df["production_cost"]
        )
        logging.debug("Step 2: Matched production cost with options dataset.")

        # Average material cost for unmatched option codes
        avg_material_cost = options_df.groupby("Option_Code")["Material_Cost"].mean().reset_index()
        merged_df = merged_df.merge(
            avg_material_cost.rename(columns={"Material_Cost": "avg_material_cost"}),
            left_on="Options_Code",
            right_on="Option_Code",
            how="left"
        )
        merged_df["production_cost"] = np.where(
            merged_df["production_cost"].isnull(),
            merged_df["avg_material_cost"],
            merged_df["production_cost"]
        )
        logging.debug("Step 3: Used average material cost for unmatched records.")

        # Default production cost to 45% of Sales_Price for unmatched records
        merged_df["production_cost"] = np.where(
            merged_df["production_cost"].isnull(),
            merged_df["Sales_Price"] * 0.45,
            merged_df["production_cost"]
        )
        logging.debug("Step 4: Defaulted production cost to 45% of sales price.")

        # Calculate profit
        merged_df["profit"] = merged_df["Sales_Price"] - merged_df["production_cost"]
        logging.info("Data enrichment completed successfully.")
        return merged_df[["VIN", "Options_Code", "Model_Text", "Sales_Price", "Material_Cost","production_cost", "profit"]]

    except Exception as e:
        logging.error(f"Data enrichment failed: {str(e)}")
        raise