import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# Define known categories
known_categories = [
    'Policy Inquiries', 'Claims', 'Billing and Payments', 'Customer Support', 
    'Renewals', 'Documentation', 'Quotes', 'Cancellations', 'Compliance and Legal', 
    'Marketing and Promotions', 'Internal Communications'
]

# Define the attachment paths
category_to_attachments = {
    'Policy Inquiries': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Policy Inquiries/sample_for_inquiry.pdf',
    'Claims': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Claims/claims.pdf',
    'Billing and Payments': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Billing and Payments/bills.png',
    'Customer Support': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Customer Support/customer support.jpeg',
    'Renewals': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Renewals/renewal.pdf',
    'Documentation': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Documentation/documentation.pdf',
    'Quotes': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Quotes/casual_photo.jpeg',
    'Cancellations': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Cancellations/spam_danger.jpeg',
    'Compliance and Legal': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Compliance and Legal/legal notice.pdf',
    'Marketing and Promotions': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Internal Communications/autoGEN_4_agents_R_paper.pdf',
    'Internal Communications': '/data/aiuserinj/sarjil/mail_summarizer/attachments/Internal Communications/autoGEN_4_agents_R_paper.pdf'
}

def process_json_and_send_emails(json_file_path):
    # Load email data from JSON file
    with open(json_file_path, 'r') as json_file:
        email_data_list = json.load(json_file)

    for email_data in email_data_list:
        email_id = email_data.get('ID', '')
        email_from = email_data.get('From', '')
        email_subject = email_data.get('Subject', '')
        email_content = email_data.get('Content', '')
        
        # Extract and clean classifier output
        raw_output = email_data.get('Classifier Output', '')
        if isinstance(raw_output, tuple):
            raw_output = raw_output[0]
        
        # Extract category from raw_output
        category = next((cat for cat in known_categories if cat in raw_output), 'Unknown Category')
        
        # Extract responder output
        raw_output_from_responder = email_data.get('Responder Output', '')
        if isinstance(raw_output_from_responder, tuple):
            raw_output_from_responder = raw_output_from_responder[0]

        # Prepare the email
        msg = MIMEMultipart()
        msg['From'] = 'youremail@gmail.com'
        msg['To'] = email_from
        msg['Subject'] = f"Re: {email_subject}"
        msg.add_header('In-Reply-To', email_id)
        msg.add_header('References', email_id)

        # Email body with formatted classifier and responder outputs
        body = f"Classifier Output: {raw_output}\n\nResponder Output:\n{raw_output_from_responder}\n"
        msg.attach(MIMEText(body, 'plain'))

        # Attach specific file based on extracted category
        attachment_path = category_to_attachments.get(category, '')
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={Path(attachment_path).name}')
                msg.attach(part)

        # Send the email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'youremail@gmail.com'
        smtp_password = 'wurd '  # Replace with your actual password

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            print('Reply sent successfully.')
        except Exception as e:
            print(f'Failed to send email. Error: {e}')

# Call the function with your JSON file path
# process_json_and_send_emails('/path/to/your/json_file.json')
