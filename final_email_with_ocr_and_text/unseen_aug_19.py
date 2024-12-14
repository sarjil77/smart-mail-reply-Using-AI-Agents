import imaplib
import email
from email.header import decode_header
import json

email_user = "xyz@gmail.com"
email_pass = "958 bolt a champion"

# File path for storing JSON data
json_file_path = '/data/aiuserinj/sarjil/mail_summarizer/final_email_with_ocr_and_text/unseen_emails_info.json'

# Initialize IMAP client
imap = imaplib.IMAP4_SSL("imap.gmail.com")

def login():
    imap.login(email_user, email_pass)

def logout():
    imap.close()
    imap.logout()

def fetch_unseen_emails():
    imap.select("inbox")
    status, messages = imap.search(None, '(UNSEEN)')
    email_ids = messages[0].split()
    return email_ids

def extract_email_info(email_id):
    # Extract information as before (omitted for brevity)
    
    _, msg_data = imap.fetch(email_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = decode_header(msg["subject"])[0][0]
            from_ = decode_header(msg["from"])[0][0]
            date = msg["Date"]

            # If subject or from is bytes, decode to str
            if isinstance(subject, bytes):
                subject = subject.decode()
            if isinstance(from_, bytes):
                from_ = from_.decode()

            # Extract content preview
            content = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain" and not part.get_content_disposition():
                        content += part.get_payload(decode=True).decode(errors='ignore')
            else:
                content = msg.get_payload(decode=True).decode(errors='ignore')

            # Extract attachment information
            attachment_count = 0
            attachments = []
            if msg.is_multipart():
                for part in msg.walk():
                    content_disposition = str(part.get("Content-Disposition"))
                    if "attachment" in content_disposition:
                        attachment_count += 1
                        filename = part.get_filename()
                        if filename:
                            if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
                                attachments.append("JPEG")
                            elif filename.lower().endswith(".pdf"):
                                attachments.append("PDF")

            return {
                "Subject": subject,
                "From": from_,
                "Date": date,
                "Content Preview": content[:100],  # Preview first 100 characters
                "Attachment Count": attachment_count,
                "Attachment Types": attachments
            }
    return None

def save_to_json(email_infos, filename=json_file_path):
    with open(filename, 'w') as file:
        json.dump(email_infos, file, indent=4)
    print(f"Data saved to {filename}")

def fetch_unseen_email_count():
    login()
    email_ids = fetch_unseen_emails()
    logout()
    return len(email_ids)

def load_unseen_emails():
    with open(json_file_path, 'r') as file:
        return json.load(file)

def main():
    login()
    email_ids = fetch_unseen_emails()
    email_infos = [extract_email_info(email_id) for email_id in email_ids if extract_email_info(email_id)]
    save_to_json(email_infos)
    logout()

if __name__ == "__main__":
    main()
