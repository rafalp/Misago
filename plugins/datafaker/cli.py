import click
from faker import Faker
from misago.cli import cli
from misago.utils.async_context import uses_database

from .users import create_fake_user


@cli.add_command
@click.command(short_help="Creates fake users accounts")
@click.argument("count", default=1, type=int)
@uses_database
async def createfakeusers(count):
    if count == 1:
        click.echo("Creating fake user:")
    elif count > 1:
        click.echo(f"Creating {count} fake users:")
    else:
        raise click.UsageError("'count' argument's value can't be negative.")

    fake = Faker()
    for _ in range(count):
        user = await create_fake_user(fake)
        click.echo(f"- {user.name} <{user.email}>")
