from time import sleep

import requests
import subprocess
import os
from pathlib import Path

REPO_ROOT = Path(os.path.realpath(__file__)).parent.parent


def test_main():
    docker = subprocess.run(["docker-compose", "up", "-d"], cwd=REPO_ROOT)
    while True:
        print("Trying to get connection to a microservice")
        try:
            resp = requests.get("http://localhost:5052")
            print(resp.text)
            resp.raise_for_status()
            break
        except Exception as e:
            print(e)
            pass
        sleep(1)

    resp = requests.post("http://localhost:5052/events", data={"uid": "asd_uid", "message": "asdasd_msg"})
    assert resp.text == 'Added new event'
