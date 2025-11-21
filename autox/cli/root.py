import click

from autox import __version__, config
from autox.autox_logger import logger
from autox.cli.run_tests import run_api_tests, run_ui_tests


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="autox")
@click.option("--help", is_flag=True, help="Show this message and exit.")
@click.option(
    "--log-level",
    type=click.Choice(["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False),
    help="Set the logging level for the autox CLI and pytest.",
)
@click.pass_context
def cli(ctx, help, log_level):
    """
    autox CLI - A command-line tool for managing tasks. \n

    # TO DO: THESE OPTIONS ARE STILL WORK IN PROGRESS. \n

    autox CLI Provides the following [OPTIONS]:

    - deploy: Deploy the test-application \n
    - switch: Switch to a different configuration \n
    - list: List available configurations \n
    - run: Run the test-application \n

    Use 'autox COMMAND --help' for detailed information on each command. \n
    """

    # The config will always start set to INFO based on the default in the logger setup
    # If the CLI differs, we should update the config and set the log level and handlers
    if log_level:
        if config.log_level != log_level:
            config.log_level = log_level
            logger.setLevel(config.log_level)
            for handler in logger.handlers:
                handler.setLevel(config.log_level)
            logger.info(f"Log level updated to {config.log_level}.")

    if ctx.invoked_subcommand is None:
        if help:
            click.echo(cli.get_help(ctx))
        else:
            click.echo("Use 'autox --help' for usage details.")


cli.add_command(run_ui_tests)
cli.add_command(run_api_tests)
