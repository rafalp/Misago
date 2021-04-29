from dataclasses import replace
from typing import ClassVar, Type

from sqlalchemy.sql import TableClause

from .mapper import DoesNotExist, Mapper, MultipleObjectsReturned


class Model:
    DoesNotExist: ClassVar[Type[DoesNotExist]]
    MultipleObjectsReturned: ClassVar[Type[MultipleObjectsReturned]]

    id: int
    query: ClassVar[Mapper]

    def replace(self, **kwargs):
        return replace(self, **kwargs)

    def refresh_from_db(self):
        return self.query.one(id=self.id)


class ModelsRegistry(dict):
    def register(self, name: str, model: Type[Model], table: TableClause):
        self[name] = Mapper(table, model)


model_registry = ModelsRegistry()


def register_model(name: str, table: TableClause):
    def register(model: Type[Model]):
        mapper = Mapper(table, model)
        model_registry[name] = mapper

        model.query = mapper
        model.DoesNotExist = mapper.DoesNotExist
        model.MultipleObjectsReturned = mapper.MultipleObjectsReturned

        return model

    return register
