#!/usr/bin/env python3
"""
UW Directory Email Automation Tool

⚠️ UW Email Sending Limits:
- Maximum 150 recipients per batch
- Spread sending over several hours
- UW-IT: "Sending large batches will trigger the email to be held"
- Risk of blocklisting if limits exceeded
"""
import os
import sys
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import *
except ImportError:
    print("Error: config.py not found. Please copy config.example.py to config.py and fill in your credentials.")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/email_campaign.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EmailCampaign:
    def __init__(self):
        self.sent_count = 0
        self.failed_count = 0
        self.sent_emails = []
        self.failed_emails = []

    def read_email_list(self, filename):
        """Read email addresses and names from a file."""
        email_list = []
        try:
            if not os.path.exists(filename):
                logger.error(f"Email list file not found: {filename}")
                return []

            with open(filename, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue

                    if ':' in line:
                        try:
                            name, email = line.split(':', 1)
                            email_list.append((name.strip(), email.strip()))
                        except ValueError:
                            logger.warning(f"Invalid format in line {line_num}: {line}")
                    else:
                        logger.warning(f"No separator found in line {line_num}: {line}")

            logger.info(f"Loaded {len(email_list)} email addresses from {filename}")
            return email_list

        except Exception as e:
            logger.error(f"Error reading email list: {e}")
            return []

    def read_email_template(self, template_file):
        """Read email template from file."""
        try:
            if not os.path.exists(template_file):
                logger.error(f"Email template file not found: {template_file}")
                return ""

            with open(template_file, 'r') as file:
                template = file.read()

            logger.info(f"Loaded email template from {template_file}")
            return template

        except Exception as e:
            logger.error(f"Error reading email template: {e}")
            return ""

    def validate_email(self, email):
        """Basic email validation."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def send_email(self, recipient_name, recipient_email, subject, body):
        """Send an email to a recipient."""
        if not self.validate_email(recipient_email):
            logger.warning(f"Invalid email format: {recipient_email}")
            self.failed_count += 1
            self.failed_emails.append((recipient_name, recipient_email, "Invalid email format"))
            return False

        # Create message
        message = MIMEMultipart()
        message['From'] = UW_USERNAME
        message['To'] = recipient_email
        message['Subject'] = subject

        # Add body to email
        message.attach(MIMEText(body, 'plain'))

        try:
            # Create SMTP session
            server = smtplib.SMTP('smtp.uw.edu', 587)
            server.starttls()

            # Login to the server
            server.login(UW_USERNAME, UW_PASSWORD)

            # Send email
            server.send_message(message)

            # Close the server connection
            server.quit()

            logger.info(f"Email sent successfully to {recipient_name} ({recipient_email})")
            self.sent_count += 1
            self.sent_emails.append((recipient_name, recipient_email))
            return True

        except smtplib.SMTPAuthenticationError:
            error_msg = "Authentication failed. Check your UW email credentials."
            logger.error(f"SMTP Authentication Error: {error_msg}")
            self.failed_count += 1
            self.failed_emails.append((recipient_name, recipient_email, error_msg))
            return False

        except smtplib.SMTPRecipientsRefused:
            error_msg = "Recipient email address refused"
            logger.error(f"SMTP Recipients Refused for {recipient_email}: {error_msg}")
            self.failed_count += 1
            self.failed_emails.append((recipient_name, recipient_email, error_msg))
            return False

        except smtplib.SMTPException as e:
            error_msg = f"SMTP error: {str(e)}"
            logger.error(f"SMTP Error for {recipient_email}: {error_msg}")
            self.failed_count += 1
            self.failed_emails.append((recipient_name, recipient_email, error_msg))
            return False

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"Failed to send email to {recipient_name} ({recipient_email}): {error_msg}")
            self.failed_count += 1
            self.failed_emails.append((recipient_name, recipient_email, error_msg))
            return False

    def personalize_email(self, template, recipient_name):
        """Personalize email template with recipient's name."""
        try:
            first_name = recipient_name.split()[0]
            personalized = template.replace("{FIRST_NAME}", first_name)
            personalized = personalized.replace("{FULL_NAME}", recipient_name)
            return personalized
        except Exception as e:
            logger.warning(f"Could not personalize email for {recipient_name}: {e}")
            return template

    def save_campaign_report(self):
        """Save a report of the email campaign."""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            report_file = f"../reports/email_campaign_report_{timestamp}.txt"

            with open(report_file, 'w') as f:
                f.write("Email Campaign Report\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Campaign Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Emails Sent: {self.sent_count}\n")
                f.write(f"Total Emails Failed: {self.failed_count}\n")
                f.write(f"Success Rate: {(self.sent_count/(self.sent_count+self.failed_count)*100):.1f}%\n\n")

                if self.sent_emails:
                    f.write("Successfully Sent Emails:\n")
                    f.write("-" * 30 + "\n")
                    for name, email in self.sent_emails:
                        f.write(f"{name}: {email}\n")
                    f.write("\n")

                if self.failed_emails:
                    f.write("Failed Emails:\n")
                    f.write("-" * 15 + "\n")
                    for name, email, error in self.failed_emails:
                        f.write(f"{name}: {email} - {error}\n")

            logger.info(f"Campaign report saved to {report_file}")

        except Exception as e:
            logger.error(f"Failed to save campaign report: {e}")

    def run_campaign(self, email_list_file=None, template_file=None, subject=None):
        """Run the complete email campaign."""
        try:
            # Use default values if not provided
            email_list_file = email_list_file or OUTPUT_EMAILS_FILE
            template_file = template_file or EMAIL_TEMPLATE_FILE
            subject = subject or EMAIL_SUBJECT

            logger.info("Starting email campaign...")

            # Read email list
            email_list = self.read_email_list(email_list_file)
            if not email_list:
                logger.error("No email addresses found. Campaign aborted.")
                return

            # Read email template
            template = self.read_email_template(template_file)
            if not template:
                logger.error("No email template found. Campaign aborted.")
                return

            # Confirm before sending
            print(f"\nEmail Campaign Summary:")
            print(f"Total recipients: {len(email_list)}")
            print(f"Email subject: {subject}")
            print(f"Delay between emails: {EMAIL_DELAY} seconds")
            print(f"Template file: {template_file}")

            # UW Email Limits Warning
            if len(email_list) > 150:
                print(f"\n⚠️  WARNING: Large batch detected ({len(email_list)} recipients)")
                print("UW-IT recommends batches under 150 recipients to avoid email holds.")
                print("Consider splitting into smaller batches or increasing delays.")

            response = input("\nDo you want to proceed with the campaign? (y/N): ")
            if response.lower() != 'y':
                logger.info("Campaign cancelled by user")
                return

            # Send emails
            logger.info(f"Starting to send {len(email_list)} emails...")

            for i, (name, email) in enumerate(email_list, 1):
                try:
                    logger.info(f"Processing {i}/{len(email_list)}: {name} ({email})")

                    # Personalize email
                    personalized_body = self.personalize_email(template, name)

                    # Send email
                    success = self.send_email(name, email, subject, personalized_body)

                    # Progress update
                    if i % 10 == 0:
                        logger.info(f"Progress: {i}/{len(email_list)} emails processed")

                    # Delay between emails (except for the last one)
                    if i < len(email_list):
                        time.sleep(EMAIL_DELAY)

                except KeyboardInterrupt:
                    logger.info("Campaign interrupted by user")
                    break
                except Exception as e:
                    logger.error(f"Error processing {name} ({email}): {e}")
                    self.failed_count += 1
                    self.failed_emails.append((name, email, str(e)))
                    continue

            # Campaign completed
            logger.info("Email campaign completed!")
            logger.info(f"Successfully sent: {self.sent_count}")
            logger.info(f"Failed: {self.failed_count}")

            # Save report
            self.save_campaign_report()

        except Exception as e:
            logger.error(f"Campaign failed: {e}")
            raise

def main():
    """Main function to run the email campaign."""
    try:
        campaign = EmailCampaign()

        # Check if email list exists
        if not os.path.exists(OUTPUT_EMAILS_FILE):
            logger.error(f"Email list file not found: {OUTPUT_EMAILS_FILE}")
            logger.info("Please run the scraping script first to generate email list.")
            return

        # Run campaign
        campaign.run_campaign()

    except KeyboardInterrupt:
        logger.info("Email campaign interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()