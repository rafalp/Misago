# Querying database

## Table of contents

- [Querying models](#querying-models)
- [Select](#select)
  - [Selecting single object](#selecting-single-object)
  - [Selecting some values of single object](#selecting-some-values-of-single-object)
  - [Selecting single value](#selecting-single-value)
  - [Selecting list of all results](#selecting-list-of-all-results)
  - [Selecting list of all results limited to selected columns](#selecting-list-of-all-results-limited-to-selected-columns)
  - [Selecting flat list of values of single column](#selecting-flat-list-of-values-of-single-column)
  - [Selecting list of all results in batches](#selecting-list-of-all-results-in-batches)
  - [Selecting column values in batches](#selecting-column-values-in-batches)
  - [Joins](#joins)
  - [Ordering results](#ordering-results)
  - [Limiting results](#limiting-results)
  - [Offset results](#offset-results)
  - [Making results distinct](#making-results-distinct)
  - [Using selects in subqueries](#using-selects-in-subqueries)
- [Insert](#insert)
  - [Bulk insert](#bulk-insert)
- [Update](#update)
- [Delete](#delete)
- [Lookups](#lookups)
- [Transactions](#transactions)
- [Executing raw queries](#executing-raw-queries)


## Querying models

Every model extending `misago.database.models.Model` and registered with `misago.database.models.register_model` has `query` attribute containing instance of query builder class that can be used to construct and execute queries against it's table:

```python
from misago.users.models import User


async def get_user_by_id(id: int):
    await User.query.one(id=id)
```

In addition to `query` attribute, models also have `table` attribute that can be used to construct SQL Alchemy expressions:

```python
from misago.database import database
from misago.users.models import User, UserGroup


async def run_complex_query():
    users_table = User.table
    groups_table = UserGroup.table

    query = User.table.select([users_table.c.id, users_table.c.name]).where(
        users_table.c.group_id=groups_table.select().where(groups_table.c.is_admin=True)
    )
    await database.fetch_all(query=query)
```


## Select

### Selecting single object

To retrieve single object matching query, use `one()` method:

```python
from misago.users.models import User

user = await User.query.one()
```

If query returns more than one result it will raise `misago.database.models.MultipleObjectsReturned` exception. If no results are found, `misago.database.models.DoesNotExist` will be raised.

`one()` accepts kwargs as filters:

```python
from misago.users.models import User

# Select user with id 100
user = await User.query.one(id=100)

# Select user with id 500 but only if they are admin
admin = await User.query.one(id=500, is_admin=True)
```

`one()` can also be used on queries that were already filtered with `filter` and `exclude`.


### Selecting some values of single object

To retrieve some values of single object matching query, use `one()` with names of columns passed to it:

```python
from misago.users.models import User

user_id, user_name, user_email = await User.query.one("id", "name", "email")
```

By default the result is returned as a tuple, but you can request named tuple instead by using `named=True` option:

```python
from misago.users.models import User

user = await User.query.one("id", "name", named=True)  # <Result(id=1, name="User")>
```

### Selecting single value

To retrieve single value of single object matching query, use `one_flat()` with name of column:

```python
from misago.users.models import User

user_name = await User.query.one_flat("name")
```


### Selecting list of all results

To retrieve all results matching query, use `all()` method:

```python
from misago.users.models import User

all_users = await User.query.all()
```


### Selecting list of all results limited to selected columns

To retrieve only some of columns for all results matching query, pass those columns names to `all()`:

```python
from misago.users.models import User

all_users = await User.query.all("id", "name", "email")
for id, name, email in all_users:
    ...
```

By default results are returned as a tuple, but you can request named tuple instead by using `named=True` option:

```python
from misago.users.models import User

all_users = await User.query.all("id", "name", "email", named=True)
for user in all_users:
    await do_something(user.id, user.name, user.email)
```


### Selecting flat list of values of single column

To retrieve values from single column as flat list use `all_flat()`:

```python
from misago.users.models import User

users_ids = await User.query.all_flat("id")  # [1, 3, 4, 5...]
```


### Selecting list of all results in batches

In situations when you want to walk over large number of results from the database (eg. to process them in celery task), you can slice query into smaller batches to reduce memory usage at expense of longer iteration time:

```python
from misago.threads.models import Thread

async for thread in Thread.query.batch():
    ...
```

By default objects are pulled in batches of 20. This value can be set through `step_size` option:

```python
from misago.threads.models import Thread

async for thread in Thread.query.batch(step_size=50):
    ...
```

By default objects are ordered by `id` column in descending order, so most recent objects are returned first. To change column or order use `cursor_column` and `descending` options:

```python
from misago.threads.models import Thread

# Threads will now be returned in ascending order
async for thread in Thread.query.batch(descending=False):
    ...

# Threads will now be ordered by last post id 
async for thread in Thread.query.batch(cursor_column="last_post_id"):
    ...
```

> **Note:**  `cursor_column` doesn't support joined tables.

You can also limit results to selected columns, but you need to make sure that list of columns includes cursor column. Results are then returned as named tuples:

```python
from misago.threads.models import Thread

# Threads will now be returned in ascending order
async for thread in Thread.query.batch("id", "title"):
    print(thread)  # <Result(id=1, title="Hello world!")>
```


### Selecting column values in batches

`batch_flat` does what `all_flat` does, but in batches:

```python
from misago.threads.models import Thread

# Threads will now be returned in ascending order
async for thread_title in Thread.query.batch_flat("title"):
    print(thread_title)  # "New thread"
```

> **Note:**  `batch_flat` doesn't support queries with joins.


### Joins

If model's table specifies foreign keys, you can include related objects in query results with `join_on`. Result for query with joins is list of tuples of individual objects:

```python
from misago.threads.models import Thread

for thread, starter in await Thread.query.join_on("starter_id").all():
    print(thread)  # <Thread(...)>
    print(starter)  # <User(...)> or None
```

To follow deep relations, separate join steps with dot (`.`):

```python
from misago.threads.models import Thread

for thread, starter in await Thread.query.join_on("first_post_id.poster_id").all():
    print(thread)  # <Thread(...)>
    print(starter)  # <User(...)> or None


for thread, starter, post in await Thread.query.join_on("first_post_id.poster_id", "first_post_id").all():
    print(thread)  # <Thread(...)>
    print(starter)  # <User(...)> or None
    print(post)  # <Post(...)> or None
```

To limit select only to some columns, prepend column name with join name:

```python
from misago.threads.models import Thread

for thread_id, starter_name in await Thread.query.join_on("starter_id").all("id", "starter_id.name"):
    ...
```

If you use `named=True` option, columns will be grouped by object:

```python
from misago.threads.models import Thread

for thread, starter in await Thread.query.join_on("starter_id").all("id", "starter_id.name", named=True):
    print(thread)  # <Result(id=1)>
    print(starter)  # <Result(name="Aerith")> or None
```

Tables in join queries are aliased. To retrieve aliased table for use in SQL Alchemy expression access Query's `state.join_root` attribute for main table and `state.join_tables` dict for joined tables:

```python
query = Thread.query.join_on("starter_id")
users_join = query.state.join_tables["starter_id"]
query = query.filter(users_join.c.slug == "admin")
```

For lookups spanning joins you can also use shortcut:

```python
query = Thread.query.join_on("starter_id").filter(**{"starter_id.slug": "admin"})
```

Note that lookups spanning joins may be very inefficient and are generally discouraged.


### Ordering results

To make select query ordered, call `order_by` on query with one or more column names:

```python
from misago.users.models import User

users_sorted_by_name = await User.query.order_by("name").all()
```

To reverse the order, prefix column name with minus:

```python
from misago.users.models import User

users_sorted_by_name = await User.query.order_by("-name").all()
```

To order by multiple columns, specify them one after another:

```python
from misago.threads.models import Thread

threads_sorted_by_title = await Thread.query.order_by("title", "id").all()
```


### Limiting results

To limit number of query results, call `limit` with `int` as only argument:

```python
from misago.users.models import User

five_oldest_users = await User.query.order_by("id").limit(5).all()
```

To remove limit from query, call `limit` without arguments:

```python
from misago.users.models import User

all_oldest_users = await User.query.order_by("id").limit(5).limit().all()
```

This is useful in utilities transforming queries.


### Offset results

To offset results (eg. for offset pagination), call `offset` with `int` as only argument:

```python
from misago.users.models import User

next_oldest_users = await User.query.order_by("id").offset(5).all()
```

To remove offset from query, call `offset` without arguments:

```python
from misago.users.models import User

all_oldest_users = await User.query.order_by("id").offset(5).offset().all()
```

This is useful in utilities transforming queries.


### Making results distinct

Combine `all` or `batch` with `distinct()` to make results distinct:

```python
from misago.threads.models import Thread

categories_with_threads = await Thread.query.distinct().all_flat("category_id")
```


### Using selects in subqueries

Use `subquery("column")` method to make your query work as subquery:

```python
from misago.threads.models import Thread, Post

user_posted_in_threads_ids = (
    Post.query
    .filter(poster_id=123)
    .distinct()
    .subquery("thread_id")
)
threads_with_user_posts = Thread.query.filter(id__in=user_posted_in_threads_ids)

async for thread in threads_with_user_posts.batch():
    print(thread)  # <Thread(...)>
```

If you want to convert subquery to SQL Alchemy expression, use `as_select_expression`:

```python
from misago.threads.models import Thread, Post

user_posted_in_threads_ids = (
    Post.query
    .filter(poster_id=123)
    .distinct()
    .subquery("thread_id")
    .as_select_expression()
)
threads_with_user_posts = Thread.query.filter(id=user_posted_in_threads_ids)

async for thread in threads_with_user_posts.batch():
    print(thread)  # <Thread(...)>
```


## Insert

To insert new data into database, use `insert` on unfiltered query:

```python
from misago.threads.models import Thread

new_thread = await Thread.query.insert(title="Thread title!", slug="thread-title")
```

`insert()` returns new model instance with attributes having values from `insert` arguments. This instance will also have its `id` attribute set to value returned by the database.


### Bulk insert

To bulk insert values pass list of dicts to `insert_bulk`:

```python
from misago.threads.models import Thread

Thread.query.insert_bulk(
    [
        {"title": "Thread A", "slug": "thread-a"},
        {"title": "Thread B", "slug": "thread-b"},
        {"title": "Thread C", "slug": "thread-c"},
    ]
)
```

`insert_bulk()` has no return value.


## Update

To update all objects run `update_all` on unfiltered query:

```python
from misago.threads.models import Thread

await Thread.query.update_all(is_closed=False)
```

To update only some objects in database run `update`:

```python
from misago.threads.models import Thread

await Thread.query.filter(id=2137).update(is_closed=False)
```

Both `update_all` and `update` take values to save to database as kwargs. Those values can be basic Python values (like `int` or `str`) or SQL Alchemy expressions:

```python
from misago.threads.models import Thread

await Thread.query.filter(id=2137).update(replies=Thread.table.c.replies + 1)
```


## Delete

To delete all objects run `delete_all` on unfiltered query:

```python
from misago.threads.models import Thread

await Thread.query.delete_all()
```

To delete only some objects in database run `delete`:

```python
from misago.threads.models import Thread

await Thread.query.filter(id=2137).delete()
```


## Lookups

Lookups are arguments passed to `filter()` and `exclude()` methods to set `WHERE` clause on final query.

`filter` limits results only to those that match specified lookups while `exclude` limits results to those that DON'T match specified lookups:

```python
from misago.users.models import User

# All admins
all_admins = await User.query.filter(is_admin=True).all()

# All non-admins
all_non_admins = await User.query.exclude(is_admin=True).all()
```

Multiple lookups can be passed to function at same time:

```python
from misago.users.models import User

# All admins that aren't moderators
all_admins = await User.query.filter(is_admin=True, is_mod=False).all()
```

Both `filter()` andd `exclude()` can be combined within single query:

```python
from misago.users.models import User

# All admins that aren't moderators
all_admins = await User.query.filter(is_admin=True).exclude(is_mod=True).all()
```


### Equals

`column=value` will produce `col = val` SQL expression for `filter` and `cal = val OR col is None` for exclude.

If value is `None`, `IS NULL` and `NOT IS NULL` expression will be produced instead.

If value is an SQL Alchemy expression, `IN ()` expression with subquery will be created instead.


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
from misago.database import database

# Run query
await database.execute(
    query="UPDATE misago_settings SET value = 'Test Forum ' WHERE name = 'forum_name'"
)

# Run select
cache_versions = await database.fetch_all(query="SELECT * FROM misago_cache_versions")
```

See "databases" library [documentation](https://www.encode.io/databases/database_queries/) for more examples.
