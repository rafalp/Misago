from ariadne_graphql_modules import CollectionType

from .queries import AdminUserQueries, UserQueries
from .user import AdminUserType, UserType
from .usercreate import AdminUserCreateMutation, UserCreateMutation
from .userdelete import AdminUserDeleteMutation
from .userupdate import AdminUserUpdateMutation


class AdminUserMutations(CollectionType):
    __types__ = [
        AdminUserCreateMutation,
        AdminUserDeleteMutation,
        AdminUserUpdateMutation,
    ]


class UserMutations(CollectionType):
    __types__ = [
        UserCreateMutation,
    ]


__all__ = [
    "AdminUserMutations",
    "AdminUserQueries",
    "AdminUserType",
    "UserMutations",
    "UserQueries",
    "UserType",
]
