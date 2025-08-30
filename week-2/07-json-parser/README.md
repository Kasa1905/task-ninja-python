# 🔄 JSON Parser - Project #7

## 🎯 Problem Statement

Create a Python script that reads data from a JSON file, manipulates it, and writes the updated data back to a new JSON file. The tool should handle nested structures, validation, and various JSON operations.

## 🎓 Learning Objectives

By completing this project, you will learn:
- Working with JSON using Python's `json` module
- Parsing and manipulating nested data structures
- File I/O operations for JSON files
- Data validation and error handling
- JSON schema concepts
- Data transformation techniques

## 🔧 Features

- **JSON Reading/Writing**: Load and save JSON files
- **Data Manipulation**: Add, update, delete JSON properties
- **Nested Structure Handling**: Work with complex JSON objects
- **Data Validation**: Validate JSON structure and content
- **Pretty Printing**: Format JSON output for readability
- **Search and Filter**: Find specific data within JSON
- **Merge Operations**: Combine multiple JSON files

## 📋 Requirements

```
# No external dependencies required
# This project uses only built-in Python modules
```

## 🚀 How to Run

1. Navigate to the project directory:
```bash
cd week-2/07-json-parser
```

2. Run the JSON parser:
```bash
python main.py
```

## 💡 Key Concepts Demonstrated

### 1. JSON Operations
- Loading and parsing JSON data
- Writing formatted JSON output
- Handling JSON encoding/decoding errors

### 2. Data Manipulation
- Adding and updating JSON properties
- Deleting elements from JSON structures
- Merging multiple JSON objects

### 3. Error Handling
- JSON parsing error management
- File operation error handling
- Data validation techniques

## 📊 Sample Usage

### Basic JSON Processing:
```
🔄 JSON Parser
=================
1. 📖 Load and Display JSON
2. ✏️  Modify JSON Data
3. 🔍 Search JSON Content
4. 🔗 Merge JSON Files
5. ✅ Validate JSON Structure

Enter choice: 1
Enter JSON file path: user_data.json

📋 JSON Content:
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "active": true
    }
  ],
  "timestamp": "2025-08-26T10:30:00Z"
}
```

### Data Modification:
```
✏️ Modify JSON Data
==================
Current data loaded: user_data.json
What would you like to modify?
1. Add new property
2. Update existing property
3. Delete property

Enter choice: 1
Enter property path (e.g., users.0.age): users.0.age
Enter value: 25

✅ Added property successfully!
💾 Save changes to file? (y/n): y
```

## 🎯 Learning Outcome

After completing this project, you'll understand:
- JSON data format and structure
- Python's json module capabilities
- Data manipulation techniques
- File I/O best practices
- Error handling in data processing

## 🏆 Bonus Challenges

1. **JSON Schema Validation**: Implement schema validation
2. **JSON to CSV Converter**: Convert JSON arrays to CSV
3. **Configuration Manager**: Use JSON for app configuration
4. **API Data Processor**: Process JSON from APIs
5. **JSON Database**: Create a simple JSON-based database

## 🔗 Related Projects

- **Project 6**: CSV & Excel Handler - File format conversion
- **Project 8**: API Calls - JSON data from APIs
- **Project 12**: Email Sender - JSON configuration files

---

*This is Project #7 in our Python Projects Series. Master JSON data handling! 🔄📄*
