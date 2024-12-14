from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Load JSON data from file
def load_json_data():
    with open('/data/aiuserinj/sarjil/mail_summarizer/final_email_with_ocr_and_text/unseen_emails_info.json', 'r') as file:
        data = json.load(file)
    return data

# Fetch unseen mail count from unseen_count.py
def get_unseen_mail_count():
    from unseen_count import fetch_unseen_email_count
    return fetch_unseen_email_count()

# Updated dashboard data function
def get_dashboard_data():
    data = load_json_data()
    
    # Fetch unseen mail count
    unseen_mails = get_unseen_mail_count()
    pending_responses = 5  # This might come from the JSON or other logic
    completed_responses = unseen_mails - pending_responses
    error_log = ["Error fetching email #3", "Timeout in response generation"]  # This might be part of the JSON as well
    
    emails = [{
    "id": i + 1,
    "sender": email["From"],
    "subject": email["Subject"],
    "content_preview": email["Content Preview"][:100],  # Just a preview
    "received_date": email["Date"],
    "attachment_count": email["Attachment Count"],
    "attachment_types": email["Attachment Types"]
        } for i, email in enumerate(data)]
    
    return {
        "unseen_mails": unseen_mails,
        "pending_responses": pending_responses,
        "completed_responses": completed_responses,
        "error_log": error_log,
        "emails": emails
    }

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
    data = get_dashboard_data()
    email = next((email for email in data['emails'] if email['id'] == email_id), None)
    if email:
        email['content'] = data[email_id - 1]["Content"]  # Full content from JSON
    return jsonify(email) if email else ('', 404)

if __name__ == '__main__':
    app.run(port=4996, debug=True)
