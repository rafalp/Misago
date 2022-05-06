from ariadne_graphql_modules import CollectionType

from .queries import ThreadQueries
from .thread import ThreadType
from .threadclose import ThreadCloseMutation
from .threadcreate import ThreadCreateMutation
from .threaddelete import ThreadDeleteMutation
from .threadmove import ThreadMoveMutation
from .threadopen import ThreadOpenMutation
from .threadrename import ThreadRenameMutation
from .threadsbulkclose import ThreadsBulkCloseMutation
from .threadsbulkdelete import ThreadsBulkDeleteMutation
from .threadsbulkmove import ThreadsBulkMoveMutation
from .threadsbulkopen import ThreadsBulkOpenMutation


class ThreadMutations(CollectionType):
    __types__ = [
        ThreadCreateMutation,
        ThreadRenameMutation,
        ThreadCloseMutation,
        ThreadOpenMutation,
        ThreadMoveMutation,
        ThreadDeleteMutation,
        ThreadsBulkCloseMutation,
        ThreadsBulkOpenMutation,
        ThreadsBulkMoveMutation,
        ThreadsBulkDeleteMutation,
    ]


__all__ = [
    "ThreadMutations",
    "ThreadQueries",
    "ThreadType",
]
