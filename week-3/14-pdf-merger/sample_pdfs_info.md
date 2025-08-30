# Sample PDF Files for Testing

This directory contains sample PDF files for testing the PDF merger tool.

## Creating Test PDFs

If you need to create sample PDF files for testing, you can:

1. **Use any office application** (Word, LibreOffice, Google Docs) and export as PDF
2. **Use online PDF generators** to create simple test documents
3. **Use the Python script below** to generate test PDFs:

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_pdf(filename, title, pages=3):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    for page in range(1, pages + 1):
        c.drawString(100, height - 100, f"{title}")
        c.drawString(100, height - 150, f"This is page {page} of {pages}")
        c.drawString(100, height - 200, f"Sample content for testing PDF merger")
        c.drawString(100, height - 250, f"Generated automatically for demo purposes")
        
        if page < pages:
            c.showPage()
    
    c.save()
    print(f"Created: {filename}")

# Create sample PDFs
create_sample_pdf("document1.pdf", "First Document", 3)
create_sample_pdf("document2.pdf", "Second Document", 2)
create_sample_pdf("document3.pdf", "Third Document", 4)
```

## Install reportlab for PDF generation:
```bash
pip install reportlab
```

## File Structure

```
14-pdf-merger/
├── main.py              # Main application
├── requirements.txt     # Dependencies
├── README.md           # Documentation
├── sample_pdfs/        # Test PDF files
│   ├── document1.pdf   # Sample PDF 1
│   ├── document2.pdf   # Sample PDF 2
│   └── document3.pdf   # Sample PDF 3
└── merged_output.pdf   # Output file (created after merge)
```

## Usage Examples

### GUI Mode
```bash
python main.py
```

### CLI Mode
```bash
python main.py --cli
```

### Direct Command Line Merge
```bash
python main.py --files document1.pdf document2.pdf document3.pdf --output combined.pdf
```
