import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = None


def pytest_addoption(parser):
    # Use a distinct option name to avoid conflict with pytest-playwright's
    # `--browser` option (which only accepts 'chromium, firefox, webkit').
    parser.addoption(
        "--selenium-browser",
        action="store",
        default="chrome",
        help="Type in browser name for selenium tests (chrome/firefox/edge)",
    )
    # Use boolean flags for headless to avoid passing string values.
    # `--headless` and `--headless-mode` both enable headless mode when provided.
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run selenium tests in headless mode",
    )
    parser.addoption(
        "--headless-mode",
        action="store_true",
        default=False,
        help="Alias for --headless; enable headless mode",
    )


@pytest.fixture(scope="class")
def setup_driver(request):
    # Prefer explicit selenium-specific option to avoid clashes with other plugins
    browser = request.config.getoption("--selenium-browser")
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        # Treat either flag as enabling headless mode
        headless_flag = bool(request.config.getoption("--headless") or request.config.getoption("--headless-mode"))
        if headless_flag:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://the-internet.herokuapp.com/")
    driver.maximize_window()

    request.cls.driver = driver
    yield driver
    driver.quit()
