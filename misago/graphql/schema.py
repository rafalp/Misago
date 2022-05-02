from ariadne_graphql_modules import BaseType, make_executable_schema
from graphql import GraphQLSchema

from . import auth, avatar, settings, user
from .hooks import create_admin_schema_hook, create_public_schema_hook

ADMIN_TYPES = [
    auth.AdminLoginMutation,
    auth.AuthQueries,
    settings.AdminSettingsQueries,
    settings.AdminSettingsUpdateMutation,
    user.AdminUserCreateMutation,
    user.AdminUserDeleteMutation,
    user.AdminUserQueries,
    user.AdminUserUpdateMutation,
]

PUBLIC_TYPES = [
    auth.LoginMutation,
    auth.AuthQueries,
    avatar.AvatarUploadMutation,
    settings.SettingsQueries,
    user.UserCreateMutation,
    user.UserQueries,
]


def create_admin_schema() -> GraphQLSchema:
    return create_admin_schema_hook.call_action(create_schema_action, *ADMIN_TYPES)


def create_public_schema() -> GraphQLSchema:
    return create_public_schema_hook.call_action(create_schema_action, *PUBLIC_TYPES)


def create_schema_action(*types: BaseType) -> GraphQLSchema:
    return make_executable_schema(*types)
