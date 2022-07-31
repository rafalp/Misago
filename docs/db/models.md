# Defining models

After defining new database table in `tables` module in your plugin or Misago itself you may want to create a model for it. Doing so has three main advantages:

- It provides typings for query results.
- It provides a place for implementing model-specific logic, like create/update/delete operations.
- It makes it easier to query underlying database table.


## Basic model

Misago provides `Model` base class that implements minimal contract for models:

- `id: int` attribute
- `DoesNotExist` and `MultipleObjectsReturned` exceptions specific to this model
- `table` and `query` class attributes
- `replace` class method for `dataclasses.replace(model, **attrs)` in case of models being dataclasses
- `fetch_from_db` instance method that queries database and returns update model.
- `diff` instance method thats useful in updates.

For sake of this guide we will implement "report" model representing record from "reports" table.

Start with defining custom class extending `Model`:

```python
from datetime import datetime

from misago.database.models import Model


class Report(Model):
    message: str
    url: str
    created_at: datetime
    is_closed: bool
```

Now you need to let Misago know about this model's existence, and that it should be used to represent results from your `reports` table. To do this, import both your table (created using SQL Alchemy's `Table`) and `register_model` decorator from `misago.databases.table`:

```python
from datetime import datetime

from misago.database.models import Model, register_model
from myplugin.tables import reports


@register_model(reports)
class Report(Model):
    message: str
    url: str
    created_at: datetime
    is_closed: bool
```

Misago will now know about this model and will use it to represent query results from `reports` table.

It will also populate model's `table`, `query`, `DoesNotExist` and `MultipleObjectsReturned` class attributes.

By default model's name will be same as `Report.__name__`, but we can override this passing name as second argument to `@register_model`:

```python
from datetime import datetime

from misago.database.models import Model, register_model
from myplugin.tables import reports


@register_model(reports, "Report")
class ReportModel(Model):
    message: str
    url: str
    created_at: datetime
    is_closed: bool
```


## Model initialization

`Report` model is missing `__init__` method that Misago will call with kwargs representing model's database columns. We could define this method ourself:

```python
from datetime import datetime

from misago.database.models import Model, register_model
from myplugin.tables import reports


@register_model(reports)
class Report(Model):
    message: str
    url: str
    created_at: datetime
    is_closed: bool

    def __init__(
        self,
        id: int,
        message: str,
        url: str,
        created_at: datetime,
        is_closed: bool,
    ):
        self.id = id
        self.message = message
        self.url = url
        self.created_at = created_at
        self.is_closed = is_closed
```

However Python has better solution for this problem in form of dataclasses:

```python
from dataclasses import dataclass
from datetime import datetime

from misago.database.models import Model, register_model
from myplugin.tables import reports


@register_model(reports)
@dataclass
class Report(Model):
    message: str
    url: str
    created_at: datetime
    updated_at: datetime
    is_closed: bool
```

Now we can create instances of our model like this:

```python
from misago.utils import timezone

from .models import Report

r = Report(
    id=1,
    message="Bad user!",
    url="http://misago-project.org/t/bad-thread-2137",
    created_at=timezone.now(),
    updated_at=timezone.now(),
    is_closed=False,
)
```

Turning our model into dataclass solves one of requirements it has to meet: a way for ORM to convert database record into custom model instance. Pseudocode for this process looks like this:

```python
from misago.database import database


async def select_reports_from_db():
    records = await database.fetch_all("SELECT * FROM reports")
    return [Report(**record_dict) for record_dict in records]
```


## Creating new instances in database

Misago ORM has no opinion on how models should be created in database. You can create factory function that takes arguments, does database insert through `database.execute` and returns `Report` instance. In fact this is pattern that Misago core uses, defining `create` classmethod on models.

Lets define our own `create` method on `Report` model:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from misago.database.models import Model, register_model
from misago.utils import timezone

from myplugin.tables import reports


@register_model(reports)
@dataclass
class Report(Model):
    message: str
    url: str
    created_at: datetime
    updated_at: datetime
    is_closed: bool

    @classmethod
    async def create(
        cls,
        message: str,
        url: str,
        created_at: Optional[datetime],
        updated_at: Optional[datetime],
        is_closed: bool = False,
    ) -> "Report":
        now = timezone.now()

        return await cls.query.insert(
            message=message,
            url=url,
            created_at=created_at or now,
            updated_at=updated_at or created_at or now,
            is_closed=is_closed,
        )
```

We can now insert new instance of `Report` to database like this:

```python
async def example_function():
    r = await Report.create(
        message="Bad user!",
        url="http://misago-project.org/t/bad-thread-2137",
    )

    r.id  # Report's ID has been populated from database!

    report_from_db = await Report.query.one(id=r.id)
    assert report_from_db == r  # Report was saved to database successfully
```


## Updating instance

To update model in the database, you can run update query:

```python
async def update_report(r: Report):
    await Report.query.filter(id=r.id).update(
        message="New message value"
    )
