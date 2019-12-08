from typing import Any, Dict, List, Mapping, Union

from sqlalchemy.sql import TableClause

from .database import database


async def insert(table: TableClause, **values: Dict[str, Any]) -> Union[str, int]:
    query = table.insert(None).values(**values)
    return await database.execute(query)


async def fetch_all(table: TableClause) -> List[Mapping]:
    return await database.fetch_all(table.select(None))


async def delete(table: TableClause, row_id=Any):
    if not len(table.primary_key.columns) == 1:
        raise ValueError(
            "'delete' shortcut can't be used for tables with composite primary key"
        )

    pk = list(table.primary_key.columns)[0]
    query = table.delete(None).where(pk == row_id)
    await database.execute(query)
