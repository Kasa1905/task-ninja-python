# Python Project 17: Data Aggregation with Pandas 📊🧠

## Problem Statement
Build a script that performs aggregation operations on structured data — essential for summarizing business insights like total sales, averages, or counts.

## Features
- Grouping (`groupby`) and aggregate functions
- Multi-level aggregation with `.agg()`
- Sorting and exporting summaries to Excel
- CLI arguments for input/output

## Usage
1. Install requirements:
```bash
pip install pandas openpyxl
```
2. Run the script:
```bash
python main.py --input sample_cleaned_data.csv --output aggregated_report.xlsx
```

## Try Modifying
- Use `.agg()` for custom multi-metric summaries
- Filter by date/year before aggregation
- Add charts using `matplotlib` or `openpyxl`
