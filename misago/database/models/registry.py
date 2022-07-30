from typing import Dict, Type

from sqlalchemy.sql import TableClause

from .model import Model
from .query import RootQuery
from .querystate import QueryState


class MapperRegistry:
    tables: Dict[str, TableClause]
    mappings: Dict[str, Type | Type[dict]]
    models: Dict[str, Type[Model] | Type[dict]]

    def __init__(self):
        self.tables = {}
        self.mappings = {}
        self.models = {}

    def set_mapping(self, table: TableClause, repr_: Type | Type[dict]):
        self.tables[table.name] = table
        self.mappings[table.name] = repr_

    def set_model(self, name: str, model: Type | Type[dict]):
        self.models[name] = model

    def query_table(self, table: TableClause) -> "RootQuery":
        state = QueryState(table)
        return RootQuery(self, state)


mapper_registry = MapperRegistry()


def register_model(name: str, table: TableClause):
    def register(model: Type[Model]):
        mapper_registry.set_mapping(table, model)
        mapper_registry.set_model(name, model)

        model.query = mapper_registry.query_table(table)
        model.table = table

        return model

    return register
