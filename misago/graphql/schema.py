from typing import Type

from ariadne_graphql_modules import BaseType, make_executable_schema
from graphql import GraphQLSchema

from . import (
    auth,
    avatar,
    category,
    forumstats,
    post,
    richtext,
    search,
    settings,
    sitesetup,
    thread,
    user,
)
from .hooks import create_admin_schema_hook, create_public_schema_hook

ADMIN_TYPES = [
    auth.AdminLoginMutation,
    auth.AuthQueries,
    category.AdminCategoryMutations,
    category.AdminCategoryQueries,
    settings.AdminSettingsMutations,
    settings.AdminSettingsQueries,
    user.AdminUserMutations,
    user.AdminUserQueries,
]

PUBLIC_TYPES = [
    auth.LoginMutation,
    auth.AuthQueries,
    avatar.AvatarUploadMutation,
    category.CategoryQueries,
    forumstats.ForumStatsQueries,
    post.PostMutations,
    post.PostQueries,
    richtext.RichTextQueries,
    search.SearchQueries,
    settings.SettingsQueries,
    sitesetup.SiteSetupMutation,
    thread.ThreadMutations,
    thread.ThreadQueries,
    user.UserMutations,
    user.UserQueries,
]


def create_admin_schema() -> GraphQLSchema:
    return create_admin_schema_hook.call_action(create_schema_action, *ADMIN_TYPES)


def create_public_schema() -> GraphQLSchema:
    return create_public_schema_hook.call_action(create_schema_action, *PUBLIC_TYPES)


def create_schema_action(*types: Type[BaseType]) -> GraphQLSchema:
    return make_executable_schema(*types)
