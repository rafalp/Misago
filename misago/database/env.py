from alembic import context
from sqlalchemy import engine_from_config, pool

from misago.tables import metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
