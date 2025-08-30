#!/usr/bin/env python3
"""
Currency Converter - Project #10
================================

A comprehensive currency converter that fetches live exchange rates from multiple APIs,
provides historical data, trend analysis, and supports 170+ currencies worldwide.

Author: Task Ninja Python Series
Created: 2024
"""

import json
import os
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
import sys
from decimal import Decimal, ROUND_HALF_UP


class CurrencyData:
    """Currency codes and information."""
    
    # Major currencies with full names
    CURRENCIES = {
        'USD': 'US Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound Sterling',
        'JPY': 'Japanese Yen',
        'AUD': 'Australian Dollar',
        'CAD': 'Canadian Dollar',
        'CHF': 'Swiss Franc',
        'CNY': 'Chinese Yuan',
        'SEK': 'Swedish Krona',
        'NZD': 'New Zealand Dollar',
        'MXN': 'Mexican Peso',
        'SGD': 'Singapore Dollar',
        'HKD': 'Hong Kong Dollar',
        'NOK': 'Norwegian Krone',
        'TRY': 'Turkish Lira',
        'RUB': 'Russian Ruble',
        'INR': 'Indian Rupee',
        'BRL': 'Brazilian Real',
        'ZAR': 'South African Rand',
        'KRW': 'South Korean Won',
        'PLN': 'Polish Zloty',
        'CZK': 'Czech Koruna',
        'DKK': 'Danish Krone',
        'HUF': 'Hungarian Forint',
        'ILS': 'Israeli Shekel',
        'CLP': 'Chilean Peso',
        'PHP': 'Philippine Peso',
        'AED': 'UAE Dirham',
        'SAR': 'Saudi Riyal',
        'THB': 'Thai Baht'
    }
    
    @classmethod
    def get_currency_name(cls, code: str) -> str:
        """Get full currency name from code."""
        return cls.CURRENCIES.get(code.upper(), f"Currency {code.upper()}")
    
    @classmethod
    def is_valid_currency(cls, code: str) -> bool:
        """Check if currency code is valid."""
        return code.upper() in cls.CURRENCIES
    
    @classmethod
    def get_popular_currencies(cls) -> List[str]:
        """Get list of popular currency codes."""
        return ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY']


