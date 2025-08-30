#!/usr/bin/env python3
"""
Weather App - Project #9
========================

A comprehensive weather application that fetches live weather data from OpenWeatherMap API,
provides forecasts, alerts, and maintains search history with an interactive CLI interface.

Author: Task Ninja Python Series
Created: 2024
"""

import json
import os
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sys

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback color class
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""


class WeatherIcons:
    """Weather condition icons and representations."""
    
    ICONS = {
        'clear sky': '☀️',
        'few clouds': '🌤️',
        'scattered clouds': '⛅',
        'broken clouds': '☁️',
        'overcast clouds': '☁️',
        'shower rain': '🌦️',
        'rain': '🌧️',
        'thunderstorm': '⛈️',
        'snow': '❄️',
        'mist': '🌫️',
        'fog': '🌫️',
        'haze': '🌫️',
        'dust': '🌪️',
        'sand': '🌪️',
        'smoke': '💨',
        'default': '🌡️'
    }
    
    @classmethod
    def get_icon(cls, description: str) -> str:
        """Get weather icon for description."""
        return cls.ICONS.get(description.lower(), cls.ICONS['default'])


class WeatherCache:
    """Simple caching system for weather data."""
    
    def __init__(self, cache_duration: int = 600):  # 10 minutes default
        self.cache_duration = cache_duration
        self.cache_file = "weather_cache.json"
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load cache from file."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _save_cache(self):
        """Save cache to file."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception:
            pass
    
    def get(self, key: str) -> Optional[Dict]:
        """Get cached data if still valid."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_duration:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, data: Dict):
        """Cache data with timestamp."""
        self.cache[key] = (data, time.time())
        self._save_cache()


class WeatherHistory:
    """Manage weather search history."""
    
    def __init__(self):
        self.history_file = "weather_history.json"
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Load search history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def _save_history(self):
        """Save history to file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception:
            pass
    
    def add_search(self, city: str, weather_data: Dict):
        """Add a search to history."""
        entry = {
            'city': city,
            'searched_at': datetime.now().isoformat(),
            'temperature': weather_data.get('main', {}).get('temp'),
            'condition': weather_data.get('weather', [{}])[0].get('description')
        }
        
        # Keep only last 50 searches
        self.history = [entry] + self.history[:49]
        self._save_history()
    
    def get_recent_cities(self, limit: int = 10) -> List[str]:
        """Get recently searched cities."""
        cities = []
        seen = set()
        for entry in self.history:
            city = entry['city']
            if city not in seen:
                cities.append(city)
                seen.add(city)
                if len(cities) >= limit:
                    break
        return cities


class WeatherFormatter:
    """Format weather data for display."""
    
    @staticmethod
    def format_temperature(temp: float, unit: str = 'C') -> str:
        """Format temperature with unit."""
        if unit.upper() == 'F':
            return f"{temp:.1f}°F"
        elif unit.upper() == 'K':
            return f"{temp:.1f}K"
        else:
            return f"{temp:.1f}°C"
    
    @staticmethod
    def convert_temperature(temp: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between units."""
        if from_unit == to_unit:
            return temp
        
        # Convert to Celsius first
        if from_unit.upper() == 'F':
            celsius = (temp - 32) * 5/9
        elif from_unit.upper() == 'K':
            celsius = temp - 273.15
        else:
            celsius = temp
        
        # Convert from Celsius to target
        if to_unit.upper() == 'F':
            return celsius * 9/5 + 32
        elif to_unit.upper() == 'K':
            return celsius + 273.15
        else:
            return celsius
    
    @staticmethod
    def format_wind_direction(degrees: float) -> str:
        """Convert wind direction degrees to compass direction."""
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    @staticmethod
    def format_time(timestamp: int, timezone_offset: int = 0) -> str:
        """Format Unix timestamp to readable time."""
        dt = datetime.fromtimestamp(timestamp + timezone_offset)
        return dt.strftime("%H:%M")


