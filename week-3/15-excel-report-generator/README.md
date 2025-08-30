# Python Project 15: Excel Report Generator 📊🧠

## Problem Statement
Build a script that reads raw data and automatically generates a formatted Excel report — ideal for automating monthly sales, inventory, or analytics reports.

## What You'll Learn
- Using `pandas` and `openpyxl`
- Data processing and Excel writing
- Auto-formatting and report automation

## Features
- Reads raw CSV data
- Summarizes sales by region
- Writes multiple sheets into one Excel file
- Auto-formats summary sheet (bold headers, highlights top region)
- CLI arguments for input/output files

## Usage
1. Install requirements:
   ```bash
   pip install pandas openpyxl
   ```
2. Run the script:
   ```bash
   python main.py --input sample_sales_data.csv --output sales_report.xlsx
   ```

## Sample Data
See `sample_sales_data.csv` for example input.

## Try Modifying
- Apply conditional formatting
- Add charts using `xlsxwriter`
- Automate with a scheduler (e.g., weekly report)

## Use Cases
- Monthly sales summaries
- Automated client reports
- Inventory or financial tracking
