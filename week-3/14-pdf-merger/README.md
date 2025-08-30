# 📄 PDF Merger Tool - Project #14

## 🎯 Problem Statement

Create a Python script to merge multiple PDF files into a single document. Perfect for combining reports, portfolios, invoices, chapters, or any collection of PDF documents with advanced features like page selection, bookmarks, and metadata management.

## 🎓 Learning Objectives

By completing this project, you will learn:
- PDF manipulation using PyPDF2 and pypdf libraries
- File system operations and directory management
- GUI development with tkinter
- Drag-and-drop file handling
- Metadata extraction and manipulation
- Error handling for file operations

## 🔧 Features

- **Simple PDF Merging**: Combine multiple PDFs into one document
- **Advanced Merging**: Select specific pages from each PDF
- **GUI Interface**: Drag-and-drop file selection interface
- **CLI Interface**: Command-line tool for batch operations
- **File Sorting**: Sort files by name, date, or size
- **Preview Mode**: See PDF info before merging
- **Bookmark Preservation**: Maintain PDF bookmarks and metadata
- **Password Protection**: Handle password-protected PDFs
- **Batch Processing**: Merge multiple sets of PDFs

## 📋 Requirements

```
PyPDF2>=3.0.1
pypdf>=3.0.1
tkinter
pillow>=10.0.0
```

## 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Navigate to Project Directory**:
   ```bash
   cd week-3/14-pdf-merger
   ```

3. **Run GUI Version**:
   ```bash
   python main.py
   ```

4. **Run CLI Version**:
   ```bash
   python main.py --cli
   ```

## 💡 Key Concepts Demonstrated

### 1. PDF Manipulation
- PDF reading and writing operations
- Page extraction and insertion
- Metadata handling and preservation

### 2. File Management
- Directory traversal and file filtering
- File sorting and organization
- Batch processing operations

### 3. User Interface Design
- GUI development with tkinter
- Drag-and-drop functionality
- Progress indicators and status updates

## 📊 Sample Usage

### GUI Mode:
```
📄 PDF Merger Tool - GUI
=======================
1. Drag & drop PDF files into the application
2. Reorder files by dragging in the list
3. Preview PDF information (pages, size, metadata)
4. Choose merge options (all pages or specific ranges)
5. Set output filename and location
6. Click "Merge PDFs" to combine files

✅ Merged 5 PDFs (127 pages) → output.pdf
💾 File saved to: /Users/documents/merged_documents.pdf
```

### CLI Mode:
```
📄 PDF Merger Tool - CLI
=======================
Enter PDF files (drag files here or type paths):
1. /path/to/document1.pdf (15 pages)
2. /path/to/document2.pdf (23 pages)
3. /path/to/document3.pdf (8 pages)

🔧 Merge Options:
• All pages from all documents
• Specific page ranges (e.g., 1-5, 10, 15-20)
• Sort files by: name, date, size

📄 Total: 46 pages from 3 documents
💾 Output file: merged_output.pdf

✅ Successfully merged PDFs!
```

### Advanced Features:
```
🔍 PDF Analysis:
================
Document 1: report.pdf
• Pages: 25
• Size: 2.3 MB
• Created: 2024-08-15
• Author: John Doe
• Password Protected: No

📑 Merge Options:
• Include bookmarks: Yes
• Preserve metadata: Yes
• Page range: 1-25 (all)
• Insert blank pages: No

🎯 Advanced Features:
• Add page numbers
• Insert separator pages
• Combine similar documents
• Remove duplicate pages
```

## 🎯 Learning Outcome

After completing this project, you'll understand:
- PDF structure and manipulation techniques
- File handling and batch processing
- GUI application development
- Error handling for file operations
- Metadata management and preservation

## 🏆 Bonus Challenges

1. **PDF Splitter**: Create reverse functionality to split PDFs
2. **OCR Integration**: Add text extraction from scanned PDFs
3. **Web Interface**: Build a web-based PDF merger
4. **Cloud Integration**: Add Google Drive/Dropbox support
5. **PDF Optimization**: Compress merged PDFs to reduce file size

## 🔗 Related Projects

- **Project 11**: File Organizer - File management foundations
- **Project 13**: WhatsApp Automation - File sharing automation
- **Project 15**: Excel Report Generator - Document automation

---

*This is Project #14 in our Python Projects Series. Master PDF manipulation! 📄🔧*
