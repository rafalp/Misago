import os
import time
from importlib import import_module
from typing import Dict

from alembic.command import revision, upgrade
from alembic.config import Config

from .. import migrations as misago_migrations
from ..plugins import plugins


class MigrationError(Exception):
    pass


def make_migrations(
    module_name: str, message: str, *, data_migration: bool, dry_run: bool
):
    migrations_map = get_migrations_map()
    print(migrations_map)

    config = Config()
    config.set_main_option("sqlalchemy.url", "postgres://misago:misago@postgres/misago")
    config.set_main_option("script_location", os.path.dirname(__file__))
    config.set_main_option("version_locations", " ".join(migrations_map.values()))

    revision(
        config,
        message,
        autogenerate=True,
        branch_label=module_name,
        version_path=migrations_map[module_name],
    )


def run_migrations(*_, dry_run: bool):
    migrations = import_module(f"misago.migrations")

    config = Config()
    config.set_main_option("sqlalchemy.url", "postgres://misago:misago@postgres/misago")
    config.set_main_option("script_location", os.path.dirname(__file__))
    config.set_main_option("version_locations", os.path.dirname(migrations.__file__))

    upgrade(config, "heads")


def get_migrations_map() -> Dict[str, str]:
    migrations = [("misago", misago_migrations)]
    migrations += plugins.import_modules_if_exists("migrations")
    return {k: os.path.dirname(v.__file__) for k, v in migrations}
