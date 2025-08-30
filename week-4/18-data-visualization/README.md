# Python Project 18: Data Visualization with Matplotlib & Seaborn 📈🎨

## Problem Statement
Create insightful visualizations from data to uncover patterns, trends, and outliers for better business and analytical decisions.

## What You'll Learn
- Plotting with `matplotlib`
- Stylish graphs using `seaborn`
- Customizing titles, labels, and colors
- Creating multiple plot types

## Features
- Line plots for time series data
- Bar charts for categorical comparisons
- Pie charts for distribution analysis
- Correlation heatmaps
- High-quality PNG export
- CLI arguments for input/output

## Usage
1. Install requirements:
```bash
pip install pandas matplotlib seaborn
```
2. Run the script:
```bash
python main.py --input sample_sales_data.csv --output-dir charts --show
```

## Chart Types Generated
- `sales_over_time.png` - Line plot of sales trends
- `sales_by_region.png` - Bar chart of regional performance
- `sales_by_product_pie.png` - Pie chart of product distribution
- `correlation_heatmap.png` - Feature correlation matrix

## Try Modifying
- Add `hue=` parameter for category grouping
- Experiment with different color palettes
- Create scatter plots for two variables
- Add trend lines to time series

## Use Cases
- Sales trends & seasonal analysis
- Product/category comparisons
- Reporting for management
- Exploratory data analysis
