#!/usr/bin/env python3
"""
API Calls - Project #8
======================

A comprehensive Python tool for making API calls, processing responses,
and handling various public APIs with error management and data persistence.

Author: Task Ninja Python Series
Created: 2024
"""

import json
import requests
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import sys
from urllib.parse import urlparse, urljoin


class APIClient:
    """
    A versatile API client for making HTTP requests and processing responses.
    """
    
    def __init__(self, base_url: str = "", default_headers: Optional[Dict[str, str]] = None):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for API endpoints
            default_headers: Default headers to include in requests
        """
        self.base_url = base_url
        self.session = requests.Session()
        
        # Set default headers
        default_headers = default_headers or {}
        self.session.headers.update({
            'User-Agent': 'Python-API-Client/1.0',
            'Accept': 'application/json',
            **default_headers
        })
        
        self.request_count = 0
        self.rate_limit = None
        self.last_request_time = 0
    
    def _handle_rate_limit(self):
        """Handle rate limiting between requests."""
        if self.rate_limit:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.rate_limit:
                time.sleep(self.rate_limit - time_since_last)
        
        self.last_request_time = time.time()
    
    def _build_url(self, endpoint: str) -> str:
        """Build complete URL from base URL and endpoint."""
        if endpoint.startswith(('http://', 'https://')):
            return endpoint
        return urljoin(self.base_url, endpoint)
    
    def make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: int = 30
    ) -> Tuple[bool, Dict]:
        """
        Make an HTTP request.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint or full URL
            params: URL parameters
            data: Form data
            json_data: JSON data for request body
            headers: Additional headers
            timeout: Request timeout in seconds
            
        Returns:
            Tuple of (success, response_data)
        """
        try:
            self._handle_rate_limit()
            
            url = self._build_url(endpoint)
            method = method.upper()
            
            # Merge headers
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            print(f"🌐 Making {method} request to: {url}")
            
            # Make the request
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=request_headers,
                timeout=timeout
            )
            
            self.request_count += 1
            
            # Handle response
            response.raise_for_status()
            
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {'text': response.text, 'status_code': response.status_code}
            
            print(f"✅ Request successful! Status: {response.status_code}")
            return True, response_data
            
        except requests.exceptions.RequestException as e:
            error_data = {
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                'url': url
            }
            print(f"❌ Request failed: {e}")
            return False, error_data
    
    def get(self, endpoint: str, **kwargs) -> Tuple[bool, Dict]:
        """Make a GET request."""
        return self.make_request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Tuple[bool, Dict]:
        """Make a POST request."""
        return self.make_request('POST', endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> Tuple[bool, Dict]:
        """Make a PUT request."""
        return self.make_request('PUT', endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Tuple[bool, Dict]:
        """Make a DELETE request."""
        return self.make_request('DELETE', endpoint, **kwargs)


class DataProcessor:
    """
    Process and transform API response data.
    """
    
    @staticmethod
    def extract_fields(data: Dict, fields: List[str]) -> Dict:
        """Extract specific fields from data."""
        extracted = {}
        for field in fields:
            if '.' in field:
                # Handle nested fields
                keys = field.split('.')
                value = data
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        value = None
                        break
                extracted[field] = value
            else:
                extracted[field] = data.get(field)
        return extracted
    
    @staticmethod
    def filter_data(data: List[Dict], condition: callable) -> List[Dict]:
        """Filter data based on a condition function."""
        return [item for item in data if condition(item)]
    
    @staticmethod
    def transform_data(data: List[Dict], transformer: callable) -> List[Dict]:
        """Transform data using a transformer function."""
        return [transformer(item) for item in data]
    
    @staticmethod
    def aggregate_data(data: List[Dict], group_by: str, aggregator: str = 'count') -> Dict:
        """Aggregate data by a field."""
        groups = {}
        for item in data:
            key = item.get(group_by, 'unknown')
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        
        if aggregator == 'count':
            return {k: len(v) for k, v in groups.items()}
        elif aggregator == 'sum':
            return {k: sum(item.get('value', 0) for item in v) for k, v in groups.items()}
        else:
            return groups


class APIDataFetcher:
    """
    Main class for fetching and processing data from various APIs.
    """
    
    def __init__(self):
        self.client = APIClient()
        self.processor = DataProcessor()
        self.output_dir = "api_data"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save_data(self, data: Any, filename: str) -> bool:
        """Save data to a JSON file."""
        try:
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            print(f"💾 Data saved to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Failed to save data: {e}")
            return False
    
    def fetch_random_users(self, count: int = 5) -> Dict:
        """Fetch random user data from RandomUser API."""
        print(f"\n🧑 Fetching {count} random users...")
        
        success, data = self.client.get(
            "https://randomuser.me/api/",
            params={'results': count, 'inc': 'name,email,phone,location,picture'}
        )
        
        if success and 'results' in data:
            users = data['results']
            
            # Process user data
            processed_users = []
            for user in users:
                processed_user = {
                    'full_name': f"{user['name']['first']} {user['name']['last']}",
                    'email': user['email'],
                    'phone': user['phone'],
                    'city': user['location']['city'],
                    'country': user['location']['country'],
                    'picture': user['picture']['medium']
                }
                processed_users.append(processed_user)
            
            result = {
                'fetched_at': datetime.now().isoformat(),
                'count': len(processed_users),
                'users': processed_users
            }
            
            self.save_data(result, 'users.json')
            print(f"📋 Processed {len(processed_users)} users with names and emails")
            return result
        else:
            print("❌ Failed to fetch user data")
            return {}
    
    def fetch_news_headlines(self, category: str = 'technology') -> Dict:
        """Fetch news headlines from NewsAPI (requires API key)."""
        print(f"\n📰 Fetching {category} news headlines...")
        
        # Note: This requires a free API key from newsapi.org
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key:
            print("⚠️ NewsAPI key not found. Set NEWS_API_KEY environment variable.")
            return {}
        
        success, data = self.client.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                'category': category,
                'country': 'us',
                'pageSize': 10,
                'apiKey': api_key
            }
        )
        
        if success and 'articles' in data:
            articles = data['articles']
            
            # Process articles
            processed_articles = []
            for article in articles:
                processed_article = {
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'url': article.get('url'),
                    'published_at': article.get('publishedAt'),
                    'source': article.get('source', {}).get('name')
                }
                processed_articles.append(processed_article)
            
            result = {
                'fetched_at': datetime.now().isoformat(),
                'category': category,
                'count': len(processed_articles),
                'articles': processed_articles
            }
            
            self.save_data(result, f'news_{category}.json')
            print(f"📋 Processed {len(processed_articles)} news articles")
            return result
        else:
            print("❌ Failed to fetch news data")
            return {}
    
    def fetch_crypto_prices(self, coins: List[str] = None) -> Dict:
        """Fetch cryptocurrency prices from CoinGecko API."""
        coins = coins or ['bitcoin', 'ethereum', 'cardano']
        coin_list = ','.join(coins)
        
        print(f"\n🪙 Fetching prices for: {', '.join(coins)}")
        
        success, data = self.client.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                'ids': coin_list,
                'vs_currencies': 'usd,eur',
                'include_24hr_change': 'true'
            }
        )
        
        if success:
            # Process price data
            processed_prices = []
            for coin_id, price_data in data.items():
                processed_price = {
                    'coin': coin_id,
                    'usd_price': price_data.get('usd'),
                    'eur_price': price_data.get('eur'),
                    'change_24h': price_data.get('usd_24h_change')
                }
                processed_prices.append(processed_price)
            
            result = {
                'fetched_at': datetime.now().isoformat(),
                'count': len(processed_prices),
                'prices': processed_prices
            }
            
            self.save_data(result, 'crypto_prices.json')
            print(f"📋 Processed prices for {len(processed_prices)} cryptocurrencies")
            return result
        else:
            print("❌ Failed to fetch crypto data")
            return {}
    
    def fetch_weather_data(self, city: str = 'London') -> Dict:
        """Fetch weather data from OpenWeatherMap API (requires API key)."""
        print(f"\n🌦️ Fetching weather for {city}...")
        
        api_key = os.getenv('WEATHER_API_KEY')
        if not api_key:
            print("⚠️ Weather API key not found. Set WEATHER_API_KEY environment variable.")
            return {}
        
        success, data = self.client.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                'q': city,
                'appid': api_key,
                'units': 'metric'
            }
        )
        
        if success:
            # Process weather data
            result = {
                'fetched_at': datetime.now().isoformat(),
                'city': data.get('name'),
                'country': data.get('sys', {}).get('country'),
                'temperature': data.get('main', {}).get('temp'),
                'feels_like': data.get('main', {}).get('feels_like'),
                'humidity': data.get('main', {}).get('humidity'),
                'description': data.get('weather', [{}])[0].get('description'),
                'wind_speed': data.get('wind', {}).get('speed')
            }
            
            self.save_data(result, f'weather_{city.lower()}.json')
            print(f"📋 Processed weather data for {city}")
            return result
        else:
            print("❌ Failed to fetch weather data")
            return {}
    
    def make_custom_api_call(self, url: str, method: str = 'GET', params: Dict = None) -> Dict:
        """Make a custom API call to any endpoint."""
        print(f"\n📡 Making custom {method} request to {url}")
        
        if method.upper() == 'GET':
            success, data = self.client.get(url, params=params)
        elif method.upper() == 'POST':
            success, data = self.client.post(url, json_data=params)
        else:
            print(f"❌ Method {method} not supported in this demo")
            return {}
        
        if success:
            # Determine data type and count
            if isinstance(data, list):
                count = len(data)
                data_type = "items"
            elif isinstance(data, dict):
                if 'data' in data and isinstance(data['data'], list):
                    count = len(data['data'])
                    data_type = "items"
                else:
                    count = len(data)
                    data_type = "fields"
            else:
                count = 1
                data_type = "item"
            
            result = {
                'fetched_at': datetime.now().isoformat(),
                'url': url,
                'method': method,
                'count': count,
                'data': data
            }
            
            filename = f"api_response_{int(time.time())}.json"
            self.save_data(result, filename)
            print(f"📊 Received {count} {data_type}")
            return result
        else:
            print("❌ Custom API call failed")
            return {}


def display_menu():
    """Display the main menu."""
    print("\n" + "="*40)
    print("🌍 API Data Fetcher")
    print("="*40)
    print("1. 🧑 Fetch Random Users")
    print("2. 📰 Get News Headlines")
    print("3. 🪙 Cryptocurrency Prices")
    print("4. 🌦️ Weather Data")
    print("5. 📡 Custom API Call")
    print("6. 📊 Show Request Statistics")
    print("7. 🗂️ List Saved Data Files")
    print("0. 🚪 Exit")
    print("="*40)


def main():
    """Main application loop."""
    fetcher = APIDataFetcher()
    
    print("🌍 Welcome to API Data Fetcher!")
    print("This tool helps you fetch data from various APIs and save it for analysis.")
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (0-7): ").strip()
            
            if choice == '0':
                print("\n👋 Thanks for using API Data Fetcher!")
                break
            
            elif choice == '1':
                count = input("How many users to fetch? (1-50, default=5): ").strip()
                try:
                    count = int(count) if count else 5
                    count = max(1, min(50, count))  # Limit between 1-50
                except ValueError:
                    count = 5
                
                result = fetcher.fetch_random_users(count)
                if result:
                    print(f"\n✅ Fetched {result['count']} users successfully!")
            
            elif choice == '2':
                print("\nAvailable categories: business, entertainment, general, health, science, sports, technology")
                category = input("Enter category (default=technology): ").strip()
                category = category if category else 'technology'
                
                result = fetcher.fetch_news_headlines(category)
                if result:
                    print(f"\n✅ Fetched {result['count']} news articles!")
            
            elif choice == '3':
                print("\nEnter cryptocurrency IDs (comma-separated)")
                print("Popular: bitcoin, ethereum, cardano, polkadot, chainlink")
                coins_input = input("Coins (default=bitcoin,ethereum,cardano): ").strip()
                
                if coins_input:
                    coins = [coin.strip() for coin in coins_input.split(',')]
                else:
                    coins = ['bitcoin', 'ethereum', 'cardano']
                
                result = fetcher.fetch_crypto_prices(coins)
                if result:
                    print(f"\n✅ Fetched prices for {result['count']} cryptocurrencies!")
            
            elif choice == '4':
                city = input("Enter city name (default=London): ").strip()
                city = city if city else 'London'
                
                result = fetcher.fetch_weather_data(city)
                if result:
                    print(f"\n✅ Fetched weather data for {result['city']}!")
            
            elif choice == '5':
                print("\n📡 Custom API Call")
                print("="*20)
                url = input("Enter API URL: ").strip()
                if not url:
                    print("❌ URL is required")
                    continue
                
                method = input("Enter request type (GET/POST, default=GET): ").strip().upper()
                method = method if method in ['GET', 'POST'] else 'GET'
                
                params = {}
                if method == 'GET':
                    params_input = input("Enter URL parameters (key=value,key2=value2): ").strip()
                    if params_input:
                        try:
                            for param in params_input.split(','):
                                key, value = param.split('=', 1)
                                params[key.strip()] = value.strip()
                        except ValueError:
                            print("⚠️ Invalid parameter format, ignoring...")
                            params = {}
                
                result = fetcher.make_custom_api_call(url, method, params)
                if result:
                    print(f"\n✅ Custom API call successful!")
            
            elif choice == '6':
                print(f"\n📊 Request Statistics")
                print(f"Total requests made: {fetcher.client.request_count}")
                print(f"Output directory: {fetcher.output_dir}")
            
            elif choice == '7':
                print(f"\n🗂️ Saved Data Files in {fetcher.output_dir}:")
                try:
                    files = os.listdir(fetcher.output_dir)
                    json_files = [f for f in files if f.endswith('.json')]
                    if json_files:
                        for i, file in enumerate(json_files, 1):
                            file_path = os.path.join(fetcher.output_dir, file)
                            file_size = os.path.getsize(file_path)
                            print(f"{i:2d}. {file} ({file_size} bytes)")
                    else:
                        print("No data files found.")
                except FileNotFoundError:
                    print("Output directory not found.")
            
            else:
                print("❌ Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
