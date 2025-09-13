# Python Project 20: Dashboard Basics using Plotly & Dash 📊🖥️

## Problem Statement
Create an interactive dashboard to visualize and explore your data — ideal for reporting, monitoring KPIs, and user-driven analysis.

## Features
- Interactive web dashboard using Dash
- Multiple visualization types:
  - Monthly trend line chart
  - Product performance pie chart
  - Regional analysis bar chart
  - Year-over-year comparison
- KPI metrics cards
- Dynamic view selector
- Responsive layout
- Clean, modern design

## What You'll Learn
- Building web dashboards with Dash
- Interactive data visualization with Plotly
- Callback functions for interactivity
- Data aggregation and KPI calculation
- Web layout design

## Usage
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the dashboard:
   ```bash
   python main.py
   ```

3. Open in browser:
   ```
   http://localhost:8050
   ```

## Input Data Format
The dashboard expects a CSV file with these columns:
- `Date`: Date of sale (YYYY-MM-DD format)
- `Sales`: Numeric sales value
- `Product`: Product name/category
- `Region`: Sales region

See `sample_sales_data.csv` for example format.

## Dashboard Components
1. KPI Cards:
   - Total Sales
   - Average Sale
   - Product Count
   - Region Count

2. Interactive Charts:
   - Monthly Sales Trend
   - Product Performance
   - Regional Analysis
   - Year-over-Year Comparison

## Try Modifying
- Add date range selector
- Implement data filters
- Create additional visualizations
- Add data table view
- Customize color schemes
- Add export functionality

## Use Cases
- Sales performance monitoring
- Product analysis
- Regional comparisons
- Executive reporting
- Data exploration

## Resources
- [Dash Documentation](https://dash.plotly.com/)
- [Plotly Python](https://plotly.com/python/)
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
