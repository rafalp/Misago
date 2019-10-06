import click

from .database.migrations import make_migrations, run_migrations


@click.group()
def cli():
    pass


@cli.add_command
@click.command()
@click.argument("module")
@click.argument("description")
def makemigrations(module: str, description: str):
    make_migrations(module, description)


@cli.add_command
@click.command()
def migrate():
    run_migrations()
