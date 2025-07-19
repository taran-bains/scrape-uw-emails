# UW Directory Scraping and Email Automation Configuration
# Copy this file to config.py and fill in your credentials

# UW Directory credentials
UW_USERNAME = "your_netid@uw.edu"
UW_PASSWORD = "your_password"

# Note: UW_USERNAME and UW_PASSWORD are used for both directory access and email sending

# Email campaign settings
EMAIL_SUBJECT = "Research Study Invitation"
EMAIL_TEMPLATE_FILE = "email_blast/email_text.txt"

# Scraping settings
HEADLESS_MODE = True  # Set to False to see the browser in action
SEARCH_DELAY = 2  # Delay between searches in seconds
EMAIL_DELAY = 15  # Delay between emails in seconds

# ⚠️ UW Email Sending Limits
# UW-IT: "Sending large batches will trigger the email to be held.
# I would recommend smaller batches up to around 150 recipients
# and spread out the sending every few hours should get you under the thresholds."
# Risk: Exceeding limits may result in blocklisting

# Filtering criteria
MIN_CLASS_STANDING = "Freshman"  # Minimum class standing to include
MAX_CLASS_STANDING = "Sophomore"  # Maximum class standing to include
EXCLUDED_MAJORS = ["Informatics"]  # Majors to exclude
INCLUDED_MAJORS = []  # Majors to include (empty list = include all except excluded)
# Examples:
# INCLUDED_MAJORS = ["Computer Science", "Engineering"]  # Only include CS and Engineering students
# EXCLUDED_MAJORS = ["Informatics", "Business"]  # Exclude Informatics and Business students

# Debug settings
DEBUG = False  # Set to True for verbose logging
SAVE_HTML = False  # Save HTML pages for debugging

# File paths
COMBINATIONS_FILE = "email_scrape/combinations.txt"
OUTPUT_EMAILS_FILE = "email_scrape/emails.txt"
SELECTED_EMAILS_FILE = "email_scrape/selected_emails.txt"