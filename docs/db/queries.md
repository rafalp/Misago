# Querying database

## Table of contents

- [Transactions](#transactions)
- [Executing raw queries](#executing-raw-queries)


## Transactions

To run database queries within transaction use `database.transaction` asynchronous context manager:

```python
from misago.database import database

async with database.transaction():
    post = await Post.create(thread_id=thread.id, content="Hello world!")
    await thread.update(last_post_id=post.id)
```

You can also use it as decorator:

```python
from misago.database import database


@database.transaction()
async def create_post(thread: Thread, content: str):
    post = await Post.create(thread_id=thread.id, content=content)
    await thread.update(last_post_id=post.id)
    return post
```

If you need manual control on commit or rollback, use `transaction()` return value:

```python
transaction = await database.transaction()
try:
    ...
except:
    await transaction.rollback()
else:
    await transaction.commit()
```

For more examples see ["databases" documentation](https://www.encode.io/databases/connections_and_transactions/#transactions).


## Executing raw queries

To run raw query against the database, use `database` instance from `misago.database`:

```python
# Run query
await database.execute(
    query="UPDATE misago_settings SET value = 'Test Forum ' WHERE name = 'forum_name'"
)

# Run select
cache_versions = await database.fetch_all(query="SELECT * FROM misago_cache_versions")
```

See "databases" library [documentation](https://www.encode.io/databases/database_queries/) for more examples.
