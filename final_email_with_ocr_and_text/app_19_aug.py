from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Load unseen emails from JSON
def load_json_data():
    from unseen_aug_19 import load_unseen_emails
    return load_unseen_emails()

# Fetch unseen mail count from unseen_count.py
def get_unseen_mail_count():
    from unseen_count import fetch_unseen_email_count
    return fetch_unseen_email_count()

# Updated dashboard data function
def get_dashboard_data():
    data = load_json_data()
    
    # Fetch unseen mail count
    unseen_mails = get_unseen_mail_count()

    emails = [{
        "id": i + 1,
        "subject": email["Subject"],
        "from": email["From"],
        "date": email["Date"],
        "content_preview": email["Content Preview"],  # Preview first 100 characters
        "attachment_count": email["Attachment Count"],
        "attachment_types": email["Attachment Types"]
    } for i, email in enumerate(data)]
    
    return {
        "unseen_mails": unseen_mails,
        "emails": emails
    }

@app.route('/')
def index():
    return render_template('aug19.html')

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
        emails = [email for email in emails if sender.lower() in email['from'].lower()]
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

if __name__ == '__main__':
    app.run(debug=True)
