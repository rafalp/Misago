from ariadne_graphql_modules import CollectionType

from .post import PostType
from .postcreate import PostCreateMutation
from .postdelete import PostDeleteMutation
from .postsbulkdelete import PostsBulkDeleteMutation
from .postupdate import PostUpdateMutation
from .queries import PostQueries


class PostMutations(CollectionType):
    __types__ = [
        PostCreateMutation,
        PostUpdateMutation,
        PostDeleteMutation,
        PostsBulkDeleteMutation,
    ]


__all__ = [
    "PostMutations",
    "PostQueries",
    "PostType",
]
