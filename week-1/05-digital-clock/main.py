#!/usr/bin/env python3
"""
Digital Clock - Project #5
A simple digital clock using Python that updates in real time.

Author: Task Ninja Python Series
Project: Week 1 - Python Mini Projects
"""

import sys
import time
import argparse
from datetime import datetime
from typing import Optional

try:
    from tkinter import Tk, Label, Frame, Button, messagebox, colorchooser
    from tkinter import font as tk_font
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("⚠️  tkinter not available. GUI mode disabled.")


class DigitalClock:
    """A digital clock with both CLI and GUI modes."""
    
    def __init__(self, cli_mode: bool = False):
        """
        Initialize the digital clock.
        
        Args:
            cli_mode (bool): Whether to run in CLI mode
        """
        self.cli_mode = cli_mode
        self.running = True
        self.format_24h = True
        self.show_date = True
        self.bg_color = "black"
        self.fg_color = "cyan"
        self.font_family = "Helvetica"
        self.font_size = 40
        
        if not cli_mode and GUI_AVAILABLE:
            self.setup_gui()
    
    def setup_gui(self):
        """Set up the GUI components."""
        self.app = Tk()
        self.app.title("🕒 Digital Clock")
        self.app.geometry("400x150")
        self.app.resizable(False, False)
        self.app.configure(bg=self.bg_color)
        
        # Handle window close
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create main frame
        self.main_frame = Frame(self.app, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill='both')
        
        # Clock label
        self.clock_label = Label(
            self.main_frame,
            bg=self.bg_color,
            fg=self.fg_color,
            font=(self.font_family, self.font_size),
            relief='flat'
        )
        self.clock_label.pack(expand=True)
        
        # Date label
        self.date_label = Label(
            self.main_frame,
            bg=self.bg_color,
            fg=self.fg_color,
            font=(self.font_family, 12),
            relief='flat'
        )
        self.date_label.pack()
        
        # Control buttons frame
        self.controls_frame = Frame(self.app, bg=self.bg_color)
        self.controls_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        
        # Buttons
        Button(self.controls_frame, text="Format", command=self.toggle_format,
               bg="gray20", fg="white", font=("Arial", 8)).pack(side='left', padx=2)
        Button(self.controls_frame, text="Date", command=self.toggle_date,
               bg="gray20", fg="white", font=("Arial", 8)).pack(side='left', padx=2)
        Button(self.controls_frame, text="Colors", command=self.change_colors,
               bg="gray20", fg="white", font=("Arial", 8)).pack(side='left', padx=2)
        Button(self.controls_frame, text="Fullscreen", command=self.toggle_fullscreen,
               bg="gray20", fg="white", font=("Arial", 8)).pack(side='right', padx=2)
        
        # Start the clock
        self.update_gui_time()
    
    def get_current_time(self) -> str:
        """Get current time as formatted string."""
        now = datetime.now()
        
        if self.format_24h:
            time_str = now.strftime("%H:%M:%S")
        else:
            time_str = now.strftime("%I:%M:%S %p")
        
        return time_str
    
    def get_current_date(self) -> str:
        """Get current date as formatted string."""
        now = datetime.now()
        return now.strftime("%A, %B %d, %Y")
    
    def update_gui_time(self):
        """Update the GUI clock display."""
        if not self.running:
            return
        
        current_time = self.get_current_time()
        self.clock_label.config(text=current_time)
        
        if self.show_date:
            current_date = self.get_current_date()
            self.date_label.config(text=current_date)
            self.date_label.pack()
        else:
            self.date_label.pack_forget()
        
        # Schedule next update
        self.clock_label.after(1000, self.update_gui_time)
    
    def toggle_format(self):
        """Toggle between 12h and 24h format."""
        self.format_24h = not self.format_24h
        print(f"⏰ Switched to {'24-hour' if self.format_24h else '12-hour'} format")
    
    def toggle_date(self):
        """Toggle date display."""
        self.show_date = not self.show_date
        print(f"📅 Date display {'enabled' if self.show_date else 'disabled'}")
    
    def change_colors(self):
        """Change clock colors."""
        try:
            # Choose background color
            bg_color = colorchooser.askcolor(title="Choose background color")[1]
            if bg_color:
                self.bg_color = bg_color
                self.app.configure(bg=bg_color)
                self.main_frame.configure(bg=bg_color)
                self.controls_frame.configure(bg=bg_color)
            
            # Choose text color
            fg_color = colorchooser.askcolor(title="Choose text color")[1]
            if fg_color:
                self.fg_color = fg_color
                self.clock_label.configure(bg=self.bg_color, fg=fg_color)
                self.date_label.configure(bg=self.bg_color, fg=fg_color)
        except Exception as e:
            print(f"❌ Error changing colors: {e}")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        try:
            current_state = self.app.attributes('-fullscreen')
            self.app.attributes('-fullscreen', not current_state)
            
            if not current_state:  # Going to fullscreen
                self.font_size = 80
                self.clock_label.configure(font=(self.font_family, self.font_size))
                self.controls_frame.pack_forget()
            else:  # Exiting fullscreen
                self.font_size = 40
                self.clock_label.configure(font=(self.font_family, self.font_size))
                self.controls_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        except Exception as e:
            print(f"❌ Error toggling fullscreen: {e}")
    
    def on_closing(self):
        """Handle window closing."""
        self.running = False
        self.app.destroy()
    
    def run_gui(self):
        """Run the GUI version."""
        if not GUI_AVAILABLE:
            print("❌ GUI not available. Please install tkinter or use CLI mode.")
            return
        
        print("🕒 Starting Digital Clock GUI...")
        print("💡 Use the buttons to customize your clock!")
        print("🖱️  Click 'Fullscreen' for a larger display")
        print("⌨️  Press ESC in fullscreen to exit")
        
        # Bind escape key for fullscreen exit
        self.app.bind('<Escape>', lambda e: self.app.attributes('-fullscreen', False))
        
        try:
            self.app.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Clock stopped. Goodbye!")
        finally:
            self.running = False
    
    def run_cli(self):
        """Run the CLI version."""
        print("🕒 Digital Clock (CLI Mode)")
        print("=" * 40)
        print("Controls:")
        print("- Ctrl+C to exit")
        print("- Format:", "24-hour" if self.format_24h else "12-hour")
        print("- Date display:", "enabled" if self.show_date else "disabled")
        print("-" * 40)
        
        try:
            while self.running:
                # Clear screen (works on most terminals)
                print("\033[2J\033[H", end="")
                
                # Display clock
                current_time = self.get_current_time()
                print(f"\n{'':>15}🕒 {current_time}")
                
                if self.show_date:
                    current_date = self.get_current_date()
                    print(f"{'':>10}{current_date}")
                
                print(f"\n{'':>15}Press Ctrl+C to exit")
                
                # Wait for 1 second
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n👋 Digital Clock stopped. Goodbye!")
        finally:
            self.running = False


