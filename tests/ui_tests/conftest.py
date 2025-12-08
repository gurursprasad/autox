import base64
import os
import pytest
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from autox.config import config
from autox.autox_logger import logger

driver = None
failed_tests = []


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
    global driver
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

    # driver.get("https://the-internet.herokuapp.com/")
    driver.get(config.app_url)
    driver.maximize_window()

    request.cls.driver = driver
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    global failed_tests, driver
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    # Check if the driver is an instance of WebDriver
    if isinstance(driver, WebDriver):
        if report.when == "call" or report.when == "setup":
            xfail = hasattr(report, "wasxfail")
            if (report.skipped and xfail) or (report.failed and not xfail):
                file_name = report.nodeid.replace("::", "_") + ".png"
                _capture_screenshot(file_name)
                if os.path.exists(file_name):
                    with open(file_name, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                    html = (
                        '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:304px;height:228px;" '
                        'onclick="window.open(this.src)" align="right"/></div>' % encoded_string
                    )
                    extra.append(pytest_html.extras.html(html))
                else:
                    logger.error(f"Screenshot file {file_name} not found.")

                # Collect failed tests
                failed_tests.append(
                    {
                        "name": item.name,
                        "nodeid": report.nodeid,
                        "longrepr": report.longrepr,
                        "screenshot": file_name,
                    }
                )
            report.extra = extra


def _capture_screenshot(name):
    global driver
    try:
        if isinstance(driver, WebDriver):
            driver.get_screenshot_as_file(name)
        else:
            logger.error(f"No driver available to capture screenshot as {name}.")
    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")
