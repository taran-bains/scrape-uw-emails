import smtplib
import email.message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Test smtp server
def test_smtp_server():
    # Create a message
    msg = MIMEMultipart()
    msg['Subject'] = 'Test Email'
    msg['From'] = 'tbains@uw.edu'
    msg['To'] = 'tbains@uw.edu'
    msg.attach(MIMEText('This is a test email', 'plain'))

    # Connect to the SMTP server
    server = smtplib.SMTP('smtp.uw.edu', 587)
    server.starttls()
    server.login('tbains@uw.edu', 'Sahil_Taran123')
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    test_smtp_server()