def simple_gui_clock():
    """Simple GUI clock matching the original code."""
    if not GUI_AVAILABLE:
        print("❌ tkinter not available for GUI mode")
        return
    
    app = Tk()
    app.title("🕒 Digital Clock")
    app.geometry("300x100")
    app.resizable(False, False)
    app.configure(bg="black")
    
    clock_label = Label(
        app, 
        bg="black", 
        fg="cyan", 
        font=("Helvetica", 40), 
        relief='flat'
    )
    clock_label.place(x=20, y=20)
    
    def update_time():
        current_time = time.strftime("%H:%M:%S")
        clock_label.config(text=current_time)
        clock_label.after(1000, update_time)
    
    update_time()
    
    print("🕒 Simple Digital Clock started!")
    print("Close the window to exit.")
    
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\n👋 Clock stopped.")


def main():
    """Main function to run the digital clock."""
    parser = argparse.ArgumentParser(description="Digital Clock Application")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--simple", action="store_true", help="Run simple GUI (original code)")
    parser.add_argument("--format", choices=["12", "24"], default="24", help="Time format")
    parser.add_argument("--no-date", action="store_true", help="Hide date display")
    
    args = parser.parse_args()
    
    if args.simple:
        simple_gui_clock()
        return
    
    # Create clock instance
    clock = DigitalClock(cli_mode=args.cli)
    
    # Apply command line options
    clock.format_24h = (args.format == "24")
    clock.show_date = not args.no_date
    
    # Welcome message
    print("🎉 Welcome to Digital Clock!")
    
    if args.cli or not GUI_AVAILABLE:
        clock.run_cli()
    else:
        clock.run_gui()


if __name__ == "__main__":
    # If no arguments provided, show usage and run simple version
    if len(sys.argv) == 1:
        print("🕒 Digital Clock - Running simple GUI version")
        print("Use --help for more options")
        simple_gui_clock()
    else:
        main()