class WeatherApp:
    """Main weather application class."""
    
    def __init__(self):
        self.api_key = self._get_api_key()
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache = WeatherCache()
        self.history = WeatherHistory()
        self.formatter = WeatherFormatter()
        self.unit = 'C'  # Default temperature unit
    
    def _get_api_key(self) -> str:
        """Get API key from environment variable."""
        api_key = os.getenv('WEATHER_API_KEY')
        if not api_key:
            print(f"{Fore.RED}❌ Error: WEATHER_API_KEY environment variable not set!")
            print(f"{Fore.YELLOW}💡 Get a free API key from: https://openweathermap.org/api")
            print(f"{Fore.CYAN}📝 Set it with: export WEATHER_API_KEY='your_key_here'")
            sys.exit(1)
        return api_key
    
    def _make_request(self, endpoint: str, params: Dict) -> Tuple[bool, Dict]:
        """Make API request with error handling."""
        params['appid'] = self.api_key
        
        try:
            print(f"{Fore.BLUE}🌐 Fetching weather data...")
            response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=10)
            
            if response.status_code == 200:
                return True, response.json()
            elif response.status_code == 404:
                return False, {"error": "City not found"}
            elif response.status_code == 401:
                return False, {"error": "Invalid API key"}
            else:
                return False, {"error": f"API error: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            return False, {"error": f"Network error: {str(e)}"}
    
    def get_current_weather(self, city: str) -> Optional[Dict]:
        """Get current weather for a city."""
        cache_key = f"current_{city.lower()}"
        
        # Check cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            print(f"{Fore.GREEN}📦 Using cached data...")
            return cached_data
        
        params = {
            'q': city,
            'units': 'metric'
        }
        
        success, data = self._make_request('weather', params)
        
        if success:
            self.cache.set(cache_key, data)
            self.history.add_search(city, data)
            return data
        else:
            print(f"{Fore.RED}❌ {data.get('error', 'Unknown error')}")
            return None
    
    def get_forecast(self, city: str, days: int = 5) -> Optional[Dict]:
        """Get weather forecast for a city."""
        cache_key = f"forecast_{city.lower()}_{days}"
        
        # Check cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            print(f"{Fore.GREEN}📦 Using cached forecast data...")
            return cached_data
        
        params = {
            'q': city,
            'units': 'metric',
            'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
        }
        
        success, data = self._make_request('forecast', params)
        
        if success:
            self.cache.set(cache_key, data)
            return data
        else:
            print(f"{Fore.RED}❌ {data.get('error', 'Unknown error')}")
            return None
    
    def display_current_weather(self, weather_data: Dict):
        """Display current weather information."""
        city = weather_data['name']
        country = weather_data['sys']['country']
        
        # Main weather info
        main = weather_data['main']
        weather = weather_data['weather'][0]
        wind = weather_data.get('wind', {})
        
        # Temperature conversions
        temp_c = main['temp']
        temp_f = self.formatter.convert_temperature(temp_c, 'C', 'F')
        feels_like_c = main['feels_like']
        feels_like_f = self.formatter.convert_temperature(feels_like_c, 'C', 'F')
        
        # Weather icon
        icon = WeatherIcons.get_icon(weather['description'])
        
        # Display header
        print(f"\n{Style.BRIGHT}{Fore.CYAN}🌡️ Current Weather in {city}, {country}")
        print("=" * 50)
        
        # Temperature
        print(f"{Fore.YELLOW}Temperature: {Style.BRIGHT}{temp_c:.1f}°C{Style.RESET_ALL} ({temp_f:.1f}°F)")
        print(f"{Fore.YELLOW}Feels like: {feels_like_c:.1f}°C ({feels_like_f:.1f}°F)")
        
        # Condition
        print(f"{Fore.GREEN}Condition: {weather['description'].title()} {icon}")
        
        # Additional details
        print(f"{Fore.BLUE}Humidity: {main['humidity']}%")
        print(f"{Fore.BLUE}Pressure: {main['pressure']} hPa")
        
        # Wind information
        if 'speed' in wind:
            wind_speed_kmh = wind['speed'] * 3.6  # Convert m/s to km/h
            wind_dir = ""
            if 'deg' in wind:
                wind_dir = f" {self.formatter.format_wind_direction(wind['deg'])}"
            print(f"{Fore.MAGENTA}Wind: {wind_speed_kmh:.1f} km/h{wind_dir}")
        
        # Visibility
        if 'visibility' in weather_data:
            visibility_km = weather_data['visibility'] / 1000
            print(f"{Fore.CYAN}Visibility: {visibility_km:.1f} km")
        
        # Sunrise/Sunset
        if 'sys' in weather_data:
            sys_data = weather_data['sys']
            timezone_offset = weather_data.get('timezone', 0)
            
            if 'sunrise' in sys_data and 'sunset' in sys_data:
                sunrise = self.formatter.format_time(sys_data['sunrise'], timezone_offset)
                sunset = self.formatter.format_time(sys_data['sunset'], timezone_offset)
                print(f"{Fore.YELLOW}🌅 Sun: Rises {sunrise} | Sets {sunset}")
    
    def display_forecast(self, forecast_data: Dict, days: int = 5):
        """Display weather forecast."""
        city = forecast_data['city']['name']
        country = forecast_data['city']['country']
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}📅 {days}-Day Weather Forecast for {city}, {country}")
        print("=" * 60)
        
        # Group forecasts by day
        daily_forecasts = {}
        for item in forecast_data['list'][:days * 8]:
            date = datetime.fromtimestamp(item['dt']).date()
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)
        
        # Display daily summaries
        for i, (date, forecasts) in enumerate(list(daily_forecasts.items())[:days]):
            # Get day name
            if i == 0:
                day_name = "Today"
            elif i == 1:
                day_name = "Tomorrow"
            else:
                day_name = date.strftime("%a")
            
            # Calculate daily averages
            temps = [f['main']['temp'] for f in forecasts]
            conditions = [f['weather'][0]['description'] for f in forecasts]
            rain_probs = [f.get('pop', 0) * 100 for f in forecasts]
            
            avg_temp = sum(temps) / len(temps)
            max_temp = max(temps)
            min_temp = min(temps)
            most_common_condition = max(set(conditions), key=conditions.count)
            max_rain_prob = max(rain_probs) if rain_probs else 0
            
            # Get icon
            icon = WeatherIcons.get_icon(most_common_condition)
            
            # Format display
            temp_display = f"{avg_temp:.0f}°C ({min_temp:.0f}-{max_temp:.0f})"
            condition_display = most_common_condition.title()
            rain_display = f"Rain: {max_rain_prob:.0f}%"
            
            print(f"{Fore.YELLOW}{day_name:<10} | {Fore.GREEN}{temp_display:<12} | {icon} {condition_display:<15} | {Fore.BLUE}{rain_display}")
    
    def display_history(self):
        """Display weather search history."""
        if not self.history.history:
            print(f"{Fore.YELLOW}📝 No search history found.")
            return
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}📝 Recent Weather Searches")
        print("=" * 50)
        
        for i, entry in enumerate(self.history.history[:10], 1):
            searched_time = datetime.fromisoformat(entry['searched_at']).strftime("%m/%d %H:%M")
            city = entry['city']
            temp = entry.get('temperature', 'N/A')
            condition = entry.get('condition', 'N/A')
            
            temp_display = f"{temp:.1f}°C" if isinstance(temp, (int, float)) else temp
            print(f"{i:2d}. {Fore.YELLOW}{city:<15} | {Fore.GREEN}{temp_display:<8} | {Fore.BLUE}{condition.title():<15} | {Fore.CYAN}{searched_time}")
    
    def display_menu(self):
        """Display main menu."""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}🌦️ Weather App - Live Weather Data")
        print("=" * 50)
        print(f"{Fore.GREEN}1. 🌡️ Current Weather")
        print(f"{Fore.GREEN}2. 📅 5-Day Forecast")
        print(f"{Fore.GREEN}3. 🌍 Compare Cities")
        print(f"{Fore.GREEN}4. 📝 Search History")
        print(f"{Fore.GREEN}5. ⚙️ Settings")
        print(f"{Fore.GREEN}6. ℹ️ About")
        print(f"{Fore.RED}0. 🚪 Exit")
        print("=" * 50)
    
    def compare_cities(self, cities: List[str]):
        """Compare weather across multiple cities."""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}🌍 Weather Comparison")
        print("=" * 60)
        
        weather_data = []
        for city in cities:
            data = self.get_current_weather(city)
            if data:
                weather_data.append(data)
        
        if not weather_data:
            print(f"{Fore.RED}❌ No valid weather data found for comparison.")
            return
        
        # Display comparison table
        print(f"{Fore.YELLOW}{'City':<15} | {'Temp':<8} | {'Condition':<15} | {'Humidity':<8} | {'Wind':<10}")
        print("-" * 60)
        
        for data in weather_data:
            city = data['name']
            temp = f"{data['main']['temp']:.1f}°C"
            condition = data['weather'][0]['description'].title()
            humidity = f"{data['main']['humidity']}%"
            wind_speed = data.get('wind', {}).get('speed', 0) * 3.6
            wind = f"{wind_speed:.1f} km/h"
            
            print(f"{Fore.CYAN}{city:<15} | {Fore.GREEN}{temp:<8} | {Fore.BLUE}{condition:<15} | {Fore.MAGENTA}{humidity:<8} | {Fore.YELLOW}{wind:<10}")
    
    def run(self):
        """Main application loop."""
        print(f"{Style.BRIGHT}{Fore.GREEN}🌦️ Welcome to Weather App!")
        print(f"{Fore.CYAN}Get live weather data for any city worldwide.")
        
        while True:
            self.display_menu()
            
            try:
                choice = input(f"\n{Fore.WHITE}Enter your choice (0-6): ").strip()
                
                if choice == '0':
                    print(f"\n{Fore.GREEN}👋 Thanks for using Weather App!")
                    break
                
                elif choice == '1':
                    # Current weather
                    city = input(f"{Fore.CYAN}Enter city name: ").strip()
                    if city:
                        weather_data = self.get_current_weather(city)
                        if weather_data:
                            self.display_current_weather(weather_data)
                    else:
                        print(f"{Fore.RED}❌ City name cannot be empty.")
                
                elif choice == '2':
                    # 5-day forecast
                    city = input(f"{Fore.CYAN}Enter city name: ").strip()
                    if city:
                        forecast_data = self.get_forecast(city)
                        if forecast_data:
                            self.display_forecast(forecast_data)
                    else:
                        print(f"{Fore.RED}❌ City name cannot be empty.")
                
                elif choice == '3':
                    # Compare cities
                    print(f"{Fore.CYAN}Enter cities to compare (comma-separated):")
                    cities_input = input("Cities: ").strip()
                    if cities_input:
                        cities = [city.strip() for city in cities_input.split(',')]
                        if len(cities) >= 2:
                            self.compare_cities(cities)
                        else:
                            print(f"{Fore.RED}❌ Please enter at least 2 cities.")
                    else:
                        print(f"{Fore.RED}❌ No cities entered.")
                
                elif choice == '4':
                    # Search history
                    self.display_history()
                
                elif choice == '5':
                    # Settings
                    print(f"\n{Fore.CYAN}⚙️ Settings")
                    print(f"Current temperature unit: {self.unit}")
                    new_unit = input("Enter temperature unit (C/F/K): ").strip().upper()
                    if new_unit in ['C', 'F', 'K']:
                        self.unit = new_unit
                        print(f"{Fore.GREEN}✅ Temperature unit set to {new_unit}")
                    else:
                        print(f"{Fore.RED}❌ Invalid unit. Use C, F, or K.")
                
                elif choice == '6':
                    # About
                    print(f"\n{Style.BRIGHT}{Fore.CYAN}ℹ️ About Weather App")
                    print("=" * 30)
                    print(f"{Fore.GREEN}📱 Weather App v1.0")
                    print(f"{Fore.BLUE}🌍 Powered by OpenWeatherMap API")
                    print(f"{Fore.YELLOW}👨‍💻 Task Ninja Python Series")
                    print(f"{Fore.MAGENTA}📊 Features: Current weather, forecasts, history, comparisons")
                
                else:
                    print(f"{Fore.RED}❌ Invalid choice. Please try again.")
                
                # Wait for user input before continuing
                if choice != '0':
                    input(f"\n{Fore.WHITE}Press Enter to continue...")
            
            except KeyboardInterrupt:
                print(f"\n\n{Fore.GREEN}👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n{Fore.RED}❌ An error occurred: {e}")


def main():
    """Entry point of the application."""
    try:
        app = WeatherApp()
        app.run()
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to start Weather App: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
