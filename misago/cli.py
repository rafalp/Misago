import click

from .database.migrations import (
    make_migrations,
    run_migrations,
    show_migrations_history,
)


@click.group()
def cli():
    pass


@cli.add_command
@click.command()
@click.argument("module")
@click.argument("description")
@click.option("--empty", is_flag=True, flag_value=True)
def initmigrations(module: str, description: str, empty: bool = False):
    make_migrations(module, description, initial=True, empty=empty)


@cli.add_command
@click.command()
@click.argument("module")
@click.argument("description")
@click.option("--empty", is_flag=True, flag_value=True)
def makemigrations(module: str, description: str, empty: bool = False):
    make_migrations(module, description, empty=empty)


@cli.add_command
@click.command()
def migrate():
    run_migrations()


@cli.add_command
@click.command()
def migrationshistory():
    show_migrations_history()


# TODO:
# - get migrations status
