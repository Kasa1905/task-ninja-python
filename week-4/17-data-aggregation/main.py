import pandas as pd
import argparse

# CLI

def get_args():
    parser = argparse.ArgumentParser(description='Data Aggregation with Pandas')
    parser.add_argument('--input', '-i', default='sample_cleaned_data.csv', help='Path to cleaned CSV file')
    parser.add_argument('--output', '-o', default='aggregated_report.xlsx', help='Path to output Excel file')
    return parser.parse_args()


def aggregate_data(input_csv, output_excel):
    df = pd.read_csv(input_csv)

    # Ensure Sales exists and is numeric
    if 'Sales' in df.columns:
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
    else:
        raise ValueError("Input data must contain a 'Sales' column")

    # By Region
    region_sales = df.groupby('Region', dropna=False)['Sales'].sum().reset_index().sort_values('Sales', ascending=False)

    # By Product (average)
    product_avg = df.groupby('Product', dropna=False)['Sales'].mean().reset_index().sort_values('Sales', ascending=False)

    # Multi-level aggregation
    region_product = df.groupby(['Region', 'Product'], dropna=False)['Sales'].agg(['sum','mean','count']).reset_index()
    region_product.columns = ['Region','Product','Total Sales','Average Sales','Count']
    region_product = region_product.sort_values(['Region','Total Sales'], ascending=[True,False])

    # Write to Excel
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        region_sales.to_excel(writer, index=False, sheet_name='By Region')
        product_avg.to_excel(writer, index=False, sheet_name='By Product Avg')
        region_product.to_excel(writer, index=False, sheet_name='Region_Product')

    print(f'Aggregated report written to: {output_excel}')


if __name__ == '__main__':
    args = get_args()
    aggregate_data(args.input, args.output)
