import pytest
import requests
import responses
from autox.autox_logger import logger

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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test failures and log them to autox_logger."""
    outcome = yield
    rep = outcome.get_result()
    
    # Log test failures and errors only for the test call phase (not setup/teardown)
    if call.when == "call":
        if rep.failed:
            test_name = item.name
            if hasattr(rep, 'longttr') and rep.longttr:
                error_msg = rep.longttr
            else:
                error_msg = "Test assertion failed"
            logger.error(f"TEST FAILED: {test_name} - {error_msg}")
        
        elif rep.error:
            test_name = item.name
            if hasattr(rep, 'longttr') and rep.longttr:
                error_msg = rep.longttr
            else:
                error_msg = "Test error occurred"
            logger.error(f"TEST ERROR: {test_name} - {error_msg}")
