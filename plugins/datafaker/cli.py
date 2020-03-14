import random

import click
from faker import Faker
from misago.categories.get import get_all_categories
from misago.cli import cli
from misago.threads.update import update_thread
from misago.utils.async_context import uses_database

from .categories import create_fake_category
from .history import create_fake_forum_history
from .randomrow import get_random_thread, get_random_user
from .shortcuts import get_random_poster
from .threads import create_fake_post, create_fake_thread
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
@click.command(short_help="Creates fake threads")
@click.argument("count", default=1, type=int)
@uses_database
async def createfakethreads(count):
    if count == 1:
        click.echo("Creating fake threads:")
    elif count > 1:
        click.echo(f"Creating {count} fake threads:")
    else:
        raise click.UsageError("'count' argument's value can't be negative.")

    categories = await get_all_categories()
    if not categories:
        raise click.UsageError("No categories have been found.")

    fake = Faker()
    for _ in range(count):
        category = random.choice(categories)
        starter, starter_name = await get_random_poster(fake)

        thread = await create_fake_thread(
            category, starter=starter, starter_name=starter_name,
        )
        click.echo(f"- #{thread.id} in {category.name}")


@cli.add_command
@click.command(short_help="Creates fake posts")
@click.argument("count", default=1, type=int)
@uses_database
async def createfakeposts(count):
    if count == 1:
        click.echo("Creating fake posts:")
    elif count > 1:
        click.echo(f"Creating {count} fake posts:")
    else:
        raise click.UsageError("'count' argument's value can't be negative.")

    fake = Faker()
    for _ in range(count):
        thread = await get_random_thread()
        if not thread:
            raise click.UsageError("No threads have been found in the database.")

        poster, poster_name = await get_random_poster(fake)

        post = await create_fake_post(thread, poster=poster, poster_name=poster_name)
        click.echo(f"- {post.poster_name} in thread #{thread.id}")


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


@cli.add_command
@click.command(short_help="Creates fake forum history")
@click.argument("days", default=40, type=int)
@click.argument("daily_actions", default=50, type=int)
@uses_database
async def createfakehistory(days, daily_actions):
    if days == 1:
        click.echo("Creating fake forum history for single day:")
    elif days > 1:
        click.echo(f"Creating fake forum history for {days} days:")
    else:
        raise click.UsageError("'days' argument's value can't be negative.")

    if daily_actions < 2:
        raise click.UsageError(
            "'daily_actions' argument's value can't be lower than 2."
        )

    fake = Faker()
    async for action in create_fake_forum_history(fake, days, daily_actions):
        click.echo(f"- {action}")
