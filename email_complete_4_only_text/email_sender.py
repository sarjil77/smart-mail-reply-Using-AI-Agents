import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_json_file(file_path):
    """Reads the JSON file and returns the parsed data."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_email_info(email_entry):
    """Extracts email details and responses from a single JSON entry."""
    from_email = email_entry.get("From", "not_found@example.com")
    subject = email_entry.get("Subject", "No Subject")
    responder_response = email_entry.get("Responder Output", "No Response")
    
    return from_email, subject, responder_response

def create_email(to_email, subject, body, smtp_username, attachments=None):
    """Creates a MIMEMultipart object to represent the email."""
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    if attachments:
        for attachment in attachments:
            try:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(attachment, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={attachment}')
                msg.attach(part)
            except Exception as e:
                logging.error(f"Failed to attach file {attachment}. Error: {e}")
                
    return msg

def send_email(msg, smtp_server, smtp_port, smtp_username, smtp_password):
    """Connects to the SMTP server and sends the email."""
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, msg['To'], msg.as_string())
        server.quit()
        logging.info(f"Response email sent successfully to {msg['To']}.")
    except Exception as e:
        logging.error(f"Failed to send email to {msg['To']}. Error: {e}")

def send_responses_from_json(json_file_path, smtp_username):
    """Reads the JSON file, extracts email info, and sends responses."""
    # Read the JSON data
    json_data = read_json_file(json_file_path)
    
    # Email account credentials
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_password = 'wurd evqm aphc rety'  # Replace with your actual SMTP password
    
    # Process each email entry
    for email_entry in json_data:
        # Extract email details and response
        from_email, original_subject, responder_response = extract_email_info(email_entry)
        
        if from_email and responder_response:
            # Create the response email
            to_email = from_email
            subject = f"Re: {original_subject}"  # Prefix with "Re:"
            body = responder_response  # Use the responder's response as the email body
            
            # Example: List of attachments (update with actual file paths as needed)
            attachments = [
                # '/data/aiuserinj/sarjil/mail_summarizer/handling_attachments/WC - Zurich - 1.PDF',
                # '/data/aiuserinj/sarjil/mail_summarizer/handling_attachments/coverages_ex.jpg'
            ]
            
            # Create the email message
            msg = create_email(to_email, subject, body, smtp_username, attachments)
            
            # Send the email
            send_email(msg, smtp_server, smtp_port, smtp_username, smtp_password)
        else:
            logging.warning("Failed to send email due to missing information.")

    logging.info("Sent all response emails.")

if __name__ == "__main__":
    send_responses_from_json('/data/aiuserinj/sarjil/mail_summarizer/email_complete_4_only_text/task_output2.json', 'uremail@gmail.com')
