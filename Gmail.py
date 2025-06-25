import requests
import json
import time
import re

# API endpoint for 1secmail
BASE_URL = "https://www.1secmail.com/api/v1/"

def get_random_email():
    """Generate a random temporary email address."""
    response = requests.get(f"{BASE_URL}?action=genRandomMailbox&count=1")
    if response.status_code == 200:
        return response.json()[0]
    return None

def get_emails(email):
    """Fetch emails for the given email address."""
    login, domain = email.split("@")
    response = requests.get(f"{BASE_URL}?action=getMessages&login={login}&domain={domain}")
    if response.status_code == 200:
        return response.json()
    return []

def get_email_content(email, message_id):
    """Fetch email content by message ID."""
    login, domain = email.split("@")
    response = requests.get(f"{BASE_URL}?action=readMessage&login={login}&domain={domain}&id={message_id}")
    if response.status_code == 200:
        return response.json()
    return None

def extract_verification_code(email_body):
    """Extract a 6-digit verification code from email body."""
    code = re.search(r'\b\d{6}\b', email_body)
    return code.group(0) if code else None

def main():
    # Generate a random email
    email = get_random_email()
    if not email:
        print("Failed to generate email.")
        return
    print(f"Temporary email: {email}")

    # Poll for new emails (e.g., for 60 seconds)
    print("Waiting for verification code...")
    for _ in range(12):  # Check every 5 seconds, 12 times
        messages = get_emails(email)
        if messages:
            # Get the latest email
            latest_message = messages[0]
            message_id = latest_message['id']
            email_content = get_email_content(email, message_id)
            if email_content:
                body = email_content.get('textBody', '') or email_content.get('htmlBody', '')
                code = extract_verification_code(body)
                if code:
                    print(f"Verification code: {code}")
                    return
        time.sleep(5)
    print("No verification code received.")

if __name__ == '__main__':
    main()