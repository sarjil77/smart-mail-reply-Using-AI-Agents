from flask import Flask, render_template, jsonify, request
import json
import os
from unseen_count_Info import update_email_data, fetch_unseen_email_count

app = Flask(__name__)

# Path to the JSON file
json_file_path = '/data/aiuserinj/sarjil/mail_summarizer/final_email_with_ocr_and_text/unseen_emails_info.json'

# Load JSON data from file
def load_json_data():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    return []

# Fetch unseen mail count based on loaded JSON data
def get_unseen_mail_count():
    json_data = load_json_data()
    return len(json_data)

# Updated dashboard data function
def get_dashboard_data():
    json_data = load_json_data()
    unseen_mails = get_unseen_mail_count()
    pending_responses = 5  # Example static value
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

@app.route('/')
def index():
    return render_template('index_19.1.html')

@app.route('/api/dashboard-data', methods=['GET'])
def dashboard_data():
    data = get_dashboard_data()
    return jsonify(data)

@app.route('/api/emails', methods=['GET'])
def get_emails():
    data = get_dashboard_data()
    emails = data["emails"]

    # Filtering
    sender = request.args.get('sender')
    subject = request.args.get('subject')
    if sender:
        emails = [email for email in emails if sender.lower() in email['sender'].lower()]
    if subject:
        emails = [email for email in emails if subject.lower() in email['subject'].lower()]

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = 6
    start = (page - 1) * per_page
    end = start + per_page
    paginated_emails = emails[start:end]
    total_pages = (len(emails) + per_page - 1) // per_page

    return jsonify({
        "emails": paginated_emails,
        "total_pages": total_pages,
        "current_page": page
    })

@app.route('/api/email/<int:email_id>', methods=['GET'])
def get_email_details(email_id):
    json_data = load_json_data()
    email = next((email for email in json_data if email['id'] == email_id), None)
    if email:
        email['content'] = email.get("Content", "")  # Full content from JSON
    return jsonify(email) if email else ('', 404)

if __name__ == '__main__':
    app.run(port=4997, debug=True)
