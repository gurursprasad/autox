import click

from autox.autox_logger import logger
from autox.utilities.common_utils import execute_command_realtime


# cli root group
@click.group(name="run-tests", help="Choose tests to run")
def run_tests_group():
    """Run UI and API tests."""
    pass


@click.command(name="ui", help="Runs all UI tests from autox/tests/ui_tests directory")
@click.option("--browser", default="chrome", help="Browser to run test on. Default browser is Chrome.")
@click.option(
    "--headless",
    is_flag=True,
    default=False,
    help="Set --headless to run tests in headless mode. Default is normal mode.",
)
def run_ui_tests(browser, headless=False):
    # Build command as a list of executable + args so subprocess runs correctly
    cmd = [
        "pytest",
        "-v",
        "-s",
        "--html=report.html",
        "--capture=tee-sys",
        "--self-contained-html",
        "--junitxml=results/test-results.xml",
    ]

    if browser:
        cmd.append(f"--selenium-browser={browser}")

    if headless:
        cmd.append("--headless")

    # Test path should come after all pytest options
    cmd.append("tests/ui_tests")

    exit_code = execute_command_realtime(cmd)
    if exit_code != 0:
        logger.error("Issue running UI tests")


@click.command(name="api", help="Runs all API tests from autox/tests/api_tests directory")
def run_api_tests():
    # Build command as a list of executable + args so subprocess runs correctly
    cmd = [
        "pytest",
        "-v",
        "-s",
        "--html=report.html",
        "--capture=tee-sys",
        "--self-contained-html",
        "--junitxml=results/test-results.xml",
    ]

    # Test path should come after all pytest options
    cmd.append("tests/api_tests")

    exit_code = execute_command_realtime(cmd)
    if exit_code != 0:
        logger.error("Issue running API tests")


run_tests_group.add_command(run_ui_tests)
run_tests_group.add_command(run_api_tests)
