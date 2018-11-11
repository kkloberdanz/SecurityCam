#!/usr/bin/env python3


from multiprocessing import Process
from flask import Flask, render_template, Response
import pycam as camera
import security
from flask_login import LoginManager
from flask_login import login_required


app = Flask(__name__)
login = LoginManager(app)


@app.route('/')
#@login_required
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(frames):
    while True:
        frame = next(frames)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/livestream')
#@login_required
def livestream():
    frames = camera.stream()
    return Response(gen(frames),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # Start camera daemon
    proc = Process(target=camera.record)
    proc.start()

    # Start server
    app.run(host='192.168.0.106', port=5000, threaded=True)
