# 📊 CSV & Excel Handler - Project #6

## 🎯 Problem Statement

Create a Python script that can read data from CSV files and write it to Excel files (and vice versa). The tool should handle data manipulation, filtering, and format conversion efficiently.

## 🎓 Learning Objectives

By completing this project, you will learn:
- Reading and writing CSV files using pandas
- Excel file manipulation with ExcelWriter
- Data manipulation and transformation
- File format conversion techniques
- Data validation and cleaning
- Error handling for file operations

## 🔧 Features

- **Bidirectional Conversion**: CSV ↔ Excel conversion
- **Data Filtering**: Select specific columns or rows
- **Data Cleaning**: Handle missing values and duplicates
- **Multiple Sheets**: Support for multiple Excel worksheets
- **Data Validation**: Verify data integrity during conversion
- **Batch Processing**: Convert multiple files at once
- **Custom Formatting**: Apply styles to Excel outputs

## 📋 Requirements

```
pandas>=1.5.0
openpyxl>=3.0.0
xlsxwriter>=3.0.0
```

## 🚀 How to Run

1. Navigate to the project directory:
```bash
cd week-2/06-csv-excel-handler
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the handler:
```bash
python main.py
```

## 💡 Key Concepts Demonstrated

### 1. Data Processing
- Reading and writing different file formats
- Data manipulation with pandas DataFrames
- Handling missing and malformed data

### 2. File Operations
- File format detection and validation
- Batch file processing
- Error handling for I/O operations

### 3. Data Analysis
- Data filtering and selection
- Statistical analysis and summaries
- Data visualization preparation

## 📊 Sample Usage

### CSV to Excel Conversion:
```
📊 CSV & Excel Handler
========================
1. 📁 Convert CSV to Excel
2. 📈 Convert Excel to CSV
3. 🔍 View File Data
4. 🧹 Clean Data
5. 📋 Batch Convert

Enter choice: 1
Enter CSV file path: sales_data.csv
Enter output Excel file: sales_report.xlsx

✅ Successfully converted CSV to Excel!
📈 Processed 1,250 rows and 8 columns
💾 Saved to: sales_report.xlsx
```

### Data Preview:
```
📋 Data Preview (first 5 rows):
   Date        Product    Sales  Region
0  2025-01-01  Widget A   1250   North
1  2025-01-02  Widget B   980    South
2  2025-01-03  Widget A   1100   East
3  2025-01-04  Widget C   750    West
4  2025-01-05  Widget B   1300   North

📊 Data Summary:
- Total Rows: 1,250
- Total Columns: 8
- Missing Values: 15
- Data Types: 3 numeric, 5 text
```

## 🎯 Learning Outcome

After completing this project, you'll understand:
- Data manipulation with pandas library
- File I/O operations for different formats
- Data cleaning and validation techniques
- Building data processing pipelines
- Error handling in data operations

## 🏆 Bonus Challenges

1. **Data Visualization**: Generate charts from the data
2. **Database Integration**: Save/load data from databases
3. **API Export**: Send converted data to external APIs
4. **Scheduled Processing**: Automate regular file conversions
5. **GUI Interface**: Create a drag-and-drop file converter

## 🔗 Related Projects

- **Project 7**: JSON Parser - Additional data format handling
- **Project 8**: API Calls - Data from external sources
- **Project 15**: Excel Report Generator - Advanced Excel features

---

*This is Project #6 in our Python Projects Series. Master data processing! 📊🔄*
