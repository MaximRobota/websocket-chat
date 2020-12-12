#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, jsonify, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask_login import LoginManager, UserMixin, current_user, login_user, \
    logout_user
from flask_session import Session
# import requests

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
login = LoginManager(app)
Session(app)
socketio = SocketIO(app, async_mode=async_mode, manage_session=False)
thread = None
thread_lock = Lock()


class User(UserMixin, object):
    def __init__(self, id=None):
        self.id = id


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


# @app.route('/sessions')
# def sessions():
#     return render_template('sessions.html')
#
#
# @app.route('/session', methods=['GET', 'POST'])
# def session_access():
#     if request.method == 'GET':
#         return jsonify({
#             'session': session.get('value', ''),
#             'user': current_user.id
#                 if current_user.is_authenticated else 'anonymous'
#         })
#     data = request.get_json()
#     if 'session' in data:
#         session['value'] = data['session']
#     elif 'user' in data:
#         if data['user']:
#             login_user(User(data['user']))
#         else:
#             logout_user()
#     return '', 204


@socketio.on('connect')
def connect():
    # resp = requests.post("http://localhost:5051/user", data={"name": username, "password": "pass"}).json()
    print(22222222222222)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('new_event')
def message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event')
def broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_room_event',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)


@login.user_loader
def load_user(id):
    return User(id)


@socketio.on('get-session')
def get_session():
    emit('refresh-session', {
        'session': session.get('value', ''),
        'user': current_user.id
            if current_user.is_authenticated else 'anonymous'
    })


@socketio.on('set-session')
def set_session(data):
    if 'session' in data:
        session['value'] = data['session']
    elif 'user' in data:
        if data['user'] is not None:
            login_user(User(data['user']))
        else:
            logout_user()

app.run(host='0.0.0.0', port=80, debug=True)
