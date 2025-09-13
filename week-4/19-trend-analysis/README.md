# Python Project 19: Trend Analysis using Pandas & Seaborn 📊📅

## Problem Statement
Analyze time-based data to detect trends, seasonality, and growth patterns—vital for business forecasting and decision-making.

## Features
- Time series data analysis with pandas
- Multiple visualization types:
  - Sales trend line plot
  - Rolling averages
  - Year-over-year heatmap
  - Trend line analysis
- Flexible data resampling (daily/weekly/monthly/quarterly)
- CLI interface for easy use
- High-quality chart export

## What You'll Learn
- Time series manipulation with Pandas
- Rolling averages & trend lines
- Seasonal trend visualization
- Grouping data by time periods
- Data resampling techniques

## Usage
1. Install requirements:
   ```bash
   pip install pandas seaborn matplotlib numpy
   ```

2. Run basic analysis:
   ```bash
   python main.py --input sample_sales_data.csv --output charts
   ```

3. Change analysis frequency:
   ```bash
   python main.py --input sample_sales_data.csv --frequency W  # Weekly analysis
   ```

## Input Data Format
The input CSV should have at least these columns:
- `Date`: Date of the sale (YYYY-MM-DD format)
- `Sales`: Numeric sales value

See `sample_sales_data.csv` for example format.

## Output
Generates multiple visualization charts:
- `sales_trend.png`: Overall trend with moving average
- `sales_heatmap.png`: Year-over-year comparison heatmap

## Try Modifying
- Adjust rolling average window size
- Add anomaly detection
- Implement different trend detection algorithms
- Export trend data to Excel

## Use Cases
- Sales trend analysis
- Seasonal pattern detection
- Growth monitoring
- Revenue forecasting
