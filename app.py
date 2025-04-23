from flask import Flask, render_template, redirect, Response
from camera import VideoCamera
from face_recog import is_authenticated_and_get_name
import csv
from datetime import datetime
import os

app = Flask(__name__)
camera = VideoCamera()

authenticated = False
user_name = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    global user_name
    if authenticated:
        return render_template('dashboard.html', name=user_name)
    else:
        return redirect('/')

@app.route('/video_feed')
def video_feed():
    return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/check_auth')
def check_auth():
    global authenticated, user_name
    frame = camera.get_frame()
    authenticated, user_name = is_authenticated_and_get_name(frame)

    if authenticated and user_name:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('attendance.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([user_name, now])
        return redirect('/dashboard')

    return redirect('/login')

if __name__ == '__main__':
    if not os.path.exists('attendance.csv'):
        with open('attendance.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Datetime'])

    app.run(debug=True)