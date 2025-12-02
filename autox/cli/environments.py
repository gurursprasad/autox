import click

from autox.config import EnvVars


# cli root group
@click.group(name="env-management", help="crud operations for env management")
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


@click.command(name="get-active-env", help="Prints the active environment.")
def check_active_env():
    EnvVars.get_active_env()


@click.command(name="set-active-env", help="Sets the specified env to active.")
@click.option("--env", default=None, help="Env name to be set.")
def set_active(env):
    EnvVars.set_active_env(env)


@click.command(name="add-env-var", help="Add a new env in this format: {key=value}.")
@click.argument("env_var", required=True)
def add_env_var(env_var):
    """Add an environment variable for the active env.

    The argument must be in the literal form: `{KEY=VALUE}` (including the
    surrounding braces). The key and value are trimmed of surrounding
    whitespace. The parsed pair is forwarded to `EnvVars.add_new_env_var`.
    """
    s = env_var.strip()
    if not (s.startswith("{") and s.endswith("}")):
        raise click.BadParameter("env_var must be in format {KEY=VALUE}")

    inner = s[1:-1].strip()
    if "=" not in inner:
        raise click.BadParameter("env_var must contain '=' separator")

    key, value = inner.split("=", 1)
    key = key.strip()
    value = value.strip()

    if not key:
        raise click.BadParameter("env_var key cannot be empty")

    # Forward as keyword args so the config handler receives named values
    EnvVars.add_new_env_var(**{key: value})


env_group.add_command(create_new_env)
env_group.add_command(check_active_env)
env_group.add_command(set_active)
env_group.add_command(add_env_var)
