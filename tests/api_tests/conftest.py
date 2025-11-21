import pytest
import requests
import responses

# @pytest.fixture(scope="session")
# def config():
#     with open(os.path.join(os.path.dirname(__file__), "config/config.yaml"), "r") as file:
#         return yaml.safe_load(file)


@pytest.fixture(scope="session")
def session(config):
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    session.headers.update({"Authorization": f"Bearer {config.api_key}"})
    return session


@pytest.fixture(scope="session")
def base_url(config):
    return config.api_url


@pytest.fixture
def mock_service_response():
    with responses.RequestsMock() as resp:
        yield resp
