import click


@click.group()
def cli():
    pass


@cli.add_command
@click.command()
@click.argument("module")
@click.argument("message")
def makemigrations(module: str, message: str):
    from .db.migrations import MigrationError, make_migrations

    try:
        make_migrations(module, message, data_migration=True, dry_run=True)
    except MigrationError as e:
        click.echo(click.style(str(e), fg="red"))


@cli.add_command
@click.command()
def migrate():
    from .db.migrations import run_migrations

    run_migrations(dry_run=True)
