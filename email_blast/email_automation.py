#!/usr/bin/env python3
"""
UW Directory Email Automation Tool

⚠️ UW Email Sending Limits:
- Maximum 150 recipients per batch
- Spread sending over several hours
- UW-IT: "Sending large batches will trigger the email to be held"
- Risk of blocklisting if limits exceeded
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time  # Add time module for sleep functionality

def read_email_list(filename):
    """Read email addresses and names from a file."""
    email_list = []
    with open(filename, 'r') as file:
        for line in file:
            if ':' in line:
                name, email = line.strip().split(':')
                email_list.append((name.strip(), email.strip()))
    return email_list

def send_email(sender_email, sender_password, recipient_name, recipient_email, subject, body):
    """Send an email to a recipient."""
    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    try:
        # Create SMTP session
        server = smtplib.SMTP('smtp.uw.edu', 587)
        server.starttls()

        # Login to the server
        server.login(sender_email, sender_password)

        # Send email
        server.send_message(message)
        print(f"Email sent successfully to {recipient_name} ({recipient_email} at {time.time()})")

        # Close the server connection
        server.quit()
    except Exception as e:
        print(f"Failed to send email to {recipient_name} ({recipient_email}): {str(e)}")

def get_email_input():
    sender_email = input("Enter your Gmail address: ")
    sender_password = input("Enter your Gmail app password: ")
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
    return sender_email, sender_password, subject, body

def main():
    # Import configuration
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    try:
        from config import UW_USERNAME as sender_email, UW_PASSWORD as sender_password, EMAIL_SUBJECT as subject
    except ImportError:
        print("Error: config.py not found. Please copy config.example.py to config.py and fill in your credentials.")
        sys.exit(1)

    # Read email list
    email_list = read_email_list('email_scrape/emails.txt')

    # Send emails to each recipient
    text = open('email_blast/email_text.txt', 'r').read()
    for name, email in email_list:
        first_name = name.split()[0]
        body = "Dear " + first_name + ",\n\n" + text
        send_email(sender_email, sender_password, name, email, subject, body)
        # Add a delay between emails to avoid triggering spam detection
        time.sleep(15)

if __name__ == "__main__":
    main()