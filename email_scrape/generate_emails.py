from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# Import configuration
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import UW_USERNAME as username, UW_PASSWORD as password, MIN_CLASS_STANDING, MAX_CLASS_STANDING, EXCLUDED_MAJORS, INCLUDED_MAJORS
except ImportError:
    print("Error: config.py not found. Please copy config.example.py to config.py and fill in your credentials.")
    sys.exit(1)

# Setup webdriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

def sign_in(driver):
  driver.get('https://directory.uw.edu/')
  WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'sign-in')))
  sign_in_button = driver.find_element(By.ID, 'sign-in')
  sign_in_button.click()
  WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'weblogin_netid')))
  username_field = driver.find_element(By.ID, 'weblogin_netid')
  if username_field:
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, 'weblogin_password')
    password_field.send_keys(password)
    sign_in_button = driver.find_element(By.ID, 'submit_button')
    sign_in_button.click()
    print('Waiting for 2FA')
  WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'trust-browser-button')))
  trust_button = driver.find_element(By.ID, 'trust-browser-button')
  if trust_button:
    trust_button.click()


def search(driver, term):
  print('Searching for ' + term)
  WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'query')))

  # Input term into search bar
  search_bar = driver.find_element(By.ID, 'query')
  search_bar.clear()
  search_bar.send_keys(term)

  # Click 'Students only' radio button
  students_only = driver.find_element(By.ID, 'population-option-students')
  students_only.click()

  # Click 'Full layout' radio button
  full_layout = driver.find_element(By.ID, 'length-full')
  full_layout.click()

  search_button = driver.find_element(By.ID, 'search')
  search_button.click()

def extract_emails(driver, term):
  anchor_element = driver.find_element(By.ID, f'students-name-contains-{term}')
  person_cards = anchor_element.find_elements(By.XPATH, 'following-sibling::div[@class="person-card"]')
  eligible_emails = []
  for card in person_cards:
    try:
      # Extract name, class standing, major, and email
      name = card.find_element(By.CLASS_NAME, 'person-name').text
      details = card.find_element(By.CSS_SELECTOR, 'ul.no-style-list').text

      # Check eligibility criteria
      if check_eligibility(details):
        email = card.find_element(By.XPATH, './/li[contains(text(), "Email:")]').text.split(': ')[1]
        eligible_emails.append((name, email))
        print("Found: " + name + ' - ' + email)
    except NoSuchElementException:
      # Handle the case where no email is found
      print(f"No email found for {name}. Skipping this entry.")

  return eligible_emails

def check_eligibility(details):
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
    print(f"Error checking eligibility: {e}")
    return False

#Create dictionary of emails to names
emails_to_names = {}

# For each string
with open('combinations.txt', 'r') as f:
  # Go to page, sign in
  sign_in(driver)
  for line in f:
    term = line.strip()
    # Search
    search(driver, term)
    try:
      WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, f'students-name-contains-{term}')))
      # Extract emails
      emails = extract_emails(driver, term)
      for email, name in emails:
        emails_to_names[email] = name
    except TimeoutException:
      # Handle the case where no matches are found
      print(f"No matches found for {term}. Moving to the next search term.")
      continue
  driver.quit()

# Save dictionary to file
with open('emails.txt', 'w') as f:
  for email in emails_to_names:
    f.write(email + ': ' + emails_to_names[email] + '\n')

