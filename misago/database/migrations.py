import os
from typing import Dict

from alembic.command import heads, history, revision, upgrade
from alembic.config import Config

from .. import migrations as misago_migrations
from ..plugins import plugins
from .sqlalchemy import database_url


def make_migrations(
    package_name: str, description: str, *, initial: bool = False, empty: bool = False
):
    migrations_map = get_migrations_map()
    config = get_migrations_config(migrations_map)

    revision(
        config,
        description,
        autogenerate=not empty,
        branch_label=package_name if initial else None,
        head="base" if initial else f"{package_name}@head",
        version_path=migrations_map[package_name],
    )


def run_migrations():
    migrations_map = get_migrations_map()
    config = get_migrations_config(migrations_map)

    upgrade(config, "heads")
    heads(config, verbose=True)


def show_migrations_history():
    migrations_map = get_migrations_map()
    config = get_migrations_config(migrations_map)
    history(config, indicate_current=True, verbose=True)


def get_migrations_map() -> Dict[str, str]:
    migrations = [("misago", misago_migrations)]
    migrations += plugins.import_modules_if_exists("migrations")
    return {k: os.path.dirname(v.__file__) for k, v in migrations}


def get_migrations_config(migrations_map: Dict[str, str]) -> Config:
    config = Config()
    config.set_main_option("sqlalchemy.url", database_url)
    config.set_main_option("script_location", os.path.dirname(__file__))
    config.set_main_option("version_locations", " ".join(migrations_map.values()))
    return config
