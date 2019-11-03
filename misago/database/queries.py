from typing import Any, Dict, List, Mapping, Union

from .database import database


async def insert(table, **values: Dict[str, Any]) -> Union[str, int]:
    query = table.insert(None).values(**values)
    return await database.execute(query)


async def fetch_all(table) -> List[Mapping]:
    return await database.fetch_all(table.select(None))
