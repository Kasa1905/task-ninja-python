#!/usr/bin/env python3
"""
Number Guessing Game - Project #3
A CLI game where users guess a randomly generated number.

Author: Task Ninja Python Series
Project: Week 1 - Python Mini Projects
"""

import random
from typing import Optional


class NumberGuessingGame:
    """A number guessing game with different difficulty levels."""
    
    def __init__(self, min_number: int = 1, max_number: int = 100, max_attempts: int = 7):
        """
        Initialize the game.
        
        Args:
            min_number (int): Minimum number in range
            max_number (int): Maximum number in range
            max_attempts (int): Maximum attempts allowed
        """
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts
        self.secret_number = random.randint(min_number, max_number)
        self.attempts = 0
        self.guesses = []
        self.game_won = False
    
    def make_guess(self, guess: int) -> str:
        """
        Process a player's guess.
        
        Args:
            guess (int): The player's guess
            
        Returns:
            str: Feedback message
        """
        self.attempts += 1
        self.guesses.append(guess)
        
        if guess == self.secret_number:
            self.game_won = True
            return "🎉 Correct! You guessed it!"
        elif guess < self.secret_number:
            return "📉 Too low!"
        else:
            return "📈 Too high!"
    
    def is_game_over(self) -> bool:
        """Check if game is over."""
        return self.game_won or self.attempts >= self.max_attempts
    
    def get_remaining_attempts(self) -> int:
        """Get remaining attempts."""
        return self.max_attempts - self.attempts
    
    def get_game_summary(self) -> str:
        """Get game summary."""
        if self.game_won:
            return f"🏆 You won in {self.attempts} attempts!"
        else:
            return f"😢 Game over! The number was {self.secret_number}."


def get_difficulty_level() -> tuple:
    """
    Get difficulty level from user.
    
    Returns:
        tuple: (min_num, max_num, max_attempts, level_name)
    """
    print("\n🎯 Choose Difficulty Level:")
    print("1. Easy (1-50, 10 attempts)")
    print("2. Medium (1-100, 7 attempts)")
    print("3. Hard (1-200, 5 attempts)")
    print("4. Expert (1-500, 8 attempts)")
    
    while True:
        choice = input("Enter difficulty (1-4): ").strip()
        
        if choice == '1':
            return (1, 50, 10, "Easy")
        elif choice == '2':
            return (1, 100, 7, "Medium")
        elif choice == '3':
            return (1, 200, 5, "Hard")
        elif choice == '4':
            return (1, 500, 8, "Expert")
        else:
            print("❌ Invalid choice. Please enter 1-4.")


def get_valid_guess(min_num: int, max_num: int) -> int:
    """
    Get a valid guess from user.
    
    Args:
        min_num (int): Minimum valid number
        max_num (int): Maximum valid number
        
    Returns:
        int: Valid guess
    """
    while True:
        try:
            guess = int(input(f"Enter your guess ({min_num}-{max_num}): "))
            if min_num <= guess <= max_num:
                return guess
            else:
                print(f"❌ Please enter a number between {min_num} and {max_num}.")
        except ValueError:
            print("❌ Please enter a valid number.")


def play_game() -> bool:
    """
    Play one game session.
    
    Returns:
        bool: True if player wants to play again
    """
    # Get difficulty level
    min_num, max_num, max_attempts, level = get_difficulty_level()
    
    # Create game instance
    game = NumberGuessingGame(min_num, max_num, max_attempts)
    
    print(f"\n🎲 {level} Mode: Guess the number between {min_num} and {max_num}")
    print(f"You have {max_attempts} attempts. Good luck!")
    print("-" * 50)
    
    # Game loop
    while not game.is_game_over():
        print(f"\nAttempt {game.attempts + 1}/{max_attempts}")
        
        guess = get_valid_guess(min_num, max_num)
        feedback = game.make_guess(guess)
        
        print(feedback)
        
        if not game.game_won and game.get_remaining_attempts() > 0:
            remaining = game.get_remaining_attempts()
            print(f"Attempts remaining: {remaining}")
            
            # Provide hints
            if remaining <= 2 and len(game.guesses) > 1:
                closest = min(game.guesses, key=lambda x: abs(x - game.secret_number))
                print(f"💡 Hint: Your closest guess was {closest}")
    
    # Game over
    print("\n" + "=" * 50)
    print(game.get_game_summary())
    
    if game.guesses:
        print(f"Your guesses: {', '.join(map(str, game.guesses))}")
    
    # Ask to play again
    while True:
        play_again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if play_again in ['y', 'yes']:
            return True
        elif play_again in ['n', 'no']:
            return False
        else:
            print("❌ Please enter 'y' for yes or 'n' for no.")


def show_game_rules():
    """Display game rules."""
    print("\n📖 Game Rules:")
    print("1. I'll think of a number within the chosen range")
    print("2. You have limited attempts to guess it")
    print("3. I'll tell you if your guess is too high or too low")
    print("4. Try to guess the number before running out of attempts!")
    print("5. The fewer attempts you use, the better your score!")


def main():
    """Main function to run the number guessing game."""
    print("🎮 Welcome to the Number Guessing Game!")
    print("=" * 50)
    
    show_game_rules()
    
    games_played = 0
    games_won = 0
    
    while True:
        games_played += 1
        print(f"\n🆕 Game #{games_played}")
        
        if play_game():
            # Check if they won the last game
            continue
        else:
            break
    
    # Final statistics
    if games_played > 0:
        print(f"\n📊 Final Statistics:")
        print(f"Games played: {games_played}")
        print(f"Thanks for playing! 🎉")
    
    print("👋 Goodbye! Come back soon!")


if __name__ == "__main__":
    main()
