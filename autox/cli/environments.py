import click

from autox.autox_logger import logger
from autox.config import EnvVars
from autox.utilities.common_utils import execute_command_realtime


# cli root group
@click.group(name="env", help="crud operations for env management")
def env_group():
    """Manage Env."""
    pass


@click.command(name="create-new-env", help="Creates a new environment and sets it to active.")
# Accept an optional positional argument and an optional --env-name option.
# If both are provided, --env-name takes precedence.
@click.argument("positional_env_name", required=False)
@click.option("--env-name", "opt_env_name", default=None, help="Env name to be created.")
def create_new_env(positional_env_name=None, opt_env_name=None):
    """Create a new environment.

    Usage:
        - `autox env create-new-env` -> creates an env with a generated name
        - `autox env create-new-env gp1` -> creates an env named `gp1`
        - `autox env create-new-env --env-name gp1` -> same as above (option takes precedence)
    """
    env_name = opt_env_name or positional_env_name
    EnvVars.create_env(env_name)


@click.command(name="get-active-env", help="Prints the active environment")
def check_active_env():
    EnvVars.get_active_env()


env_group.add_command(create_new_env)
env_group.add_command(check_active_env)
