from dataclasses import replace
from typing import ClassVar

from sqlalchemy.sql import TableClause

from .query import RootQuery


class Model:
    id: int

    query: ClassVar[RootQuery]
    table: ClassVar[TableClause]

    def replace(self, **kwargs):
        return replace(self, **kwargs)

    def fetch_from_db(self):
        return self.query.one(id=self.id)
