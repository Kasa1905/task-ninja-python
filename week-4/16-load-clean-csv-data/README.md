# Python Project 16: Load & Clean CSV Data 🧹📂

## Problem Statement
Build a script that loads raw CSV data, cleans it, and prepares it for analysis — a must-have skill for data science and reporting tasks.

## What You'll Learn
- Reading CSVs with `pandas`
- Handling missing data
- Data type correction & formatting
- Exporting clean data

## Features
- Loads raw CSV data
- Drops duplicates
- Fills missing sales values with 0
- Converts date column to datetime
- Removes rows with missing essential fields
- Exports cleaned data
- CLI arguments for input/output files

## Usage
1. Install requirements:
   ```bash
   pip install pandas
   ```
2. Run the script:
   ```bash
   python main.py --input sample_raw_data.csv --output cleaned_data.csv
   ```

## Sample Data
See `sample_raw_data.csv` for example input.

## Try Modifying
- Normalize column names
- Add logging to track issues
- Integrate with Excel writer

## Use Cases
- Data preprocessing for analysis
- Cleaning exported reports
- Fixing user-entered datasets
