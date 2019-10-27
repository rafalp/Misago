from typing import Any, Dict, Union

from .database import database


async def insert(table, **values: Dict[str, Any]) -> Union[str, int]:
    query = table.insert(None).values(**values)
    return await database.execute(query)
