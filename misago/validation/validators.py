from typing import Optional, Union, cast

from sqlalchemy.sql import select

from ..auth import get_authenticated_user
from ..categories import CategoryTypes
from ..database import database
from ..errors import (
    CategoryDoesNotExistError,
    CategoryIsClosedError,
    EmailIsNotAvailableError,
    ErrorsList,
    PostDoesNotExistError,
    ThreadDoesNotExistError,
    ThreadIsClosedError,
    UsernameIsNotAvailableError,
)
from ..loaders import load_category, load_post, load_thread
from ..tables import users
from ..types import AsyncValidator, Category, GraphQLContext, Post, Thread
from ..users.email import get_email_hash


async def _get_category_type(context: GraphQLContext, category_id: int) -> int:
    category = await load_category(context, category_id)
    if category:
        return category.type
    return 0


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

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, category: Category, _=None) -> Category:
        if category.is_closed:
            user = await get_authenticated_user(self._context)
            if not user or not user.is_moderator:
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
    _category_type: int

    def __init__(
        self, context: GraphQLContext, category_type: int = CategoryTypes.THREADS
    ):
        self._context = context
        self._category_type = category_type

    async def __call__(self, post_id: Union[int, str], _=None) -> Post:
        post = await load_post(self._context, post_id)
        if not post:
            raise PostDoesNotExistError(post_id=post_id)
        category_type = await _get_category_type(self._context, post.category_id)
        if category_type != self._category_type:
            raise PostDoesNotExistError(post_id=post_id)
        return post


class ThreadCategoryValidator(AsyncValidator):
    _context: GraphQLContext
    _validator: AsyncValidator

    def __init__(self, context: GraphQLContext, category_validator: AsyncValidator):
        self._context = context
        self._validator = category_validator

    @property
    def category_validator(self) -> AsyncValidator:
        return self._validator

    async def __call__(self, thread: Thread, errors: ErrorsList) -> Thread:
        category = await load_category(self._context, thread.category_id)
        category = cast(Category, category)
        await self._validator(category, errors)
        return thread


class ThreadExistsValidator(AsyncValidator):
    _context: GraphQLContext
    _category_type: int

    def __init__(
        self, context: GraphQLContext, category_type: int = CategoryTypes.THREADS
    ):
        self._context = context
        self._category_type = category_type

    async def __call__(self, thread_id: Union[int, str], _=None) -> Thread:
        thread = await load_thread(self._context, thread_id)
        if not thread:
            raise ThreadDoesNotExistError(thread_id=thread_id)
        category_type = await _get_category_type(self._context, thread.category_id)
        if category_type != self._category_type:
            raise ThreadDoesNotExistError(thread_id=thread_id)
        return thread


class ThreadIsOpenValidator(AsyncValidator):
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, thread: Thread, _=None) -> Thread:
        if thread.is_closed:
            user = await get_authenticated_user(self._context)
            if not user or not user.is_moderator:
                raise ThreadIsClosedError(thread_id=thread.id)
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
