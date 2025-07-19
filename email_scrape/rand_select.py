# Randomly select 1000 emails from the email list
import random

# Read the email list into a dictionary from entries in the form: First Last: email@domain.com
email_to_name = {}
with open('email_scrape/remaining_emails1.txt', 'r') as file:
  for line in file:
    name, email = line.split(': ')
    email_to_name[email] = name

# Randomly select 1000 emails from dictionary and remove from dictionary
selected_emails_to_names = {}
selected_emails = random.sample(list(email_to_name.keys()), 1000)
for email in selected_emails:
  selected_emails_to_names[email] = email_to_name[email]
  del email_to_name[email]

# Write the selected emails to a new file
with open('email_scrape/selected_emails2.txt', 'w') as file:
  for email in selected_emails_to_names:
    file.write(selected_emails_to_names[email] + ': ' + email)

# Write the remaining emails to a new file
with open('email_scrape/remaining_emails2.txt', 'w') as file:
  for email in email_to_name:
    file.write(email_to_name[email] + ': ' + email)
