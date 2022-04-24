from ariadne_graphql_modules import BaseType, make_executable_schema
from graphql import GraphQLSchema

from . import auth, user
from .hooks import create_admin_schema_hook, create_public_schema_hook

ADMIN_TYPES = [
    auth.AdminLoginMutation,
    auth.AuthQueries,
    user.AdminUserQueries,
]

PUBLIC_TYPES = [
    auth.LoginMutation,
    auth.AuthQueries,
    user.UserQueries,
]


def create_admin_schema() -> GraphQLSchema:
    return create_admin_schema_hook.call_action(create_schema_action, *ADMIN_TYPES)


def create_public_schema() -> GraphQLSchema:
    return create_public_schema_hook.call_action(create_schema_action, *PUBLIC_TYPES)


def create_schema_action(*types: BaseType) -> GraphQLSchema:
    return make_executable_schema(*types)
