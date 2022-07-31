from dataclasses import replace
from typing import Any, ClassVar, Dict, Type

from sqlalchemy.sql import TableClause

from .exceptions import DoesNotExist, MultipleObjectsReturned
from .query import RootQuery


class Model:
    DoesNotExist: ClassVar[Type[DoesNotExist]]
    MultipleObjectsReturned: ClassVar[Type[MultipleObjectsReturned]]

    id: int

    query: ClassVar[RootQuery]
    table: ClassVar[TableClause]

    def diff(self, **kwargs) -> dict:
        changes: Dict[str, Any] = {}
        for key, value in kwargs.items():
            if value is not None and getattr(self, key) != value:
                changes[key] = value
        return changes

    def replace(self, **kwargs):
        return replace(self, **kwargs)

    def fetch_from_db(self):
        return self.query.one(id=self.id)
