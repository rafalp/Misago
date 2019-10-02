import click

from .database.migrations import MigrationError, make_migrations, run_migrations


@click.group()
def cli():
    pass


@cli.add_command
@click.command()
@click.argument("module")
@click.argument("message")
def makemigrations(module: str, message: str):
    try:
        make_migrations(module, message, data_migration=True, dry_run=True)
    except MigrationError as e:
        click.echo(click.style(str(e), fg="red"))


@cli.add_command
@click.command()
def migrate():
    run_migrations()
