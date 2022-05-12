from typing import Protocol, Type

from ariadne_graphql_modules import BaseType
from graphql import GraphQLSchema

from ...hooks import FilterHook


class CreatePublicSchemaAction(Protocol):
    def __call__(self, *types: Type[BaseType]) -> GraphQLSchema:
        pass


class CreatePublicSchemaFilter(Protocol):
    def __call__(
        self, action: CreatePublicSchemaAction, *types: Type[BaseType]
    ) -> GraphQLSchema:
        pass


class CreatePublicSchemaHook(
    FilterHook[CreatePublicSchemaAction, CreatePublicSchemaFilter]
):
    is_async = False

    def call_action(
        self, action: CreatePublicSchemaAction, *types: Type[BaseType]
    ) -> GraphQLSchema:
        return self.filter(action, *types)


create_public_schema_hook = CreatePublicSchemaHook()
