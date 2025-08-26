#!/usr/bin/env python3
"""
To-Do List (CLI) - Project #2
A command-line To-Do List app for task management.

Author: Task Ninja Python Series
Project: Week 1 - Python Mini Projects
"""

import os
import json
from datetime import datetime
from typing import List, Dict


class TodoList:
    """A simple command-line todo list manager."""
    
    def __init__(self, filename: str = "tasks.json"):
        """
        Initialize the TodoList.
        
        Args:
            filename (str): File to store tasks
        """
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self) -> List[Dict]:
        """
        Load tasks from file.
        
        Returns:
            List[Dict]: List of tasks
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_tasks(self) -> None:
        """Save tasks to file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except IOError as e:
            print(f"❌ Error saving tasks: {e}")
    
    def show_tasks(self) -> None:
        """Display all tasks."""
        if not self.tasks:
            print("📝 No tasks yet. Add some tasks to get started!")
            return
        
        print("\n📋 Your Tasks:")
        print("-" * 50)
        
        for i, task in enumerate(self.tasks, 1):
            status = "✅" if task.get('completed', False) else "⭕"
            priority = task.get('priority', 'Normal')
            created = task.get('created', 'Unknown')
            
            print(f"{i:2d}. {status} {task['task']}")
            print(f"    Priority: {priority} | Created: {created}")
            
            if task.get('completed'):
                print(f"    Completed: {task.get('completed_date', 'Unknown')}")
            print()
    
    def add_task(self, task_text: str, priority: str = "Normal") -> None:
        """
        Add a new task.
        
        Args:
            task_text (str): Task description
            priority (str): Task priority (Low, Normal, High)
        """
        if not task_text.strip():
            print("❌ Task cannot be empty!")
            return
        
        new_task = {
            'task': task_text.strip(),
            'completed': False,
            'priority': priority,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'completed_date': None
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"✅ Task added: '{task_text}'")
    
    def delete_task(self, index: int) -> None:
        """
        Delete a task by index.
        
        Args:
            index (int): Task index (1-based)
        """
        if 1 <= index <= len(self.tasks):
            removed_task = self.tasks.pop(index - 1)
            self.save_tasks()
            print(f"🗑️  Deleted: '{removed_task['task']}'")
        else:
            print("❌ Invalid task number.")
    
    def complete_task(self, index: int) -> None:
        """
        Mark a task as completed.
        
        Args:
            index (int): Task index (1-based)
        """
        if 1 <= index <= len(self.tasks):
            if self.tasks[index - 1]['completed']:
                print("❌ Task already completed!")
                return
            
            self.tasks[index - 1]['completed'] = True
            self.tasks[index - 1]['completed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.save_tasks()
            print(f"🎉 Completed: '{self.tasks[index - 1]['task']}'")
        else:
            print("❌ Invalid task number.")
    
    def uncomplete_task(self, index: int) -> None:
        """
        Mark a task as incomplete.
        
        Args:
            index (int): Task index (1-based)
        """
        if 1 <= index <= len(self.tasks):
            if not self.tasks[index - 1]['completed']:
                print("❌ Task is not completed!")
                return
            
            self.tasks[index - 1]['completed'] = False
            self.tasks[index - 1]['completed_date'] = None
            self.save_tasks()
            print(f"↩️  Uncompleted: '{self.tasks[index - 1]['task']}'")
        else:
            print("❌ Invalid task number.")
    
    def edit_task(self, index: int, new_text: str) -> None:
        """
        Edit a task's text.
        
        Args:
            index (int): Task index (1-based)
            new_text (str): New task text
        """
        if 1 <= index <= len(self.tasks):
            if not new_text.strip():
                print("❌ Task cannot be empty!")
                return
            
            old_text = self.tasks[index - 1]['task']
            self.tasks[index - 1]['task'] = new_text.strip()
            self.save_tasks()
            print(f"✏️  Updated: '{old_text}' → '{new_text}'")
        else:
            print("❌ Invalid task number.")
    
    def show_stats(self) -> None:
        """Display task statistics."""
        if not self.tasks:
            print("📊 No tasks to show stats for.")
            return
        
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed
        
        print(f"\n📊 Task Statistics:")
        print(f"Total tasks: {total}")
        print(f"Completed: {completed}")
        print(f"Pending: {pending}")
        print(f"Completion rate: {(completed/total*100):.1f}%")


def get_priority() -> str:
    """Get task priority from user."""
    while True:
        priority = input("Enter priority (L)ow, (N)ormal, (H)igh [N]: ").strip().upper()
        
        if priority == '' or priority == 'N':
            return "Normal"
        elif priority == 'L':
            return "Low"
        elif priority == 'H':
            return "High"
        else:
            print("❌ Invalid priority. Please enter L, N, or H.")


def get_valid_number(prompt: str, max_num: int) -> int:
    """Get a valid number from user input."""
    while True:
        try:
            num = int(input(prompt))
            if 1 <= num <= max_num:
                return num
            else:
                print(f"❌ Please enter a number between 1 and {max_num}.")
        except ValueError:
            print("❌ Please enter a valid number.")


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 40)
    print("📝 To-Do List Manager")
    print("=" * 40)
    print("1. 👀 View Tasks")
    print("2. ➕ Add Task")
    print("3. ✅ Complete Task")
    print("4. ↩️  Uncomplete Task")
    print("5. ✏️  Edit Task")
    print("6. 🗑️  Delete Task")
    print("7. 📊 Show Statistics")
    print("8. 🚪 Exit")
    print("-" * 40)


