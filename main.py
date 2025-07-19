#!/usr/bin/env python3
"""
UW Directory Scraping and Email Automation Tool
Main script for orchestrating the complete workflow
"""

import os
import sys
import time
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_config():
    """Check if configuration file exists and is properly set up."""
    if not os.path.exists('config.py'):
        print("❌ Configuration file not found!")
        print("Please copy config.example.py to config.py and fill in your credentials.")
        return False

    try:
        from config import UW_USERNAME, UW_PASSWORD
        if not all([UW_USERNAME, UW_PASSWORD]):
            print("❌ Configuration incomplete!")
            print("Please fill in all required credentials in config.py")
            return False
        return True
    except ImportError as e:
        print(f"❌ Configuration error: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import selenium
        import smtplib
        print("✅ All dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def scrape_emails():
    """Run the email scraping process."""
    print("\n📧 Starting email scraping...")
    try:
        os.chdir('email_scrape')
        os.system('python generate_emails_improved.py')
        os.chdir('..')

        # Check if emails were scraped
        if os.path.exists('email_scrape/emails.txt'):
            with open('email_scrape/emails.txt', 'r') as f:
                email_count = len(f.readlines())
            print(f"✅ Email scraping completed! Found {email_count} emails")
            return True
        else:
            print("❌ No emails were scraped")
            return False
    except Exception as e:
        print(f"❌ Email scraping failed: {e}")
        return False

def select_random_emails():
    """Randomly select a subset of emails."""
    print("\n🎲 Selecting random emails...")
    try:
        os.chdir('email_scrape')
        os.system('python rand_select.py')
        os.chdir('..')
        print("✅ Random email selection completed")
        return True
    except Exception as e:
        print(f"❌ Random selection failed: {e}")
        return False

def send_email_campaign():
    """Run the email campaign."""
    print("\n📤 Starting email campaign...")
    try:
        os.chdir('email_blast')
        os.system('python email_automation_improved.py')
        os.chdir('..')
        print("✅ Email campaign completed")
        return True
    except Exception as e:
        print(f"❌ Email campaign failed: {e}")
        return False

def show_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("UW Directory Scraping and Email Automation Tool")
    print("="*50)
    print("1. Complete Workflow (Scrape + Send)")
    print("2. Scrape Emails from UW Directory")
    print("3. Select Random Emails")
    print("4. Send Email Campaign")
    print("5. Check Configuration")
    print("6. Exit")
    print("-"*50)

def run_complete_workflow():
    """Run the complete workflow from start to finish."""
    print("\n🚀 Starting complete workflow...")

    steps = [
        ("Scrape emails", scrape_emails),
        ("Send email campaign", send_email_campaign)
    ]

    for step_name, step_func in steps:
        print(f"\n--- {step_name} ---")
        if not step_func():
            print(f"❌ Workflow failed at: {step_name}")
            return False

    print("\n🎉 Complete workflow finished successfully!")
    return True

def main():
    """Main function."""
    print("Welcome to UW Directory Scraping and Email Automation Tool!")

    # Check configuration and dependencies
    if not check_config():
        return

    if not check_dependencies():
        return

    while True:
        show_menu()

        try:
            choice = input("\nEnter your choice (1-6): ").strip()

            if choice == '1':
                run_complete_workflow()

            elif choice == '2':
                scrape_emails()

            elif choice == '3':
                select_random_emails()

            elif choice == '4':
                send_email_campaign()

            elif choice == '5':
                if check_config():
                    print("✅ Configuration is valid")
                check_dependencies()

            elif choice == '6':
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid choice. Please enter a number between 1-6.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")

        # Ask if user wants to continue
        if choice != '6':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()