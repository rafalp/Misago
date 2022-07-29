from typing import Dict, Type, Union

from sqlalchemy.sql import TableClause

from .model import Model
from .query import RootQuery
from .querystate import QueryState


class ObjectMapper:
    tables: Dict[str, TableClause]
    mappings: Dict[str, Union[Type, dict]]
    models: Dict[str, Type[Model]]

    def __init__(self):
        self.tables = {}
        self.mappings = {}
        self.models = {}

    def set_mapping(self, table: TableClause, repr_: Union[Type, dict]):
        self.tables[table.name] = table
        self.mappings[table.name] = repr_

    def set_model(self, name: str, model: Union[Type, dict]):
        self.models[name] = model

    def query_table(self, table: TableClause) -> "RootQuery":
        state = QueryState(table)
        return RootQuery(self, state)


object_mapper = ObjectMapper()


def register_model(name: str, table: TableClause):
    def register(model: Type[Model]):
        object_mapper.set_mapping(table, model)
        object_mapper.set_model(name, model)

        model.query = object_mapper.query_table(table)
        model.table = table

        return model

    return register
