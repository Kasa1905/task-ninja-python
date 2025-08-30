# 💱 Currency Converter - Project #10

## 🎯 Problem Statement

Create a Python script that converts one currency to another using live exchange rates from real-time APIs. Build a comprehensive currency conversion tool with historical rates, trend analysis, and multi-currency support.

## 🎓 Learning Objectives

By completing this project, you will learn:
- Working with financial APIs and exchange rates
- Real-time data processing and caching
- Currency code validation and formatting
- Mathematical calculations with precision
- Data visualization and trend analysis
- Building interactive financial tools

## 🔧 Features

- **Real-Time Conversion**: Live exchange rates from multiple APIs
- **Multi-Currency Support**: 170+ currencies worldwide
- **Historical Rates**: Track exchange rate trends
- **Batch Conversion**: Convert multiple amounts at once
- **Rate Alerts**: Set alerts for target exchange rates
- **Favorite Pairs**: Save frequently used currency pairs
- **Offline Mode**: Cached rates when internet unavailable
- **Calculator Mode**: Interactive conversion calculator

## 📋 Requirements

```
requests>=2.28.0
python-dateutil>=2.8.2
matplotlib>=3.6.0
```

## 🚀 How to Run

1. **Navigate to project directory**:
   ```bash
   cd week-2/10-currency-converter
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the currency converter**:
   ```bash
   python main.py
   ```

## 💡 Key Concepts Demonstrated

### 1. Financial APIs
- Exchange rate APIs integration
- Rate fetching and processing
- API fallback mechanisms

### 2. Data Processing
- Currency validation
- Precision handling for financial calculations
- Rate caching and historical tracking

### 3. User Interface
- Interactive CLI with menus
- Input validation and formatting
- Real-time rate updates

## 📊 Sample Usage

### Basic Conversion:
```
💱 Currency Converter - Live Exchange Rates
==========================================
From Currency (USD): USD
To Currency (EUR): EUR
Amount: 100

💰 Conversion Result
===================
100.00 USD = 92.45 EUR
Exchange Rate: 1 USD = 0.9245 EUR
Last Updated: 2024-08-26 14:30:25 UTC

💡 Quick conversions:
   $10 USD = €9.25 EUR
   $50 USD = €46.23 EUR
   $1,000 USD = €924.50 EUR
```

### Historical Analysis:
```
📈 USD/EUR Exchange Rate Trend (7 days)
======================================
2024-08-19: 0.9234 EUR (+0.12%)
2024-08-20: 0.9267 EUR (+0.36%)
2024-08-21: 0.9245 EUR (-0.24%)
2024-08-22: 0.9289 EUR (+0.48%)
2024-08-23: 0.9276 EUR (-0.14%)
2024-08-24: 0.9251 EUR (-0.27%)
2024-08-25: 0.9245 EUR (-0.06%)

📊 Average Rate: 0.9258 EUR
📈 Trend: Slightly Bearish (-0.14%)
```

## 🎯 Learning Outcome

After completing this project, you'll understand:
- Financial API integration patterns
- Currency conversion mathematics
- Real-time data handling
- Financial application development
- Rate trend analysis

## 🏆 Bonus Challenges

1. **Portfolio Tracker**: Track multi-currency investment portfolio
2. **Rate Notifications**: Email/SMS alerts for rate changes
3. **Mobile App**: Convert to mobile application
4. **Crypto Support**: Add cryptocurrency conversions
5. **Trading Simulator**: Build currency trading game

## 🔗 Related Projects

- **Project 8**: API Calls - API integration foundations
- **Project 9**: Weather App - Real-time data applications
- **Project 6**: CSV/Excel Handler - Data export for rates

---

*This is Project #10 in our Python Projects Series. Master financial data! 💱💰*
