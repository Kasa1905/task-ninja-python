# 🌍 API Calls - Project #8

## 🎯 Problem Statement

Write a Python script that fetches live data from a public API, processes it, and saves it to a JSON file. The tool should handle various APIs, error scenarios, and data processing operations.

## 🎓 Learning Objectives

By completing this project, you will learn:
- Making GET requests with Python's `requests` module
- Handling API responses and HTTP status codes
- Parsing and processing JSON API data
- Error handling for network operations
- Data extraction and transformation
- API authentication and rate limiting

## 🔧 Features

- **Multiple API Support**: Work with various public APIs
- **Error Handling**: Robust error management for API calls
- **Data Processing**: Extract and transform API responses
- **Rate Limiting**: Handle API rate limits gracefully
- **Data Persistence**: Save processed data to files
- **Authentication**: Support for API keys and tokens
- **Batch Processing**: Handle multiple API requests

## 📋 Requirements

```
requests>=2.28.0
```

## 🚀 How to Run

1. Navigate to the project directory:
```bash
cd week-2/08-api-calls
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the API client:
```bash
python main.py
```

## 💡 Key Concepts Demonstrated

### 1. HTTP Requests
- Making GET, POST, PUT, DELETE requests
- Handling request headers and parameters
- Working with response objects

### 2. API Integration
- Understanding REST API patterns
- Handling different response formats
- Authentication methods

### 3. Error Handling
- Network error management
- HTTP status code handling
- Retry mechanisms

## 📊 Sample Usage

### Random User API:
```
🌍 API Data Fetcher
==================
1. 🧑 Fetch Random Users
2. 📰 Get News Headlines
3. 🪙 Cryptocurrency Prices
4. 🌦️ Weather Data
5. 📊 Custom API Call

Enter choice: 1
How many users to fetch? 5

API Data Fetched Successfully!

📋 Processed user data saved to users.json
✅ Extracted 5 users with names and emails
```

### Custom API Call:
```
📡 Custom API Call
=================
Enter API URL: https://jsonplaceholder.typicode.com/posts
Enter request type (GET/POST): GET

✅ Request successful! Status: 200
📊 Received 100 posts
💾 Data saved to api_response.json
```

## 🎯 Learning Outcome

After completing this project, you'll understand:
- How to interact with REST APIs
- HTTP methods and status codes
- JSON data processing techniques
- Error handling in network programming
- API authentication patterns

## 🏆 Bonus Challenges

1. **API Dashboard**: Create a dashboard showing data from multiple APIs
2. **Data Caching**: Implement caching to reduce API calls
3. **Webhook Handler**: Create endpoints to receive API webhooks
4. **API Monitoring**: Monitor API uptime and response times
5. **GraphQL Support**: Add support for GraphQL APIs

## 🔗 Related Projects

- **Project 7**: JSON Parser - Processing API responses
- **Project 9**: Weather App - Specific API implementation
- **Project 10**: Currency Converter - Real-time API data

---

*This is Project #8 in our Python Projects Series. Master API integration! 🌍📡*
