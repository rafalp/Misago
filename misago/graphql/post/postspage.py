from ariadne_graphql_modules import ObjectType, gql

from ..pagination import OffsetPageInfoType
from .post import PostType


class PostsPageType(ObjectType):
    __schema__ = gql(
        """
        type PostsPage {
            totalCount: Int!
            totalPages: Int!
            results: [Post!]!
            pageInfo: OffsetPageInfo!
        }
        """
    )
    __aliases__ = {
        "totalCount": "total_count",
        "totalPages": "total_pages",
        "pageInfo": "page_info",
    }
    __requires__ = [OffsetPageInfoType, PostType]
