#!/usr/bin/env python3
"""
File Organizer - Project #11
A Python script to automatically organize files by their extensions.

Author: Task Ninja Python Series
Project: Week 3 - Automation with Python
"""

import os
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime


class FileOrganizer:
    """
    A class to organize files in a directory based on their extensions.
    """
    
    def __init__(self, directory: str = None, config_file: str = "config.json"):
        """
        Initialize the FileOrganizer.
        
        Args:
            directory (str): Target directory to organize
            config_file (str): Configuration file path
        """
        self.directory = Path(directory) if directory else Path.cwd()
        self.config_file = config_file
        self.organized_files = []
        
        # Default file type mappings
        self.default_mappings = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
            'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods', '.numbers'],
            'Presentations': ['.ppt', '.pptx', '.odp', '.key'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb'],
            'Executables': ['.exe', '.msi', '.dmg', '.deb', '.rpm', '.appimage']
        }
        
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file or create default config."""
        config_path = Path(self.config_file)
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.file_mappings = config.get('file_mappings', self.default_mappings)
                    print(f"✅ Loaded configuration from {self.config_file}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  Error loading config: {e}. Using default settings.")
                self.file_mappings = self.default_mappings
        else:
            self.file_mappings = self.default_mappings
            self.save_config()
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        config = {
            'file_mappings': self.file_mappings,
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"💾 Configuration saved to {self.config_file}")
        except IOError as e:
            print(f"❌ Error saving config: {e}")
    
    def get_file_category(self, file_path: Path) -> Optional[str]:
        """
        Determine the category of a file based on its extension.
        
        Args:
            file_path (Path): Path to the file
            
        Returns:
            Optional[str]: Category name or None if not found
        """
        extension = file_path.suffix.lower()
        
        for category, extensions in self.file_mappings.items():
            if extension in extensions:
                return category
        
        return None
    
    def scan_directory(self) -> Dict[str, List[Path]]:
        """
        Scan directory and categorize files.
        
        Returns:
            Dict[str, List[Path]]: Dictionary of categories and their files
        """
        categorized_files = {}
        
        try:
            for item in self.directory.iterdir():
                # Skip directories and hidden files
                if item.is_dir() or item.name.startswith('.'):
                    continue
                
                category = self.get_file_category(item)
                if category:
                    if category not in categorized_files:
                        categorized_files[category] = []
                    categorized_files[category].append(item)
                else:
                    # Uncategorized files
                    if 'Others' not in categorized_files:
                        categorized_files['Others'] = []
                    categorized_files['Others'].append(item)
        
        except PermissionError:
            print(f"❌ Permission denied accessing {self.directory}")
            return {}
        
        return categorized_files
    
    def create_category_folder(self, category: str) -> Path:
        """
        Create a folder for the given category.
        
        Args:
            category (str): Category name
            
        Returns:
            Path: Path to the created folder
        """
        folder_path = self.directory / category
        folder_path.mkdir(exist_ok=True)
        return folder_path
    
    def move_file(self, file_path: Path, destination_folder: Path, dry_run: bool = False) -> bool:
        """
        Move a file to the destination folder.
        
        Args:
            file_path (Path): Source file path
            destination_folder (Path): Destination folder path
            dry_run (bool): If True, only simulate the move
            
        Returns:
            bool: True if successful, False otherwise
        """
        destination_path = destination_folder / file_path.name
        
        # Handle duplicate files
        counter = 1
        original_destination = destination_path
        while destination_path.exists():
            stem = original_destination.stem
            suffix = original_destination.suffix
            destination_path = destination_folder / f"{stem}_{counter}{suffix}"
            counter += 1
        
        if dry_run:
            print(f"🔄 Would move: {file_path.name} → {destination_folder.name}/{destination_path.name}")
            return True
        
        try:
            shutil.move(str(file_path), str(destination_path))
            self.organized_files.append({
                'original': str(file_path),
                'new': str(destination_path),
                'category': destination_folder.name
            })
            print(f"✅ Moved: {file_path.name} → {destination_folder.name}/")
            return True
        
        except (PermissionError, FileNotFoundError, shutil.Error) as e:
            print(f"❌ Error moving {file_path.name}: {e}")
            return False
    
    def organize(self, dry_run: bool = False) -> None:
        """
        Organize files in the directory.
        
        Args:
            dry_run (bool): If True, only simulate the organization
        """
        print(f"🗂️  {'Simulating' if dry_run else 'Organizing'} files in: {self.directory}")
        print("=" * 50)
        
        categorized_files = self.scan_directory()
        
        if not categorized_files:
            print("📂 No files to organize!")
            return
        
        total_files = sum(len(files) for files in categorized_files.values())
        print(f"📊 Found {total_files} files to organize")
        print()
        
        organized_count = 0
        
        for category, files in categorized_files.items():
            print(f"📁 {category} ({len(files)} files):")
            
            if not dry_run:
                folder_path = self.create_category_folder(category)
            else:
                folder_path = self.directory / category
            
            for file_path in files:
                if self.move_file(file_path, folder_path, dry_run):
                    organized_count += 1
            
            print()
        
        print("=" * 50)
        print(f"🎉 {'Would organize' if dry_run else 'Organized'} {organized_count}/{total_files} files")
        
        if not dry_run and organized_count > 0:
            self.save_organization_log()
    
    def save_organization_log(self) -> None:
        """Save a log of organized files for potential undo operation."""
        log_file = self.directory / "organization_log.json"
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'directory': str(self.directory),
            'organized_files': self.organized_files
        }
        
        try:
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
            print(f"📝 Organization log saved to {log_file}")
        except IOError as e:
            print(f"⚠️  Could not save organization log: {e}")
    
    def undo_organization(self) -> None:
        """Undo the last organization operation."""
        log_file = self.directory / "organization_log.json"
        
        if not log_file.exists():
            print("❌ No organization log found. Cannot undo.")
            return
        
        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)
            
            print("🔄 Undoing last organization...")
            
            for file_info in reversed(log_data['organized_files']):
                original_path = Path(file_info['original'])
                current_path = Path(file_info['new'])
                
                if current_path.exists():
                    try:
                        shutil.move(str(current_path), str(original_path))
                        print(f"↩️  Restored: {original_path.name}")
                    except (PermissionError, FileNotFoundError, shutil.Error) as e:
                        print(f"❌ Error restoring {original_path.name}: {e}")
            
            # Remove empty category folders
            for category in set(file_info['category'] for file_info in log_data['organized_files']):
                category_path = self.directory / category
                if category_path.exists() and category_path.is_dir():
                    try:
                        if not any(category_path.iterdir()):  # Check if empty
                            category_path.rmdir()
                            print(f"🗑️  Removed empty folder: {category}")
                    except OSError:
                        pass  # Folder not empty or permission error
            
            # Remove the log file
            log_file.unlink()
            print("✅ Undo operation completed!")
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Error reading organization log: {e}")
    
    def display_stats(self) -> None:
        """Display statistics about the directory."""
        categorized_files = self.scan_directory()
        
        print(f"📊 Directory Statistics: {self.directory}")
        print("=" * 40)
        
        total_files = 0
        for category, files in categorized_files.items():
            file_count = len(files)
            total_files += file_count
            print(f"{category:<15}: {file_count:>3} files")
        
        print("-" * 40)
        print(f"{'Total':<15}: {total_files:>3} files")


def main():
    """Main function to run the File Organizer."""
    parser = argparse.ArgumentParser(description="Organize files by their extensions")
    parser.add_argument("--directory", "-d", 
                       help="Directory to organize (default: current directory)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Preview changes without actually moving files")
    parser.add_argument("--undo", action="store_true",
                       help="Undo the last organization operation")
    parser.add_argument("--stats", action="store_true",
                       help="Show directory statistics only")
    parser.add_argument("--config", default="config.json",
                       help="Configuration file path")
    
    args = parser.parse_args()
    
    # Create organizer instance
    organizer = FileOrganizer(args.directory, args.config)
    
    # Handle different operations
    if args.undo:
        organizer.undo_organization()
    elif args.stats:
        organizer.display_stats()
    else:
        # Show stats before organization
        organizer.display_stats()
        print()
        
        # Ask for confirmation if not dry run
        if not args.dry_run:
            response = input("Do you want to proceed with organization? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("❌ Organization cancelled.")
                return
        
        # Organize files
        organizer.organize(args.dry_run)


if __name__ == "__main__":
    main()
