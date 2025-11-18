import click

# @click.command()
# @click.option("--help", is_flag=True, help="Show this message and exit.")
# @click.argument('name')
# def cli(count, name):
#     pass

@click.command()
def cli():
    """Prints a greeting."""
    click.echo("Hello, World!")