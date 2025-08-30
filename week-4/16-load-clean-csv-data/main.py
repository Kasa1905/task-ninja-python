import pandas as pd
import argparse

# --- CLI Arguments ---
def get_args():
    parser = argparse.ArgumentParser(description="Load & Clean CSV Data: Cleans raw CSV for analysis.")
    parser.add_argument('--input', '-i', default='sample_raw_data.csv', help='Path to input CSV file')
    parser.add_argument('--output', '-o', default='cleaned_data.csv', help='Path to output cleaned CSV file')
    return parser.parse_args()

# --- Main Logic ---
def clean_csv(input_csv, output_csv):
    # Load CSV file
    df = pd.read_csv(input_csv)

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Fill missing 'Sales' with 0
    if 'Sales' in df.columns:
        df['Sales'] = df['Sales'].fillna(0)

    # Convert 'Date' column to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Remove rows with missing essential fields
    essential_fields = [col for col in ['Region', 'Product'] if col in df.columns]
    if essential_fields:
        df = df.dropna(subset=essential_fields)

    # Export cleaned data
    df.to_csv(output_csv, index=False)
    print(f"Cleaned data exported to: {output_csv}")

if __name__ == "__main__":
    args = get_args()
    clean_csv(args.input, args.output)
