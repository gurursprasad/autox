from enum import Enum
from pathlib import Path
import click
from dotenv import dotenv_values, load_dotenv

# Set autox root and environments directory paths
AUTOX_ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENTS_DIR = Path(AUTOX_ROOT, "environments")


class ConfigMap(Enum):
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
