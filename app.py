#!/usr/bin/env python3


from importlib import import_module
import os
from flask import Flask, render_template, Response
import pycam as camera


app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(frames):
    while True:
        frame = next(frames)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/livestream')
def livestream():
    frames = camera.stream()
    return Response(gen(frames),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.0.106', threaded=True)
