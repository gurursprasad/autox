import click

from autox import config
from autox.deploy_infra.terraform import Terraform

TF_DIRECTORY_PATH = config.tf_directory_path


# cli root group
@click.group(name="deploy-infra", help="Deploy infra using terraform")
def deploy_group():
    """Deploy Infra"""
    pass


@click.command(name="terraform-init", help="Prepare your working directory for other commands.")
def tf_init():
    Terraform.terraform_run("init", TF_DIRECTORY_PATH)


@click.command(name="terraform-apply", help="Create or update infrastructure.")
def tf_apply():
    Terraform.terraform_run("apply", TF_DIRECTORY_PATH)


@click.command(name="terraform-destroy", help="Destroy previously-created infrastructure.")
def tf_destroy():
    Terraform.terraform_run("destroy", TF_DIRECTORY_PATH)


deploy_group.add_command(tf_init)
deploy_group.add_command(tf_apply)
deploy_group.add_command(tf_destroy)
