import logging
import pandas as pd

def validate_data(df, options_data):
    """
    Validates the enriched dataset for missing values, inconsistencies, and rule adherence.

    Args:
        df (pd.DataFrame): The enriched dataset to validate.
        options_data (pd.DataFrame): The options dataset for validation reference.

    Returns:
        dict: A summary of validation results.
    """
    logging.info("Starting data validation...")

    try:
        # Rule 1: Sales_Price <= 0 => Production_Cost = 0
        invalid_zero_costs = df[(df["Sales_Price"] <= 0) & (df["production_cost"] != 0)]
        logging.warning(f"Invalid Zero Costs: {len(invalid_zero_costs)}")

        # Rule 2: Exact match in options_data
        invalid_exact_matches = df[
            (df["Sales_Price"] > 0) &
            pd.notnull(df["Material_Cost"]) &
            (df["production_cost"] != df["Material_Cost"])
        ]
        logging.warning(f"Invalid Exact Matches: {len(invalid_exact_matches)}")

        # Rule 3: Average Material_Cost for unmatched Option_Codes
        avg_material_cost = options_data.groupby("Option_Code")["Material_Cost"].mean().to_dict()
        df["Avg_Material_Cost"] = df["Options_Code"].map(avg_material_cost)

        invalid_avg_costs = df[
            (df["Sales_Price"] > 0) &
            pd.isnull(df["Material_Cost"]) &
            (df["production_cost"] != df["Avg_Material_Cost"])
        ]
        logging.warning(f"Invalid Average Costs: {len(invalid_avg_costs)}")

        # Rule 4: No Option_Code match => 45% of Sales_Price
        invalid_fallback_costs = df[
            (df["Sales_Price"] > 0) &
            pd.isnull(df["Options_Code"]) &
            (df["production_cost"] != (df["Sales_Price"] * 0.45))
        ]
        logging.warning(f"Invalid Fallback Costs: {len(invalid_fallback_costs)}")

        # Rule 5: Validate Profit calculation
        invalid_profits = df[df["profit"] != (df["Sales_Price"] - df["production_cost"])]
        logging.warning(f"Invalid Profits: {len(invalid_profits)}")

        # Rule6: Production_Cost should be equal to Material_Cost, Avg_Material_Cost, or 45% of Sales_Price
        valid_costs = (
            # Rule 1: If Sales_Price <= 0, Production_Cost must be 0
            (df['Sales_Price'] <= 0) & (df['production_cost'] == 0) |
            
            # Rule 2: Production_Cost should exactly match Material_Cost
            (df['production_cost'] == df['Material_Cost']) |
            
            # Rule 3: Production_Cost should exactly match Avg_Material_Cost (if Material_Cost is missing)
            (df['production_cost'] == df['Avg_Material_Cost']) |
            
            # Rule 4: Fallback condition - Production_Cost should be exactly 45% of Sales_Price
            (df['production_cost'] == df['Sales_Price'] * 0.45)
        )

        # Invalid production costs (rows where none of the conditions match)
        invalid_costs = df[~valid_costs]
        logging.info(f"Invalid Production Costs: {len(invalid_costs)}")

        # General Check: Missing Values
        missing_values = df.isnull().sum()
        logging.info(f"Missing Values:\n{missing_values}")

        # Log validation completion
        logging.info("Data validation completed successfully.")

        # Compile validation summary
        validation_summary = {
            "Invalid Zero Costs": len(invalid_zero_costs),
            "Invalid Exact Matches": len(invalid_exact_matches),
            "Invalid Average Costs": len(invalid_avg_costs),
            "Invalid Fallback Costs": len(invalid_fallback_costs),
            "Invalid Profits": len(invalid_profits),
            "Invalid Production Costs": len(invalid_costs),
            "Missing Values": missing_values.to_dict()
        }

        return validation_summary

    except Exception as e:
        logging.error(f"Data validation failed: {str(e)}")
        raise