#!/usr/bin/env python3
"""
WhatsApp Message Automation - Project #13
=========================================

A comprehensive WhatsApp automation tool using pywhatkit for sending scheduled messages,
bulk messaging, media sharing, and contact management with an interactive CLI interface.

Author: Task Ninja Python Series
Created: 2024
"""

import pywhatkit as pwk
import pandas as pd
import os
import json
import time
import schedule
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import sys
from pathlib import Path
import threading
import re


class ContactManager:
    """Manage WhatsApp contacts and contact lists."""
    
    def __init__(self):
        self.contacts_file = "contacts.json"
        self.contacts = self._load_contacts()
    
    def _load_contacts(self) -> Dict[str, str]:
        """Load contacts from JSON file."""
        try:
            if os.path.exists(self.contacts_file):
                with open(self.contacts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading contacts: {e}")
        return {}
    
    def _save_contacts(self):
        """Save contacts to JSON file."""
        try:
            with open(self.contacts_file, 'w', encoding='utf-8') as f:
                json.dump(self.contacts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving contacts: {e}")
    
    def add_contact(self, phone: str, name: str) -> bool:
        """Add a new contact."""
        if self._validate_phone(phone):
            self.contacts[phone] = name
            self._save_contacts()
            print(f"✅ Added contact: {name} ({phone})")
            return True
        else:
            print(f"❌ Invalid phone number format: {phone}")
            return False
    
    def remove_contact(self, phone: str) -> bool:
        """Remove a contact."""
        if phone in self.contacts:
            name = self.contacts.pop(phone)
            self._save_contacts()
            print(f"✅ Removed contact: {name} ({phone})")
            return True
        else:
            print(f"❌ Contact not found: {phone}")
            return False
    
    def get_contact_name(self, phone: str) -> str:
        """Get contact name by phone number."""
        return self.contacts.get(phone, phone)
    
    def list_contacts(self) -> List[Tuple[str, str]]:
        """Get list of all contacts."""
        return [(phone, name) for phone, name in self.contacts.items()]
    
    def _validate_phone(self, phone: str) -> bool:
        """Validate phone number format."""
        # Basic validation for international format
        pattern = r'^\+\d{1,4}\d{6,14}$'
        return bool(re.match(pattern, phone))
    
    def import_from_csv(self, csv_file: str) -> int:
        """Import contacts from CSV file."""
        try:
            df = pd.read_csv(csv_file)
            count = 0
            
            for _, row in df.iterrows():
                phone = str(row.get('phone', '')).strip()
                name = str(row.get('name', '')).strip()
                
                if phone and name and self._validate_phone(phone):
                    self.contacts[phone] = name
                    count += 1
            
            self._save_contacts()
            print(f"✅ Imported {count} contacts from {csv_file}")
            return count
            
        except Exception as e:
            print(f"❌ Error importing contacts: {e}")
            return 0


class MessageTemplates:
    """Manage message templates for common use cases."""
    
    def __init__(self):
        self.templates_file = "message_templates.json"
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load message templates from file."""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        
        # Default templates
        return {
            "greeting": "Hello! Hope you're having a great day! 😊",
            "reminder": "⏰ Reminder: Don't forget about {event} at {time}!",
            "birthday": "🎉 Happy Birthday! Wishing you all the best on your special day! 🎂",
            "meeting": "📅 Meeting reminder: {meeting_title} at {time}. See you there!",
            "promotion": "🔥 Special offer just for you! Check out our latest deals.",
            "thank_you": "🙏 Thank you for your support! We truly appreciate it.",
            "follow_up": "👋 Following up on our previous conversation. Let me know if you need anything!",
            "holiday": "🎊 Wishing you and your family a wonderful {holiday}! Enjoy!"
        }
    
    def _save_templates(self):
        """Save templates to file."""
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving templates: {e}")
    
    def get_template(self, name: str) -> Optional[str]:
        """Get a message template by name."""
        return self.templates.get(name)
    
    def list_templates(self) -> Dict[str, str]:
        """Get all available templates."""
        return self.templates.copy()
    
    def add_template(self, name: str, message: str):
        """Add a new template."""
        self.templates[name] = message
        self._save_templates()
        print(f"✅ Template '{name}' added successfully!")
    
    def format_template(self, template: str, **kwargs) -> str:
        """Format template with variables."""
        try:
            return template.format(**kwargs)
        except KeyError as e:
            print(f"⚠️ Missing template variable: {e}")
            return template


class MessageLogger:
    """Log sent messages for tracking and analytics."""
    
    def __init__(self):
        self.log_file = "message_log.json"
        self.logs = self._load_logs()
    
    def _load_logs(self) -> List[Dict]:
        """Load message logs from file."""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def _save_logs(self):
        """Save logs to file."""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.logs, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"❌ Error saving logs: {e}")
    
    def log_message(self, phone: str, message: str, status: str = "sent", message_type: str = "text"):
        """Log a sent message."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "phone": phone,
            "message": message[:100] + "..." if len(message) > 100 else message,
            "status": status,
            "type": message_type
        }
        
        self.logs.append(log_entry)
        
        # Keep only last 1000 logs
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
        
        self._save_logs()
    
    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        """Get recent message logs."""
        return self.logs[-count:] if self.logs else []
    
    def get_stats(self) -> Dict:
        """Get messaging statistics."""
        if not self.logs:
            return {"total": 0, "success": 0, "failed": 0}
        
        total = len(self.logs)
        success = len([log for log in self.logs if log.get('status') == 'sent'])
        failed = total - success
        
        return {
            "total": total,
            "success": success,
            "failed": failed,
            "success_rate": f"{(success/total)*100:.1f}%" if total > 0 else "0%"
        }


class WhatsAppAutomation:
    """Main WhatsApp automation class."""
    
    def __init__(self):
        self.contacts = ContactManager()
        self.templates = MessageTemplates()
        self.logger = MessageLogger()
        self.scheduled_jobs = []
    
    def send_instant_message(self, phone: str, message: str) -> bool:
        """Send an instant WhatsApp message."""
        try:
            print(f"📤 Sending instant message to {self.contacts.get_contact_name(phone)}...")
            print("🌐 Opening WhatsApp Web...")
            
            # Send message instantly (with 15 second delay)
            pwk.sendwhatmsg_instantly(phone, message, 15, True)
            
            print("✅ Message sent successfully!")
            self.logger.log_message(phone, message, "sent", "instant")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            self.logger.log_message(phone, message, "failed", "instant")
            return False
    
    def schedule_message(self, phone: str, message: str, hour: int, minute: int) -> bool:
        """Schedule a WhatsApp message for specific time."""
        try:
            print(f"📅 Scheduling message to {self.contacts.get_contact_name(phone)} for {hour:02d}:{minute:02d}")
            print("🌐 Opening WhatsApp Web...")
            
            # Schedule message
            pwk.sendwhatmsg(phone, message, hour, minute)
            
            print("✅ Message scheduled and sent successfully!")
            self.logger.log_message(phone, message, "sent", "scheduled")
            return True
            
        except Exception as e:
            print(f"❌ Failed to schedule message: {e}")
            self.logger.log_message(phone, message, "failed", "scheduled")
            return False
    
    def send_bulk_messages(self, phone_list: List[str], message: str, delay: int = 20) -> Dict:
        """Send bulk messages to multiple contacts."""
        results = {"success": 0, "failed": 0, "total": len(phone_list)}
        
        print(f"📤 Starting bulk message to {results['total']} contacts...")
        print(f"⏱️ Using {delay} second delay between messages")
        
        for i, phone in enumerate(phone_list, 1):
            contact_name = self.contacts.get_contact_name(phone)
            print(f"\n📱 [{i}/{results['total']}] Sending to {contact_name}...")
            
            try:
                pwk.sendwhatmsg_instantly(phone, message, delay, True)
                print(f"✅ Message sent to {contact_name}")
                self.logger.log_message(phone, message, "sent", "bulk")
                results["success"] += 1
                
            except Exception as e:
                print(f"❌ Failed to send to {contact_name}: {e}")
                self.logger.log_message(phone, message, "failed", "bulk")
                results["failed"] += 1
            
            # Additional delay between messages
            if i < len(phone_list):
                print(f"⏳ Waiting {delay} seconds before next message...")
                time.sleep(delay)
        
        return results
    
    def send_media_message(self, phone: str, media_path: str, caption: str = "") -> bool:
        """Send media file (image) with optional caption."""
        try:
            if not os.path.exists(media_path):
                print(f"❌ Media file not found: {media_path}")
                return False
            
            contact_name = self.contacts.get_contact_name(phone)
            print(f"📸 Sending media to {contact_name}...")
            print("🌐 Opening WhatsApp Web...")
            
            # Send image immediately
            pwk.sendwhats_image(phone, media_path, caption, 15, True)
            
            print("✅ Media sent successfully!")
            self.logger.log_message(phone, f"Media: {os.path.basename(media_path)}", "sent", "media")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send media: {e}")
            self.logger.log_message(phone, f"Media: {os.path.basename(media_path)}", "failed", "media")
            return False
    
    def create_recurring_message(self, phone: str, message: str, schedule_time: str, frequency: str = "daily"):
        """Create a recurring message schedule."""
        def job():
            self.send_instant_message(phone, message)
        
        if frequency == "daily":
            schedule.every().day.at(schedule_time).do(job)
        elif frequency == "weekly":
            schedule.every().week.at(schedule_time).do(job)
        elif frequency == "hourly":
            schedule.every().hour.do(job)
        
        self.scheduled_jobs.append(job)
        print(f"✅ Recurring message scheduled ({frequency}) at {schedule_time}")
    
    def run_scheduler(self):
        """Run the message scheduler in background."""
        def scheduler_loop():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        scheduler_thread.start()
        print("⏰ Message scheduler started in background")


class WhatsAppApp:
    """Main application interface."""
    
    def __init__(self):
        self.automation = WhatsAppAutomation()
        print("💬 WhatsApp Automation Tool Initialized!")
        print("⚠️ Make sure you're logged into WhatsApp Web in your default browser")
    
    def display_menu(self):
        """Display main menu."""
        print("\n" + "="*50)
        print("💬 WhatsApp Automation Tool")
        print("="*50)
        print("1. 📅 Schedule Message")
        print("2. ⚡ Send Instant Message")
        print("3. 📤 Bulk Messaging")
        print("4. 📁 Send Media")
        print("5. 👥 Manage Contacts")
        print("6. 📝 Message Templates")
        print("7. 🔄 Recurring Messages")
        print("8. 📊 Message Statistics")
        print("9. 📜 Recent Message Logs")
        print("0. 🚪 Exit")
        print("="*50)
    
    def handle_schedule_message(self):
        """Handle scheduled message input."""
        print("\n📅 Schedule Message")
        print("="*20)
        
        phone = input("📞 Enter phone number (with country code): ").strip()
        if not phone.startswith('+'):
            phone = '+' + phone
        
        # Show templates
        templates = self.automation.templates.list_templates()
        if templates:
            print("\n📝 Available templates:")
            for i, (name, _) in enumerate(templates.items(), 1):
                print(f"{i}. {name}")
            
            use_template = input("\nUse template? (y/n): ").strip().lower() == 'y'
            if use_template:
                try:
                    template_num = int(input("Enter template number: ")) - 1
                    template_name = list(templates.keys())[template_num]
                    message = templates[template_name]
                    
                    # Ask for template variables
                    if '{' in message and '}' in message:
                        print("📝 This template requires variables:")
                        variables = {}
                        import re
                        var_names = re.findall(r'\{(\w+)\}', message)
                        for var in var_names:
                            variables[var] = input(f"Enter {var}: ")
                        message = self.automation.templates.format_template(message, **variables)
                    
                except (ValueError, IndexError):
                    message = input("💬 Enter message: ")
            else:
                message = input("💬 Enter message: ")
        else:
            message = input("💬 Enter message: ")
        
        try:
            hour = int(input("🕐 Enter hour (24-hour format): "))
            minute = int(input("🕐 Enter minute: "))
            
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                self.automation.schedule_message(phone, message, hour, minute)
            else:
                print("❌ Invalid time format")
        except ValueError:
            print("❌ Please enter valid numbers for time")
    
    def handle_instant_message(self):
        """Handle instant message input."""
        print("\n⚡ Send Instant Message")
        print("="*25)
        
        phone = input("📞 Enter phone number (with country code): ").strip()
        if not phone.startswith('+'):
            phone = '+' + phone
        
        message = input("💬 Enter message: ")
        
        confirm = input(f"\n📤 Send message to {self.automation.contacts.get_contact_name(phone)}? (y/n): ")
        if confirm.strip().lower() == 'y':
            self.automation.send_instant_message(phone, message)
    
    def handle_bulk_messaging(self):
        """Handle bulk messaging setup."""
        print("\n📤 Bulk Messaging")
        print("="*17)
        
        print("Select contact source:")
        print("1. Enter phone numbers manually")
        print("2. Use saved contacts")
        print("3. Import from CSV file")
        
        choice = input("Enter choice: ").strip()
        phone_list = []
        
        if choice == '1':
            print("Enter phone numbers (one per line, press Enter twice to finish):")
            while True:
                phone = input("📞 Phone: ").strip()
                if not phone:
                    break
                if not phone.startswith('+'):
                    phone = '+' + phone
                phone_list.append(phone)
        
        elif choice == '2':
            contacts = self.automation.contacts.list_contacts()
            if contacts:
                print("\n👥 Saved Contacts:")
                for i, (phone, name) in enumerate(contacts, 1):
                    print(f"{i}. {name} ({phone})")
                
                selected = input("\nEnter contact numbers (comma-separated) or 'all': ").strip()
                if selected.lower() == 'all':
                    phone_list = [phone for phone, _ in contacts]
                else:
                    try:
                        indices = [int(x.strip()) - 1 for x in selected.split(',')]
                        phone_list = [contacts[i][0] for i in indices if 0 <= i < len(contacts)]
                    except (ValueError, IndexError):
                        print("❌ Invalid selection")
                        return
            else:
                print("❌ No saved contacts found")
                return
        
        elif choice == '3':
            csv_file = input("📁 Enter CSV file path: ").strip()
            try:
                df = pd.read_csv(csv_file)
                phone_list = ['+' + str(phone).strip() for phone in df['phone'] if pd.notna(phone)]
                print(f"📊 Loaded {len(phone_list)} contacts from CSV")
            except Exception as e:
                print(f"❌ Error reading CSV: {e}")
                return
        
        if not phone_list:
            print("❌ No contacts selected")
            return
        
        message = input("💬 Enter message: ")
        delay = input("⏱️ Delay between messages (seconds, default 20): ").strip()
        delay = int(delay) if delay.isdigit() else 20
        
        print(f"\n📊 Ready to send to {len(phone_list)} contacts with {delay}s delay")
        confirm = input("Continue? (y/n): ").strip().lower()
        
        if confirm == 'y':
            results = self.automation.send_bulk_messages(phone_list, message, delay)
            print(f"\n📈 Bulk messaging complete!")
            print(f"✅ Success: {results['success']}")
            print(f"❌ Failed: {results['failed']}")
            print(f"📊 Total: {results['total']}")
    
    def handle_media_message(self):
        """Handle media message sending."""
        print("\n📁 Send Media")
        print("="*12)
        
        phone = input("📞 Enter phone number (with country code): ").strip()
        if not phone.startswith('+'):
            phone = '+' + phone
        
        media_path = input("📁 Enter media file path: ").strip()
        caption = input("📝 Enter caption (optional): ").strip()
        
        if os.path.exists(media_path):
            self.automation.send_media_message(phone, media_path, caption)
        else:
            print("❌ Media file not found")
    
    def handle_contact_management(self):
        """Handle contact management."""
        while True:
            print("\n👥 Contact Management")
            print("="*20)
            print("1. ➕ Add Contact")
            print("2. ❌ Remove Contact")
            print("3. 📋 List Contacts")
            print("4. 📥 Import from CSV")
            print("0. ⬅️ Back")
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                phone = input("📞 Phone number (with country code): ").strip()
                if not phone.startswith('+'):
                    phone = '+' + phone
                name = input("👤 Name: ").strip()
                self.automation.contacts.add_contact(phone, name)
            
            elif choice == '2':
                phone = input("📞 Phone number to remove: ").strip()
                if not phone.startswith('+'):
                    phone = '+' + phone
                self.automation.contacts.remove_contact(phone)
            
            elif choice == '3':
                contacts = self.automation.contacts.list_contacts()
                if contacts:
                    print("\n📋 Saved Contacts:")
                    for i, (phone, name) in enumerate(contacts, 1):
                        print(f"{i:2d}. {name:<20} {phone}")
                else:
                    print("📭 No contacts saved")
            
            elif choice == '4':
                csv_file = input("📁 CSV file path: ").strip()
                count = self.automation.contacts.import_from_csv(csv_file)
                if count > 0:
                    print(f"✅ Successfully imported {count} contacts")
    
    def handle_message_templates(self):
        """Handle message template management."""
        while True:
            print("\n📝 Message Templates")
            print("="*20)
            print("1. 📋 List Templates")
            print("2. ➕ Add Template")
            print("3. 🔧 Use Template")
            print("0. ⬅️ Back")
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                templates = self.automation.templates.list_templates()
                print("\n📋 Available Templates:")
                for name, message in templates.items():
                    print(f"\n🏷️ {name}:")
                    print(f"   {message[:80]}{'...' if len(message) > 80 else ''}")
            
            elif choice == '2':
                name = input("🏷️ Template name: ").strip()
                message = input("💬 Template message: ").strip()
                self.automation.templates.add_template(name, message)
            
            elif choice == '3':
                templates = self.automation.templates.list_templates()
                if templates:
                    print("\n📋 Available Templates:")
                    template_names = list(templates.keys())
                    for i, name in enumerate(template_names, 1):
                        print(f"{i}. {name}")
                    
                    try:
                        template_num = int(input("Select template: ")) - 1
                        if 0 <= template_num < len(template_names):
                            template_name = template_names[template_num]
                            message = templates[template_name]
                            print(f"\n📝 Template: {message}")
                            
                            phone = input("📞 Phone number: ").strip()
                            if not phone.startswith('+'):
                                phone = '+' + phone
                            
                            self.automation.send_instant_message(phone, message)
                    except ValueError:
                        print("❌ Invalid selection")
                else:
                    print("📭 No templates available")
    
    def handle_recurring_messages(self):
        """Handle recurring message setup."""
        print("\n🔄 Recurring Messages")
        print("="*20)
        
        phone = input("📞 Phone number: ").strip()
        if not phone.startswith('+'):
            phone = '+' + phone
        
        message = input("💬 Message: ").strip()
        
        print("\n⏰ Frequency options:")
        print("1. Daily")
        print("2. Weekly")
        print("3. Hourly")
        
        freq_choice = input("Select frequency: ").strip()
        frequency_map = {'1': 'daily', '2': 'weekly', '3': 'hourly'}
        frequency = frequency_map.get(freq_choice, 'daily')
        
        if frequency != 'hourly':
            schedule_time = input("⏰ Time (HH:MM format): ").strip()
        else:
            schedule_time = "00:00"  # Not used for hourly
        
        self.automation.create_recurring_message(phone, message, schedule_time, frequency)
        
        # Start scheduler if not already running
        self.automation.run_scheduler()
    
    def show_statistics(self):
        """Show messaging statistics."""
        print("\n📊 Message Statistics")
        print("="*20)
        
        stats = self.automation.logger.get_stats()
        print(f"📈 Total Messages: {stats['total']}")
        print(f"✅ Successful: {stats['success']}")
        print(f"❌ Failed: {stats['failed']}")
        print(f"📊 Success Rate: {stats['success_rate']}")
    
    def show_recent_logs(self):
        """Show recent message logs."""
        print("\n📜 Recent Message Logs")
        print("="*22)
        
        logs = self.automation.logger.get_recent_logs(10)
        if logs:
            for log in reversed(logs):  # Show newest first
                timestamp = datetime.fromisoformat(log['timestamp']).strftime("%m/%d %H:%M")
                phone = log['phone']
                message = log['message']
                status = log['status']
                msg_type = log['type']
                
                status_icon = "✅" if status == "sent" else "❌"
                print(f"{status_icon} {timestamp} | {phone} | {msg_type} | {message}")
        else:
            print("📭 No message logs found")
    
    def run(self):
        """Main application loop."""
        print("\n💬 Welcome to WhatsApp Automation Tool!")
        print("🔧 Make sure WhatsApp Web is logged in on your default browser")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (0-9): ").strip()
                
                if choice == '0':
                    print("\n👋 Thanks for using WhatsApp Automation Tool!")
                    break
                
                elif choice == '1':
                    self.handle_schedule_message()
                
                elif choice == '2':
                    self.handle_instant_message()
                
                elif choice == '3':
                    self.handle_bulk_messaging()
                
                elif choice == '4':
                    self.handle_media_message()
                
                elif choice == '5':
                    self.handle_contact_management()
                
                elif choice == '6':
                    self.handle_message_templates()
                
                elif choice == '7':
                    self.handle_recurring_messages()
                
                elif choice == '8':
                    self.show_statistics()
                
                elif choice == '9':
                    self.show_recent_logs()
                
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
    """Entry point of the application."""
    try:
        # Check if pywhatkit is installed
        import pywhatkit
        print("✅ pywhatkit library detected")
        
        app = WhatsAppApp()
        app.run()
        
    except ImportError:
        print("❌ pywhatkit library not found!")
        print("📦 Install it with: pip install pywhatkit")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start WhatsApp Automation Tool: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
