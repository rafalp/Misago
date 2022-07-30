# Using database

## Database access layer (DBAL)

Misago uses [encode/databases](https://github.com/encode/databases) as DBAL with [asyncpg](https://magicstack.github.io/asyncpg/current/) as PostgreSQL database driver.

Database connection is importable as `from misago.database import database`.


## Imperative ORM

Misago uses custom light-weight imperative ORM that abstracts away [SQL Alchemy's expressions](https://docs.sqlalchemy.org/en/20/).

This ORM knows about [SQL Alchemy's tables](https://docs.sqlalchemy.org/en/20/core/metadata.html) and knows what Python types (mostly dataclasses but also plain dicts for simple M2M tables) to use to represent those tables rows.

Misago database structure is located in [`misago.tables`](../misago/tables.py) module.


## Migrations

[Alembic](https://alembic.sqlalchemy.org/en/latest/) is used for database migrations with [pyscopg2](https://www.psycopg.org/docs/) as backend.

> **Note for Django devs**: Unlike Django which generates Migrations by diffing models with existing migrations, Alembic diffs tables to state of database running latest migrations instead.
>
> All existing migrations need to be applied on database before new migration may be generated.

