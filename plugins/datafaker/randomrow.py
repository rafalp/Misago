import random
from typing import Any, Mapping, Optional

from misago.database import database
from misago.tables import threads, users
from misago.types import Thread, User
from sqlalchemy import select, func
from sqlalchemy.sql import TableClause


async def get_random_thread() -> Optional[Thread]:
    row = await get_random_table_row(threads)
    if row:
        return Thread(**row)

    return None


async def get_random_user() -> Optional[User]:
    row = await get_random_table_row(users)
    if row:
        return User(**row)

    return None


async def get_random_table_row(table: TableClause) -> Optional[Mapping[Any, Any]]:
    rows_count = await database.fetch_val(select([func.count()]).select_from(table))

    if not rows_count:
        return None

    query = table.select(None).offset(random.randint(0, rows_count - 1)).limit(1)
    return await database.fetch_one(query)