def main():
    """Main function to run the todo list application."""
    print("🎉 Welcome to your To-Do List Manager!")
    
    todo = TodoList()
    
    while True:
        display_menu()
        
        choice = input("Choose an option (1-8): ").strip()
        
        if choice == '1':
            todo.show_tasks()
        
        elif choice == '2':
            task_text = input("📝 Enter task: ").strip()
            if task_text:
                priority = get_priority()
                todo.add_task(task_text, priority)
            else:
                print("❌ Task cannot be empty!")
        
        elif choice == '3':
            if not todo.tasks:
                print("❌ No tasks to complete!")
                continue
            
            todo.show_tasks()
            try:
                index = get_valid_number("Enter task number to complete: ", len(todo.tasks))
                todo.complete_task(index)
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled.")
        
        elif choice == '4':
            if not todo.tasks:
                print("❌ No tasks to uncomplete!")
                continue
            
            todo.show_tasks()
            try:
                index = get_valid_number("Enter task number to uncomplete: ", len(todo.tasks))
                todo.uncomplete_task(index)
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled.")
        
        elif choice == '5':
            if not todo.tasks:
                print("❌ No tasks to edit!")
                continue
            
            todo.show_tasks()
            try:
                index = get_valid_number("Enter task number to edit: ", len(todo.tasks))
                new_text = input("Enter new task text: ").strip()
                if new_text:
                    todo.edit_task(index, new_text)
                else:
                    print("❌ Task cannot be empty!")
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled.")
        
        elif choice == '6':
            if not todo.tasks:
                print("❌ No tasks to delete!")
                continue
            
            todo.show_tasks()
            try:
                index = get_valid_number("Enter task number to delete: ", len(todo.tasks))
                confirm = input(f"Are you sure you want to delete task {index}? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    todo.delete_task(index)
                else:
                    print("❌ Deletion cancelled.")
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled.")
        
        elif choice == '7':
            todo.show_stats()
        
        elif choice == '8':
            print("👋 Thank you for using To-Do List Manager! Stay productive!")
            break
        
        else:
            print("❌ Invalid option. Please choose 1-8.")
        
        # Wait for user to press Enter before showing menu again
        if choice in ['1', '7']:
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
