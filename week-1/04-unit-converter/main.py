#!/usr/bin/env python3
"""
Unit Converter - Project #4
A CLI app that converts units like km to miles, Celsius to Fahrenheit.

Author: Task Ninja Python Series
Project: Week 1 - Python Mini Projects
"""

import sys
from typing import Dict, Callable


class UnitConverter:
    """A comprehensive unit converter with multiple categories."""
    
    def __init__(self):
        """Initialize the converter with all conversion functions."""
        self.converters = {
            'distance': {
                'name': '📏 Distance',
                'functions': {
                    'km_to_miles': ('Kilometers to Miles', self.km_to_miles),
                    'miles_to_km': ('Miles to Kilometers', self.miles_to_km),
                    'km_to_feet': ('Kilometers to Feet', self.km_to_feet),
                    'feet_to_km': ('Feet to Kilometers', self.feet_to_km),
                    'm_to_feet': ('Meters to Feet', self.m_to_feet),
                    'feet_to_m': ('Feet to Meters', self.feet_to_m),
                }
            },
            'temperature': {
                'name': '🌡️ Temperature', 
                'functions': {
                    'c_to_f': ('Celsius to Fahrenheit', self.c_to_f),
                    'f_to_c': ('Fahrenheit to Celsius', self.f_to_c),
                    'c_to_k': ('Celsius to Kelvin', self.c_to_k),
                    'k_to_c': ('Kelvin to Celsius', self.k_to_c),
                    'f_to_k': ('Fahrenheit to Kelvin', self.f_to_k),
                    'k_to_f': ('Kelvin to Fahrenheit', self.k_to_f),
                }
            },
            'weight': {
                'name': '⚖️ Weight',
                'functions': {
                    'kg_to_lb': ('Kilograms to Pounds', self.kg_to_lb),
                    'lb_to_kg': ('Pounds to Kilograms', self.lb_to_kg),
                    'kg_to_oz': ('Kilograms to Ounces', self.kg_to_oz),
                    'oz_to_kg': ('Ounces to Kilograms', self.oz_to_kg),
                    'g_to_oz': ('Grams to Ounces', self.g_to_oz),
                    'oz_to_g': ('Ounces to Grams', self.oz_to_g),
                }
            },
            'volume': {
                'name': '🥤 Volume',
                'functions': {
                    'l_to_gal': ('Liters to Gallons', self.l_to_gal),
                    'gal_to_l': ('Gallons to Liters', self.gal_to_l),
                    'l_to_cups': ('Liters to Cups', self.l_to_cups),
                    'cups_to_l': ('Cups to Liters', self.cups_to_l),
                    'ml_to_oz': ('Milliliters to Fluid Ounces', self.ml_to_oz),
                    'oz_to_ml': ('Fluid Ounces to Milliliters', self.oz_to_ml),
                }
            }
        }
    
    # Distance conversions
    def km_to_miles(self, km: float) -> float:
        """Convert kilometers to miles."""
        return km * 0.621371
    
    def miles_to_km(self, miles: float) -> float:
        """Convert miles to kilometers."""
        return miles / 0.621371
    
    def km_to_feet(self, km: float) -> float:
        """Convert kilometers to feet."""
        return km * 3280.84
    
    def feet_to_km(self, feet: float) -> float:
        """Convert feet to kilometers."""
        return feet / 3280.84
    
    def m_to_feet(self, meters: float) -> float:
        """Convert meters to feet."""
        return meters * 3.28084
    
    def feet_to_m(self, feet: float) -> float:
        """Convert feet to meters."""
        return feet / 3.28084
    
    # Temperature conversions
    def c_to_f(self, celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return (celsius * 9/5) + 32
    
    def f_to_c(self, fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius."""
        return (fahrenheit - 32) * 5/9
    
    def c_to_k(self, celsius: float) -> float:
        """Convert Celsius to Kelvin."""
        return celsius + 273.15
    
    def k_to_c(self, kelvin: float) -> float:
        """Convert Kelvin to Celsius."""
        return kelvin - 273.15
    
    def f_to_k(self, fahrenheit: float) -> float:
        """Convert Fahrenheit to Kelvin."""
        return self.c_to_k(self.f_to_c(fahrenheit))
    
    def k_to_f(self, kelvin: float) -> float:
        """Convert Kelvin to Fahrenheit."""
        return self.c_to_f(self.k_to_c(kelvin))
    
    # Weight conversions
    def kg_to_lb(self, kg: float) -> float:
        """Convert kilograms to pounds."""
        return kg * 2.20462
    
    def lb_to_kg(self, lb: float) -> float:
        """Convert pounds to kilograms."""
        return lb / 2.20462
    
    def kg_to_oz(self, kg: float) -> float:
        """Convert kilograms to ounces."""
        return kg * 35.274
    
    def oz_to_kg(self, oz: float) -> float:
        """Convert ounces to kilograms."""
        return oz / 35.274
    
    def g_to_oz(self, grams: float) -> float:
        """Convert grams to ounces."""
        return grams * 0.035274
    
    def oz_to_g(self, oz: float) -> float:
        """Convert ounces to grams."""
        return oz / 0.035274
    
    # Volume conversions
    def l_to_gal(self, liters: float) -> float:
        """Convert liters to gallons (US)."""
        return liters * 0.264172
    
    def gal_to_l(self, gallons: float) -> float:
        """Convert gallons (US) to liters."""
        return gallons / 0.264172
    
    def l_to_cups(self, liters: float) -> float:
        """Convert liters to cups (US)."""
        return liters * 4.22675
    
    def cups_to_l(self, cups: float) -> float:
        """Convert cups (US) to liters."""
        return cups / 4.22675
    
    def ml_to_oz(self, ml: float) -> float:
        """Convert milliliters to fluid ounces."""
        return ml * 0.033814
    
    def oz_to_ml(self, oz: float) -> float:
        """Convert fluid ounces to milliliters."""
        return oz / 0.033814


def get_valid_number(prompt: str) -> float:
    """Get a valid number from user input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Please enter a valid number.")


def display_main_menu():
    """Display the main category menu."""
    print("\n" + "=" * 40)
    print("🌍 Unit Converter")
    print("=" * 40)
    print("Select conversion category:")
    print("1. 📏 Distance (km, miles, feet, meters)")
    print("2. 🌡️  Temperature (Celsius, Fahrenheit, Kelvin)")
    print("3. ⚖️  Weight (kg, pounds, ounces, grams)")
    print("4. 🥤 Volume (liters, gallons, cups, ml)")
    print("5. 🔄 Quick Convert (original simplified)")
    print("6. 🚪 Exit")
    print("-" * 40)


def display_category_menu(category_data: Dict) -> Dict:
    """Display conversion options for a category."""
    print(f"\n{category_data['name']} Converter")
    print("-" * 30)
    
    functions = list(category_data['functions'].items())
    for i, (key, (name, func)) in enumerate(functions, 1):
        print(f"{i}. {name}")
    
    print(f"{len(functions) + 1}. ← Back to main menu")
    
    return functions


def quick_convert():
    """Simple converter matching the original code."""
    print("\n🌍 Unit Converter (Quick Mode)")
    print("1. Kilometers to Miles")
    print("2. Miles to Kilometers") 
    print("3. Celsius to Fahrenheit")
    print("4. Fahrenheit to Celsius")
    
    choice = input("Choose conversion (1-4): ")
    
    converter = UnitConverter()
    
    try:
        if choice == '1':
            km = get_valid_number("Enter kilometers: ")
            result = converter.km_to_miles(km)
            print(f"{km} km = {result:.2f} miles")
        elif choice == '2':
            miles = get_valid_number("Enter miles: ")
            result = converter.miles_to_km(miles)
            print(f"{miles} miles = {result:.2f} km")
        elif choice == '3':
            c = get_valid_number("Enter Celsius: ")
            result = converter.c_to_f(c)
            print(f"{c}°C = {result:.2f}°F")
        elif choice == '4':
            f = get_valid_number("Enter Fahrenheit: ")
            result = converter.f_to_c(f)
            print(f"{f}°F = {result:.2f}°C")
        else:
            print("❌ Invalid choice.")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function to run the unit converter."""
    print("🎉 Welcome to the Unit Converter!")
    
    converter = UnitConverter()
    
    while True:
        display_main_menu()
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '6':
            print("👋 Thank you for using the Unit Converter! Goodbye!")
            break
        elif choice == '5':
            quick_convert()
            continue
        elif choice in ['1', '2', '3', '4']:
            category_map = {
                '1': 'distance',
                '2': 'temperature', 
                '3': 'weight',
                '4': 'volume'
            }
            
            category = category_map[choice]
            category_data = converter.converters[category]
            
            while True:
                functions = display_category_menu(category_data)
                
                try:
                    sub_choice = int(input(f"Enter choice (1-{len(functions) + 1}): "))
                    
                    if sub_choice == len(functions) + 1:
                        break  # Back to main menu
                    elif 1 <= sub_choice <= len(functions):
                        func_key, (func_name, func) = functions[sub_choice - 1]
                        
                        # Get input value
                        input_prompt = f"Enter value to convert: "
                        value = get_valid_number(input_prompt)
                        
                        # Perform conversion
                        result = func(value)
                        
                        # Display result
                        print(f"✅ {func_name}: {value} = {result:.4f}")
                        
                        # Ask if user wants to continue
                        continue_choice = input("\nContinue with this category? (y/n): ").strip().lower()
                        if continue_choice not in ['y', 'yes']:
                            break
                    else:
                        print("❌ Invalid choice!")
                        
                except ValueError:
                    print("❌ Please enter a valid number!")
                except Exception as e:
                    print(f"❌ Error: {e}")
        else:
            print("❌ Invalid choice! Please select 1-6.")
        
        # Ask if user wants to continue
        print()
        continue_choice = input("Perform another conversion? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            print("👋 Thank you for using the Unit Converter! Goodbye!")
            break


if __name__ == "__main__":
    main()
