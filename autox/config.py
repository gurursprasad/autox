import os
from enum import Enum
from pathlib import Path
from typing import Optional

import click
from autox.autox_logger import logger

from pydantic import BaseModel, Field

from autox.helpers.os_helpers import (
    create_and_write_to_file,
    generate_random_name,
    make_directory,
    open_and_read_from_file,
    write_to_file,
)

# Set autox root and environments directory paths
AUTOX_ROOT = Path(__file__).resolve().parent.parent
ENVIRONMENTS_DIR = Path(AUTOX_ROOT, "env_vars")


class ConfigMap(Enum):
    app_url = "APP_URL"
    api_url = "API_URL"
    api_key = "API_KEY"
    log_level = "LOG_LEVEL"
    # AWS related configurations
    aws_region = "AWS_REGION"
    aws_availability_zone = "AWS_AVAILABILITY_ZONE"
    aws_account_id = "AWS_ACCOUNT_ID"
    eks_cluster_name = "EKS_CLUSTER_NAME"
    # GitHub related configurations
    github_token = "GITHUB_TOKEN"
    github_repo_owner = "GITHUB_REPO_OWNER"
    # Terraform repo related configurations
    tf_github_repo = "TF_GITHUB_REPO"
    tf_github_branch = "TF_GITHUB_BRANCH"

    def source(self, default=None, convert_to_bool=False, post_process=None):
        env_variable_name = self.value

        def default_factory():
            env_variable_value = os.environ.get(env_variable_name, default)

            # Convert to bool if specified and the value is a string
            if convert_to_bool and isinstance(env_variable_value, str):
                env_variable_value = env_variable_value.upper() in {"TRUE", "YES", "1"}

            # Posr process if specified and a function is provided
            if post_process and env_variable_value:
                env_variable_value = post_process(env_variable_value)

            return env_variable_value

        return Field(default_factory=default_factory)

    def can_be_saved(self):
        return not hasattr(self, "do_not_save")


class Config(BaseModel):
    app_url: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.app_url.value))
    api_url: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.api_url.value))
    api_key: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.api_key.value))
    log_level: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.log_level.value))

    # AWS related configurations
    aws_region: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.aws_region.value))
    aws_availability_zone: Optional[str] = Field(
        default_factory=lambda: os.environ.get(ConfigMap.aws_availability_zone.value)
    )
    aws_account_id: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.aws_account_id.value))
    eks_cluster_name: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.eks_cluster_name.value))

    # GitHub related configurations
    github_token: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.github_token.value))
    github_repo_owner: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.github_repo_owner.value))

    # Terraform repo related configurations
    tf_github_repo: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.tf_github_repo.value))
    tf_github_branch: Optional[str] = Field(default_factory=lambda: os.environ.get(ConfigMap.tf_github_branch.value))


class EnvVars:
    def __init__(self):
        pass

    @staticmethod
    def create_env(env_name=None):
        # File paths and names
        if not env_name:
            env_name = generate_random_name()
        env_directory = os.path.join(ENVIRONMENTS_DIR, env_name)
        active_file_path = os.path.join(ENVIRONMENTS_DIR, "active")

        # Create /env_vars directory
        make_directory(ENVIRONMENTS_DIR)

        # Generate random name and add that name to /env_vars/active file
        create_and_write_to_file(active_file_path, env_name)

        # Create a /env_vars/random_env_name directory
        make_directory(env_directory)
        # Create the env_var file inside /env_vars/random_env_name and write the mandatory configs to it
        config = Config()
        # Exclude obvious secrets from the env file and write the rest as
        # KEY=VALUE lines where KEY is the environment variable name.
        SECRET_ENV_VARS = {"API_KEY", "GITHUB_TOKEN", "AWS_ACCOUNT_ID"}

        cfg = config.dict()
        lines = []
        for attr_name, val in cfg.items():
            # Map attribute name (e.g. 'app_url') -> env var name (e.g. 'APP_URL')
            try:
                env_var_name = ConfigMap[attr_name].value
            except KeyError:
                # Skip attributes we don't have a mapping for
                continue

            if env_var_name in SECRET_ENV_VARS:
                # Skip secrets entirely
                continue

            # If the value is None, write an empty value (KEY=)
            value_str = "" if val is None else str(val)
            lines.append(f"{env_var_name}={value_str}")

        env_text = "\n".join(lines) + ("\n" if lines else "")
        create_and_write_to_file(os.path.join(env_directory, "env"), env_text)

    @staticmethod
    def get_active_env():
        active_file_path = os.path.join(ENVIRONMENTS_DIR, "active")
        active_env = open_and_read_from_file(active_file_path)
        if not active_env:
            logger.warning(f"The file {active_file_path} is empty")
            return
        logger.info(f"Active env selected is: {active_env}")

    @staticmethod
    def set_active_env(env_name):
        active_file_path = os.path.join(ENVIRONMENTS_DIR, "active")
        w = write_to_file(active_file_path, mode="w", text=env_name)
        if not w:
            logger.error("Error setting active env")
            return
        logger.info(f"Set active env to: {env_name}")

    @staticmethod
    def add_new_env_var(**kwargs):
        active_file_path = os.path.join(ENVIRONMENTS_DIR, "active")
        active_env = open_and_read_from_file(active_file_path)
        if not active_env:
            logger.warning(f"The file {active_file_path} is empty")
            return
        active_env = active_env.strip()
        logger.info(f"Active env selected is: {active_env}")
        env_directory = os.path.join(ENVIRONMENTS_DIR, active_env)
        logger.debug(env_directory)

        # Ensure env directory exists
        make_directory(env_directory)

        env_file = os.path.join(env_directory, "env")

        # Read existing env file contents (all lines)
        existing_lines = []
        if os.path.exists(env_file):
            try:
                with open(env_file, "r") as f:
                    existing_lines = f.read().splitlines()
            except Exception:
                logger.exception(f"Failed to read env file: {env_file}")

        # Update or append key=value pairs from kwargs
        for k, v in kwargs.items():
            logger.debug(f"Setting env var: {k}={v}")
            found = False
            for i, line in enumerate(existing_lines):
                if not line:
                    continue
                # Split only on first '=' to allow '=' in the value
                parts = line.split("=", 1)
                if parts[0] == k:
                    existing_lines[i] = f"{k}={v}"
                    found = True
                    break

            if not found:
                existing_lines.append(f"{k}={v}")

        new_text = "\n".join(existing_lines) + ("\n" if existing_lines else "")
        w = write_to_file(env_file, mode="w", text=new_text)
        if not w:
            logger.error(f"Error writing updated env file: {env_file}")
        else:
            logger.info(f"Updated env file: {env_file}")
   

config = Config()
