from ariadne_graphql_modules import CollectionType

from .queries import AdminUserGroupQueries, UserGroupQueries
from .usergroup import AdminUserGroupType, UserGroupType
from .usergroupcreate import AdminUserGroupCreateMutation


class AdminUserGroupMutations(CollectionType):
    __types__ = [
        AdminUserGroupCreateMutation,
    ]


__all__ = [
    "AdminUserGroupMutations",
    "AdminUserGroupQueries",
    "AdminUserGroupType",
    "UserGroupQueries",
    "UserGroupType",
]
