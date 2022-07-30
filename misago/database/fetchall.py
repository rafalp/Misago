from typing import List

from sqlalchemy.sql import ClauseElement

from .database import database
from .models import record_dict


async def fetch_all_assoc(
    query: ClauseElement | str, values: dict = None
) -> List[dict]:
    return [record_dict(record) for record in await database.fetch_all(query, values)]
