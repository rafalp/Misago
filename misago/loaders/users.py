from typing import Awaitable, Iterable, Optional, Sequence, Union

from ..types import GraphQLContext, User
from ..users.get import get_users_by_id
from .loader import get_loader


def load_user(
    context: GraphQLContext, user_id: Union[int, str]
) -> Awaitable[Optional[User]]:
    loader = get_loader(context, "user_loader", get_users_by_id)
    return loader.load(user_id)


def load_users(
    context: GraphQLContext, ids: Sequence[Union[int, str]]
) -> Awaitable[Sequence[Optional[User]]]:
    loader = get_loader(context, "user_loader", get_users_by_id)
    return loader.load_many(ids)


def store_user(context: GraphQLContext, user: User):
    loader = get_loader(context, "user_loader", get_users_by_id)
    loader.clear(user.id)
    loader.prime(user.id, user)


def store_users(context: GraphQLContext, users: Iterable[User]):
    loader = get_loader(context, "user_loader", get_users_by_id)
    for user in users:
        loader.clear(user.id)
        loader.prime(user.id, user)


def clear_user(context: GraphQLContext, user: User):
    loader = get_loader(context, "user_loader", get_users_by_id)
    loader.clear(user.id)


def clear_users(context: GraphQLContext):
    loader = get_loader(context, "user_loader", get_users_by_id)
    loader.clear_all()
