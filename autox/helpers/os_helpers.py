import os
import uuid
from pathlib import Path
import namer
from autox.autox_logger import logger


def generate_random_name():
    name = namer.generate(category="computer_science")
    logger.debug(f"Generated a random name: {name}")
    return name  # Example: 'crazy-supernova'


def generate_random_id():
    rand_id = uuid.uuid4().hex[:6]
    logger.debug(f"Generated a random id: {rand_id}")
    return rand_id


def make_directory(directory_name):
    try:
        p = Path(directory_name)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory_name}")
        else:
            logger.debug(f"'{directory_name}' directory exists. Skipping creation")
    except Exception as e:
        logger.exception(e)
        logger.error(f"Error creating directory '{directory_name}'")


def create_and_write_to_file(file_path, env_name=None):
    try:
        p = Path(file_path)
        # Ensure parent directory exists
        if not p.parent.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created parent directory for file: {p.parent}")

        logger.info(f"Creating file: {file_path}")
        with p.open("w") as f:
            if env_name is not None:
                # Ensure we write a string (caller may pass non-str objects)
                if not isinstance(env_name, str):
                    env_text = str(env_name)
                else:
                    env_text = env_name
                f.write(env_text)
    except Exception as e:
        logger.exception(e)
        logger.error(f"Error creating file '{file_path}'")


def open_and_read_from_file(file_path, env_name=None):
    try:
        p = Path(file_path)
        # If the parent dir doesn't exist, log that at DEBUG (no automatic creation here).
        if not p.parent.exists():
            logger.debug(f"Parent directory does not exist for the file: {file_path}")

        logger.debug(f"Reading from file: {file_path}")
        with p.open("r") as f:
            env_text = f.readline()
            if not env_text:
                # Keep this at DEBUG so callers can decide whether empty content is noteworthy.
                logger.debug(f"File {file_path} is empty")
            return env_text
    except Exception as e:
        logger.exception(e)
        logger.error(f"Error reading from file '{file_path}'")


def write_to_file(file_path, mode=None, text=None):
    try:
        p = Path(file_path)
        # Ensure parent directory exists
        if not p.parent.exists():
            logger.warning(f"Specified file does not exist: {file_path}")
            return
        
        logger.info(f"Specified file located and writing to file: {file_path}")
        
        if not mode:
            mode = "w"

        with p.open(str(mode)) as f:
            if text is not None:
                # Ensure we write a string (caller may pass non-str objects)
                if not isinstance(text, str):
                    env_text = str(text)
                else:
                    env_text = text
                f.write(env_text)
        return True
    except Exception as e:
        logger.error(f"Error writing to file '{file_path}'")
        return e
