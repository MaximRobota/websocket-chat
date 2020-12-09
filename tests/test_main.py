from time import sleep
import pytest
import requests
import subprocess
import os
from pathlib import Path

REPO_ROOT = Path(os.path.realpath(__file__)).parent.parent


@pytest.fixture
def prepare_services():
    subprocess.run(["docker-compose", "down"], cwd=REPO_ROOT)
    subprocess.run(["docker-compose", "build"], cwd=REPO_ROOT)
    docker = subprocess.run(["docker-compose", "up", "-d"], cwd=REPO_ROOT)
    for i in range(8):
        print("Trying to get connection to a microservice")
        try:
            resp = requests.get("http://localhost:5051")
            print(resp.text)
            resp.raise_for_status()
            break
        except Exception as e:
            # print(e)
            pass
        sleep(5)
    yield
    subprocess.run(["docker-compose", "down"], cwd=REPO_ROOT)


@pytest.mark.usefixtures("prepare_services")
def test_user():
    useremail = "Vasiya@gm.com"
    resp = requests.post("http://localhost:5051/auth/register", data={"email": useremail, "password": "pass"}).json()
    assert "user" in resp
    assert resp["user"]["email"] == useremail
    assert "id" in resp["user"]
