# 💬 WhatsApp Message Automation - Project #13

## 🎯 Problem Statement

Build a Python script that automatically sends WhatsApp messages using WhatsApp Web. Perfect for reminders, greetings, promotional messages, or team notifications with scheduling capabilities.

## 🎓 Learning Objectives

By completing this project, you will learn:
- WhatsApp Web automation using pywhatkit
- Browser automation and web scraping concepts
- Message scheduling and timing management
- File and media sharing automation
- Contact management and bulk messaging
- Error handling for web automation

## 🔧 Features

- **Scheduled Messaging**: Send messages at specific times
- **Instant Messaging**: Send messages immediately
- **Bulk Messaging**: Send to multiple contacts
- **Media Sharing**: Send images, documents, and files
- **Contact Management**: Manage recipient lists
- **Message Templates**: Pre-defined message formats
- **Delivery Tracking**: Monitor message status
- **Interactive CLI**: User-friendly interface

## 📋 Requirements

```
pywhatkit>=5.4
opencv-python>=4.8.0
Pillow>=10.0.0
pandas>=1.5.0
schedule>=1.2.0
```

## 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup WhatsApp Web**:
   - Make sure you're logged into WhatsApp Web in your default browser
   - Keep your phone connected to internet

3. **Navigate to Project Directory**:
   ```bash
   cd week-3/13-whatsapp-automation
   ```

4. **Run the Automation Script**:
   ```bash
   python main.py
   ```

## 💡 Key Concepts Demonstrated

### 1. Web Automation
- Browser control and navigation
- WhatsApp Web interface interaction
- Timing and synchronization

### 2. Message Scheduling
- Time-based automation
- Delayed execution
- Recurring messages

### 3. File Handling
- Media file processing
- Contact list management
- Message template loading

## 📊 Sample Usage

### Scheduled Message:
```
💬 WhatsApp Automation Tool
============================
1. 📅 Schedule Message
2. ⚡ Send Instant Message
3. 📤 Bulk Messaging
4. 📁 Send Media
5. 👥 Manage Contacts

Enter choice: 1

📞 Enter phone number (with country code): +1234567890
💬 Enter message: Hello! This is a scheduled message.
🕐 Enter hour (24-hour format): 17
🕐 Enter minute: 30

✅ Message scheduled for 17:30
🌐 Opening WhatsApp Web...
⏰ Waiting for scheduled time...
📤 Message sent successfully!
```

### Bulk Messaging:
```
📤 Bulk Messaging
================
📁 Load contacts from: contacts.txt
💬 Enter message template: Happy New Year! 🎉

📊 Found 5 contacts:
   ✓ +1234567890 (John Doe)
   ✓ +9876543210 (Jane Smith)
   ✓ +1122334455 (Mike Johnson)

🚀 Sending messages...
   ✅ Message sent to John Doe
   ✅ Message sent to Jane Smith
   ✅ Message sent to Mike Johnson

📈 Summary: 5/5 messages sent successfully
```

## ⚠️ Important Notes

### **Prerequisites:**
- **WhatsApp Web Login**: Must be logged in to WhatsApp Web
- **Internet Connection**: Stable connection required
- **Phone Connection**: Keep your phone online
- **Browser**: Default browser will be used

### **Limitations:**
- **Rate Limiting**: WhatsApp may limit message frequency
- **Browser Dependency**: Requires browser automation
- **Manual QR**: May need to scan QR code occasionally

### **Best Practices:**
- **Respect Privacy**: Only send to consenting recipients
- **Message Limits**: Avoid spamming (max 20-30 messages/hour)
- **Content Guidelines**: Follow WhatsApp's terms of service

## 🎯 Learning Outcome

After completing this project, you'll understand:
- Web automation principles and browser control
- WhatsApp Web API limitations and workarounds
- Scheduled task execution in Python
- Media file handling and automation
- Contact management systems

## 🏆 Bonus Challenges

1. **GUI Interface**: Create a tkinter GUI for the automation tool
2. **Message Analytics**: Track delivery status and read receipts
3. **Template System**: Advanced message templating with variables
4. **Group Messaging**: Automate group message sending
5. **Chatbot Integration**: Connect with AI chatbot for responses

## 🔗 Related Projects

- **Project 12**: Email Sender - Alternative messaging automation
- **Project 11**: File Organizer - File management for media sharing
- **Project 8**: API Calls - Understanding automation principles

---

*This is Project #13 in our Python Projects Series. Master WhatsApp automation! 💬🤖*
