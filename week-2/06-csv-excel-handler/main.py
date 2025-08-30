#!/usr/bin/env python3
"""
CSV & Excel Handler - Project #6
Read data from CSV files and write to Excel files (and vice versa).

Author: Task Ninja Python Series
Project: Week 2 - Data Handling & APIs
"""

import pandas as pd
import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any


class CSVExcelHandler:
    """A class to handle CSV and Excel file operations."""
    
    def __init__(self):
        """Initialize the handler."""
        self.current_data: Optional[pd.DataFrame] = None
        self.current_file: Optional[str] = None
    
    def read_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Read data from a CSV file.
        
        Args:
            file_path (str): Path to CSV file
            **kwargs: Additional arguments for pd.read_csv
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"CSV file not found: {file_path}")
            
            # Default parameters
            csv_params = {
                'encoding': 'utf-8',
                'na_values': ['', 'NULL', 'null', 'None'],
                'keep_default_na': True
            }
            csv_params.update(kwargs)
            
            data = pd.read_csv(file_path, **csv_params)
            self.current_data = data
            self.current_file = file_path
            
            print(f"✅ Successfully read CSV file: {file_path}")
            print(f"📊 Shape: {data.shape[0]} rows, {data.shape[1]} columns")
            
            return data
            
        except Exception as e:
            print(f"❌ Error reading CSV file: {e}")
            raise
    
    def read_excel(self, file_path: str, sheet_name: str = 0, **kwargs) -> pd.DataFrame:
        """
        Read data from an Excel file.
        
        Args:
            file_path (str): Path to Excel file
            sheet_name (str): Sheet name or index
            **kwargs: Additional arguments for pd.read_excel
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Excel file not found: {file_path}")
            
            # Default parameters
            excel_params = {
                'sheet_name': sheet_name,
                'na_values': ['', 'NULL', 'null', 'None'],
                'keep_default_na': True
            }
            excel_params.update(kwargs)
            
            data = pd.read_excel(file_path, **excel_params)
            self.current_data = data
            self.current_file = file_path
            
            print(f"✅ Successfully read Excel file: {file_path}")
            print(f"📊 Shape: {data.shape[0]} rows, {data.shape[1]} columns")
            
            return data
            
        except Exception as e:
            print(f"❌ Error reading Excel file: {e}")
            raise
    
    def write_excel(self, data: pd.DataFrame, file_path: str, 
                   sheet_name: str = 'Sheet1', **kwargs) -> None:
        """
        Write data to an Excel file.
        
        Args:
            data (pd.DataFrame): Data to write
            file_path (str): Output file path
            sheet_name (str): Sheet name
            **kwargs: Additional arguments for to_excel
        """
        try:
            # Default parameters
            excel_params = {
                'index': False,
                'sheet_name': sheet_name,
                'engine': 'openpyxl'
            }
            excel_params.update(kwargs)
            
            data.to_excel(file_path, **excel_params)
            
            print(f"✅ Successfully wrote Excel file: {file_path}")
            print(f"📊 Wrote {data.shape[0]} rows and {data.shape[1]} columns")
            
        except Exception as e:
            print(f"❌ Error writing Excel file: {e}")
            raise
    
    def write_csv(self, data: pd.DataFrame, file_path: str, **kwargs) -> None:
        """
        Write data to a CSV file.
        
        Args:
            data (pd.DataFrame): Data to write
            file_path (str): Output file path
            **kwargs: Additional arguments for to_csv
        """
        try:
            # Default parameters
            csv_params = {
                'index': False,
                'encoding': 'utf-8'
            }
            csv_params.update(kwargs)
            
            data.to_csv(file_path, **csv_params)
            
            print(f"✅ Successfully wrote CSV file: {file_path}")
            print(f"📊 Wrote {data.shape[0]} rows and {data.shape[1]} columns")
            
        except Exception as e:
            print(f"❌ Error writing CSV file: {e}")
            raise
    
    def csv_to_excel(self, csv_path: str, excel_path: str, **kwargs) -> None:
        """
        Convert CSV file to Excel file.
        
        Args:
            csv_path (str): Input CSV file path
            excel_path (str): Output Excel file path
            **kwargs: Additional arguments
        """
        print(f"🔄 Converting CSV to Excel...")
        print(f"📁 Input: {csv_path}")
        print(f"📁 Output: {excel_path}")
        
        data = self.read_csv(csv_path)
        self.write_excel(data, excel_path, **kwargs)
        
        print("✅ Conversion completed successfully!")
    
    def excel_to_csv(self, excel_path: str, csv_path: str, 
                    sheet_name: str = 0, **kwargs) -> None:
        """
        Convert Excel file to CSV file.
        
        Args:
            excel_path (str): Input Excel file path
            csv_path (str): Output CSV file path
            sheet_name (str): Sheet name or index
            **kwargs: Additional arguments
        """
        print(f"🔄 Converting Excel to CSV...")
        print(f"📁 Input: {excel_path}")
        print(f"📁 Output: {csv_path}")
        
        data = self.read_excel(excel_path, sheet_name=sheet_name)
        self.write_csv(data, csv_path, **kwargs)
        
        print("✅ Conversion completed successfully!")
    
    def display_data_info(self, data: Optional[pd.DataFrame] = None) -> None:
        """Display information about the data."""
        if data is None:
            data = self.current_data
        
        if data is None:
            print("❌ No data loaded!")
            return
        
        print("\n📊 Data Information:")
        print("=" * 50)
        print(f"Shape: {data.shape[0]} rows × {data.shape[1]} columns")
        print(f"Columns: {list(data.columns)}")
        print(f"Data types:\n{data.dtypes}")
        print(f"Missing values:\n{data.isnull().sum()}")
        
        print("\n📋 First 5 rows:")
        print(data.head())
        
        if data.shape[0] > 5:
            print("\n📋 Last 5 rows:")
            print(data.tail())
    
    def clean_data(self, data: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Clean the data by handling missing values and duplicates.
        
        Args:
            data (pd.DataFrame): Data to clean
            
        Returns:
            pd.DataFrame: Cleaned data
        """
        if data is None:
            data = self.current_data.copy()
        else:
            data = data.copy()
        
        print("🧹 Cleaning data...")
        
        # Remove duplicates
        initial_rows = len(data)
        data = data.drop_duplicates()
        duplicates_removed = initial_rows - len(data)
        
        if duplicates_removed > 0:
            print(f"🗑️  Removed {duplicates_removed} duplicate rows")
        
        # Handle missing values
        missing_info = data.isnull().sum()
        if missing_info.sum() > 0:
            print("🔧 Handling missing values...")
            for column in data.columns:
                if missing_info[column] > 0:
                    if data[column].dtype in ['int64', 'float64']:
                        # Fill numeric columns with median
                        data[column].fillna(data[column].median(), inplace=True)
                        print(f"   📊 {column}: filled with median")
                    else:
                        # Fill text columns with mode or 'Unknown'
                        mode_val = data[column].mode()
                        fill_val = mode_val[0] if len(mode_val) > 0 else 'Unknown'
                        data[column].fillna(fill_val, inplace=True)
                        print(f"   📝 {column}: filled with '{fill_val}'")
        
        print("✅ Data cleaning completed!")
        return data


