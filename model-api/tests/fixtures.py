import os
import pytest
from fastapi.testclient import TestClient
from model_api.web import create_app


MODEL = "microsoft/phi-2"
args = ["--model", MODEL, "--trust-remote-code"]


@pytest.fixture(scope="session")
def unauthorized_client():
    return TestClient(create_app(args))


@pytest.fixture(scope="session")
def client():
    auth_key = "myauthkey"
    os.environ["API_KEY"] = auth_key
    os.environ["TEMPERATURE_SCALING_FACTOR"] = "0.0"
    app = create_app(args)

    return TestClient(app, headers={"X-Auth-Key": auth_key})
