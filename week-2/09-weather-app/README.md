# 🌦️ Weather App - Project #9

## 🎯 Problem Statement

Create a Python script that fetches and displays live weather information for any city using the OpenWeatherMap API. Build a comprehensive weather application with forecasting, alerts, and data persistence.

## 🎓 Learning Objectives

By completing this project, you will learn:
- Making API requests with authentication
- Parsing and processing weather data
- Handling different units and formats
- Creating interactive CLI applications
- Data caching and persistence
- Error handling for network operations

## 🔧 Features

- **Current Weather**: Get real-time weather for any city
- **5-Day Forecast**: Extended weather predictions
- **Multiple Units**: Celsius, Fahrenheit, Kelvin support
- **Weather Alerts**: Severe weather notifications
- **Data Caching**: Cache data to reduce API calls
- **History Tracking**: Save weather search history
- **Interactive CLI**: User-friendly command interface
- **Weather Maps**: ASCII weather condition displays

## 📋 Requirements

```
requests>=2.28.0
python-dateutil>=2.8.2
colorama>=0.4.6
```

## 🚀 How to Run

1. **Get API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/api) for a free API key

2. **Set Environment Variable**:
   ```bash
   export WEATHER_API_KEY="your_api_key_here"
   ```

3. **Navigate to project directory**:
   ```bash
   cd week-2/09-weather-app
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the weather app**:
   ```bash
   python main.py
   ```

## 💡 Key Concepts Demonstrated

### 1. API Authentication
- API key management
- Environment variable usage
- Secure credential handling

### 2. Data Processing
- JSON response parsing
- Unit conversions
- Date/time formatting

### 3. User Experience
- Interactive CLI interface
- Colorized output
- Progress indicators

## 📊 Sample Usage

### Current Weather:
```
🌦️ Weather App - Live Weather Data
==================================
Enter city name: Mumbai

🌡️ Current Weather in Mumbai, IN
================================
Temperature: 28°C (82°F)
Feels like: 32°C (90°F)
Condition: Partly Cloudy ⛅
Humidity: 78%
Wind: 12 km/h SW
Pressure: 1013 hPa
Visibility: 10 km

🌅 Sun: Rises 06:15 | Sets 18:45
🌙 Moon Phase: Waxing Crescent
```

### 5-Day Forecast:
```
📅 5-Day Weather Forecast for Mumbai
===================================
Today     | 28°C | ⛅ Partly Cloudy  | Rain: 20%
Tomorrow  | 30°C | ☀️ Sunny         | Rain: 10%
Wed       | 27°C | 🌧️ Light Rain     | Rain: 80%
Thu       | 25°C | ⛈️ Thunderstorm   | Rain: 90%
Fri       | 29°C | ⛅ Partly Cloudy  | Rain: 30%
```

## 🎯 Learning Outcome

After completing this project, you'll understand:
- REST API integration and authentication
- Weather data interpretation
- CLI application development
- Data caching strategies
- Error handling patterns

## 🏆 Bonus Challenges

1. **Weather Dashboard**: Create a GUI using tkinter
2. **Weather Alerts**: Email/SMS notifications for severe weather
3. **Historical Data**: Track and analyze weather trends
4. **Location Services**: Auto-detect user location
5. **Weather Maps**: Integrate weather map visualization

## 🔗 Related Projects

- **Project 8**: API Calls - API integration foundations
- **Project 10**: Currency Converter - Another API application
- **Project 6**: CSV/Excel Handler - Data export capabilities

---

*This is Project #9 in our Python Projects Series. Master weather data! 🌦️⛈️*
