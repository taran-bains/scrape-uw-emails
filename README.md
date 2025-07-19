# UW Directory Scraping and Email Automation Tool

A Python-based tool for scraping student information from the UW Directory and automating email campaigns for research purposes.

⚠️ **IMPORTANT: This tool is specifically designed for UW students/staff with valid UW credentials and email access. It requires UW NetID for directory access and UW email for sending messages.**

## ⚠️ Critical Email Sending Limits

**UW Email System Restrictions:**
- **Batch Size Limit**: Maximum 150 recipients per batch
- **Time Spacing**: Spread sending over several hours (every few hours)
- **Risk**: Exceeding limits will trigger email holds and potential blocklisting
- **UW-IT Recommendation**: "Sending large batches will trigger the email to be held. I would recommend smaller batches up to around 150 recipients and spread out the sending every few hours should get you under the thresholds."

**Default Settings:**
- Email delay: 15 seconds between emails (configurable in `config.py`)
- Consider reducing batch sizes and increasing delays for large campaigns

## Overview

This tool consists of two main components:
1. **Email Scraper** (`email_scrape/`) - Scrapes student emails from the UW Directory based on name patterns
2. **Email Automation** (`email_blast/`) - Sends automated emails to the scraped contacts

## Features

- Automated UW Directory login and search
- Pattern-based student email extraction (Freshman/Sophomore, non-Informatics)
- Email campaign automation with customizable templates
- Rate limiting to avoid spam detection
- Random sampling of contacts for research purposes

## Prerequisites

- Python 3.7+
- Chrome browser installed
- **UW NetID credentials** (required for directory access)
- **UW email account** (required for sending emails via UW SMTP server)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/taran-bains/scrape-uw-emails.git
   cd scrape-uw-emails
   ```

2. **Run the automated setup:**
   ```bash
   python setup.py
   ```
   This will:
   - Install all required dependencies
   - Create necessary directories
   - Set up configuration file
   - Test ChromeDriver functionality

## Configuration

The setup script will automatically create `config.py` from `config.example.py`. You just need to edit it with your credentials:

```python
# UW Directory credentials
UW_USERNAME = "your_netid@uw.edu"
UW_PASSWORD = "your_password"

# Note: UW_USERNAME and UW_PASSWORD are used for both directory access and email sending

# Email campaign settings
EMAIL_SUBJECT = "Research Study Invitation"
EMAIL_TEMPLATE_FILE = "email_blast/email_text.txt"
```

## Usage

### Quick Start

Run the tool and choose from the menu:
```bash
python main.py
```

**Available Options:**
1. **Complete Workflow** - Runs scraping and email campaign automatically
2. **Scrape Emails** - Extract emails from UW Directory only
3. **Select Random Emails** - Randomly sample from scraped emails
4. **Send Email Campaign** - Send emails to scraped contacts
5. **Check Configuration** - Verify setup and dependencies
6. **Exit** - Quit the tool

### Manual Script Execution

You can also run individual scripts directly:

```bash
# Scrape emails
cd email_scrape
python generate_emails_improved.py

# Send email campaign
cd ../email_blast
python email_automation_improved.py
```

## File Structure

```
uw-directory/
├── README.md                 # This file
├── QUICKSTART.md            # Quick start guide
├── IMPROVEMENTS.md          # Summary of improvements
├── requirements.txt         # Python dependencies
├── config.example.py        # Configuration template
├── setup.py                 # Automated setup script
├── main.py                  # Main menu interface
├── .gitignore              # Git ignore rules
├── email_scrape/
│   ├── generate_emails.py              # Original scraping script
│   ├── generate_emails_improved.py     # Enhanced scraping script
│   ├── get_combos.py                   # Generate search patterns (legacy)
│   ├── rand_select.py                  # Random contact selection
│   └── combinations.txt                # Pre-generated search patterns
├── email_blast/
│   ├── email_automation.py             # Original email script
│   ├── email_automation_improved.py    # Enhanced email script
│   ├── gmail_script.py                 # Gmail automation (legacy)
│   ├── email_text.txt                  # Email template
│   └── email_list.txt                  # Generated email list
├── logs/                               # Log files (auto-created)
│   ├── .gitkeep                        # Keep directory in git
│   ├── scraping.log                    # Scraping process logs
│   └── email_campaign.log              # Email campaign logs
└── reports/                            # Campaign reports (auto-created)
    ├── .gitkeep                        # Keep directory in git
    └── email_campaign_report_*.txt     # Email campaign results
