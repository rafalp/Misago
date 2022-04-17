from typing import Callable

from ariadne_graphql_modules import BaseType
from graphql import GraphQLSchema

from ...hooks import FilterHook

CreatePublicSchemaAction = Callable[[BaseType, ...], GraphQLSchema]
CreatePublicSchemaFilter = Callable[
    [CreatePublicSchemaAction, BaseType, ...], GraphQLSchema
]


class CreatePublicSchemaHook(
    FilterHook[CreatePublicSchemaAction, CreatePublicSchemaFilter]
):
    is_async = False

    def call_action(
        self, action: CreatePublicSchemaAction, *types: BaseType
    ) -> GraphQLSchema:
        return self.filter(action, *types)


create_public_schema_hook = CreatePublicSchemaHook()
