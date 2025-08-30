import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from datetime import datetime

def get_args():
    parser = argparse.ArgumentParser(description='Data Visualization with Matplotlib & Seaborn')
    parser.add_argument('--input', '-i', default='sample_sales_data.csv', help='Path to input CSV file')
    parser.add_argument('--output-dir', '-o', default='charts', help='Directory to save chart images')
    parser.add_argument('--show', '-s', action='store_true', help='Show plots interactively')
    return parser.parse_args()

def create_visualizations(input_csv, output_dir, show_plots=False):
    # Load dataset
    df = pd.read_csv(input_csv)
    
    # Convert Date column if it exists
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Set style
    sns.set_style("whitegrid")
    plt.style.use('seaborn-v0_8')
    
    # Create output directory
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Line Plot: Sales over time
    if 'Date' in df.columns and 'Sales' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x='Date', y='Sales', marker='o')
        plt.title('Sales Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Sales', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/sales_over_time.png', dpi=300, bbox_inches='tight')
        if show_plots:
            plt.show()
        plt.close()
    
    # 2. Bar Plot: Sales by Region
    if 'Region' in df.columns and 'Sales' in df.columns:
        plt.figure(figsize=(10, 6))
        region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        sns.barplot(x=region_sales.index, y=region_sales.values, palette='viridis')
        plt.title('Total Sales by Region', fontsize=16, fontweight='bold')
        plt.xlabel('Region', fontsize=12)
        plt.ylabel('Total Sales', fontsize=12)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/sales_by_region.png', dpi=300, bbox_inches='tight')
        if show_plots:
            plt.show()
        plt.close()
    
    # 3. Pie Chart: Sales distribution by Product
    if 'Product' in df.columns and 'Sales' in df.columns:
        plt.figure(figsize=(8, 8))
        product_sales = df.groupby('Product')['Sales'].sum()
        plt.pie(product_sales.values, labels=product_sales.index, autopct='%1.1f%%', startangle=90)
        plt.title('Sales Distribution by Product', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/sales_by_product_pie.png', dpi=300, bbox_inches='tight')
        if show_plots:
            plt.show()
        plt.close()
    
    # 4. Heatmap: Correlation matrix (numeric columns only)
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 1:
        plt.figure(figsize=(8, 6))
        correlation_matrix = df[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Feature Correlation Heatmap', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        if show_plots:
            plt.show()
        plt.close()
    
    print(f"Charts saved to {output_dir}/ directory")

if __name__ == '__main__':
    args = get_args()
    create_visualizations(args.input, args.output_dir, args.show)
