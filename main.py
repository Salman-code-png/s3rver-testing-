from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
from threading import Thread, Event
import time
import random
import string
from datetime import datetime

app = Flask(__name__)
app.secret_key = "SuperSecretKey2025"

USERNAME = "Salman on fire"
PASSWORD = "salman king"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',
    'Referer': 'https://www.google.com/'
}

stop_events = {}
threads = {}
task_count = 0
task_logs = {}
MAX_TASKS = 10000

def log_message(task_id, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if task_id not in task_logs:
        task_logs[task_id] = []
    task_logs[task_id].append(f"[{timestamp}] {message}")

def send_messages(access_tokens, thread_id, hatersname, lastname, time_interval, messages, task_id):
    global task_count
    stop_event = stop_events[task_id]
    
    log_message(task_id, "Task started successfully")
    
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                try:
                    api_url = f'https://graph.facebook.com/v17.0/t_{thread_id}/'
                    message = f"{hatersname} {message1} {lastname}"
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters, headers=headers)
                    log_message(task_id, f"Sent: {message[:30]}... (Status: {response.status_code})")
                    time.sleep(time_interval)
                except Exception as e:
                    log_message(task_id, f"Error: {str(e)}")
                    time.sleep(5)
    
    log_message(task_id, "Task stopped")
    task_count -= 1
    del stop_events[task_id]
    del threads[task_id]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('send_message'))
        return '''
        <div style="color:red;text-align:center;padding:20px;">
            ❌ Invalid Username or Password!
        </div>
        ''' + login_form()
    return login_form()

def login_form():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - By S9LM9N KING</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                background: url('https://i.ibb.co/Y4MT0CSC/1740601612017.jpg') no-repeat center center fixed;
                background-size: cover;
                color: white;
                font-family: Arial, sans-serif;
                padding: 20px;
            }
            .login-box {
                background: rgba(0,0,0,0.7);
                max-width: 400px;
                margin: 50px auto;
                padding: 20px;
                border-radius: 10px;
            }
            input {
                padding: 12px;
                margin: 10px 0;
                width: 90%;
                border-radius: 5px;
                border: none;
            }
            button {
                padding: 12px;
                background: red;
                color: white;
                border: none;
                border-radius: 5px;
                width: 95%;
                font-weight: bold;
            }
            @media (max-width: 500px) {
                .login-box {
                    width: 90%;
                    padding: 15px;
                }
            }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2 style="text-align:center;">Login to Access</h2>
            <form method="post">
                <input type="text" name="username" placeholder="Enter Username" required><br>
                <input type="password" name="password" placeholder="Enter Password" required><br>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/home', methods=['GET', 'POST'])
def send_message():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if task_count >= MAX_TASKS:
            return '''
            <div style="color:yellow;text-align:center;padding:20px;">
                ⚠️ Monthly Task Limit Reached!
            </div>
            ''' + main_form()

        token_option = request.form.get('tokenOption')
        access_tokens = [request.form.get('singleToken').strip()] if token_option == 'single' else request.files['tokenFile'].read().decode().strip().splitlines()
        
        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        stop_events[task_id] = Event()
        
        thread = Thread(
            target=send_messages,
            args=(
                access_tokens,
                request.form.get('threadId').strip(),
                request.form.get('hatersname').strip(),
                request.form.get('lastname').strip(),
                int(request.form.get('time')),
                request.files['txtFile'].read().decode().splitlines(),
                task_id
            )
        )
        
        threads[task_id] = thread
        thread.start()
        task_count += 1
        
        return f'''
        <div style="color:green;text-align:center;padding:20px;">
            Task started with ID: {task_id}<br>
            <a href="/logs/{task_id}" style="color:cyan;">View Logs</a>
        </div>
        ''' + main_form()

    return main_form()

def main_form():
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>S9LM9N KING Tool</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                background: url('https://i.ibb.co/7N2tfWYv/1736256093345.jpg') no-repeat center center fixed;
                background-size: cover;
                color: white;
                font-family: Arial, sans-serif;
                padding: 20px;
            }}
            .main-box {{
                background: rgba(0,0,0,0.7);
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                border-radius: 10px;
            }}
            input, select, button {{
                padding: 12px;
                margin: 8px 0;
                width: 95%;
                border-radius: 5px;
                border: none;
            }}
            button {{
                background: red;
                color: white;
                font-weight: bold;
            }}
            a {{
                color: cyan;
                text-decoration: none;
            }}
            @media (max-width: 600px) {{
                .main-box {{
                    width: 90%;
                    padding: 15px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="main-box">
            <h2 style="text-align:center;">Users Running: {task_count} / {MAX_TASKS}</h2>
            <form method="post" enctype="multipart/form-data">
                <select name="tokenOption" required>
                    <option value="single">Single Token</option>
                    <option value="multiple">Token File</option>
                </select><br>
                <input type="text" name="singleToken" placeholder="Enter Single Token"><br>
                <input type="file" name="tokenFile"><br>
                <input type="text" name="threadId" placeholder="Enter Inbox/Convo ID" required><br>
                <input type="text" name="hatersname" placeholder="Enter Hater Name" required><br>
                <input type="text" name="lastname" placeholder="Enter Last Name" required><br>
                <input type="number" name="time" placeholder="Enter Time (seconds)" required><br>
                <input type="file" name="txtFile" required><br>
                <button type="submit">Run</button>
            </form>
            
            <form method="post" action="/stop">
                <input type="text" name="taskId" placeholder="Enter Task ID to Stop" required><br>
                <button type="submit">Stop Task</button>
            </form>
            
            <p style="text-align:center;margin-top:20px;">
                <a href="/active-tasks">View Active Tasks</a>
            </p>
        </div>
    </body>
    </html>
    '''

@app.route('/logs/<task_id>')
def view_logs(task_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if task_id not in task_logs:
        return '''
        <div style="color:red;text-align:center;padding:20px;">
            No logs found for this task ID or task has been completed.
        </div>
        ''' + main_form()
    
    logs = "<br>".join(task_logs[task_id])
    return f'''
    <div style="background:rgba(0,0,0,0.7);max-width:800px;margin:20px auto;padding:20px;border-radius:10px;">
        <h2 style="text-align:center;">Logs for Task: {task_id}</h2>
        <div style="background:black;padding:15px;border-radius:5px;overflow:auto;max-height:400px;">
            {logs}
        </div>
        <p style="text-align:center;margin-top:20px;">
            <a href="/home">Back to Home</a>
        </p>
    </div>
    '''

@app.route('/active-tasks')
def active_tasks():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    active = "<br>".join([f'<a href="/logs/{task_id}">{task_id}</a>' for task_id in threads.keys()])
    return f'''
    <div style="background:rgba(0,0,0,0.7);max-width:600px;margin:20px auto;padding:20px;border-radius:10px;">
        <h2 style="text-align:center;">Active Tasks</h2>
        <div style="text-align:center;">
            {active if active else "No active tasks"}
        </div>
        <p style="text-align:center;margin-top:20px;">
            <a href="/home">Back to Home</a>
        </p>
    </div>
    '''

@app.route('/stop', methods=['POST'])
def stop_task():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'''
        <div style="color:green;text-align:center;padding:20px;">
            Task {task_id} stopped successfully.
        </div>
        ''' + main_form()
    return '''
    <div style="color:red;text-align:center;padding:20px;">
        Invalid Task ID or task already completed.
    </div>
    ''' + main_form()

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=21405, debug=True)