```

But we would like to be able to update `Report` instances we are working with in the code. To achieve that we can define `update` method that will take fields to update, compare their values against current ones and update the model in database and return updated instance:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from misago.database.models import Model, register_model
from misago.utils import timezone

from myplugin.tables import reports


@register_model(reports)
@dataclass
class Report(Model):
    message: str
    url: str
    created_at: datetime
    updated_at: datetime
    is_closed: bool

    @classmethod
    async def create(
        cls,
        message: str,
        url: str,
        created_at: Optional[datetime],
        updated_at: Optional[datetime],
        is_closed: bool = False,
    ) -> "Report":
        now = timezone.now()

        return await cls.query.insert(
            message=message,
            url=url,
            created_at=created_at or now,
            updated_at=updated_at or created_at or now,
            is_closed=is_closed,
        )

    async def update(
        self,
        *,
        message: Optional[str] = None,
        url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_closed: Optional[bool] = None,
    ) -> "Report":
        # Compare new values to current state
        changes: Dict[str, Any] = self.diff(
            message=message,
            url=url,
            created_at=created_at,
            updated_at=updated_at,
            is_closed=is_closed,
        )

        if not changes:
            return self  # No changes to make in database
        
        # Manually update `updated_at` value
        if "updated_at" not in changes:
            changes["updated_at"] = timezone.now()

        await self.query.filter(id=self.id).update(**changes)
        return self.replace(**changes)
```

Now if we update our model, only values that really changed will be saved to database, and instead of mutating our instance we will get completely new one. We are avoiding unexpected side effects from state mutability or overwriting fields that are already updated by other users:

```python
async def update_report(r: Report):
    updated_report = await Report.update(
        message="New message value"
    )
```

`self.diff` is little handy utility that compares it's kwargs against attributes on model and returns dict with difference. This reduces amount of boilerplace. It also skips attributes where new value wouldd be `None`.

> **Note:** we could instead implement method alike to Django's save() that just collects current values from instance into a dict runs update to database, but I've found that `update` approach creates less race conditions in app and makes you more conscious about state mutations.


### `None` and nullable fields

What if our model has nullable field? For example `user_id` foreign key that holds ID of user associated with given report. If our update looked like below example, it would remove the relation even if it was called without `user_id` value:

```python
async def update(
    self,
    *,
    message: Optional[str] = None,
    user_id: Optional[int] = None,
):
    changes: Dict[str, Any] = self.diff(
        message=message,
        user_id=user_id,
    )

    if not changes:
        return self  # No changes to make in database

    await self.query.filter(id=self.id).update(**changes)
    return self.replace(**changes)


await my_model.update(message="New message")  # Wooops!
```

To prevent this situation from happening, `self.diff` explicitly skips `None` values, making it up to developer to handle situation.

One solution to this problem is introducing argument to update dedicated to cleaning relation:

```python
async def update(
    self,
    *,
    message: Optional[str] = None,
    user_id: Optional[int] = None,
    clear_user_id: Optional[bool] = False,
):
    if clear_user_id and user_id is not None:
        raise ValueError("'clear_user_id' and 'user_id' can't be combined!")

    changes: Dict[str, Any] = self.diff(
        message=message,
        user_id=user_id,
    )

    if clear_user_id and self.user_id:
        changes["user_id"] = None  # Explicit unset user_id

    if not changes:
        return self  # No changes to make in database

    await self.query.filter(id=self.id).update(**changes)
    return self.replace(**changes)
```


### Increments


## Deleting instance

We can delete our model from database using delete query:

```python
await Report.query.filter(id=r.id).delete()
```

But for convenience `Report` could define `delete` method:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from misago.database.models import Model, register_model
from misago.utils import timezone

from myplugin.tables import reports


@register_model(reports)
@dataclass
class Report(Model):
    message: str
    url: str
    created_at: datetime
    updated_at: datetime
    is_closed: bool

    @classmethod
    async def create(
        cls,
        message: str,
        url: str,
        created_at: Optional[datetime],
        updated_at: Optional[datetime],
        is_closed: bool = False,
    ) -> "Report":
        now = timezone.now()

        return await cls.query.insert(
            message=message,
            url=url,
            created_at=created_at or now,
            updated_at=updated_at or created_at or now,
            is_closed=is_closed,
        )

    async def update(
        self,
        *,
        message: Optional[str] = None,
        url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_closed: Optional[bool] = None,
    ) -> "Report":
        # Compare new values to current state
        changes: Dict[str, Any] = self.diff(
            message=message,
            url=url,
            created_at=created_at,
            updated_at=updated_at,
            is_closed=is_closed,
        )

        if not changes:
            return self  # No changes to make in database
        
        # Manually update `updated_at` value
        if "updated_at" not in changes:
            changes["updated_at"] = timezone.now()

        await self.query.filter(id=self.id).update(**changes)
        return self.replace(**changes)

    async def delete(self):
        await self.query.filter(id=self.id).delete()
```


# Handling relations


## Registry

Misago maintains registry of models, tables and queries, importable as `mapper_registry` from `misago.database.models`.

This registry can be used to retrieve tables, queries and models:

```python
from misago.database.models import mapper_registry

# Get model by name
Report = mapper_registry.models["Report"]

# Get model for table
Report = mapper_registry.mappings["reports"]

# Get table by name
reports = mapper_registry.tables["reports"]
```


## Message from creator

You've likely noticed that Misago's ORM is relatively minimal in amount of features it provides out of box.

This is by design. Misago's ORM was created as a stop gap solution to a problem of SQL Alchemy's expressions being too verbose for use en masse and no mature async ORM being available yet in Python.

The truth to how web apps like Misago use database is that 99% of its queries are simple selects, updates, inserts and deletes with basic where clauses where records are filtered by one or few columns.

So I've decided to create simple ORM that addresses those 99% of cases and lets me fall-back to raw queries or SQL Alchemy expressions for remaining 1% so I can be merry on my mission to implement internet forum software and not universal async ORM for Python alike to SQL Alchemy or Django.

Once async ORMs mature, I will be happy to re-investigate them and set on work to move Misago from custom solution to one of those. But as of mid 2022 we are still not there yet.
