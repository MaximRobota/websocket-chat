#!/usr/bin/env python
import logging

import requests
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, rooms


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route("/")
def index():
    return "OK !"


@socketio.on('connect')
def connect():
    app.logger.info("Connected!")
    auth = request.headers['Authorization']
    headers = {'Authorization': auth}
    app.logger.info(f"Auth {auth}")
    resp_status = requests.get(
        'http://identity-service:80/auth/status',
        headers=headers
    )
    if resp_status.status_code != 200:
        return False
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('join')
def join(message):
    join_room(message['room'])
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})


@socketio.on('my_room_event')
def send_room_message(message):
    emit('my_room_event',
         {'data': message['data']},
         room=message['room'])


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
