# 📧 Email Sender Script - Project #12

## 🎯 Problem Statement

Create a Python script that automates sending emails via SMTP — useful for reminders, reports, or alerts.

## 🎓 Learning Objectives

By completing this project, you will learn:
- SMTP protocol basics and email automation
- Using `smtplib` & `email` modules
- Formatting HTML and text emails
- Sending attachments securely
- Email authentication and security best practices

## 🔧 Features

- **Multiple Email Formats**: Plain text and HTML emails
- **Attachment Support**: Send files with your emails
- **Bulk Emailing**: Send to multiple recipients
- **Template System**: Use email templates
- **Security**: Secure authentication with app passwords
- **Error Handling**: Graceful handling of email failures

## 📋 Requirements

```
# Requirements for this project
smtplib      # Built-in Python module
email        # Built-in Python module
python-dotenv>=0.20.0   # For environment variables
```

## 🚀 How to Run

1. Navigate to the project directory:
```bash
cd week-3/12-email-sender
```

2. Install dependencies:
```bash
pip install python-dotenv
```

3. Set up your email credentials:
```bash
cp .env.example .env
# Edit .env with your email credentials
```

4. Run the email sender:
```bash
python main.py
```

## 💡 Key Concepts Demonstrated

### 1. SMTP Protocol
- Connecting to email servers
- Authentication methods
- Secure connections (SSL/TLS)

### 2. Email Composition
- Creating email messages
- Setting headers (To, From, Subject)
- HTML vs plain text content

### 3. File Operations
- Reading email templates
- Handling attachments
- Processing recipient lists

### 4. Security Best Practices
- Using environment variables for credentials
- App-specific passwords
- Error handling for authentication

## 📊 Sample Usage

### Basic Email:
```python
from email_sender import EmailSender

sender = EmailSender()
sender.send_email(
    to="recipient@example.com",
    subject="Test Subject",
    body="Hello, this is a test email!"
)
```

### HTML Email with Attachment:
```python
sender.send_html_email(
    to="recipient@example.com",
    subject="Report",
    html_content="<h1>Monthly Report</h1><p>Please find the report attached.</p>",
    attachments=["report.pdf"]
)
```

## 🎯 Learning Outcome

After completing this project, you'll understand:
- How email protocols work (SMTP)
- Email automation and scripting
- Security considerations for email automation
- Building professional email systems
- Integration with other automation tools

## ⚠️ Important Security Notes

1. **Never hardcode passwords** in your source code
2. **Use app-specific passwords** for Gmail/Outlook
3. **Enable 2FA** on your email account
4. **Use environment variables** for sensitive data
5. **Validate recipient emails** before sending

## 🏆 Bonus Challenges

1. **Email Templates**: Create a template system with placeholders
2. **Scheduling**: Send emails at specific times
3. **Email Tracking**: Track email delivery and opens
4. **Database Integration**: Load recipients from a database
5. **GUI Interface**: Create a simple email client interface

## 🔗 Related Projects

- **Project 6**: CSV handling for recipient lists
- **Project 8**: API integration for dynamic content
- **Project 11**: File organization for attachment management

---

*This is Project #12 in our Python Projects Series. Master email automation! 📧🚀*
