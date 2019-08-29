import click


@click.group()
def cli():
    pass


@cli.add_command
@click.command()
def makemigrations():
    from .db.migrations import MigrationError, make_migrations

    try:
        make_migrations("misago", data_migration=True, dry_run=True)
    except MigrationError as e:
        click.echo(click.style(str(e), fg="red"))


@cli.add_command
@click.command()
def migrate():
    from .db.migrations import run_migrations

    run_migrations(dry_run=True)
