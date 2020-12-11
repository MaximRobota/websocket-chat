import os
import pytest
import requests
import socketio
import subprocess
from pathlib import Path
from loguru import logger
from time import sleep

REPO_ROOT = Path(os.path.realpath(__file__)).parent.parent


@pytest.fixture
def prepare_services():
    # devnull so that there is not output
    subprocess.run(['docker-compose', 'down'], cwd=REPO_ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['docker-compose', 'build'], cwd=REPO_ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Popen instead of .run() so that we do not wait for the process to finish
    # -d is removed so that the output comes to the 'docker' variable
    #
    docker = subprocess.Popen(['docker-compose', 'up'], cwd=REPO_ROOT)
    for i in range(8):
        logger.info('Trying to get connection to a microservice')
        try:
            resp = requests.get('http://localhost:5051')
            resp.raise_for_status()
            break
        except Exception as e:
            logger.error(e)
            pass
        sleep(5)
        # remove this, this is so we wait some time and then start a test,
        # just let the logs settle a little, and stop spamming
        for _ in range(5):
            logger.info("Established connection to microservice")
            sleep(1)
        subprocess.run(['docker-compose', 'ps'], cwd=REPO_ROOT)
        sleep(5)
    yield
    docker.kill()


def register_user(email, password):
    return requests.post(
        'http://localhost:5051/auth/register', data={'email': email, 'password': password}).json()


def login_user(email, password):
    return requests.post(
        'http://localhost:5051/auth/login', data={'email': email, 'password': password}).json()


@pytest.mark.usefixtures('prepare_services')
def test_registrer():
    user_email = 'Vasiya@gm.com'
    password = 'pass'
    resp_register = register_user(user_email, password)
    assert 'user' in resp_register
    assert resp_register['user']['email'] == user_email
    assert 'id' in resp_register['user']


@pytest.mark.usefixtures('prepare_services')
def test_login():
    user_email = 'Vasiya@gm.com'
    password = 'pass'
    resp_register = register_user(user_email, password)
    resp_login = login_user(user_email, password)
    assert 'auth_token' in resp_login
    assert resp_login['user']['email'] == user_email
    assert 'id' in resp_login['user']


@pytest.mark.usefixtures('prepare_services')
def test_user_status():
    user_email = 'Vasiya@gm.com'
    password = 'pass'
    resp_register = register_user(user_email, password)
    assert 'user' in resp_register
    assert 'auth_token' in resp_register

    resp_login = login_user(user_email, password)

    assert 'user' in resp_login
    assert 'auth_token' in resp_login

    headers = {'Authorization': 'Bearer ' + resp_login['auth_token']}
    resp_status = requests.get('http://localhost:5051/auth/status', headers=headers)
    resp_status_json = resp_status.json()
    assert resp_status_json['user']['email'] == user_email
    assert 'id' in resp_status_json['user']


@pytest.mark.usefixtures('prepare_services')
def test_user_status_fake_token():
    user_email = 'Vasiya@gm.com'
    password = 'pass'
    resp_register = register_user(user_email, password)
    assert 'user' in resp_register
    assert 'auth_token' in resp_register

    headers = {'Authorization': 'Bearer 123asd23asd23'}
    resp_status = requests.get('http://localhost:5051/auth/status', headers=headers)
    resp_status_json = resp_status.json()
    assert resp_status_json['status'] == 'fail'


@pytest.mark.usefixtures('prepare_services')
def test_connect_send_message_ws():
    user_email = 'Vasiya@gm.com'
    password = 'pass'
    register_user(user_email, password)
    resp_login = login_user(user_email, password)

    # assert 'auth_token' in resp_login

    headers = {'Authorization': 'Bearer ' + resp_login['auth_token']}
    resp_status = requests.get('http://localhost:5051/auth/status', headers=headers)
    resp_status_json = resp_status.json()
    # assert resp_status_json['user']['email'] == user_email
    # assert 'id' in resp_status_json['user']

    sio = socketio.AsyncClient()

    @sio.event
    async def connect():
        await sio.connect('http://localhost:5053')
        await sio.wait()
        print('my sid is')

        if sio.connected:
            await sio.emit('my message', ["join", {"room": "1"}])
            assert 'id' != 'id'
    # connect()
    #
    # @sio.event
    # def my_event(sid, data):
    #     # handle the message
    #     return "OK", 123

    # sio.disconnect()