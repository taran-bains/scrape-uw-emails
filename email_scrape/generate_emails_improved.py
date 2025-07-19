import os
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

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
        logging.FileHandler('../logs/scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UWDirectoryScraper:
    def __init__(self):
        self.driver = None
        self.emails_to_names = {}
        self.setup_driver()

    def setup_driver(self):
        """Setup Chrome driver with appropriate options."""
        try:
            chrome_options = Options()
            # if HEADLESS_MODE:
            #     chrome_options.add_argument("--headless")
            # chrome_options.add_argument("--no-sandbox")
            # chrome_options.add_argument("--disable-dev-shm-usage")
            # chrome_options.add_argument("--disable-gpu")
            # chrome_options.add_argument("--window-size=1920,1080")

            # Use simple Chrome driver setup (same as original implementation)
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise

    def sign_in(self):
        """Sign in to UW Directory."""
        try:
            logger.info("Navigating to UW Directory...")
            self.driver.get('https://directory.uw.edu/')

            # Wait for and click sign-in button
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, 'sign-in'))
            )
            sign_in_button = self.driver.find_element(By.ID, 'sign-in')
            sign_in_button.click()

            # Wait for login form and enter credentials
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, 'weblogin_netid'))
            )

            username_field = self.driver.find_element(By.ID, 'weblogin_netid')
            password_field = self.driver.find_element(By.ID, 'weblogin_password')

            username_field.send_keys(UW_USERNAME)
            password_field.send_keys(UW_PASSWORD)

            # Submit login form
            submit_button = self.driver.find_element(By.ID, 'submit_button')
            submit_button.click()

            logger.info("Waiting for 2FA authentication...")

            # Handle 2FA trust browser button
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.ID, 'trust-browser-button'))
                )
                trust_button = self.driver.find_element(By.ID, 'trust-browser-button')
                trust_button.click()
                logger.info("2FA authentication completed")
            except TimeoutException:
                logger.info("No trust browser button found, continuing...")

        except Exception as e:
            logger.error(f"Sign-in failed: {e}")
            raise

    def search(self, term):
        """Search for a term in the UW Directory."""
        try:
            logger.info(f"Searching for: {term}")

            # Wait for search form
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, 'query'))
            )

            # Clear and enter search term
            search_bar = self.driver.find_element(By.ID, 'query')
            search_bar.clear()
            search_bar.send_keys(term)

            # Select 'Students only' option
            students_only = self.driver.find_element(By.ID, 'population-option-students')
            students_only.click()

            # Select 'Full layout' option
            full_layout = self.driver.find_element(By.ID, 'length-full')
            full_layout.click()

            # Submit search
            search_button = self.driver.find_element(By.ID, 'search')
            search_button.click()

            # Wait for results
            time.sleep(SEARCH_DELAY)

        except Exception as e:
            logger.error(f"Search failed for term '{term}': {e}")
            raise

    def extract_emails(self, term):
        """Extract eligible emails from search results."""
        eligible_emails = []

        try:
            # Wait for results container
            WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.ID, f'students-name-contains-{term}'))
            )

            anchor_element = self.driver.find_element(By.ID, f'students-name-contains-{term}')
            person_cards = anchor_element.find_elements(By.XPATH, 'following-sibling::div[@class="person-card"]')

            logger.info(f"Found {len(person_cards)} person cards for term '{term}'")

            for card in person_cards:
                try:
                    # Extract name and details
                    name = card.find_element(By.CLASS_NAME, 'person-name').text
                    details = card.find_element(By.CSS_SELECTOR, 'ul.no-style-list').text

                    # Check eligibility criteria
                    is_eligible = self._check_eligibility(details)

                    if is_eligible:
                        email_element = card.find_element(By.XPATH, './/li[contains(text(), "Email:")]')
                        email = email_element.text.split(': ')[1]
                        eligible_emails.append((name, email))
                        logger.info(f"Found eligible contact: {name} - {email}")

                except NoSuchElementException as e:
                    logger.debug(f"Could not extract data from person card: {e}")
                    continue
                except Exception as e:
                    logger.warning(f"Error processing person card: {e}")
                    continue

        except TimeoutException:
            logger.warning(f"No results found for term '{term}'")
        except Exception as e:
            logger.error(f"Error extracting emails for term '{term}': {e}")

        return eligible_emails

    def _check_eligibility(self, details):
        """Check if a student meets the eligibility criteria."""
        try:
            # Check class standing
            has_valid_standing = (
                MIN_CLASS_STANDING.lower() in details.lower() or
                MAX_CLASS_STANDING.lower() in details.lower()
            )

            if not has_valid_standing:
                return False

            # Check included majors (if specified)
            if INCLUDED_MAJORS:
                has_included_major = any(
                    major.lower() in details.lower() for major in INCLUDED_MAJORS
                )
                if not has_included_major:
                    return False

            # Check excluded majors
            has_excluded_major = any(
                major.lower() in details.lower() for major in EXCLUDED_MAJORS
            )

            return not has_excluded_major

        except Exception as e:
            logger.debug(f"Error checking eligibility: {e}")
            return False

    def save_results(self):
        """Save scraped emails to file."""
        try:
            output_file = 'emails.txt'  # Use local path when running from email_scrape directory
            with open(output_file, 'w') as f:
                for email, name in self.emails_to_names.items():
                    f.write(f"{email}: {name}\n")

            logger.info(f"Saved {len(self.emails_to_names)} emails to {output_file}")

        except Exception as e:
            logger.error(f"Failed to save results: {e}")
            raise

    def run(self):
        """Run the complete scraping process."""
        try:
            logger.info("Starting UW Directory scraping process...")

            # Sign in
            self.sign_in()

            # Read search combinations
            combinations_file = 'combinations.txt'  # Use local path when running from email_scrape directory
            if not os.path.exists(combinations_file):
                logger.error(f"Combinations file not found: {combinations_file}")
                return

            with open(combinations_file, 'r') as f:
                combinations = [line.strip() for line in f if line.strip()]

            logger.info(f"Processing {len(combinations)} search combinations...")

            # Process each combination
            for i, term in enumerate(combinations, 1):
                try:
                    logger.info(f"Processing {i}/{len(combinations)}: {term}")

                    # Search for the term
                    self.search(term)

                    # Extract emails
                    emails = self.extract_emails(term)

                    # Add to results
                    for name, email in emails:
                        self.emails_to_names[email] = name

                    # Progress update
                    if i % 10 == 0:
                        logger.info(f"Progress: {i}/{len(combinations)} combinations processed")

                except Exception as e:
                    logger.error(f"Error processing term '{term}': {e}")
                    continue

            # Save results
            self.save_results()

            logger.info("Scraping process completed successfully!")

        except Exception as e:
            logger.error(f"Scraping process failed: {e}")
            raise
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("Browser closed")

def main():
    """Main function to run the scraper."""
    try:
        scraper = UWDirectoryScraper()
        scraper.run()
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()