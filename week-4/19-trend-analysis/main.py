import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
from typing import Optional

class TrendAnalyzer:
    def __init__(self, data_file: str):
        """Initialize TrendAnalyzer with data file path."""
        self.df = pd.read_csv(data_file, parse_dates=['Date'])
        self.df.set_index('Date', inplace=True)
        
    def resample_data(self, freq: str = 'M') -> pd.Series:
        """Resample data to specified frequency (M=monthly, W=weekly, Q=quarterly)."""
        return self.df['Sales'].resample(freq).sum()
    
    def calculate_rolling_average(self, data: pd.Series, window: int = 3) -> pd.Series:
        """Calculate rolling average with specified window size."""
        return data.rolling(window).mean()
    
    def plot_trend(self, data: pd.Series, title: str, output_file: Optional[str] = None):
        """Create and save/show trend plot."""
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")
        
        # Plot actual data
        sns.lineplot(x=data.index, y=data.values, label='Actual')
        
        # Add rolling average
        rolling_avg = self.calculate_rolling_average(data)
        plt.plot(rolling_avg.index, rolling_avg.values, 
                label=f'{window}-Period Moving Average', 
                linewidth=2, linestyle='--')
        
        # Add trend line
        z = np.polyfit(range(len(data)), data.values, 1)
        p = np.poly1d(z)
        plt.plot(data.index, p(range(len(data))), 
                label='Trend Line', 
                linestyle=':', linewidth=2)
        
        plt.title(title, fontsize=14, pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Sales', fontsize=12)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def analyze_seasonality(self, freq: str = 'M', output_dir: Optional[str] = None):
        """Perform complete trend analysis with multiple views."""
        # Resample data
        resampled_data = self.resample_data(freq)
        
        # 1. Basic trend plot
        self.plot_trend(
            resampled_data,
            f'Sales Trend ({freq})',
            f'{output_dir}/sales_trend.png' if output_dir else None
        )
        
        # 2. Year-over-year comparison
        if freq in ['M', 'W']:
            plt.figure(figsize=(12, 6))
            year_data = self.df.groupby([self.df.index.year, 
                                       getattr(self.df.index, 
                                              'month' if freq == 'M' else 'week')])['Sales'].sum()
            year_data = year_data.unstack(0)
            sns.heatmap(year_data, cmap='YlOrRd', annot=True, fmt='.0f')
            plt.title(f'Sales by {"Month" if freq == "M" else "Week"} and Year', 
                     fontsize=14, pad=20)
            plt.tight_layout()
            if output_dir:
                plt.savefig(f'{output_dir}/sales_heatmap.png', dpi=300, bbox_inches='tight')
                plt.close()
            else:
                plt.show()
        
        return resampled_data

def main():
    parser = argparse.ArgumentParser(description='Analyze sales trends and patterns')
    parser.add_argument('--input', '-i', default='sample_sales_data.csv',
                       help='Input CSV file with Date and Sales columns')
    parser.add_argument('--output', '-o', default='charts',
                       help='Output directory for charts')
    parser.add_argument('--frequency', '-f', default='M',
                       choices=['D', 'W', 'M', 'Q'],
                       help='Resampling frequency (D=daily, W=weekly, M=monthly, Q=quarterly)')
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Analyze trends
    analyzer = TrendAnalyzer(args.input)
    analyzer.analyze_seasonality(args.frequency, str(output_dir))
    print(f"Charts saved to {output_dir}/")

if __name__ == "__main__":
    import numpy as np  # Required for trend line calculation
    main()
