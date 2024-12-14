from flask import Flask, render_template, jsonify, request
import json
import os
import subprocess
from unseen_count_Info import update_email_data

app = Flask(__name__)

# Configuration paths for JSON files
FETCHED_EMAIL_JSON_PATH = '/data/aiuserinj/sarjil/mail_summarizer/final_email_with_ocr_and_text/unseen_emails_info.json'
RESPONSE_JSON_PATH = '/data/aiuserinj/sarjil/mail_summarizer/final_email_with_ocr_and_text/all_email_results_aug_18.json'

# Load JSON data from a specific file path
def load_json_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

# Fetch unseen mail count based on loaded JSON data
def get_unseen_mail_count():
    return len(load_json_data(FETCHED_EMAIL_JSON_PATH))

# Updated dashboard data function
def get_dashboard_data():
    json_data = load_json_data(FETCHED_EMAIL_JSON_PATH)
    unseen_mails = get_unseen_mail_count()
    pending_responses = get_unseen_mail_count()  # Example static value
    completed_responses = unseen_mails - pending_responses
    error_log = ["Error fetching email #3", "Timeout in response generation"]  # Example static errors
    
    emails = [{
        "id": i + 1,
        "sender": email["From"],
        "subject": email["Subject"],
        "content_preview": email["Content Preview"][:100],
        "received_date": email["Date"],
        "attachment_count": email["Attachment Count"],
        "attachment_types": [att["Filename"] for att in email.get("Attachments", [])]
    } for i, email in enumerate(json_data)]
    
    return {
        "unseen_mails": unseen_mails,
        "pending_responses": pending_responses,
        "completed_responses": completed_responses,
        "error_log": error_log,
        "emails": emails
    }

# Route to trigger unseen email fetching
@app.route('/api/fetch-unseen-emails', methods=['POST'])
def fetch_unseen_emails():
    update_email_data()  # This will fetch the unseen emails and update the JSON
    return jsonify({"message": "Unseen emails fetched successfully."}), 200

# Route for the dashboard data
@app.route('/api/dashboard-data', methods=['GET'])
def dashboard_data():
    data = get_dashboard_data()
    return jsonify(data)

# Pagination function
def get_paginated_emails(page=1, sender=None, subject=None, per_page=5):
    emails = get_dashboard_data()['emails']
    
    # Apply filters if provided
    if sender:
        emails = [email for email in emails if sender.lower() in email['sender'].lower()]
    if subject:
        emails = [email for email in emails if subject.lower() in email['subject'].lower()]
    
    # Calculate pagination details
    total_emails = len(emails)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_emails = emails[start:end]
    total_pages = (total_emails + per_page - 1) // per_page  # Ceiling division
    
    return {
        "emails": paginated_emails,
        "total_pages": total_pages,
        "current_page": page
    }

# Route for paginated emails
@app.route('/api/emails', methods=['GET'])
def get_emails():
    page = int(request.args.get('page', 1))
    sender = request.args.get('sender', None)
    subject = request.args.get('subject', None)
    
    paginated_emails = get_paginated_emails(page, sender, subject)
    return jsonify(paginated_emails)

# Route for specific email details
@app.route('/api/email/<int:email_id>', methods=['GET'])
def get_email_details(email_id):
    emails = get_dashboard_data()['emails']
    email = next((email for email in emails if email['id'] == email_id), None)
    if email:
        return jsonify(email)
    return jsonify({"error": "Email not found"}), 404

# New route to get response details
@app.route('/api/response-details', methods=['GET'])
def get_response_details():
    json_data = load_json_data(RESPONSE_JSON_PATH)
    print("Loaded JSON Data:", json_data)  # Add this line for debugging
    response_details = [{
        "id": email.get("ID", "N/A"),
        "sender": email.get("From", "N/A"),
        "subject": email.get("Subject", "N/A"),
        "received_date": email.get("Received", "N/A"),
        "classifier_output": email.get("Classifier Output", "N/A"),
        "responder_output": email.get("Responder Output", "N/A")
    } for i, email in enumerate(json_data)]
    
    if response_details:
        return jsonify({"response_details": response_details})
    else:
        return jsonify({"error": "No response data available"}), 404


# New route to run main.py
@app.route('/api/run-main', methods=['POST'])
def run_main():
    try:
        subprocess.run(['python3', 'main_aug_20.py'], check=True)  # Adjust the command if needed
        return jsonify({"message": "Email workflow executed successfully."}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"message": "Failed to execute the email workflow.", "error": str(e)}), 500

# Home route to render the template
@app.route('/')
def index():
    return render_template('final.html')

if __name__ == '__main__':
    update_email_data()  # Initial email data update
    app.run(port= 5000,debug=True)
