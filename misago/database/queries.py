from typing import Any, Dict, List, Mapping, Sequence, Union

from sqlalchemy import func
from sqlalchemy.sql import ClauseElement, ColumnElement, TableClause, select

from .database import database


async def insert(table: TableClause, **values: Dict[str, Any]) -> Union[str, int]:
    query = table.insert(None).values(**values)
    return await database.execute(query)


async def update(table: TableClause, row_id: Union[str, int], **values: Dict[str, Any]):
    pk = get_table_pk(table)
    query = table.update(None).values(**values).where(pk == row_id)
    await database.execute(query)


async def fetch_all(table: TableClause) -> List[Mapping]:
    return await database.fetch_all(table.select(None))


async def count(clause: ClauseElement) -> int:
    return await database.fetch_val(select([func.count()]).select_from(clause))


async def delete(table: TableClause, row_id=Any):
    pk = get_table_pk(table)
    query = table.delete(None).where(pk == row_id)
    await database.execute(query)


async def delete_many(table: TableClause, rows_ids=Sequence[Any]):
    pk = get_table_pk(table)
    query = table.delete(None).where(pk.in_(rows_ids))
    await database.execute(query)


def get_table_pk(table: TableClause) -> ColumnElement:
    if not len(table.primary_key.columns) == 1:
        raise ValueError(
            "queery shortcuts can't be used for tables with composite primary key"
        )

    return list(table.primary_key.columns)[0]
