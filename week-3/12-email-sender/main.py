#!/usr/bin/env python3
"""
Email Sender Script - Project #12
Automate email sending with SMTP for reminders, reports, and alerts.

Author: Task Ninja Python Series
Project: Week 3 - Automation with Python
"""

import smtplib
import os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Dict
import json
from datetime import datetime


class EmailSender:
    """A class to handle email sending operations."""
    
    def __init__(self, config_file: str = "email_config.json"):
        """
        Initialize the EmailSender.
        
        Args:
            config_file (str): Configuration file path
        """
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """
        Load email configuration.
        
        Returns:
            Dict: Email configuration
        """
        # Default configuration
        default_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "use_tls": True,
            "sender_email": "",
            "sender_password": "",
            "sender_name": "Python Email Sender"
        }
        
        # Try to load from file
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                    default_config.update(file_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  Error loading config file: {e}")
        
        # Override with environment variables if available
        env_config = {
            "sender_email": os.getenv("EMAIL_ADDRESS", default_config["sender_email"]),
            "sender_password": os.getenv("EMAIL_PASSWORD", default_config["sender_password"]),
            "smtp_server": os.getenv("SMTP_SERVER", default_config["smtp_server"]),
            "smtp_port": int(os.getenv("SMTP_PORT", default_config["smtp_port"])),
        }
        
        default_config.update({k: v for k, v in env_config.items() if v})
        
        return default_config
    
    def setup_smtp_connection(self) -> smtplib.SMTP:
        """
        Set up SMTP connection.
        
        Returns:
            smtplib.SMTP: SMTP server connection
        """
        try:
            if self.config["use_tls"]:
                server = smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"])
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.config["smtp_server"], self.config["smtp_port"])
            
            server.login(self.config["sender_email"], self.config["sender_password"])
            return server
        
        except smtplib.SMTPAuthenticationError:
            raise Exception("❌ Email authentication failed. Check your credentials.")
        except smtplib.SMTPConnectError:
            raise Exception("❌ Failed to connect to SMTP server.")
        except Exception as e:
            raise Exception(f"❌ SMTP connection error: {e}")
    
    def send_simple_email(self, to: str, subject: str, body: str) -> bool:
        """
        Send a simple text email.
        
        Args:
            to (str): Recipient email address
            subject (str): Email subject
            body (str): Email body text
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create message
            msg = EmailMessage()
            msg['From'] = f"{self.config['sender_name']} <{self.config['sender_email']}>"
            msg['To'] = to
            msg['Subject'] = subject
            msg.set_content(body)
            
            # Send email
            with self.setup_smtp_connection() as server:
                server.send_message(msg)
            
            print(f"✅ Email sent successfully to {to}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {to}: {e}")
            return False
    
    def send_html_email(self, to: str, subject: str, html_content: str, 
                       text_content: Optional[str] = None, 
                       attachments: Optional[List[str]] = None) -> bool:
        """
        Send an HTML email with optional attachments.
        
        Args:
            to (str): Recipient email address
            subject (str): Email subject
            html_content (str): HTML content
            text_content (Optional[str]): Plain text alternative
            attachments (Optional[List[str]]): List of file paths to attach
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.config['sender_name']} <{self.config['sender_email']}>"
            msg['To'] = to
            msg['Subject'] = subject
            msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            
            # Add text content
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if self.add_attachment(msg, file_path):
                        print(f"📎 Attached: {Path(file_path).name}")
                    else:
                        print(f"⚠️  Failed to attach: {file_path}")
            
            # Send email
            with self.setup_smtp_connection() as server:
                server.send_message(msg)
            
            print(f"✅ HTML email sent successfully to {to}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send HTML email to {to}: {e}")
            return False
    
    def add_attachment(self, msg: MIMEMultipart, file_path: str) -> bool:
        """
        Add an attachment to the email message.
        
        Args:
            msg (MIMEMultipart): Email message object
            file_path (str): Path to the file to attach
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                print(f"❌ Attachment file not found: {file_path}")
                return False
            
            # Check file size (limit to 25MB)
            file_size = file_path.stat().st_size
            if file_size > 25 * 1024 * 1024:  # 25MB
                print(f"❌ Attachment too large (>25MB): {file_path}")
                return False
            
            # Read and attach file
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {file_path.name}'
            )
            
            msg.attach(part)
            return True
            
        except Exception as e:
            print(f"❌ Error adding attachment {file_path}: {e}")
            return False
    
    def send_bulk_emails(self, recipients: List[str], subject: str, 
                        body: str, is_html: bool = False) -> Dict[str, bool]:
        """
        Send emails to multiple recipients.
        
        Args:
            recipients (List[str]): List of recipient email addresses
            subject (str): Email subject
            body (str): Email body
            is_html (bool): Whether body is HTML
            
        Returns:
            Dict[str, bool]: Dictionary mapping recipients to success status
        """
        results = {}
        
        print(f"📧 Sending bulk emails to {len(recipients)} recipients...")
        
        for i, recipient in enumerate(recipients, 1):
            print(f"Sending {i}/{len(recipients)} to {recipient}...")
            
            if is_html:
                success = self.send_html_email(recipient, subject, body)
            else:
                success = self.send_simple_email(recipient, subject, body)
            
            results[recipient] = success
        
        # Summary
        successful = sum(results.values())
        print(f"\n📊 Bulk email summary:")
        print(f"✅ Successful: {successful}/{len(recipients)}")
        print(f"❌ Failed: {len(recipients) - successful}/{len(recipients)}")
        
        return results
    
    def load_email_template(self, template_path: str, **kwargs) -> str:
        """
        Load and populate an email template.
        
        Args:
            template_path (str): Path to template file
            **kwargs: Variables to substitute in template
            
        Returns:
            str: Populated template content
        """
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Simple variable substitution
            for key, value in kwargs.items():
                template = template.replace(f"{{{key}}}", str(value))
            
            return template
            
        except FileNotFoundError:
            print(f"❌ Template file not found: {template_path}")
            return ""
        except Exception as e:
            print(f"❌ Error loading template: {e}")
            return ""


def load_recipients_from_file(file_path: str) -> List[str]:
    """
    Load recipient emails from a text file.
    
    Args:
        file_path (str): Path to file containing emails (one per line)
        
    Returns:
        List[str]: List of email addresses
    """
    try:
        with open(file_path, 'r') as f:
            emails = [line.strip() for line in f if line.strip() and '@' in line]
        return emails
    except FileNotFoundError:
        print(f"❌ Recipients file not found: {file_path}")
        return []


def interactive_email_sender():
    """Interactive email sending interface."""
    print("📧 Interactive Email Sender")
    print("=" * 30)
    
    sender = EmailSender()
    
    # Check configuration
    if not sender.config['sender_email'] or not sender.config['sender_password']:
        print("❌ Email configuration incomplete!")
        print("Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables")
        print("or create an email_config.json file.")
        return
    
    while True:
        print("\n📋 Choose an option:")
        print("1. Send simple email")
        print("2. Send HTML email")
        print("3. Send bulk emails")
        print("4. Send email with template")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            to = input("Recipient email: ").strip()
            subject = input("Subject: ").strip()
            body = input("Message: ").strip()
            
            if to and subject and body:
                sender.send_simple_email(to, subject, body)
            else:
                print("❌ All fields are required!")
        
        elif choice == '2':
            to = input("Recipient email: ").strip()
            subject = input("Subject: ").strip()
            html_body = input("HTML content: ").strip()
            attachments_input = input("Attachments (comma-separated paths, or press Enter): ").strip()
            
            attachments = [f.strip() for f in attachments_input.split(',')] if attachments_input else None
            
            if to and subject and html_body:
                sender.send_html_email(to, subject, html_body, attachments=attachments)
            else:
                print("❌ Required fields missing!")
        
        elif choice == '3':
            recipients_input = input("Recipients (comma-separated emails): ").strip()
            recipients = [email.strip() for email in recipients_input.split(',')]
            
            subject = input("Subject: ").strip()
            body = input("Message: ").strip()
            
            if recipients and subject and body:
                sender.send_bulk_emails(recipients, subject, body)
            else:
                print("❌ All fields are required!")
        
        elif choice == '4':
            template_path = input("Template file path: ").strip()
            to = input("Recipient email: ").strip()
            subject = input("Subject: ").strip()
            
            # Get template variables
            variables = {}
            print("Enter template variables (key=value), or press Enter when done:")
            while True:
                var_input = input("Variable: ").strip()
                if not var_input:
                    break
                if '=' in var_input:
                    key, value = var_input.split('=', 1)
                    variables[key.strip()] = value.strip()
            
            if template_path and to and subject:
                content = sender.load_email_template(template_path, **variables)
                if content:
                    sender.send_html_email(to, subject, content)
            else:
                print("❌ Required fields missing!")
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice!")


def main():
    """Main function to run the email sender."""
    print("🚀 Welcome to Python Email Sender!")
    
    # Check if this is being run interactively
    try:
        interactive_email_sender()
    except KeyboardInterrupt:
        print("\n👋 Email sender interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
