from typing import Callable

from ariadne_graphql_modules import BaseType
from graphql import GraphQLSchema

from ...hooks import FilterHook

CreateAdminSchemaAction = Callable[[BaseType, ...], GraphQLSchema]
CreateAdminSchemaFilter = Callable[
    [CreateAdminSchemaAction, BaseType, ...], GraphQLSchema
]


class CreateAdminSchemaHook(
    FilterHook[CreateAdminSchemaAction, CreateAdminSchemaFilter]
):
    is_async = False

    def call_action(
        self, action: CreateAdminSchemaAction, *types: BaseType
    ) -> GraphQLSchema:
        return self.filter(action, *types)


create_admin_schema_hook = CreateAdminSchemaHook()
