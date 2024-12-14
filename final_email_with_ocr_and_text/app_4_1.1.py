from flask import Flask, render_template, jsonify, Response
import subprocess
import threading
import time
import json

app = Flask(__name__)

# Path to your mail_main.py script
MAIL_MAIN_SCRIPT = 'mail_summarizer/final_email_with_ocr_and_text/mail_main.py'

# Initialize counters
stats = {
    "emailsProcessed": 0,
    "successfulResponses": 0,
    "errorCount": 0
}

def run_mail_script():
    global stats
    process = subprocess.Popen(
        ['python', MAIL_MAIN_SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    for line in process.stdout:
        # Update stats based on script output
        if "emails_processed" in line:
            stats["emailsProcessed"] = int(line.split(":")[-1].strip())
        elif "successful_responses" in line:
            stats["successfulResponses"] = int(line.split(":")[-1].strip())
        elif "errors" in line:
            stats["errorCount"] = int(line.split(":")[-1].strip())
    process.wait()

@app.route('/')
def index():
    return render_template('index1.1.html')

@app.route('/start-process')
def start_process():
    if not any(thread.is_alive() for thread in threading.enumerate() if thread.name == "mail_script"):
        thread = threading.Thread(target=run_mail_script, name="mail_script")
        thread.start()
        return jsonify({"status": "Process started"})
    else:
        return jsonify({"status": "Process already running"})

@app.route('/status')
def get_status():
    return jsonify(stats)

def generate():
    while True:
        status = get_status().json
        yield f"data: {json.dumps(status)}\n\n"
        time.sleep(1)

@app.route('/stream')
def stream():
    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
