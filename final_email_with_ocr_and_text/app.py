from flask import Flask, render_template, Response
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_logs():
    process = subprocess.Popen(['python3', 'mail_main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        formatted_line = line.decode('utf-8').strip()
        yield f"data:{formatted_line}\n\n"

    return_code = process.wait()
    if return_code == 0:
        yield f"data:Script completed successfully.\n\n"
    else:
        yield f"data:Script completed with return code {return_code}. There might have been some issues.\n\n"

@app.route('/stream')
def stream():
    return Response(generate_logs(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
