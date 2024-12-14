import imaplib
import email
from email.header import decode_header
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# IMAP server credentials
IMAP_SERVER = 'imap.gmail.com'
USERNAME = 'uremail@gmail.com'
PASSWORD = 'wu aphc rety'

def connect_to_imap_server(server, username, password):
    """Connects to the IMAP server and logs in."""
    logging.info("Connecting to the IMAP server...")
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    logging.info("Connected and logged in.")
    return mail

def fetch_unseen_emails(mail):
    """Fetches unseen emails from the mailbox."""
    mail.select('inbox')
    status, data = mail.search(None, 'UNSEEN')
    if status != 'OK':
        logging.info("No unseen emails found.")
        return []
    return data[0].split()

def extract_email_content(msg):
    """Extracts the content of the email."""
    subject = decode_header(msg["Subject"])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode()
    from_email = msg.get("From")

    content = ""
    found_plain = False

    for part in msg.walk():
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))
        if "attachment" not in content_disposition:
            if content_type == "text/plain" and not found_plain:
                content = part.get_payload(decode=True).decode()
                found_plain = True
            elif content_type == "text/html" and not found_plain:
                html_content = part.get_payload(decode=True).decode()
                clean_content = re.sub('<[^<]+?>', '', html_content)
                content = clean_content
                found_plain = True

    return from_email, subject, content

def write_email_to_file(file, from_email, subject, content):
    """Writes email details and content to the file."""
    file.write(f"From: {from_email}\n")
    file.write(f"Subject: {subject}\n")
    file.write(f"Content:\n{content.strip()}\n")
    file.write("="*50 + "\n")

def fetch_and_save_emails(output_file_path):
    try:
        mail = connect_to_imap_server(IMAP_SERVER, USERNAME, PASSWORD)
        email_ids = fetch_unseen_emails(mail)
        
        if not email_ids:
            return []

        with open(output_file_path, "w") as file:
            for num in email_ids:
                status, raw_email = mail.fetch(num, '(RFC822)')
                if status != 'OK':
                    logging.info(f"Failed to fetch email ID: {num}")
                    continue
                
                raw_email = raw_email[0][1]
                msg = email.message_from_bytes(raw_email)
                from_email, subject, content = extract_email_content(msg)
                write_email_to_file(file, from_email, subject, content)

        mail.logout()
        logging.info("Logged out from the server.")
        logging.info("Fetched emails and saved to %s", output_file_path)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_save_emails("inbox_email_content.txt")
