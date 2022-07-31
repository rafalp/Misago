# Database migrations

Misago uses [Alembic](https://alembic.sqlalchemy.org/en/latest/) database migrations with [pyscopg2](https://www.psycopg.org/docs/) as backend.

Unlike Django which generates migrations by diffing models with existing migrations, Alembic compares table definitions with state of database running latest migrations instead.

All existing migrations need to be applied on database before new migration may be generated.


## Schema migrations

To create migrations for your plugin, first make sure it has `migrations` directory containing empty `__init__.py` file.

Next, run `makemigrations PLUGIN migration_description` command from command line:

```shell
python manage.py makemigrations pluginname add_users_table
```

New migration file should appear in `migrations` directory belonging to your plugin.

To create new migration for Misago itself use `misago` as name:

```shell
python manage.py makemigrations misago add_reports_table
```


## Data migrations

To generate data migration run `makemigrations` with `--empty`:

```shell
python manage.py makemigrations pluginname default_user_groups --empty
```

This will create empty migration for you to add data migration logic to:

```python
from alembic import op

# revision identifiers, used by Alembic.
revision = "9c2392303260"
down_revision = "02a349a35f04"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
```

To run queries use `op` module imported from alembic:

```python
from alembic import op

# revision identifiers, used by Alembic.
revision = "9c2392303260"
down_revision = "02a349a35f04"
branch_labels = None
depends_on = None


def upgrade():
    groups = op.execute(
        "INSERT INTO my_table (message, url) VALUES ('Hello!', 'http://test.com');"
    )


def downgrade():
    pass
```

Alembic doesn't create table snapshots for its migrations like how Django does it, but you can still create them yourself to make database operations easier:

```python
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String

# revision identifiers, used by Alembic.
revision = "9c2392303260"
down_revision = "02a349a35f04"
branch_labels = None
depends_on = None


tmp_table = table(
    "user_ranks",
    sa.column("name", String),
    sa.column("posts", Integer),
)

ranks = [
    {"name": "New member", "posts": 0},
    {"name": "Senior member", "posts": 200},
    {"name": "Veteran member", "posts": 5000},
]


def upgrade():
    op.bulk_insert(tmp_table, ranks)


def downgrade():
    pass
```

Alembic documentation has a [reference on available migration operations](https://alembic.sqlalchemy.org/en/latest/ops.html).


## Running migrations

To run migrations, use `migrate` command from Misago's command line interface:

```shell
python manage.py migrate
```
