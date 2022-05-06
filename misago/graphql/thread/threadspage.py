from ariadne_graphql_modules import ObjectType, gql

from ..pagination import PageInfoType
from .threadedge import ThreadEdgeType


class ThreadsPageType(ObjectType):
    __schema__ = gql(
        """
        type ThreadsPage {
            edges: [ThreadEdge!]!
            pageInfo: PageInfo!
        }
        """
    )
    __aliases__ = {
        "edges": "results",
        "pageInfo": "page_info",
    }
    __requires__ = [PageInfoType, ThreadEdgeType]
