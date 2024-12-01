**Data Engineer Assessment Project**

# Overview:

This project implements an ETL (Extract, Transform, Load) pipeline for enriching a dataset with production costs to calculate the profitability of vehicle options. The pipeline follows specific rules to handle missing data and ensure accurate computations.



# Project Structure:
├── README.md
├── data
│   ├── base_data.csv
│   ├── options_data.csv
│   └── vehicle_line_mapping.csv
├── logs
│   └── data_pipeline.log
├── main.py
├── output
│   └── enriched_data.parquet
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── data_enrichment.py
│   ├── data_ingestion.py
│   ├── data_validation.py
│   └── utils.py
├── tests
│   ├── __init__.py
│   ├── test_enrichment.py
│   ├── test_ingestion.py
│   └── test_validation.py
└── venv


# Pipeline Workflow

	1.	Extract:
	          Load the input datasets (base_data.csv and options_data.csv) using the ingestion.py module.

	2.	Transform:
	        	Enrich the base_data with production costs using the following rules:
	             1.	If Sales_Price is zero or negative, set Production_Cost to 0.
	             2.	If a match exists for Option_Code and Model in options_data, use Material_Cost.
	             3.	If no exact match exists, use the average Material_Cost for the Option_Code.
	             4.	If no Option_Code match exists, set Production_Cost to 45% of Sales_Price.
		        Calculate profits as: Profit = Sales_Price - Production_Cost


	3.	Validate:
	       	1.	Check for:
	               •	Missing values in important columns like Sales_Price and Options_Code.
	               •	Invalid production_cost:
	                          •	If Sales_Price <= 0, production_cost should be 0.
	                          •	Match with Material_Cost if available.
	                          •	Use average Material_Cost for unmatched Options_Code.
	                          •	Default to 45% of Sales_Price if no Options_Code exists.
	                          •	Incorrect profit calculation (profit = Sales_Price - production_cost).
	       2.	Log the results:
	                •	Number of rows violating each rule.
	                •	Summary of missing values.

	4.	Load:
	        Save the enriched dataset as a Parquet file in the output/ directory.

# How to Run

Step 1: Set Up the Environment

	1.	Create and activate a virtual environment:

           python3 -m venv venv
           source venv/bin/activate  


	2.	Install dependencies:

            pip install -r requirements.txt

Step 2: Place Input Files

        Ensure the input files (base_data.csv and options_data.csv) are in the data/ directory.

Step 3: Run the ETL Pipeline

        Execute the main.py script:

        python3 main.py

The enriched dataset will be saved in the output/ directory as enriched_data.parquet.

Step 4: Run Tests

To verify the pipeline, run the unit tests:

pytest tests/


Output

The output file (enriched_data.parquet) is saved in the directory.

# Dependencies 
Python 3.8
pandas
numpy
pytest

