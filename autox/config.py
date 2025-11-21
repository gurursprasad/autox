import os
from enum import Enum
from pathlib import Path

import pydantic

# Set autox root and environments directory paths
AUTOX_ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENTS_DIR = Path(AUTOX_ROOT, "environments")


class ConfigMap(Enum):
    log_level = "LOG_LEVEL"
    app_url = "APP_URL"
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

        return pydantic.Field(default_factory=default_factory)

    def can_be_saved(self):
        return not hasattr(self, "do_not_save")


# class Config:
