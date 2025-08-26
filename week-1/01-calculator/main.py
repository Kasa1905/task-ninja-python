#!/usr/bin/env python3
"""
Calculator (CLI) - Project #1
A simple command-line calculator for basic arithmetic operations.

Author: Task Ninja Python Series
Project: Week 1 - Python Mini Projects
"""


def add(x: float, y: float) -> float:
    """
    Add two numbers.
    
    Args:
        x (float): First number
        y (float): Second number
        
    Returns:
        float: Sum of x and y
    """
    return x + y


def subtract(x: float, y: float) -> float:
    """
    Subtract two numbers.
    
    Args:
        x (float): First number
        y (float): Second number
        
    Returns:
        float: Difference of x and y
    """
    return x - y


def multiply(x: float, y: float) -> float:
    """
    Multiply two numbers.
    
    Args:
        x (float): First number
        y (float): Second number
        
    Returns:
        float: Product of x and y
    """
    return x * y


def divide(x: float, y: float) -> str | float:
    """
    Divide two numbers.
    
    Args:
        x (float): First number (dividend)
        y (float): Second number (divisor)
        
    Returns:
        float | str: Quotient of x and y, or error message if y is 0
    """
    if y == 0:
        return "Error: Division by zero"
    return x / y


def get_number(prompt: str) -> float:
    """
    Get a valid number from user input.
    
    Args:
        prompt (str): The prompt message to display
        
    Returns:
        float: Valid number entered by user
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Please enter a valid number.")


def get_operator() -> str:
    """
    Get a valid operator from user input.
    
    Returns:
        str: Valid operator (+, -, *, /)
    """
    valid_operators = ['+', '-', '*', '/']
    
    while True:
        operator = input("Enter your choice (+, -, *, /): ").strip()
        if operator in valid_operators:
            return operator
        else:
            print("❌ Invalid operator. Please choose from +, -, *, /")


def display_menu():
    """Display the calculator menu."""
    print("\n" + "=" * 30)
    print("🔢 Simple Calculator")
    print("=" * 30)
    print("Choose operation:")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    print("5. Exit")
    print("-" * 30)


def calculate(operator: str, num1: float, num2: float) -> str | float:
    """
    Perform calculation based on operator.
    
    Args:
        operator (str): The operation to perform
        num1 (float): First number
        num2 (float): Second number
        
    Returns:
        str | float: Result of the calculation
    """
    if operator == '+':
        return add(num1, num2)
    elif operator == '-':
        return subtract(num1, num2)
    elif operator == '*':
        return multiply(num1, num2)
    elif operator == '/':
        return divide(num1, num2)
    else:
        return "Invalid operator"


def main():
    """Main function to run the calculator."""
    print("🎉 Welcome to the Simple Calculator!")
    
    while True:
        display_menu()
        
        choice = input("Enter your choice (1-5 or +, -, *, /, exit): ").strip().lower()
        
        if choice in ['5', 'exit', 'quit', 'q']:
            print("👋 Thank you for using the calculator! Goodbye!")
            break
        
        # Handle menu number choices
        if choice == '1':
            operator = '+'
        elif choice == '2':
            operator = '-'
        elif choice == '3':
            operator = '*'
        elif choice == '4':
            operator = '/'
        elif choice in ['+', '-', '*', '/']:
            operator = choice
        else:
            print("❌ Invalid choice. Please try again.")
            continue
        
        # Get numbers from user
        print(f"\nYou selected: {operator}")
        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")
        
        # Perform calculation
        result = calculate(operator, num1, num2)
        
        # Display result
        print(f"\n📊 Result: {num1} {operator} {num2} = {result}")
        
        # Ask if user wants to continue
        continue_calc = input("\nDo you want to perform another calculation? (y/n): ").strip().lower()
        if continue_calc not in ['y', 'yes']:
            print("👋 Thank you for using the calculator! Goodbye!")
            break


if __name__ == "__main__":
    main()
