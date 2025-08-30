#!/usr/bin/env python3
"""
PDF Merger Tool - Project #14
=============================

A comprehensive PDF merger application with both GUI and CLI interfaces.
Supports advanced features like page selection, metadata preservation, 
password handling, and batch processing.

Author: Task Ninja Python Series
Created: 2024
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Union
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkinter.dnd import DND_FILES
import threading

try:
    import PyPDF2
    from PyPDF2 import PdfReader, PdfWriter
    PDF_LIBRARY = "PyPDF2"
except ImportError:
    try:
        import pypdf
        from pypdf import PdfReader, PdfWriter
        PDF_LIBRARY = "pypdf"
    except ImportError:
        print("❌ Neither PyPDF2 nor pypdf is installed!")
        print("📦 Install with: pip install PyPDF2 or pip install pypdf")
        sys.exit(1)


class PDFInfo:
    """Class to store PDF file information."""
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.filename = self.filepath.name
        self.size_bytes = 0
        self.pages = 0
        self.metadata = {}
        self.is_encrypted = False
        self.error = None
        
        self._analyze_pdf()
    
    def _analyze_pdf(self):
        """Analyze PDF file to extract information."""
        try:
            if not self.filepath.exists():
                self.error = "File not found"
                return
            
            # Get file size
            self.size_bytes = self.filepath.stat().st_size
            
            # Read PDF information
            with open(self.filepath, 'rb') as file:
                reader = PdfReader(file)
                
                self.is_encrypted = reader.is_encrypted
                self.pages = len(reader.pages)
                
                # Extract metadata
                if reader.metadata:
                    self.metadata = {
                        'title': reader.metadata.get('/Title', ''),
                        'author': reader.metadata.get('/Author', ''),
                        'subject': reader.metadata.get('/Subject', ''),
                        'creator': reader.metadata.get('/Creator', ''),
                        'producer': reader.metadata.get('/Producer', ''),
                        'creation_date': reader.metadata.get('/CreationDate', ''),
                        'modification_date': reader.metadata.get('/ModDate', '')
                    }
                
        except Exception as e:
            self.error = str(e)
    
    @property
    def size_mb(self) -> float:
        """Get file size in MB."""
        return self.size_bytes / (1024 * 1024)
    
    @property
    def size_formatted(self) -> str:
        """Get formatted file size."""
        if self.size_bytes < 1024:
            return f"{self.size_bytes} B"
        elif self.size_bytes < 1024 * 1024:
            return f"{self.size_bytes / 1024:.1f} KB"
        else:
            return f"{self.size_mb:.1f} MB"
    
    def is_valid(self) -> bool:
        """Check if PDF is valid and readable."""
        return self.error is None and self.pages > 0


class PDFMerger:
    """Core PDF merging functionality."""
    
    def __init__(self):
        self.pdf_files: List[PDFInfo] = []
        self.output_path = "merged_output.pdf"
        self.preserve_bookmarks = True
        self.preserve_metadata = True
    
    def add_pdf(self, filepath: str) -> bool:
        """Add a PDF file to the merge list."""
        pdf_info = PDFInfo(filepath)
        
        if pdf_info.is_valid():
            self.pdf_files.append(pdf_info)
            return True
        else:
            print(f"❌ Error with {filepath}: {pdf_info.error}")
            return False
    
    def remove_pdf(self, index: int) -> bool:
        """Remove a PDF from the merge list."""
        try:
            self.pdf_files.pop(index)
            return True
        except IndexError:
            return False
    
    def clear_pdfs(self):
        """Clear all PDFs from the merge list."""
        self.pdf_files.clear()
    
    def reorder_pdf(self, old_index: int, new_index: int):
        """Reorder PDFs in the merge list."""
        if 0 <= old_index < len(self.pdf_files) and 0 <= new_index < len(self.pdf_files):
            pdf = self.pdf_files.pop(old_index)
            self.pdf_files.insert(new_index, pdf)
    
    def sort_pdfs(self, sort_by: str = "name"):
        """Sort PDFs by name, date, or size."""
        if sort_by == "name":
            self.pdf_files.sort(key=lambda x: x.filename.lower())
        elif sort_by == "size":
            self.pdf_files.sort(key=lambda x: x.size_bytes)
        elif sort_by == "date":
            self.pdf_files.sort(key=lambda x: x.filepath.stat().st_mtime)
    
    def get_total_pages(self) -> int:
        """Get total number of pages across all PDFs."""
        return sum(pdf.pages for pdf in self.pdf_files)
    
    def get_total_size(self) -> int:
        """Get total size of all PDFs in bytes."""
        return sum(pdf.size_bytes for pdf in self.pdf_files)
    
    def merge_pdfs(self, output_path: str = None, page_ranges: Dict[int, str] = None, 
                   progress_callback=None) -> Tuple[bool, str]:
        """
        Merge all PDFs into a single file.
        
        Args:
            output_path: Output file path
            page_ranges: Dictionary mapping PDF index to page range (e.g., "1-5,10")
            progress_callback: Function to call with progress updates
            
        Returns:
            Tuple of (success, message)
        """
        if not self.pdf_files:
            return False, "No PDF files to merge"
        
        if output_path:
            self.output_path = output_path
        
        try:
            writer = PdfWriter()
            total_pages = 0
            processed_pages = 0
            
            # Calculate total pages for progress tracking
            for i, pdf_info in enumerate(self.pdf_files):
                if page_ranges and i in page_ranges:
                    # Count pages in specified range
                    page_range = page_ranges[i]
                    pages_in_range = self._count_pages_in_range(page_range, pdf_info.pages)
                    total_pages += pages_in_range
                else:
                    total_pages += pdf_info.pages
            
            # Merge PDFs
            for i, pdf_info in enumerate(self.pdf_files):
                if progress_callback:
                    progress_callback(f"Processing {pdf_info.filename}...", 
                                    int((processed_pages / total_pages) * 100))
                
                with open(pdf_info.filepath, 'rb') as file:
                    reader = PdfReader(file)
                    
                    # Handle password protection
                    if reader.is_encrypted:
                        # In a real application, you might prompt for password
                        try:
                            reader.decrypt("")  # Try empty password
                        except:
                            continue  # Skip encrypted files for now
                    
                    # Determine which pages to include
                    if page_ranges and i in page_ranges:
                        page_indices = self._parse_page_range(page_ranges[i], len(reader.pages))
                    else:
                        page_indices = list(range(len(reader.pages)))
                    
                    # Add pages to writer
                    for page_index in page_indices:
                        if 0 <= page_index < len(reader.pages):
                            writer.add_page(reader.pages[page_index])
                            processed_pages += 1
                            
                            if progress_callback:
                                progress = int((processed_pages / total_pages) * 100)
                                progress_callback(f"Adding page {processed_pages}/{total_pages}", progress)
                    
                    # Preserve bookmarks if requested
                    if self.preserve_bookmarks and hasattr(reader, 'outline'):
                        try:
                            writer.clone_reader_document_root(reader)
                        except:
                            pass  # Some PDFs might not support bookmark cloning
            
            # Add metadata if requested
            if self.preserve_metadata and self.pdf_files:
                first_pdf = self.pdf_files[0]
                if first_pdf.metadata:
                    writer.add_metadata({
                        '/Title': f"Merged Document - {datetime.now().strftime('%Y-%m-%d')}",
                        '/Author': first_pdf.metadata.get('author', 'PDF Merger Tool'),
                        '/Subject': 'Merged PDF Document',
                        '/Creator': 'PDF Merger Tool - Python Projects Series'
                    })
            
            # Write the merged PDF
            if progress_callback:
                progress_callback("Writing merged PDF...", 95)
            
            with open(self.output_path, 'wb') as output_file:
                writer.write(output_file)
            
            if progress_callback:
                progress_callback("Merge completed!", 100)
            
            return True, f"Successfully merged {len(self.pdf_files)} PDFs into {self.output_path}"
            
        except Exception as e:
            return False, f"Error merging PDFs: {str(e)}"
    
    def _parse_page_range(self, range_str: str, total_pages: int) -> List[int]:
        """Parse page range string like '1-5,10,15-20' into list of indices."""
        indices = []
        
        for part in range_str.split(','):
            part = part.strip()
            if '-' in part:
                start, end = part.split('-', 1)
                start = max(1, int(start.strip()))
                end = min(total_pages, int(end.strip()))
                indices.extend(range(start - 1, end))  # Convert to 0-based
            else:
                page_num = int(part.strip())
                if 1 <= page_num <= total_pages:
                    indices.append(page_num - 1)  # Convert to 0-based
        
        return sorted(set(indices))  # Remove duplicates and sort
    
    def _count_pages_in_range(self, range_str: str, total_pages: int) -> int:
        """Count number of pages in a range string."""
        return len(self._parse_page_range(range_str, total_pages))


class PDFMergerGUI:
    """GUI interface for PDF merger."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.merger = PDFMerger()
        self.setup_gui()
    
    def setup_gui(self):
        """Set up the GUI interface."""
        self.root.title("📄 PDF Merger Tool")
        self.root.geometry("800x600")
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="📄 PDF Merger Tool", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="PDF Files")
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(file_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="➕ Add PDFs", 
                  command=self.add_pdfs).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="❌ Remove Selected", 
                  command=self.remove_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="🗑️ Clear All", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=(0, 5))
        
        # Sort frame
        sort_frame = ttk.Frame(buttons_frame)
        sort_frame.pack(side=tk.RIGHT)
        
        ttk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT)
        self.sort_var = tk.StringVar(value="name")
        sort_combo = ttk.Combobox(sort_frame, textvariable=self.sort_var, 
                                 values=["name", "size", "date"], width=10)
        sort_combo.pack(side=tk.LEFT, padx=(5, 0))
        sort_combo.bind("<<ComboboxSelected>>", self.sort_pdfs)
        
        # PDF list with scrollbar
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for PDF list
        columns = ("File", "Pages", "Size", "Status")
        self.pdf_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Configure columns
        self.pdf_tree.heading("File", text="Filename")
        self.pdf_tree.heading("Pages", text="Pages")
        self.pdf_tree.heading("Size", text="Size")
        self.pdf_tree.heading("Status", text="Status")
        
        self.pdf_tree.column("File", width=300)
        self.pdf_tree.column("Pages", width=80)
        self.pdf_tree.column("Size", width=100)
        self.pdf_tree.column("Status", width=100)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.pdf_tree.yview)
        self.pdf_tree.configure(yscrollcommand=scrollbar.set)
        
        self.pdf_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready to merge PDFs")
        self.status_label.pack(padx=5, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                          maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Merge Options")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Checkboxes
        checkbox_frame = ttk.Frame(options_frame)
        checkbox_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.preserve_bookmarks_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(checkbox_frame, text="Preserve bookmarks", 
                       variable=self.preserve_bookmarks_var).pack(side=tk.LEFT)
        
        self.preserve_metadata_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(checkbox_frame, text="Preserve metadata", 
                       variable=self.preserve_metadata_var).pack(side=tk.LEFT, padx=(20, 0))
        
        # Output file frame
        output_frame = ttk.Frame(options_frame)
        output_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(output_frame, text="Output file:").pack(side=tk.LEFT)
        self.output_var = tk.StringVar(value="merged_output.pdf")
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        ttk.Button(output_frame, text="📁 Browse", 
                  command=self.browse_output).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Merge button
        merge_frame = ttk.Frame(main_frame)
        merge_frame.pack(fill=tk.X)
        
        self.merge_button = ttk.Button(merge_frame, text="🔄 Merge PDFs", 
                                      command=self.merge_pdfs)
        self.merge_button.pack(pady=10)
        
        # Bind double-click for PDF info
        self.pdf_tree.bind("<Double-1>", self.show_pdf_info)
    
    def add_pdfs(self):
        """Add PDF files to the merger."""
        filetypes = [("PDF files", "*.pdf"), ("All files", "*.*")]
        filenames = filedialog.askopenfilenames(title="Select PDF files", 
                                              filetypes=filetypes)
        
        for filename in filenames:
            if self.merger.add_pdf(filename):
                self.update_pdf_list()
    
    def remove_selected(self):
        """Remove selected PDF from the list."""
        selection = self.pdf_tree.selection()
        if selection:
            item = selection[0]
            index = self.pdf_tree.index(item)
            self.merger.remove_pdf(index)
            self.update_pdf_list()
    
    def clear_all(self):
        """Clear all PDFs from the list."""
        self.merger.clear_pdfs()
        self.update_pdf_list()
    
    def sort_pdfs(self, event=None):
        """Sort PDFs by selected criteria."""
        self.merger.sort_pdfs(self.sort_var.get())
        self.update_pdf_list()
    
    def update_pdf_list(self):
        """Update the PDF list display."""
        # Clear existing items
        for item in self.pdf_tree.get_children():
            self.pdf_tree.delete(item)
        
        # Add current PDFs
        for pdf_info in self.merger.pdf_files:
            status = "✅ Ready" if pdf_info.is_valid() else f"❌ {pdf_info.error}"
            self.pdf_tree.insert("", "end", values=(
                pdf_info.filename,
                pdf_info.pages,
                pdf_info.size_formatted,
                status
            ))
        
        # Update status
        total_files = len(self.merger.pdf_files)
        total_pages = self.merger.get_total_pages()
        total_size = self.merger.get_total_size() / (1024 * 1024)  # MB
        
        self.status_label.config(text=f"📄 {total_files} files, {total_pages} pages, {total_size:.1f} MB")
    
    def browse_output(self):
        """Browse for output file location."""
        filename = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            self.output_var.set(filename)
    
    def show_pdf_info(self, event):
        """Show detailed PDF information."""
        selection = self.pdf_tree.selection()
        if selection:
            item = selection[0]
            index = self.pdf_tree.index(item)
            pdf_info = self.merger.pdf_files[index]
            
            info_text = f"""
📄 PDF Information

Filename: {pdf_info.filename}
Path: {pdf_info.filepath}
Pages: {pdf_info.pages}
Size: {pdf_info.size_formatted}
Encrypted: {'Yes' if pdf_info.is_encrypted else 'No'}

📋 Metadata:
Title: {pdf_info.metadata.get('title', 'N/A')}
Author: {pdf_info.metadata.get('author', 'N/A')}
Subject: {pdf_info.metadata.get('subject', 'N/A')}
Creator: {pdf_info.metadata.get('creator', 'N/A')}
            """
            
            messagebox.showinfo("PDF Information", info_text.strip())
    
    def update_progress(self, message: str, progress: int):
        """Update progress bar and status."""
        self.status_label.config(text=message)
        self.progress_var.set(progress)
        self.root.update_idletasks()
    
    def merge_pdfs(self):
        """Merge the PDFs."""
        if not self.merger.pdf_files:
            messagebox.showerror("Error", "No PDF files to merge!")
            return
        
        # Update merger settings
        self.merger.preserve_bookmarks = self.preserve_bookmarks_var.get()
        self.merger.preserve_metadata = self.preserve_metadata_var.get()
        
        output_path = self.output_var.get()
        if not output_path:
            messagebox.showerror("Error", "Please specify an output filename!")
            return
        
        # Disable merge button during processing
        self.merge_button.config(state="disabled")
        
        def merge_thread():
            success, message = self.merger.merge_pdfs(output_path, 
                                                    progress_callback=self.update_progress)
            
            # Re-enable button
            self.merge_button.config(state="normal")
            
            if success:
                messagebox.showinfo("Success", f"✅ {message}")
                self.progress_var.set(0)
                self.status_label.config(text="Ready to merge PDFs")
            else:
                messagebox.showerror("Error", f"❌ {message}")
                self.progress_var.set(0)
                self.status_label.config(text="Merge failed")
        
        # Run merge in separate thread to avoid freezing GUI
        threading.Thread(target=merge_thread, daemon=True).start()
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


class PDFMergerCLI:
    """Command-line interface for PDF merger."""
    
    def __init__(self):
        self.merger = PDFMerger()
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("📄 PDF Merger Tool - CLI")
        print("="*50)
        print("1. ➕ Add PDF files")
        print("2. 📋 List current PDFs")
        print("3. ❌ Remove PDF")
        print("4. 🗑️ Clear all PDFs")
        print("5. 📊 Sort PDFs")
        print("6. ⚙️ Merge options")
        print("7. 🔄 Merge PDFs")
        print("8. ℹ️ PDF information")
        print("0. 🚪 Exit")
        print("="*50)
    
    def add_pdfs_interactive(self):
        """Interactively add PDF files."""
        print("\n📁 Add PDF Files")
        print("Enter PDF file paths (one per line, press Enter twice to finish):")
        
        while True:
            path = input("PDF path: ").strip()
            if not path:
                break
            
            if os.path.exists(path) and path.lower().endswith('.pdf'):
                if self.merger.add_pdf(path):
                    print(f"✅ Added: {Path(path).name}")
                else:
                    print(f"❌ Failed to add: {Path(path).name}")
            else:
                print(f"❌ Invalid PDF file: {path}")
    
    def list_pdfs(self):
        """List current PDFs in the merger."""
        if not self.merger.pdf_files:
            print("\n📭 No PDF files added yet")
            return
        
        print(f"\n📄 Current PDF Files ({len(self.merger.pdf_files)} total):")
        print("-" * 70)
        print(f"{'#':<3} {'Filename':<30} {'Pages':<8} {'Size':<10} {'Status'}")
        print("-" * 70)
        
        for i, pdf_info in enumerate(self.merger.pdf_files, 1):
            status = "✅ OK" if pdf_info.is_valid() else f"❌ Error"
            print(f"{i:<3} {pdf_info.filename[:29]:<30} {pdf_info.pages:<8} "
                  f"{pdf_info.size_formatted:<10} {status}")
        
        print("-" * 70)
        print(f"📊 Total: {self.merger.get_total_pages()} pages, "
              f"{self.merger.get_total_size() / (1024*1024):.1f} MB")
    
    def remove_pdf_interactive(self):
        """Interactively remove a PDF."""
        self.list_pdfs()
        
        if not self.merger.pdf_files:
            return
        
        try:
            index = int(input("\nEnter PDF number to remove: ")) - 1
            if 0 <= index < len(self.merger.pdf_files):
                filename = self.merger.pdf_files[index].filename
                self.merger.remove_pdf(index)
                print(f"✅ Removed: {filename}")
            else:
                print("❌ Invalid PDF number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def sort_pdfs_interactive(self):
        """Interactively sort PDFs."""
        print("\n📊 Sort PDFs by:")
        print("1. Name")
        print("2. Size")
        print("3. Date")
        
        choice = input("Enter choice: ").strip()
        sort_map = {'1': 'name', '2': 'size', '3': 'date'}
        
        if choice in sort_map:
            self.merger.sort_pdfs(sort_map[choice])
            print(f"✅ Sorted by {sort_map[choice]}")
        else:
            print("❌ Invalid choice")
    
    def merge_options_interactive(self):
        """Configure merge options."""
        print("\n⚙️ Merge Options")
        print(f"Current settings:")
        print(f"• Preserve bookmarks: {'Yes' if self.merger.preserve_bookmarks else 'No'}")
        print(f"• Preserve metadata: {'Yes' if self.merger.preserve_metadata else 'No'}")
        print(f"• Output file: {self.merger.output_path}")
        
        # Toggle bookmarks
        toggle_bookmarks = input("\nToggle bookmark preservation? (y/n): ").lower() == 'y'
        if toggle_bookmarks:
            self.merger.preserve_bookmarks = not self.merger.preserve_bookmarks
        
        # Toggle metadata
        toggle_metadata = input("Toggle metadata preservation? (y/n): ").lower() == 'y'
        if toggle_metadata:
            self.merger.preserve_metadata = not self.merger.preserve_metadata
        
        # Set output path
        new_output = input(f"New output file (current: {self.merger.output_path}): ").strip()
        if new_output:
            self.merger.output_path = new_output
        
        print("✅ Options updated")
    
    def show_pdf_info(self):
        """Show detailed information for a PDF."""
        self.list_pdfs()
        
        if not self.merger.pdf_files:
            return
        
        try:
            index = int(input("\nEnter PDF number for details: ")) - 1
            if 0 <= index < len(self.merger.pdf_files):
                pdf_info = self.merger.pdf_files[index]
                
                print(f"\n📄 PDF Information: {pdf_info.filename}")
                print("=" * 50)
                print(f"📁 Path: {pdf_info.filepath}")
                print(f"📄 Pages: {pdf_info.pages}")
                print(f"💾 Size: {pdf_info.size_formatted}")
                print(f"🔒 Encrypted: {'Yes' if pdf_info.is_encrypted else 'No'}")
                
                if pdf_info.metadata:
                    print(f"\n📋 Metadata:")
                    for key, value in pdf_info.metadata.items():
                        if value:
                            print(f"  • {key.title()}: {value}")
            else:
                print("❌ Invalid PDF number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def merge_pdfs_interactive(self):
        """Interactively merge PDFs."""
        if not self.merger.pdf_files:
            print("\n❌ No PDF files to merge!")
            return
        
        self.list_pdfs()
        print(f"\n🔄 Ready to merge {len(self.merger.pdf_files)} PDFs")
        print(f"📄 Total pages: {self.merger.get_total_pages()}")
        print(f"💾 Output file: {self.merger.output_path}")
        
        confirm = input("\nProceed with merge? (y/n): ").lower() == 'y'
        
        if confirm:
            def progress_callback(message, progress):
                print(f"\r{message} ({progress}%)", end="", flush=True)
            
            print("\n🔄 Merging PDFs...")
            success, message = self.merger.merge_pdfs(progress_callback=progress_callback)
            
            print()  # New line after progress
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")
    
    def run(self):
        """Run the CLI application."""
        print("📄 Welcome to PDF Merger Tool!")
        print("Combine multiple PDF files into a single document.")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (0-8): ").strip()
                
                if choice == '0':
                    print("\n👋 Thanks for using PDF Merger Tool!")
                    break
                
                elif choice == '1':
                    self.add_pdfs_interactive()
                
                elif choice == '2':
                    self.list_pdfs()
                
                elif choice == '3':
                    self.remove_pdf_interactive()
                
                elif choice == '4':
                    self.merger.clear_pdfs()
                    print("✅ All PDFs cleared")
                
                elif choice == '5':
                    self.sort_pdfs_interactive()
                
                elif choice == '6':
                    self.merge_options_interactive()
                
                elif choice == '7':
                    self.merge_pdfs_interactive()
                
                elif choice == '8':
                    self.show_pdf_info()
                
                else:
                    print("❌ Invalid choice. Please try again.")
                
                # Wait for user input before continuing
                if choice != '0':
                    input("\nPress Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="PDF Merger Tool")
    parser.add_argument("--cli", action="store_true", help="Use command-line interface")
    parser.add_argument("--files", nargs="+", help="PDF files to merge")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    if args.cli or args.files:
        # CLI mode
        cli = PDFMergerCLI()
        
        # Add files from command line
        if args.files:
            for file in args.files:
                cli.merger.add_pdf(file)
        
        # Set output path
        if args.output:
            cli.merger.output_path = args.output
        
        # If files provided, merge directly
        if args.files:
            success, message = cli.merger.merge_pdfs()
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")
        else:
            cli.run()
    else:
        # GUI mode
        try:
            gui = PDFMergerGUI()
            gui.run()
        except tk.TclError:
            print("❌ GUI not available. Use --cli flag for command-line interface.")
            cli = PDFMergerCLI()
            cli.run()


if __name__ == "__main__":
    main()
