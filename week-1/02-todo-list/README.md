# 📝 To-Do List (CLI) - Project #2

## 🎯 Problem Statement

Create a command-line To-Do List app that lets users add, view, delete, and manage tasks during a session. The app should persist tasks between sessions and provide an intuitive interface for task management.

## 🎓 Learning Objectives

By completing this project, you will learn:
- List operations and data manipulation in Python
- Using loops and conditional statements effectively
- Handling user input and menu systems
- File I/O operations for data persistence
- JSON data handling for structured storage
- Basic CLI application architecture

## 🔧 Features

- **Task Management**: Add, view, edit, and delete tasks
- **Task Status**: Mark tasks as completed/incomplete
- **Priority Levels**: Assign priority levels to tasks
- **Data Persistence**: Save tasks to JSON file
- **Statistics**: View completion rates and task counts
- **User-Friendly Interface**: Clear menus and navigation
- **Error Handling**: Input validation and error management

## 📋 Requirements

```
# No external dependencies required  
# This project uses only built-in Python modules
```

## 🚀 How to Run

1. Navigate to the project directory:
```bash
cd week-1/02-todo-list
```

2. Run the to-do list app:
```bash
python main.py
```

## 💡 Key Concepts Demonstrated

### 1. Data Structures
- Working with lists and dictionaries
- JSON serialization and deserialization
- Data persistence patterns

### 2. User Interface Design
- Menu-driven application structure
- Input validation and error handling
- User experience considerations

### 3. File Operations
- Reading and writing JSON files
- Error handling for file operations
- Data backup and recovery

## 📊 Sample Usage

### Main Menu:
```
📝 To-Do List Manager
========================================
1. 👀 View Tasks
2. ➕ Add Task
3. ✅ Complete Task
4. ✏️  Edit Task
5. 🗑️  Delete Task
6. 📊 Show Statistics
7. 🚪 Exit
```

### Adding a Task:
```
📝 Enter task: Learn Python fundamentals
Enter priority (L)ow, (N)ormal, (H)igh [N]: H
✅ Task added: 'Learn Python fundamentals'
```

### Viewing Tasks:
```
📋 Your Tasks:
--------------------------------------------------
 1. ⭕ Learn Python fundamentals
    Priority: High | Created: 2025-08-26 10:30
 
 2. ✅ Complete project documentation
    Priority: Normal | Created: 2025-08-26 09:15
    Completed: 2025-08-26 11:45
```

## 🎯 Learning Outcome

After completing this project, you'll understand:
- How to structure a CLI application with multiple features
- Data persistence techniques using JSON
- User input validation and error handling
- Menu-driven program architecture
- Task management system implementation

## 🏆 Bonus Challenges

1. **Due Dates**: Add deadline functionality for tasks
2. **Categories**: Organize tasks by categories or projects
3. **Search**: Implement task search functionality
4. **Export**: Export tasks to CSV or other formats
5. **Reminders**: Add notification system for due tasks

## 🔗 Related Projects

- **Project 1**: Calculator - Basic user input handling
- **Project 6**: CSV handling for task export functionality
- **Project 11**: File organization concepts

---

*This is Project #2 in our Python Projects Series. Perfect for learning data structures! 📝✨*
