"""
Configuration settings for the Smart Email Reply System.

This file contains all configuration variables and settings.
Create a copy of this file as 'config.py' and update with your actual credentials.
"""

# Email Configuration
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_specific_password"  # Use app-specific password for Gmail
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# AWS Configuration for OCR
AWS_ACCESS_KEY_ID = "your_aws_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_aws_secret_access_key"
AWS_REGION = "us-east-1"

# File Paths
ATTACHMENT_SAVE_PATH = "./attachments"
JSON_FILE_PATH = "./data/unseen_emails_info.json"
RESULTS_JSON_PATH = "./data/all_email_results.json"

# AI Model Configuration
AI_MODEL = "llama3.1:8b"  # Ollama model name

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Email Categories
EMAIL_CATEGORIES = [
    'Policy Inquiries',
    'Claims',
    'Billing and Payments',
    'Customer Support',
    'Renewals',
    'Documentation',
    'Quotes',
    'Cancellations',
    'Compliance and Legal',
    'Marketing and Promotions',
    'Internal Communications'
]

# Category-specific attachment mappings
CATEGORY_ATTACHMENTS = {
    'Policy Inquiries': './attachments/Policy Inquiries/sample_for_inquiry.pdf',
    'Claims': './attachments/Claims/claims.pdf',
    'Billing and Payments': './attachments/Billing and Payments/bills.png',
    'Customer Support': './attachments/Customer Support/customer support.jpeg',
    'Renewals': './attachments/Renewals/renewal.pdf',
    'Documentation': './attachments/Documentation/documentation.pdf',
    'Quotes': './attachments/Quotes/casual_photo.jpeg',
    'Cancellations': './attachments/Cancellations/spam_danger.jpeg',
    'Compliance and Legal': './attachments/Compliance and Legal/legal notice.pdf',
    'Marketing and Promotions': './attachments/Internal Communications/autoGEN_4_agents_R_paper.pdf',
    'Internal Communications': './attachments/Internal Communications/autoGEN_4_agents_R_paper.pdf'
}