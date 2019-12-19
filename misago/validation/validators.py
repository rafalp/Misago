from typing import Optional, Union

from sqlalchemy.sql import select

from ..auth import get_authenticated_user
from ..categories import CategoryTypes
from ..database import database
from ..errors import (
    CategoryDoesNotExistError,
    CategoryIsClosedError,
    EmailIsNotAvailableError,
    PostDoesNotExistError,
    ThreadDoesNotExistError,
    UsernameIsNotAvailableError,
)
from ..loaders import load_category, load_post, load_thread
from ..tables import users
from ..types import AsyncValidator, Category, GraphQLContext, Post, Thread
from ..users.email import get_email_hash


class CategoryExistsValidator(AsyncValidator):
    _context: GraphQLContext
    _category_type: int

    def __init__(
        self, context: GraphQLContext, category_type: int = CategoryTypes.THREADS
    ):
        self._context = context
        self._category_type = category_type

    async def __call__(self, category_id: Union[int, str], _=None) -> Category:
        category = await load_category(self._context, category_id)
        if not category or category.type != self._category_type:
            raise CategoryDoesNotExistError(category_id=category_id)
        return category


class CategoryIsOpenValidator(AsyncValidator):
    _context: GraphQLContext
    _exclude_moderators: bool

    def __init__(self, context: GraphQLContext, exclude_moderators: bool = True):
        self._context = context
        self._exclude_moderators = exclude_moderators

    async def __call__(self, category: Category, _=None) -> Category:
        if category.is_closed:
            if not self._exclude_moderators:
                raise CategoryIsClosedError(category_id=category.id)
            user = await get_authenticated_user(self._context)
            if user and not user.is_moderator:
                raise CategoryIsClosedError(category_id=category.id)
        return category


class EmailIsAvailableValidator(AsyncValidator):
    _exclude_user: Optional[int]

    def __init__(self, exclude_user: Optional[int] = None):
        self._exclude_user = exclude_user

    async def __call__(self, email: str, _=None) -> str:
        email_hash = get_email_hash(email)
        query = select([users.c.id]).where(users.c.email_hash == email_hash)
        if self._exclude_user:
            query = query.where(users.c.id != self._exclude_user)

        if await database.fetch_one(query):
            raise EmailIsNotAvailableError()

        return email


class PostExistsValidator(AsyncValidator):
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, post_id: Union[int, str], _=None) -> Post:
        post = await load_post(self._context, post_id)
        if not post:
            raise PostDoesNotExistError(post_id=post_id)
        return post


class ThreadExistsValidator(AsyncValidator):
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, thread_id: Union[int, str], _=None) -> Thread:
        thread = await load_thread(self._context, thread_id)
        if not thread:
            raise ThreadDoesNotExistError(thread_id=thread_id)
        return thread


class UsernameIsAvailableValidator(AsyncValidator):
    _exclude_user: Optional[int]

    def __init__(self, exclude_user: Optional[int] = None):
        self._exclude_user = exclude_user

    async def __call__(self, username: str, _=None) -> str:
        query = select([users.c.id]).where(users.c.slug == username.lower())
        if self._exclude_user:
            query = query.where(users.c.id != self._exclude_user)

        if await database.fetch_one(query):
            raise UsernameIsNotAvailableError()

        return username
