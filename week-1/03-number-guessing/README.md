# 🎯 Number Guessing Game - Project #3

## 🎯 Problem Statement

Build a CLI game where the user has to guess a randomly generated number within a limited number of attempts. The game should provide feedback and include multiple difficulty levels for enhanced gameplay.

## 🎓 Learning Objectives

By completing this project, you will learn:
- Using the `random` module for generating random numbers
- Implementing game logic with conditional statements
- Creating interactive loops for continuous gameplay
- Building feedback systems for user guidance
- Designing difficulty levels and game balance
- Error handling for user input validation

## 🔧 Features

- **Multiple Difficulty Levels**: Easy, Medium, Hard, and Expert modes
- **Smart Feedback**: "Too high" or "too low" hints
- **Attempt Tracking**: Limited attempts based on difficulty
- **Hint System**: Closest guess hints for challenging situations
- **Game Statistics**: Track games played and completion rates
- **Replay Functionality**: Play multiple rounds
- **Input Validation**: Handle invalid inputs gracefully

## 📋 Requirements

```
# No external dependencies required
# This project uses only built-in Python modules
```

## 🚀 How to Run

1. Navigate to the project directory:
```bash
cd week-1/03-number-guessing
```

2. Run the number guessing game:
```bash
python main.py
```

## 💡 Key Concepts Demonstrated

### 1. Random Number Generation
- Using `random.randint()` for number generation
- Setting ranges based on difficulty levels
- Pseudorandom number concepts

### 2. Game Logic Implementation
- Win/loss conditions
- Attempt limiting and tracking
- Feedback systems for user guidance

### 3. User Experience Design
- Difficulty selection menus
- Clear feedback messages
- Replay mechanisms

## 📊 Sample Gameplay

### Difficulty Selection:
```
🎯 Choose Difficulty Level:
1. Easy (1-50, 10 attempts)
2. Medium (1-100, 7 attempts)  
3. Hard (1-200, 5 attempts)
4. Expert (1-500, 8 attempts)
Enter difficulty (1-4): 2
```

### Game Session:
```
🎲 Medium Mode: Guess the number between 1 and 100
You have 7 attempts. Good luck!

Attempt 1/7
Enter your guess (1-100): 45
📉 Too low!
Attempts remaining: 6

Attempt 2/7
Enter your guess (1-100): 75
📈 Too high!
Attempts remaining: 5

Attempt 3/7
Enter your guess (1-100): 63
🎉 Correct! You guessed it!

🏆 You won in 3 attempts!
Your guesses: 45, 75, 63
```

## 🎯 Learning Outcome

After completing this project, you'll understand:
- How to implement game mechanics in Python
- Random number generation and usage
- Creating engaging user interactions
- Game balance and difficulty scaling
- Input validation in interactive applications

## 🏆 Bonus Challenges

1. **High Score System**: Track best performance for each difficulty
2. **Custom Ranges**: Allow users to set their own number ranges
3. **Time Limits**: Add time pressure to increase difficulty
4. **Multiplayer Mode**: Two-player guessing competition
5. **GUI Version**: Create a graphical interface using tkinter

## 🔗 Related Projects

- **Project 1**: Calculator - Basic input handling concepts
- **Project 2**: To-Do List - Menu-driven application structure
- **Project 5**: Digital Clock - GUI development basics

---

*This is Project #3 in our Python Projects Series. Learn game development fundamentals! 🎮🎯*
