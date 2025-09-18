import imaplib
import email
from email.header import decode_header
import json
import os

# Email credentials - Update these with your actual credentials
# Use app-specific password for Gmail
email_user = "your_email@gmail.com"
email_pass = "your_app_specific_password"

# File path for storing JSON data
json_file_path = '../data/unseen_emails_info.json'

# Attachment save paths
attachment_save_path = "../handling_attachments"

# Initialize IMAP client
def init_imap():
    return imaplib.IMAP4_SSL("imap.gmail.com")

def login(imap):
    try:
        imap.login(email_user, email_pass)
        print("Logged in to IMAP successfully.")
        return imap
    except Exception as e:
        print(f"IMAP login failed: {e}")

def logout(imap):
    imap.close()
    imap.logout()
    print("Logged out from IMAP.")

def fetch_unseen_email_count():
    imap = init_imap()
    login(imap)
    imap.select("inbox")
    status, messages = imap.search(None, '(UNSEEN)')
    email_ids = messages[0].split()
    logout(imap)
    print(f"Unseen email count: {len(email_ids)}")
    return len(email_ids)

def fetch_unseen_emails():
    imap = init_imap()
    login(imap)
    imap.select("inbox")
    status, messages = imap.search(None, '(UNSEEN)')
    email_ids = messages[0].split()
    
    email_infos = []
    for email_id in email_ids:
        info = extract_email_info(imap, email_id)
        if info:
            email_infos.append(info)
    
    logout(imap)
    print(f"Fetched {len(email_infos)} unseen emails.")
    return email_infos

def extract_email_info(imap, email_id):
    _, msg_data = imap.fetch(email_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = decode_header(msg["subject"])[0][0]
            from_ = decode_header(msg["from"])[0][0]
            date = msg["Date"]

            # Decode if necessary
            if isinstance(subject, bytes):
                subject = subject.decode()
            if isinstance(from_, bytes):
                from_ = from_.decode()

            content = ""
            attachments = []

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain" and not part.get_content_disposition():
                        content += part.get_payload(decode=True).decode(errors='ignore')
                    elif "attachment" in str(part.get("Content-Disposition")):
                        filename = part.get_filename()
                        if filename:
                            filepath = save_attachment(part, filename)
                            if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
                                attachment_type = "JPEG"
                            elif filename.lower().endswith(".pdf"):
                                attachment_type = "PDF"
                            else:
                                attachment_type = "Other"
                            attachments.append({
                                "Filename": filename,
                                "Path": filepath
                            })
            else:
                content = msg.get_payload(decode=True).decode(errors='ignore')

            attachment_count = len(attachments)

            email_info = {
                "Subject": subject,
                "From": from_,
                "Date": date,
                "Content Preview": content[:100],
                "Content": content,
                "Attachment Count": attachment_count,
                "Attachments": attachments
            }
            print(f"Extracted info: {email_info}")
            return email_info
    return None

def save_to_json(email_infos):
    try:
        with open(json_file_path, 'w') as file:
            json.dump(email_infos, file, indent=4)
        print(f"Data saved to {json_file_path}")
    except Exception as e:
        print(f"Failed to save data to JSON: {e}")

def save_attachment(part, filename):
    print(f"Saving attachment: {filename}")
    filepath = os.path.join(attachment_save_path, filename)
    with open(filepath, "wb") as f:
        f.write(part.get_payload(decode=True))
    print(f"Attachment saved at: {filepath}")
    return filepath

def update_email_data():
    email_infos = fetch_unseen_emails()
    save_to_json(email_infos)

if __name__ == "__main__":
    # Fetch unseen emails and save them to JSON
    update_email_data()