def simple_conversion():
    """Simple conversion matching the original code."""
    print("📊 Simple CSV to Excel Converter")
    print("=" * 40)
    
    # Read data from CSV
    try:
        csv_data = pd.read_csv("data.csv")
        print("CSV Data:")
        print(csv_data)
        
        # Write to Excel
        csv_data.to_excel("data_output.xlsx", index=False)
        print("\n✅ Data written to Excel file: data_output.xlsx")
        
        # Read back from Excel
        excel_data = pd.read_excel("data_output.xlsx")
        print("\nExcel Data:")
        print(excel_data)
        
        print("\n✅ Conversion completed successfully!")
        
    except FileNotFoundError:
        print("❌ Error: data.csv file not found!")
        print("💡 Create a sample data.csv file or use the interactive mode.")
    except Exception as e:
        print(f"❌ Error: {e}")


def create_sample_data():
    """Create a sample CSV file for testing."""
    sample_data = {
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
        'Age': [28, 34, 45, 29, 52],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
        'Salary': [50000, 75000, 85000, 62000, 95000],
        'Department': ['IT', 'Marketing', 'Finance', 'HR', 'IT']
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('sample_data.csv', index=False)
    
    print("✅ Created sample_data.csv with employee data")
    print("📋 Sample data:")
    print(df)


def interactive_mode():
    """Interactive mode for file operations."""
    handler = CSVExcelHandler()
    
    while True:
        print("\n" + "=" * 50)
        print("📊 CSV & Excel Handler")
        print("=" * 50)
        print("1. 📁 Convert CSV to Excel")
        print("2. 📈 Convert Excel to CSV")
        print("3. 📋 View File Data")
        print("4. 🧹 Clean Data")
        print("5. 📊 Create Sample Data")
        print("6. 🔄 Simple Convert (original code)")
        print("7. 🚪 Exit")
        print("-" * 50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        try:
            if choice == '1':
                csv_path = input("Enter CSV file path: ").strip()
                excel_path = input("Enter output Excel file path: ").strip()
                
                if not excel_path.endswith('.xlsx'):
                    excel_path += '.xlsx'
                
                handler.csv_to_excel(csv_path, excel_path)
            
            elif choice == '2':
                excel_path = input("Enter Excel file path: ").strip()
                csv_path = input("Enter output CSV file path: ").strip()
                
                if not csv_path.endswith('.csv'):
                    csv_path += '.csv'
                
                # Ask for sheet name
                sheet_input = input("Enter sheet name (or press Enter for first sheet): ").strip()
                sheet_name = sheet_input if sheet_input else 0
                
                handler.excel_to_csv(excel_path, csv_path, sheet_name=sheet_name)
            
            elif choice == '3':
                file_path = input("Enter file path (CSV or Excel): ").strip()
                
                if file_path.lower().endswith('.csv'):
                    data = handler.read_csv(file_path)
                elif file_path.lower().endswith(('.xlsx', '.xls')):
                    sheet_input = input("Enter sheet name (or press Enter for first sheet): ").strip()
                    sheet_name = sheet_input if sheet_input else 0
                    data = handler.read_excel(file_path, sheet_name=sheet_name)
                else:
                    print("❌ Unsupported file format! Use .csv, .xlsx, or .xls")
                    continue
                
                handler.display_data_info(data)
            
            elif choice == '4':
                if handler.current_data is None:
                    print("❌ No data loaded! Please load a file first.")
                    continue
                
                cleaned_data = handler.clean_data()
                
                save_choice = input("Save cleaned data? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes']:
                    output_path = input("Enter output file path: ").strip()
                    
                    if output_path.lower().endswith('.csv'):
                        handler.write_csv(cleaned_data, output_path)
                    elif output_path.lower().endswith('.xlsx'):
                        handler.write_excel(cleaned_data, output_path)
                    else:
                        print("❌ Please specify .csv or .xlsx extension")
            
            elif choice == '5':
                create_sample_data()
            
            elif choice == '6':
                simple_conversion()
            
            elif choice == '7':
                print("👋 Thank you for using CSV & Excel Handler!")
                break
            
            else:
                print("❌ Invalid choice! Please select 1-7.")
        
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled.")
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function to run the CSV & Excel handler."""
    print("🎉 Welcome to CSV & Excel Handler!")
    
    # Check if data.csv exists for simple mode
    if len(sys.argv) > 1 and sys.argv[1] == '--simple':
        simple_conversion()
    elif os.path.exists('data.csv'):
        print("🔍 Found data.csv file!")
        choice = input("Run simple conversion? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            simple_conversion()
        else:
            interactive_mode()
    else:
        print("💡 No data.csv found. Starting interactive mode...")
        interactive_mode()


if __name__ == "__main__":
    main()
