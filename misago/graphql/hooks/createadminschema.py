from typing import Protocol, Type

from ariadne_graphql_modules import BaseType
from graphql import GraphQLSchema

from ...hooks import FilterHook


class CreateAdminSchemaAction(Protocol):
    def __call__(self, *types: Type[BaseType]) -> GraphQLSchema:
        pass


class CreateAdminSchemaFilter(Protocol):
    def __call__(
        self, action: CreateAdminSchemaAction, *types: Type[BaseType]
    ) -> GraphQLSchema:
        pass


class CreateAdminSchemaHook(
    FilterHook[CreateAdminSchemaAction, CreateAdminSchemaFilter]
):
    is_async = False

    def call_action(
        self, action: CreateAdminSchemaAction, *types: Type[BaseType]
    ) -> GraphQLSchema:
        return self.filter(action, *types)


create_admin_schema_hook = CreateAdminSchemaHook()
