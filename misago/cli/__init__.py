import click
from alembic.util import CommandError

from ..cacheversions import invalidate_all_caches
from ..database.migrations import (
    make_migrations,
    run_migrations,
    show_migrations_history,
)
from ..utils.async_context import uses_database


@click.group()
def cli():
    pass


def alembic_command(f):
    def decorated_alembic_command(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except CommandError as e:
            click.echo(e, err=True)

    decorated_alembic_command.__name__ = f.__name__
    return decorated_alembic_command


@cli.add_command
@click.command(short_help="Invalidates all caches on the server.")
@uses_database
async def invalidatecaches():
    click.echo("Invalidated caches:")
    for cache in await invalidate_all_caches():
        click.echo(f"- {cache}")


@cli.add_command
@click.command(short_help="Creates an initial database migration for the package.")
@click.argument("package")
@click.argument("description")
@click.option(
    "--empty",
    help="Force generated migration script to be empty.",
    is_flag=True,
    flag_value=True,
)
@alembic_command
def initmigrations(package: str, description: str, empty: bool = False):
    make_migrations(package, description, initial=True, empty=empty)


@cli.add_command
@click.command(short_help="Creates new database migration for the package.")
@click.argument("package")
@click.argument("description")
@click.option(
    "--empty",
    help="Force generated migration script to be empty.",
    is_flag=True,
    flag_value=True,
)
@alembic_command
def makemigrations(package: str, description: str, empty: bool = False):
    make_migrations(package, description, empty=empty)


@cli.add_command
@click.command(short_help="Runs all database migrations.")
@alembic_command
def migrate():
    run_migrations()


@cli.add_command
@click.command(short_help="Shows database migrations history.")
@alembic_command
def migrationshistory():
    show_migrations_history()
