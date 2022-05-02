from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...conf.types import Settings
from ..adminqueries import AdminQueries
from .settings import AdminSettingsType, SettingsType


class SettingsQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            settings: Settings!
        }
        """
    )
    __requires__ = [SettingsType]

    @staticmethod
    def resolve_settings(_, info: GraphQLResolveInfo) -> Settings:
        return info.context["settings"]


class AdminSettingsQueries(AdminQueries):
    __schema__ = gql(
        """
        type Query {
            settings: Settings
        }
        """
    )
    __requires__ = [AdminSettingsType]

    @staticmethod
    def resolve_settings(_, info: GraphQLResolveInfo) -> Settings:
        return info.context["settings"]
