# Quick Start Guide

Get up and running with the UW Directory Scraping Tool in 5 minutes!

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- **UW NetID credentials** (required for directory access)
- **UW email account** (required for sending emails)

⚠️ **UW Email Limits**: Maximum 150 recipients per batch, spread over several hours to avoid blocklisting.

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd uw-directory

# Run the setup script
python setup.py
```

## Step 2: Configure Credentials

Edit `config.py` with your credentials:

```python
UW_USERNAME = "your_netid@uw.edu"
UW_PASSWORD = "your_password"
```

**Important:** This tool is only for UW students/staff with valid UW credentials and email access. UW_USERNAME and UW_PASSWORD are used for both directory access and email sending.

## Step 3: Run the Tool

```bash
python main.py
```

Choose option 1 for the complete workflow, or run individual steps as needed.

## What Each Option Does

1. **Complete Workflow** - Runs everything automatically
2. **Scrape Emails** - Extracts emails from UW Directory
3. **Select Random Emails** - Randomly samples from scraped emails
4. **Send Email Campaign** - Sends personalized emails

## Configuration Options

### Major Filtering
You can filter students by major in `config.py`:
- `INCLUDED_MAJORS`: List of majors to include (empty = include all except excluded)
- `EXCLUDED_MAJORS`: List of majors to exclude
- Example: `INCLUDED_MAJORS = ["Computer Science"]` to only include CS students

### UW Email Compliance
- **Batch Size**: Keep under 150 recipients per batch
- **Timing**: Spread campaigns over several hours
- **Delays**: Adjust `EMAIL_DELAY` in config.py (default: 15 seconds)
- **UW-IT Warning**: "Sending large batches will trigger the email to be held"

## Expected Output

- `email_scrape/emails.txt` - All scraped emails
- `email_scrape/selected_emails.txt` - Randomly selected emails
- `logs/scraping.log` - Detailed scraping process logs
- `logs/email_campaign.log` - Email campaign logs
- `reports/email_campaign_report_*.txt` - Campaign results and statistics

## Troubleshooting

### Common Issues

**"ChromeDriver not found"**
- The setup script should handle this automatically
- If not, download from [ChromeDriver website](https://chromedriver.chromium.org/)

**"Authentication failed"**
- Check your UW email credentials
- Ensure you have UW email access

**"No emails found"**
- Check your UW credentials
- Verify the search patterns in `combinations.txt`

### Getting Help

- Check the full [README.md](README.md) for detailed documentation
- Look at the log files for error details
- Ensure you're following UW policies and IRB requirements

## Ethical Considerations

⚠️ **Important:** This tool is for UW academic research only. Ensure you have:
- IRB approval for your research
- Compliance with UW policies
- Respect for student privacy
- Proper opt-out mechanisms in your emails
- **Valid UW credentials and email access**