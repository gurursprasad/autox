import datetime
import json
import random
import re
import string
import subprocess

from autox.autox_logger import logger

ANSI_ESCAPE = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]")


def execute_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(timeout=600)
    except subprocess.TimeoutExpired:
        process.kill()
        out, err = process.communicate()
    return strip_ansi_codes(out.decode("utf-8")), strip_ansi_codes(err.decode("utf-8"))


def run_command(command):
    try:
        process = subprocess.run(command, check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with return code {e.returncode}: {e.cmd}")
        if e.stdout:
            logger.error(f"{strip_ansi_codes(e.stdout.strip())}")
        if e.stderr:
            logger.error(f"{strip_ansi_codes(e.stderr.strip())}")

        return None, None

    except FileNotFoundError:
        logger.error(f"Executable not found. Check if '{command[0]}' is in your PATH.")
        return None, None

    return strip_ansi_codes(process.stdout), strip_ansi_codes(process.stderr)


def execute_command_realtime(command):
    """Runs a command locally with real-time output."""
    if isinstance(command, list):
        cmd = command
        shell = False
    else:
        cmd = command
        shell = True

    try:
        process = subprocess.Popen(
            cmd,
            shell=shell,
            stdout=None,  # Inherit parent's stdout
            stderr=None,  # Inherit parent's stderr
        )
        process.communicate(timeout=600)
        return process.returncode
    except subprocess.TimeoutExpired:
        process.kill()
        logger.error("Command timed out after 600 seconds.")
        return -1


def generate_random_id():
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(4))


def get_current_timestamp():
    ct = datetime.datetime.now()
    return ct


def scan_logs_for_pattern(log_file_path):
    ERROR_PATTERNS = ["Unexpected number", "fail to delete"]
    # WARNING_PATTERNS = [
    #     "Unable to send metrics packet"
    # ]
    try:
        with open(log_file_path, "r") as log_file:
            log_line = log_file.readline()
            for error_pattern in ERROR_PATTERNS:
                if error_pattern in log_line:
                    return log_line
        return False
    except FileNotFoundError:
        logger.error(f"Log file {log_file_path} not found.")
        return False


def read_data_from_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def strip_ansi_codes(text):
    """Removes ANSI escape codes from a string."""
    return ANSI_ESCAPE.sub("", text)
