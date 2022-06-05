from typing import List

from ariadne_graphql_modules import gql
from graphql import GraphQLResolveInfo

from ...plugins import PluginData, plugins_loader
from ..adminqueries import AdminQueries
from .plugin import PluginType


class AdminPluginQueries(AdminQueries):
    __schema__ = gql(
        """
        type Query {
            plugins: [Plugin!]!
        }
        """
    )
    __requires__ = [PluginType]

    @staticmethod
    def resolve_plugins(_, info: GraphQLResolveInfo) -> List[PluginData]:
        return plugins_loader.get_plugins_data()
