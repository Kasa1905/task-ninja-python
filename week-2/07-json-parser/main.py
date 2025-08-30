#!/usr/bin/env python3
"""
JSON Parser - Project #7
Read data from JSON files, manipulate it, and write updated data.

Author: Task Ninja Python Series
Project: Week 2 - Data Handling & APIs
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Union, Optional
from datetime import datetime


class JSONParser:
    """A comprehensive JSON parser and manipulator."""
    
    def __init__(self):
        """Initialize the JSON parser."""
        self.current_data: Optional[Dict] = None
        self.current_file: Optional[str] = None
        self.backup_data: Optional[Dict] = None
    
    def read_json(self, file_path: str) -> Dict[str, Any]:
        """
        Read data from a JSON file.
        
        Args:
            file_path (str): Path to JSON file
            
        Returns:
            Dict[str, Any]: Loaded JSON data
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"JSON file not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.current_data = data.copy()  # Keep original
            self.backup_data = data.copy()   # Backup for undo
            self.current_file = file_path
            
            print(f"✅ Successfully read JSON file: {file_path}")
            print(f"📊 Contains {len(data)} top-level keys" if isinstance(data, dict) else f"📊 Contains {len(data)} items")
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON format: {e}")
            raise
        except Exception as e:
            print(f"❌ Error reading JSON file: {e}")
            raise
    
    def write_json(self, data: Dict[str, Any], file_path: str, 
                  indent: int = 4, sort_keys: bool = False) -> None:
        """
        Write data to a JSON file.
        
        Args:
            data (Dict[str, Any]): Data to write
            file_path (str): Output file path
            indent (int): JSON indentation
            sort_keys (bool): Whether to sort keys
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
            
            print(f"✅ Successfully wrote JSON file: {file_path}")
            
        except Exception as e:
            print(f"❌ Error writing JSON file: {e}")
            raise
    
    def display_json(self, data: Optional[Dict] = None, max_depth: int = 3) -> None:
        """
        Display JSON data in a formatted way.
        
        Args:
            data (Optional[Dict]): Data to display (uses current_data if None)
            max_depth (int): Maximum depth to display
        """
        if data is None:
            data = self.current_data
        
        if data is None:
            print("❌ No JSON data loaded!")
            return
        
        print("\n📋 JSON Content:")
        print("=" * 50)
        try:
            formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
            
            # Limit output if too large
            lines = formatted_json.split('\n')
            if len(lines) > 50:
                print('\n'.join(lines[:25]))
                print(f"... ({len(lines) - 50} more lines) ...")
                print('\n'.join(lines[-25:]))
            else:
                print(formatted_json)
        except Exception as e:
            print(f"❌ Error displaying JSON: {e}")
    
    def get_nested_value(self, data: Dict, path: str) -> Any:
        """
        Get value from nested JSON using dot notation.
        
        Args:
            data (Dict): JSON data
            path (str): Path like "users.0.name"
            
        Returns:
            Any: Value at the specified path
        """
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict):
                if key in current:
                    current = current[key]
                else:
                    raise KeyError(f"Key '{key}' not found in path '{path}'")
            elif isinstance(current, list):
                try:
                    index = int(key)
                    current = current[index]
                except (ValueError, IndexError):
                    raise KeyError(f"Invalid array index '{key}' in path '{path}'")
            else:
                raise KeyError(f"Cannot access '{key}' in non-dict/list object")
        
        return current
    
    def set_nested_value(self, data: Dict, path: str, value: Any) -> None:
        """
        Set value in nested JSON using dot notation.
        
        Args:
            data (Dict): JSON data
            path (str): Path like "users.0.name"
            value (Any): Value to set
        """
        keys = path.split('.')
        current = data
        
        # Navigate to the parent of the target
        for key in keys[:-1]:
            if isinstance(current, dict):
                if key not in current:
                    # Create new dict if key doesn't exist
                    current[key] = {}
                current = current[key]
            elif isinstance(current, list):
                try:
                    index = int(key)
                    current = current[index]
                except (ValueError, IndexError):
                    raise KeyError(f"Invalid array index '{key}' in path '{path}'")
            else:
                raise KeyError(f"Cannot navigate through '{key}' in non-dict/list object")
        
        # Set the final value
        final_key = keys[-1]
        if isinstance(current, dict):
            current[final_key] = value
        elif isinstance(current, list):
            try:
                index = int(final_key)
                current[index] = value
            except (ValueError, IndexError):
                raise KeyError(f"Invalid array index '{final_key}' in path '{path}'")
        else:
            raise KeyError(f"Cannot set value in non-dict/list object")
    
    def delete_nested_value(self, data: Dict, path: str) -> None:
        """
        Delete value from nested JSON using dot notation.
        
        Args:
            data (Dict): JSON data
            path (str): Path like "users.0.name"
        """
        keys = path.split('.')
        current = data
        
        # Navigate to the parent of the target
        for key in keys[:-1]:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list):
                current = current[int(key)]
            else:
                raise KeyError(f"Cannot navigate through '{key}' in path '{path}'")
        
        # Delete the final value
        final_key = keys[-1]
        if isinstance(current, dict):
            del current[final_key]
        elif isinstance(current, list):
            current.pop(int(final_key))
        else:
            raise KeyError(f"Cannot delete from non-dict/list object")
    
    def search_json(self, data: Optional[Dict] = None, search_term: str = "", 
                   search_keys: bool = True, search_values: bool = True) -> List[str]:
        """
        Search for a term in JSON keys and/or values.
        
        Args:
            data (Optional[Dict]): Data to search
            search_term (str): Term to search for
            search_keys (bool): Search in keys
            search_values (bool): Search in values
            
        Returns:
            List[str]: List of paths where term was found
        """
        if data is None:
            data = self.current_data
        
        if data is None:
            return []
        
        results = []
        search_term = search_term.lower()
        
        def recursive_search(obj: Any, path: str = "") -> None:
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Search in keys
                    if search_keys and search_term in key.lower():
                        results.append(current_path)
                    
                    # Search in values
                    if search_values and isinstance(value, str) and search_term in value.lower():
                        results.append(current_path)
                    
                    # Recurse into nested structures
                    recursive_search(value, current_path)
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}.{i}" if path else str(i)
                    recursive_search(item, current_path)
        
        recursive_search(data)
        return results
    
    def merge_json(self, data1: Dict, data2: Dict, strategy: str = "update") -> Dict:
        """
        Merge two JSON objects.
        
        Args:
            data1 (Dict): First JSON object
            data2 (Dict): Second JSON object
            strategy (str): Merge strategy ("update", "keep_first", "deep_merge")
            
        Returns:
            Dict: Merged JSON object
        """
        if strategy == "update":
            # Simple update - data2 overwrites data1
            result = data1.copy()
            result.update(data2)
            return result
        
        elif strategy == "keep_first":
            # Keep values from data1, only add new keys from data2
            result = data1.copy()
            for key, value in data2.items():
                if key not in result:
                    result[key] = value
            return result
        
        elif strategy == "deep_merge":
            # Deep merge - recursively merge nested objects
            def deep_merge_recursive(d1: Dict, d2: Dict) -> Dict:
                result = d1.copy()
                for key, value in d2.items():
                    if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                        result[key] = deep_merge_recursive(result[key], value)
                    else:
                        result[key] = value
                return result
            
            return deep_merge_recursive(data1, data2)
        
        else:
            raise ValueError(f"Unknown merge strategy: {strategy}")
    
    def validate_json_structure(self, data: Optional[Dict] = None, 
                               schema: Optional[Dict] = None) -> bool:
        """
        Basic JSON structure validation.
        
        Args:
            data (Optional[Dict]): Data to validate
            schema (Optional[Dict]): Simple schema to validate against
            
        Returns:
            bool: Whether data is valid
        """
        if data is None:
            data = self.current_data
        
        if data is None:
            return False
        
        if schema is None:
            # Basic validation - check if it's valid JSON
            try:
                json.dumps(data)
                return True
            except (TypeError, ValueError):
                return False
        
        # Simple schema validation
        def validate_recursive(obj: Any, schema_part: Any) -> bool:
            if isinstance(schema_part, type):
                return isinstance(obj, schema_part)
            elif isinstance(schema_part, dict):
                if not isinstance(obj, dict):
                    return False
                for key, expected_type in schema_part.items():
                    if key not in obj:
                        return False
                    if not validate_recursive(obj[key], expected_type):
                        return False
                return True
            elif isinstance(schema_part, list) and len(schema_part) == 1:
                # List with expected item type
                if not isinstance(obj, list):
                    return False
                return all(validate_recursive(item, schema_part[0]) for item in obj)
            else:
                return obj == schema_part
        
        return validate_recursive(data, schema)


def simple_json_operations():
    """Simple JSON operations matching the original code."""
    print("🔄 Simple JSON Operations")
    print("=" * 40)
    
    try:
        # Read JSON file
        with open("data.json", "r") as f:
            data = json.load(f)
            print("Original Data:")
            print(json.dumps(data, indent=2))
        
        # Modify data (example: add a new key)
        data["status"] = "processed"
        data["processed_at"] = datetime.now().isoformat()
        
        # Write to a new JSON file
        with open("updated_data.json", "w") as f:
            json.dump(data, f, indent=4)
        
        print("\n✅ Updated JSON saved to updated_data.json!")
        
    except FileNotFoundError:
        print("❌ Error: data.json file not found!")
        print("💡 Create a sample data.json file or use interactive mode.")
    except Exception as e:
        print(f"❌ Error: {e}")


def create_sample_json():
    """Create a sample JSON file for testing."""
    sample_data = {
        "users": [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "age": 28,
                "active": True,
                "preferences": {
                    "theme": "dark",
                    "notifications": True
                }
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "age": 34,
                "active": False,
                "preferences": {
                    "theme": "light",
                    "notifications": False
                }
            }
        ],
        "metadata": {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "total_users": 2
        }
    }
    
    with open('sample_data.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print("✅ Created sample_data.json with user data")
    print("📋 Sample data structure:")
    print(json.dumps(sample_data, indent=2))


def interactive_mode():
    """Interactive mode for JSON operations."""
    parser = JSONParser()
    
    while True:
        print("\n" + "=" * 50)
        print("🔄 JSON Parser")
        print("=" * 50)
        print("1. 📖 Load and Display JSON")
        print("2. ✏️  Modify JSON Data")
        print("3. 🔍 Search JSON Content")
        print("4. 🔗 Merge JSON Files")
        print("5. ✅ Validate JSON Structure")
        print("6. 💾 Save Current Data")
        print("7. 📊 Create Sample JSON")
        print("8. 🔄 Simple Operations (original code)")
        print("9. 🚪 Exit")
        print("-" * 50)
        
        choice = input("Enter your choice (1-9): ").strip()
        
        try:
            if choice == '1':
                file_path = input("Enter JSON file path: ").strip()
                data = parser.read_json(file_path)
                parser.display_json(data)
            
            elif choice == '2':
                if parser.current_data is None:
                    print("❌ No JSON data loaded! Please load a file first.")
                    continue
                
                print("\n✏️ Modify JSON Data")
                print("1. Add/Update property")
                print("2. Delete property")
                print("3. Undo changes")
                
                mod_choice = input("Enter choice (1-3): ").strip()
                
                if mod_choice == '1':
                    path = input("Enter property path (e.g., users.0.age): ").strip()
                    value_str = input("Enter value (JSON format): ").strip()
                    
                    try:
                        # Try to parse as JSON
                        value = json.loads(value_str)
                    except json.JSONDecodeError:
                        # Treat as string
                        value = value_str
                    
                    parser.set_nested_value(parser.current_data, path, value)
                    print(f"✅ Set {path} = {value}")
                
                elif mod_choice == '2':
                    path = input("Enter property path to delete: ").strip()
                    parser.delete_nested_value(parser.current_data, path)
                    print(f"🗑️  Deleted {path}")
                
                elif mod_choice == '3':
                    parser.current_data = parser.backup_data.copy()
                    print("↩️  Changes undone")
            
            elif choice == '3':
                if parser.current_data is None:
                    print("❌ No JSON data loaded! Please load a file first.")
                    continue
                
                search_term = input("Enter search term: ").strip()
                results = parser.search_json(search_term=search_term)
                
                if results:
                    print(f"\n🔍 Found {len(results)} matches:")
                    for result in results:
                        print(f"  📍 {result}")
                else:
                    print("❌ No matches found")
            
            elif choice == '4':
                file1 = input("Enter first JSON file path: ").strip()
                file2 = input("Enter second JSON file path: ").strip()
                
                data1 = parser.read_json(file1)
                parser2 = JSONParser()
                data2 = parser2.read_json(file2)
                
                print("\nMerge strategies:")
                print("1. Update (second overwrites first)")
                print("2. Keep first (only add new keys)")
                print("3. Deep merge (recursive merge)")
                
                strategy_choice = input("Enter strategy (1-3): ").strip()
                strategies = {'1': 'update', '2': 'keep_first', '3': 'deep_merge'}
                strategy = strategies.get(strategy_choice, 'update')
                
                merged = parser.merge_json(data1, data2, strategy)
                parser.current_data = merged
                
                print(f"✅ Merged with strategy: {strategy}")
                parser.display_json(merged)
            
            elif choice == '5':
                if parser.current_data is None:
                    print("❌ No JSON data loaded! Please load a file first.")
                    continue
                
                is_valid = parser.validate_json_structure()
                if is_valid:
                    print("✅ JSON structure is valid")
                else:
                    print("❌ JSON structure is invalid")
            
            elif choice == '6':
                if parser.current_data is None:
                    print("❌ No JSON data loaded!")
                    continue
                
                output_path = input("Enter output file path: ").strip()
                if not output_path.endswith('.json'):
                    output_path += '.json'
                
                parser.write_json(parser.current_data, output_path)
            
            elif choice == '7':
                create_sample_json()
            
            elif choice == '8':
                simple_json_operations()
            
            elif choice == '9':
                print("👋 Thank you for using JSON Parser!")
                break
            
            else:
                print("❌ Invalid choice! Please select 1-9.")
        
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled.")
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function to run the JSON parser."""
    print("🎉 Welcome to JSON Parser!")
    
    # Check if data.json exists for simple mode
    if len(sys.argv) > 1 and sys.argv[1] == '--simple':
        simple_json_operations()
    elif os.path.exists('data.json'):
        print("🔍 Found data.json file!")
        choice = input("Run simple operations? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            simple_json_operations()
        else:
            interactive_mode()
    else:
        print("💡 No data.json found. Starting interactive mode...")
        interactive_mode()


if __name__ == "__main__":
    main()
