from flask import Flask, render_template, jsonify, request, stream_with_context, Response
import subprocess
import time
import os

app = Flask(__name__)

# Route for serving the dashboard
@app.route('/')
def index():
    return render_template('index1.2.html')

# Route to handle manual script execution
@app.route('/run-manual-script', methods=['GET'])
def run_manual_script():
    def run_script():
        process = subprocess.Popen(['python', 'mail_main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(process.stdout.readline, b''):
            yield line.decode('utf-8')
        process.stdout.close()
        process.wait()
    return Response(run_script(), mimetype='text/plain')

# Route to handle live log streaming
@app.route('/stream', methods=['GET'])
def stream():
    def generate():
        logfile = 'logfile.log'
        if os.path.exists(logfile):
            with open(logfile, 'r') as log:
                yield log.read()
        
        while True:
            with open(logfile, 'r') as log:
                data = log.read()
                yield data
            time.sleep(2)
    return Response(stream_with_context(generate()), mimetype="text/event-stream")

# Route to send an email
@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    subject = data['subject']
    recipient = data['recipient']
    body = data['body']
    # Add your email sending logic here, e.g., using smtplib
    return jsonify({"status": "Email sent"}), 200

if __name__ == '__main__':
    app.run(debug=True)
