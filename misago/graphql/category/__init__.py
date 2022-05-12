from ariadne_graphql_modules import CollectionType

from .category import AdminCategoryType, CategoryType
from .categorycreate import AdminCategoryCreateMutation
from .categorydelete import AdminCategoryDeleteMutation
from .categorymove import AdminCategoryMoveMutation
from .categoryupdate import AdminCategoryUpdateMutation
from .queries import AdminCategoryQueries, CategoryQueries


class AdminCategoryMutations(CollectionType):
    __types__ = [
        AdminCategoryCreateMutation,
        AdminCategoryMoveMutation,
        AdminCategoryUpdateMutation,
        AdminCategoryDeleteMutation,
    ]


__all__ = [
    "AdminCategoryMutations",
    "AdminCategoryQueries",
    "AdminCategoryType",
    "CategoryQueries",
    "CategoryType",
]
