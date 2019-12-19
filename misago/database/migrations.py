import os
from glob import glob
from typing import Dict, Optional

from alembic.command import heads, history, revision, upgrade
from alembic.config import Config

from .. import migrations as misago_migrations
from ..plugins import plugins
from .sqlalchemy import database_url


def make_migrations(
    package_name: str, description: str, *, initial: bool = False, empty: bool = False
):
    migrations_map = get_migrations_map()
    version_path = migrations_map[package_name]
    migration_prefix = get_migration_prefix(version_path)
    config = get_migrations_config(migrations_map, migration_prefix)

    revision(
        config,
        description,
        autogenerate=not empty,
        branch_label=package_name if initial else None,
        head="base" if initial else f"{package_name}@head",
        version_path=version_path,
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


def get_migration_prefix(package_path: str) -> str:
    glob_pattern = os.path.join(package_path, "*.py")
    python_files = len(glob(glob_pattern))
    return str(python_files).zfill(4)


def get_migrations_config(
    migrations_map: Dict[str, str], prefix: Optional[str] = None
) -> Config:
    config = Config()
    if prefix:
        config.set_main_option("file_template", f"{prefix}_%%(rev)s_%%(slug)s")
    config.set_main_option("sqlalchemy.url", database_url)
    config.set_main_option("script_location", os.path.dirname(__file__))
    config.set_main_option("version_locations", " ".join(migrations_map.values()))
    return config