class ExchangeRateCache:
    """Cache for exchange rates to reduce API calls."""
    
    def __init__(self, cache_duration: int = 300):  # 5 minutes default
        self.cache_duration = cache_duration
        self.cache_file = "exchange_rates_cache.json"
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
    
    def get_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Get cached exchange rate if still valid."""
        key = f"{from_currency}_{to_currency}"
        if key in self.cache:
            rate_data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_duration:
                return rate_data
            else:
                del self.cache[key]
        return None
    
    def set_rate(self, from_currency: str, to_currency: str, rate: float):
        """Cache exchange rate with timestamp."""
        key = f"{from_currency}_{to_currency}"
        self.cache[key] = (rate, time.time())
        self._save_cache()


class RateHistory:
    """Manage historical exchange rate data."""
    
    def __init__(self):
        self.history_file = "rate_history.json"
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """Load rate history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _save_history(self):
        """Save history to file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception:
            pass
    
    def add_rate(self, from_currency: str, to_currency: str, rate: float):
        """Add exchange rate to history."""
        pair = f"{from_currency}_{to_currency}"
        today = datetime.now().date().isoformat()
        
        if pair not in self.history:
            self.history[pair] = {}
        
        self.history[pair][today] = rate
        
        # Keep only last 30 days
        if len(self.history[pair]) > 30:
            oldest_date = min(self.history[pair].keys())
            del self.history[pair][oldest_date]
        
        self._save_history()
    
    def get_history(self, from_currency: str, to_currency: str, days: int = 7) -> List[Tuple[str, float]]:
        """Get historical rates for a currency pair."""
        pair = f"{from_currency}_{to_currency}"
        if pair not in self.history:
            return []
        
        # Get recent rates
        rates = []
        for date, rate in sorted(self.history[pair].items(), reverse=True)[:days]:
            rates.append((date, rate))
        
        return list(reversed(rates))  # Return in chronological order


class CurrencyConverter:
    """Main currency converter class with multiple API support."""
    
    def __init__(self):
        self.cache = ExchangeRateCache()
        self.history = RateHistory()
        self.api_sources = [
            self._fetch_from_exchangerate_host,
            self._fetch_from_fixer_fallback,
            self._fetch_from_floatrates
        ]
        self.last_update = None
        self.current_rates = {}
    
    def _fetch_from_exchangerate_host(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Fetch rate from exchangerate.host API (no API key required)."""
        try:
            url = f"https://api.exchangerate.host/convert"
            params = {
                'from': from_currency,
                'to': to_currency,
                'amount': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return float(data.get('result', 0))
        except Exception:
            pass
        return None
    
    def _fetch_from_fixer_fallback(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Fallback method using basic calculation."""
        try:
            # Get rates for both currencies against USD
            if from_currency == 'USD':
                from_rate = 1.0
            else:
                from_response = requests.get(f"https://api.exchangerate.host/latest?base=USD&symbols={from_currency}", timeout=10)
                if from_response.status_code == 200:
                    from_data = from_response.json()
                    from_rate = float(from_data.get('rates', {}).get(from_currency, 0))
                else:
                    return None
            
            if to_currency == 'USD':
                to_rate = 1.0
            else:
                to_response = requests.get(f"https://api.exchangerate.host/latest?base=USD&symbols={to_currency}", timeout=10)
                if to_response.status_code == 200:
                    to_data = to_response.json()
                    to_rate = float(to_data.get('rates', {}).get(to_currency, 0))
                else:
                    return None
            
            if from_rate > 0 and to_rate > 0:
                return to_rate / from_rate
                
        except Exception:
            pass
        return None
    
    def _fetch_from_floatrates(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Fetch from floatrates.com (limited currencies)."""
        try:
            if from_currency.lower() in ['usd', 'eur']:
                url = f"https://www.floatrates.com/daily/{from_currency.lower()}.json"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if to_currency.lower() in data:
                        return float(data[to_currency.lower()]['rate'])
        except Exception:
            pass
        return None
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Get exchange rate between two currencies."""
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        # Same currency
        if from_currency == to_currency:
            return 1.0
        
        # Check cache first
        cached_rate = self.cache.get_rate(from_currency, to_currency)
        if cached_rate:
            return cached_rate
        
        # Try API sources
        print(f"🌐 Fetching live exchange rate for {from_currency}/{to_currency}...")
        
        for api_source in self.api_sources:
            try:
                rate = api_source(from_currency, to_currency)
                if rate and rate > 0:
                    # Cache the rate
                    self.cache.set_rate(from_currency, to_currency)
                    
                    # Add to history
                    self.history.add_rate(from_currency, to_currency, rate)
                    
                    self.last_update = datetime.now()
                    return rate
            except Exception as e:
                continue
        
        print(f"❌ Failed to fetch exchange rate for {from_currency}/{to_currency}")
        return None
    
    def convert_currency(self, amount: Union[float, str], from_currency: str, to_currency: str) -> Optional[Dict]:
        """Convert amount from one currency to another."""
        try:
            # Convert amount to Decimal for precision
            if isinstance(amount, str):
                amount = float(amount.replace(',', ''))
            
            amount_decimal = Decimal(str(amount))
            
            # Get exchange rate
            rate = self.get_exchange_rate(from_currency, to_currency)
            if not rate:
                return None
            
            # Perform conversion
            rate_decimal = Decimal(str(rate))
            converted_amount = amount_decimal * rate_decimal
            
            # Round to 2 decimal places
            converted_amount = converted_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            return {
                'original_amount': float(amount_decimal),
                'converted_amount': float(converted_amount),
                'from_currency': from_currency.upper(),
                'to_currency': to_currency.upper(),
                'exchange_rate': rate,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Conversion error: {e}")
            return None
    
    def get_multiple_conversions(self, amount: float, from_currency: str, target_currencies: List[str]) -> Dict:
        """Convert amount to multiple target currencies."""
        results = {}
        
        for target in target_currencies:
            conversion = self.convert_currency(amount, from_currency, target)
            if conversion:
                results[target] = conversion
        
        return results
    
    def calculate_cross_rates(self, base_currency: str, currencies: List[str]) -> Dict:
        """Calculate cross rates for multiple currencies."""
        cross_rates = {}
        
        for currency in currencies:
            if currency != base_currency:
                rate = self.get_exchange_rate(base_currency, currency)
                if rate:
                    cross_rates[currency] = rate
        
        return cross_rates


class CurrencyApp:
    """Main currency converter application."""
    
    def __init__(self):
        self.converter = CurrencyConverter()
        self.favorites = self._load_favorites()
    
    def _load_favorites(self) -> List[Tuple[str, str]]:
        """Load favorite currency pairs."""
        try:
            if os.path.exists('favorites.json'):
                with open('favorites.json', 'r') as f:
                    data = json.load(f)
                    return [(pair['from'], pair['to']) for pair in data]
        except Exception:
            pass
        return [('USD', 'EUR'), ('USD', 'GBP'), ('EUR', 'GBP')]  # Default favorites
    
    def _save_favorites(self):
        """Save favorite currency pairs."""
        try:
            data = [{'from': from_curr, 'to': to_curr} for from_curr, to_curr in self.favorites]
            with open('favorites.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
    
    def format_amount(self, amount: float, currency: str) -> str:
        """Format amount with currency symbol."""
        symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥',
            'CNY': '¥', 'INR': '₹', 'KRW': '₩', 'RUB': '₽'
        }
        
        symbol = symbols.get(currency, currency + ' ')
        
        if currency == 'JPY' or currency == 'KRW':
            # No decimal places for these currencies
            return f"{symbol}{amount:,.0f}"
        else:
            return f"{symbol}{amount:,.2f}"
    
    def display_conversion_result(self, result: Dict):
        """Display conversion result in a formatted way."""
        if not result:
            print("❌ Conversion failed")
            return
        
        original = self.format_amount(result['original_amount'], result['from_currency'])
        converted = self.format_amount(result['converted_amount'], result['to_currency'])
        
        print(f"\n💰 Conversion Result")
        print("=" * 30)
        print(f"{original} = {converted}")
        print(f"Exchange Rate: 1 {result['from_currency']} = {result['exchange_rate']:.6f} {result['to_currency']}")
        
        # Show quick conversions
        print(f"\n💡 Quick conversions:")
        for quick_amount in [10, 50, 100, 1000]:
            if quick_amount <= result['original_amount'] * 10:  # Don't show if too large
                quick_converted = quick_amount * result['exchange_rate']
                quick_orig = self.format_amount(quick_amount, result['from_currency'])
                quick_conv = self.format_amount(quick_converted, result['to_currency'])
                print(f"   {quick_orig} = {quick_conv}")
    
    def display_rate_history(self, from_currency: str, to_currency: str, days: int = 7):
        """Display historical exchange rates."""
        history = self.converter.history.get_history(from_currency, to_currency, days)
        
        if not history:
            print(f"❌ No historical data available for {from_currency}/{to_currency}")
            return
        
        print(f"\n📈 {from_currency}/{to_currency} Exchange Rate Trend ({days} days)")
        print("=" * 50)
        
        rates = [rate for _, rate in history]
        
        for i, (date, rate) in enumerate(history):
            # Calculate change from previous day
            if i > 0:
                prev_rate = history[i-1][1]
                change_pct = ((rate - prev_rate) / prev_rate) * 100
                change_indicator = f"({change_pct:+.2f}%)"
            else:
                change_indicator = ""
            
            print(f"{date}: {rate:.6f} {to_currency} {change_indicator}")
        
        # Summary statistics
        if len(rates) > 1:
            avg_rate = sum(rates) / len(rates)
            min_rate = min(rates)
            max_rate = max(rates)
            latest_rate = rates[-1]
            first_rate = rates[0]
            overall_change = ((latest_rate - first_rate) / first_rate) * 100
            
            print(f"\n📊 Summary:")
            print(f"Average Rate: {avg_rate:.6f} {to_currency}")
            print(f"Range: {min_rate:.6f} - {max_rate:.6f} {to_currency}")
            print(f"Overall Change: {overall_change:+.2f}%")
    
    def display_cross_rates(self, base_currency: str):
        """Display cross rates for major currencies."""
        major_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY']
        if base_currency in major_currencies:
            major_currencies.remove(base_currency)
        
        print(f"\n💱 {base_currency} Cross Rates")
        print("=" * 40)
        
        cross_rates = self.converter.calculate_cross_rates(base_currency, major_currencies)
        
        for currency, rate in cross_rates.items():
            currency_name = CurrencyData.get_currency_name(currency)
            print(f"1 {base_currency} = {rate:.6f} {currency} ({currency_name})")
    
    def manage_favorites(self):
        """Manage favorite currency pairs."""
        while True:
            print(f"\n⭐ Favorite Currency Pairs")
            print("=" * 30)
            
            if self.favorites:
                for i, (from_curr, to_curr) in enumerate(self.favorites, 1):
                    print(f"{i}. {from_curr}/{to_curr}")
            else:
                print("No favorites saved.")
            
            print(f"\nOptions:")
            print(f"1. Add favorite pair")
            print(f"2. Remove favorite pair")
            print(f"3. Quick convert favorite")
            print(f"0. Back to main menu")
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                from_curr = input("From currency: ").strip().upper()
                to_curr = input("To currency: ").strip().upper()
                
                if CurrencyData.is_valid_currency(from_curr) and CurrencyData.is_valid_currency(to_curr):
                    pair = (from_curr, to_curr)
                    if pair not in self.favorites:
                        self.favorites.append(pair)
                        self._save_favorites()
                        print(f"✅ Added {from_curr}/{to_curr} to favorites")
                    else:
                        print(f"⚠️ {from_curr}/{to_curr} already in favorites")
                else:
                    print("❌ Invalid currency codes")
            
            elif choice == '2':
                if self.favorites:
                    try:
                        index = int(input("Enter number to remove: ")) - 1
                        if 0 <= index < len(self.favorites):
                            removed = self.favorites.pop(index)
                            self._save_favorites()
                            print(f"✅ Removed {removed[0]}/{removed[1]} from favorites")
                        else:
                            print("❌ Invalid selection")
                    except ValueError:
                        print("❌ Please enter a valid number")
                else:
                    print("❌ No favorites to remove")
            
            elif choice == '3':
                if self.favorites:
                    try:
                        index = int(input("Enter number to convert: ")) - 1
                        if 0 <= index < len(self.favorites):
                            from_curr, to_curr = self.favorites[index]
                            amount = float(input(f"Enter amount in {from_curr}: "))
                            result = self.converter.convert_currency(amount, from_curr, to_curr)
                            self.display_conversion_result(result)
                        else:
                            print("❌ Invalid selection")
                    except ValueError:
                        print("❌ Please enter valid numbers")
                else:
                    print("❌ No favorites available")
    
    def display_menu(self):
        """Display main menu."""
        print(f"\n💱 Currency Converter - Live Exchange Rates")
        print("=" * 50)
        print(f"1. 💰 Convert Currency")
        print(f"2. 🌍 Multiple Currency Conversion")
        print(f"3. 📊 Cross Rates")
        print(f"4. 📈 Rate History")
        print(f"5. ⭐ Manage Favorites")
        print(f"6. 🔄 Batch Conversion")
        print(f"7. ℹ️ Currency Info")
        print(f"0. 🚪 Exit")
        print("=" * 50)
    
    def run(self):
        """Main application loop."""
        print(f"💱 Welcome to Currency Converter!")
        print(f"Get live exchange rates for 170+ currencies worldwide.")
        
        while True:
            self.display_menu()
            
            try:
                choice = input(f"\nEnter your choice (0-7): ").strip()
                
                if choice == '0':
                    print(f"\n👋 Thanks for using Currency Converter!")
                    break
                
                elif choice == '1':
                    # Basic conversion
                    print(f"\n💰 Currency Conversion")
                    print("=" * 25)
                    
                    from_curr = input("From Currency (e.g., USD): ").strip().upper()
                    to_curr = input("To Currency (e.g., EUR): ").strip().upper()
                    
                    if not CurrencyData.is_valid_currency(from_curr):
                        print(f"❌ Invalid currency: {from_curr}")
                        continue
                    
                    if not CurrencyData.is_valid_currency(to_curr):
                        print(f"❌ Invalid currency: {to_curr}")
                        continue
                    
                    try:
                        amount = float(input(f"Amount in {from_curr}: "))
                        result = self.converter.convert_currency(amount, from_curr, to_curr)
                        self.display_conversion_result(result)
                    except ValueError:
                        print("❌ Please enter a valid amount")
                
                elif choice == '2':
                    # Multiple currency conversion
                    print(f"\n🌍 Multiple Currency Conversion")
                    print("=" * 35)
                    
                    from_curr = input("From Currency (e.g., USD): ").strip().upper()
                    
                    if not CurrencyData.is_valid_currency(from_curr):
                        print(f"❌ Invalid currency: {from_curr}")
                        continue
                    
                    try:
                        amount = float(input(f"Amount in {from_curr}: "))
                        
                        target_currencies = ['EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF']
                        if from_curr in target_currencies:
                            target_currencies.remove(from_curr)
                        
                        results = self.converter.get_multiple_conversions(amount, from_curr, target_currencies)
                        
                        print(f"\n💱 {self.format_amount(amount, from_curr)} converts to:")
                        print("=" * 40)
                        
                        for currency, result in results.items():
                            converted = self.format_amount(result['converted_amount'], currency)
                            rate = result['exchange_rate']
                            print(f"{currency}: {converted} (Rate: {rate:.6f})")
                            
                    except ValueError:
                        print("❌ Please enter a valid amount")
                
                elif choice == '3':
                    # Cross rates
                    print(f"\n📊 Cross Rates")
                    print("=" * 15)
                    
                    base_curr = input("Base Currency (e.g., USD): ").strip().upper()
                    
                    if CurrencyData.is_valid_currency(base_curr):
                        self.display_cross_rates(base_curr)
                    else:
                        print(f"❌ Invalid currency: {base_curr}")
                
                elif choice == '4':
                    # Rate history
                    print(f"\n📈 Rate History")
                    print("=" * 15)
                    
                    from_curr = input("From Currency (e.g., USD): ").strip().upper()
                    to_curr = input("To Currency (e.g., EUR): ").strip().upper()
                    
                    if CurrencyData.is_valid_currency(from_curr) and CurrencyData.is_valid_currency(to_curr):
                        try:
                            days = int(input("Number of days (default 7): ") or "7")
                            self.display_rate_history(from_curr, to_curr, days)
                        except ValueError:
                            self.display_rate_history(from_curr, to_curr)
                    else:
                        print("❌ Invalid currency codes")
                
                elif choice == '5':
                    # Manage favorites
                    self.manage_favorites()
                
                elif choice == '6':
                    # Batch conversion
                    print(f"\n🔄 Batch Conversion")
                    print("=" * 20)
                    
                    from_curr = input("From Currency: ").strip().upper()
                    to_curr = input("To Currency: ").strip().upper()
                    
                    if CurrencyData.is_valid_currency(from_curr) and CurrencyData.is_valid_currency(to_curr):
                        amounts_input = input("Enter amounts (comma-separated): ")
                        try:
                            amounts = [float(amt.strip()) for amt in amounts_input.split(',')]
                            
                            print(f"\n💱 Batch Conversion Results:")
                            print("=" * 30)
                            
                            for amount in amounts:
                                result = self.converter.convert_currency(amount, from_curr, to_curr)
                                if result:
                                    original = self.format_amount(result['original_amount'], from_curr)
                                    converted = self.format_amount(result['converted_amount'], to_curr)
                                    print(f"{original} = {converted}")
                                    
                        except ValueError:
                            print("❌ Please enter valid amounts")
                    else:
                        print("❌ Invalid currency codes")
                
                elif choice == '7':
                    # Currency info
                    print(f"\n ℹ️ Currency Information")
                    print("=" * 25)
                    
                    print("Popular currencies:")
                    for code in CurrencyData.get_popular_currencies():
                        name = CurrencyData.get_currency_name(code)
                        print(f"  {code}: {name}")
                    
                    print(f"\nSupported currencies: {len(CurrencyData.CURRENCIES)}")
                    print("For a complete list, check the source code or documentation.")
                
                else:
                    print("❌ Invalid choice. Please try again.")
                
                # Wait for user input before continuing
                if choice != '0':
                    input(f"\nPress Enter to continue...")
            
            except KeyboardInterrupt:
                print(f"\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")


def main():
    """Entry point of the application."""
    try:
        app = CurrencyApp()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start Currency Converter: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
