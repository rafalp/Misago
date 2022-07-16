# WIP: Experimental rewrite for object mapper
from dataclasses import dataclass
from typing import Dict, List, Optional, Type, Union

from sqlalchemy.sql import TableClause


class ObjectMapper:
    tables: Dict[str, TableClause]
    mappings: Dict[str, Union[Type, dict]]

    def __init__(self):
        self.tables = {}
        self.mappings = {}

    def set_mapping(self, table: TableClause, repr: Union[Type, dict]):
        self.tables[table.name] = table
        self.mappings[table.name] = repr

    def query_table(self, table: TableClause) -> "ObjectMapperQuery":
        state = ObjectMapperQueryState(table)
        return ObjectMapperQuery(self, state)


@dataclass
class ObjectMapperQueryState:
    table: TableClause
    join: Optional[List[str]]
    limit: Optional[None]


class ObjectMapperQuery:
    orm: ObjectMapper
    state: ObjectMapperQueryState

    def __init__(self, orm: ObjectMapper, state: ObjectMapperQueryState):
        self.orm = orm
        self.state = state

    def select_related(self, column: str) -> "ObjectMapperQuery":
        new_join = (self.state.join or []) + [column]
        new_state = self.state.replace(join=new_join)
        return ObjectMapperQuery(self.orm, new_state)

    async def all(self, *columns: str):
        select = self.state.table.select(None)
