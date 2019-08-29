import os
import time
from importlib import import_module

from alembic.command import revision, upgrade
from alembic.config import Config


class MigrationError(Exception):
    pass


def make_migrations(module_name: str, *, data_migration: bool, dry_run: bool):
    try:
        import_module(module_name)
        import_module(f"{module_name}.tables")
        migrations = import_module(f"{module_name}.migrations")

        if not os.path.dirname(migrations.__file__).endswith("migrations"):
            raise MigrationError(f"'{module_name}.migrations' is not a package")
    except ImportError as e:
        raise MigrationError(f"can't make migrations for '{module}': {e}")

    config = Config()
    config.set_main_option("sqlalchemy.url", "postgres://misago:misago@postgres/misago")
    config.set_main_option("script_location", os.path.dirname(__file__))
    config.set_main_option("version_locations", os.path.dirname(migrations.__file__))
    revision(config, "test message", autogenerate=True, branch_label=module_name)


def run_migrations(*_, dry_run: bool):
    migrations = import_module(f"misago.migrations")

    config = Config()
    config.set_main_option("sqlalchemy.url", "postgres://misago:misago@postgres/misago")
    config.set_main_option("script_location", os.path.dirname(__file__))
    config.set_main_option("version_locations", os.path.dirname(migrations.__file__))

    upgrade(config, "heads")
