from typing import Awaitable, Iterable, Optional, Sequence, Union

from ..graphql import GraphQLContext
from ..users.get import get_users_by_id
from ..users.models import User
from .loader import get_loader


def load_user(
    context: GraphQLContext, user_id: Union[int, str]
) -> Awaitable[Optional[User]]:
    loader = get_loader(context, "user", get_users_by_id)
    return loader.load(user_id)


def load_users(
    context: GraphQLContext, ids: Sequence[Union[int, str]]
) -> Awaitable[Sequence[Optional[User]]]:
    loader = get_loader(context, "user", get_users_by_id)
    return loader.load_many(ids)


def store_user(context: GraphQLContext, user: User):
    loader = get_loader(context, "user", get_users_by_id)
    loader.clear(user.id)
    loader.prime(user.id, user)


def store_users(context: GraphQLContext, users: Iterable[User]):
    loader = get_loader(context, "user", get_users_by_id)
    for user in users:
        loader.clear(user.id)
        loader.prime(user.id, user)


def clear_user(context: GraphQLContext, user: User):
    loader = get_loader(context, "user", get_users_by_id)
    loader.clear(user.id)


def clear_users(context: GraphQLContext, users: Iterable[User]):
    loader = get_loader(context, "user", get_users_by_id)
    for user in users:
        loader.clear(user.id)


def clear_all_users(context: GraphQLContext):
    loader = get_loader(context, "user", get_users_by_id)
    loader.clear_all()
