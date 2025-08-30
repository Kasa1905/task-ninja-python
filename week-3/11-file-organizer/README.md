# 📁 File Organizer - Project #11

## 🎯 Problem Statement

Create a Python script that automatically organizes files in a directory based on their file extensions. The script should move files into appropriate folders (Images, Documents, Videos, Audio, etc.) to keep your directories clean and organized.

## 🎓 Learning Objectives

By completing this project, you will learn:
- File system operations using `os` and `shutil` modules
- Directory traversal and file manipulation
- Error handling for file operations
- Creating automated organization systems
- Working with file paths and extensions

## 🔧 Features

- **Automatic file sorting** by extension
- **Custom folder mapping** for different file types
- **Safe operation** with error handling
- **Undo functionality** to reverse organization
- **Dry run mode** to preview changes
- **Configurable file type categories**

## 📋 Requirements

```python
# No external dependencies required - uses built-in modules only!
```

## 🚀 How to Run

1. Navigate to the project directory:
```bash
cd week-3/11-file-organizer
```

2. Run the file organizer:
```bash
python main.py
```

3. For dry run (preview only):
```bash
python main.py --dry-run
```

4. To specify a custom directory:
```bash
python main.py --directory "/path/to/your/directory"
```

## 💡 Key Concepts Demonstrated

### 1. File System Operations
- Reading directory contents
- Moving files between folders
- Creating directories programmatically

### 2. Error Handling
- Handling permission errors
- Managing duplicate files
- Graceful failure recovery

### 3. Configuration Management
- Customizable file type mappings
- User preferences
- Default settings

## 📊 Sample Input/Output

### Before Organization:
```
Downloads/
├── report.pdf
├── photo.jpg
├── song.mp3
├── video.mp4
├── document.docx
├── image.png
└── presentation.pptx
```

### After Organization:
```
Downloads/
├── Documents/
│   ├── report.pdf
│   ├── document.docx
│   └── presentation.pptx
├── Images/
│   ├── photo.jpg
│   └── image.png
├── Audio/
│   └── song.mp3
└── Videos/
    └── video.mp4
```

## 🎯 Learning Outcome

After completing this project, you'll understand:
- How to work with file systems in Python
- Best practices for file operations
- Creating user-friendly automation scripts
- Error handling in file manipulation
- Building configurable and extensible tools

## 🏆 Bonus Challenges

1. **Add scheduling**: Run the organizer automatically at set intervals
2. **Include subdirectories**: Organize files in nested folders
3. **Smart naming**: Handle duplicate files intelligently
4. **GUI version**: Create a simple GUI interface
5. **File monitoring**: Watch for new files and organize them instantly

## 🔗 Related Projects

- **Week 1**: Basic file handling concepts
- **Week 4**: Data analysis on organized files
- **Week 3**: Email automation for organization reports

---

*This is Project #11 in our Python Projects Series. Happy organizing! 📁✨*