```

## Configuration Options

### Major Filtering
Configure student filtering in `config.py`:
- `INCLUDED_MAJORS`: List of majors to include (empty = include all except excluded)
- `EXCLUDED_MAJORS`: List of majors to exclude
- Example: `INCLUDED_MAJORS = ["Computer Science", "Engineering"]` to only include CS and Engineering students

### Email Settings
- Customize `email_text.txt` for your email template
- Adjust `EMAIL_DELAY` in config.py (default: 15 seconds between emails)
- Modify `EMAIL_SUBJECT` for your campaign

### UW Email Compliance
- **Batch Size**: Keep batches under 150 recipients
- **Timing**: Spread campaigns over several hours
- **Delays**: Use EMAIL_DELAY setting (default: 15 seconds)
- **Monitoring**: Check for email holds or blocklisting
- **Compliance**: Follow UW-IT guidelines to avoid restrictions

## Important Notes

⚠️ **Ethical Considerations:**
- This tool is designed for academic research purposes
- Ensure compliance with UW policies and IRB requirements
- Respect student privacy and email preferences
- Include opt-out mechanisms in your emails

⚠️ **Technical Limitations:**
- UW Directory may have rate limiting
- UW SMTP server has sending limits
- ChromeDriver version must match your Chrome browser
- **This tool is only for UW students/staff with valid UW credentials**
- **UW Email Limits**: 150 recipients per batch, spread over several hours
- **Risk of Blocklisting**: Exceeding limits may result in email account restrictions

## Troubleshooting

### Common Issues

1. **Setup issues:**
   - Run `python setup.py` to automatically install dependencies and test setup
   - Ensure Python 3.7+ is installed
   - Check that ChromeDriver is in your PATH

2. **Configuration issues:**
   - Verify `config.py` exists and contains your UW credentials
   - Check that UW_USERNAME and UW_PASSWORD are filled in
   - Ensure you have valid UW email access

3. **Login failures:**
   - Check your UW credentials in `config.py`
   - Ensure 2FA is properly configured
   - Verify UW Directory access

4. **Email sending errors:**
   - Verify UW email credentials are correct
   - Check UW SMTP server status
   - **Check for email holds**: Large batches may be held by UW system
   - **Reduce batch size**: Keep under 150 recipients per batch
   - **Increase delays**: Spread sending over several hours

5. **No results found:**
   - Check that `combinations.txt` exists in email_scrape directory
   - Verify filtering criteria in `config.py`
   - Check logs in `logs/scraping.log` for detailed error information

### Debug Mode

Enable debug logging by setting `DEBUG = True` in `config.py`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for academic research purposes. Please ensure compliance with UW policies and applicable laws.

## Support

For issues related to:
- **Setup and configuration**: Check logs in `logs/` directory
- **UW Directory access**: Contact UW IT
- **UW Email/SMTP**: Contact UW IT
- **Python/Selenium**: Refer to official documentation
- **Tool-specific issues**: Check the logs and reports for detailed error information

## Expected Output

- `email_scrape/emails.txt` - All scraped emails
- `email_scrape/selected_emails.txt` - Randomly selected emails
- `logs/scraping.log` - Detailed scraping process logs
- `logs/email_campaign.log` - Email campaign logs
- `reports/email_campaign_report_*.txt` - Campaign results and statistics