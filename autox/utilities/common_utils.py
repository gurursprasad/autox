import datetime
import json
import random
import string
import subprocess


def execute_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(timeout=600)
    except subprocess.TimeoutExpired:
        process.kill()
        out, err = process.communicate()
    return out.decode("utf-8"), err.decode("utf-8")


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
        print("Command timed out after 600 seconds.")
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
        print(f"Log file {log_file_path} not found.")
        return False


def read_data_from_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data
