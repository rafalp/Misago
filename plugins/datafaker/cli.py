import random

import click
from faker import Faker
from misago.categories.get import get_all_categories
from misago.cli import cli
from misago.utils.async_context import uses_database

from .categories import create_fake_category
from .users import create_fake_user


@cli.add_command
@click.command(short_help="Creates fake categories")
@click.argument("count", default=1, type=int)
@uses_database
async def createfakecategories(count):
    if count == 1:
        click.echo("Creating fake category:")
    elif count > 1:
        click.echo(f"Creating {count} fake categories:")
    else:
        raise click.UsageError("'count' argument's value can't be negative.")

    fake = Faker()
    for _ in range(count):
        category = await create_fake_category(fake)
        click.echo(f"- {category.name}")


@cli.add_command
@click.command(short_help="Creates fake categories")
@click.argument("count", default=1, type=int)
@uses_database
async def createfakechildcategories(count):
    if count == 1:
        click.echo("Creating fake child category:")
    elif count > 1:
        click.echo(f"Creating {count} fake child categories:")
    else:
        raise click.UsageError("'count' argument's value can't be negative.")

    root_categories = [c for c in await get_all_categories() if not c.depth]

    fake = Faker()
    for _ in range(count):
        parent_category = random.choice(root_categories)
        category = await create_fake_category(fake, parent=parent_category)
        click.echo(f"- {category.name} (@{parent_category.name})")


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
