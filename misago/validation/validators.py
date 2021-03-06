from asyncio import gather
from typing import Any, Optional, List, Union, cast

from pydantic import PydanticTypeError, PydanticValueError
from sqlalchemy.sql import select

from ..auth import get_authenticated_user
from ..categories import CategoryTypes
from ..database import database
from ..errors import (
    AuthError,
    CategoryClosedError,
    CategoryDoesNotExistError,
    EmailNotAvailableError,
    ErrorsList,
    NotAuthorizedError,
    NotModeratorError,
    NotPostAuthorError,
    NotThreadAuthorError,
    PostDoesNotExistError,
    ThreadDoesNotExistError,
    ThreadFirstPostError,
    ThreadClosedError,
    UsernameNotAvailableError,
)
from ..loaders import load_category, load_post, load_thread
from ..tables import users
from ..types import AsyncValidator, Category, GraphQLContext, Post, Thread
from ..users.email import get_email_hash
from ..utils.lists import remove_none_items


async def _get_category_type(context: GraphQLContext, category_id: int) -> int:
    category = await load_category(context, category_id)
    if category:
        return category.type
    return 0


class BulkValidator(AsyncValidator):
    _validators: List[AsyncValidator]

    def __init__(self, validators: List[AsyncValidator]):
        self._validators = validators

    async def __call__(
        self, items: List[Any], errors: ErrorsList, field_name: str
    ) -> List[Any]:
        validators = []
        for i, item in enumerate(items):
            validators.append(
                _validate_bulk_item(
                    [field_name, str(i)], item, self._validators, errors
                )
            )

        if validators:
            validated_items = await gather(*validators)
            return remove_none_items(validated_items)

        return []


async def _validate_bulk_item(
    location: List[str], data: Any, validators: List[AsyncValidator], errors: ErrorsList
) -> Any:
    try:
        for validator in validators:
            data = await validator(data, errors, location[0])
        return data
    except (AuthError, PydanticTypeError, PydanticValueError) as error:
        errors.add_error(location, error)
        return None


class CategoryExistsValidator(AsyncValidator):
    _context: GraphQLContext
    _category_type: int

    def __init__(
        self, context: GraphQLContext, category_type: int = CategoryTypes.THREADS
    ):
        self._context = context
        self._category_type = category_type

    async def __call__(self, category_id: Union[int, str], *_) -> Category:
        category = await load_category(self._context, category_id)
        if not category or category.type != self._category_type:
            raise CategoryDoesNotExistError(category_id=category_id)
        return category


class CategoryIsOpenValidator(AsyncValidator):
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, category: Category, *_) -> Category:
        if category.is_closed:
            user = await get_authenticated_user(self._context)
            if not (user and user.is_moderator):
                raise CategoryClosedError(category_id=category.id)
        return category


class CategoryModeratorValidator(AsyncValidator):
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, category: Category, *_) -> Category:
        user = await get_authenticated_user(self._context)
        if not user or not user.is_moderator:
            raise NotModeratorError()
        return category


class EmailIsAvailableValidator(AsyncValidator):
    _exclude_user: Optional[int]

    def __init__(self, exclude_user: Optional[int] = None):
        self._exclude_user = exclude_user

    async def __call__(self, email: str, *_) -> str:
        email_hash = get_email_hash(email)
        query = select([users.c.id]).where(users.c.email_hash == email_hash)
        if self._exclude_user:
            query = query.where(users.c.id != self._exclude_user)
        if await database.fetch_one(query):
            raise EmailNotAvailableError()
        return email


class NewThreadIsClosedValidator(AsyncValidator):
    _context: GraphQLContext
    _category: Union[str, int, Category]

    def __init__(self, context: GraphQLContext, category: Union[str, int, Category]):
        self._context = context
        self._category = category

    async def __call__(self, is_closed: bool, *_) -> bool:
        if not is_closed:
            return is_closed

        category: Optional[Category] = None
        if isinstance(self._category, Category):
            category = self._category
        else:
            category = await load_category(self._context, self._category)

        user = await get_authenticated_user(self._context)

        if not category or not user or not user.is_moderator:
            raise NotModeratorError()

        return is_closed


class PostAuthorValidator(AsyncValidator):
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, post: Post, *_) -> Post:
        user = await get_authenticated_user(self._context)
        if not user:
            raise NotPostAuthorError(post_id=post.id)
        if not user.is_moderator and user.id != post.poster_id:
            raise NotPostAuthorError(post_id=post.id)
        return post


class PostCategoryValidator(AsyncValidator):
    _context: GraphQLContext
    _validator: AsyncValidator

    def __init__(self, context: GraphQLContext, category_validator: AsyncValidator):
        self._context = context
        self._validator = category_validator

    @property
    def category_validator(self) -> AsyncValidator:
        return self._validator

    async def __call__(self, post: Post, errors: ErrorsList, field_name: str) -> Post:
        category = await load_category(self._context, post.category_id)
        category = cast(Category, category)
        await self._validator(category, errors, field_name)
        return post


class PostExistsValidator(AsyncValidator):
    _context: GraphQLContext
    _category_type: int

    def __init__(
        self, context: GraphQLContext, category_type: int = CategoryTypes.THREADS
    ):
        self._context = context
        self._category_type = category_type

    async def __call__(self, post_id: Union[int, str], *_) -> Post:
        post = await load_post(self._context, post_id)
        if not post:
            raise PostDoesNotExistError(post_id=post_id)
        category_type = await _get_category_type(self._context, post.category_id)
        if category_type != self._category_type:
            raise PostDoesNotExistError(post_id=post_id)
        return post


class PostThreadValidator(AsyncValidator):
    _context: GraphQLContext
    _validator: AsyncValidator

    def __init__(self, context: GraphQLContext, thread_validator: AsyncValidator):
        self._context = context
        self._validator = thread_validator

    @property
    def thread_validator(self) -> AsyncValidator:
        return self._validator

    async def __call__(self, post: Post, errors: ErrorsList, field_name: str) -> Post:
        thread = await load_thread(self._context, post.thread_id)
        thread = cast(Thread, thread)
        await self._validator(thread, errors, field_name)
        return post


class PostsBulkValidator(BulkValidator):
    async def __call__(
        self, threads: List[Any], errors: ErrorsList, field_name: str
    ) -> List[Post]:
        return await super().__call__(threads, errors, field_name)


class ThreadAuthorValidator(AsyncValidator):
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, thread: Thread, *_) -> Thread:
        user = await get_authenticated_user(self._context)
        if not user:
            raise NotThreadAuthorError(thread_id=thread.id)
        if not user.is_moderator and user.id != thread.starter_id:
            raise NotThreadAuthorError(thread_id=thread.id)
        return thread


class ThreadCategoryValidator(AsyncValidator):
    _context: GraphQLContext
    _validator: AsyncValidator

    def __init__(self, context: GraphQLContext, category_validator: AsyncValidator):
        self._context = context
        self._validator = category_validator

    @property
    def category_validator(self) -> AsyncValidator:
        return self._validator

    async def __call__(
        self, thread: Thread, errors: ErrorsList, field_name: str
    ) -> Thread:
        category = await load_category(self._context, thread.category_id)
        category = cast(Category, category)
        await self._validator(category, errors, field_name)
        return thread


class ThreadExistsValidator(AsyncValidator):
    _context: GraphQLContext
    _category_type: int

    def __init__(
        self, context: GraphQLContext, category_type: int = CategoryTypes.THREADS
    ):
        self._context = context
        self._category_type = category_type

    async def __call__(self, thread_id: Union[int, str], *_) -> Thread:
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

    async def __call__(self, thread: Thread, *_) -> Thread:
        if thread.is_closed:
            user = await get_authenticated_user(self._context)
            if not (user and user.is_moderator):
                raise ThreadClosedError(thread_id=thread.id)
        return thread


class ThreadPostExistsValidator(AsyncValidator):
    _context: GraphQLContext
    _thread: Thread

    def __init__(self, context: GraphQLContext, thread: Thread):
        self._context = context
        self._thread = thread

    async def __call__(self, post_id: Union[int, str], *_) -> Post:
        post = await load_post(self._context, post_id)
        if not post or post.thread_id != self._thread.id:
            raise PostDoesNotExistError(post_id=post_id)
        return post


class ThreadPostIsReplyValidator(AsyncValidator):
    _thread: Thread

    def __init__(self, thread: Thread):
        self._thread = thread

    async def __call__(self, post: Post, *_) -> Post:
        if post and post.id == self._thread.first_post_id:
            raise ThreadFirstPostError(post_id=post.id)
        return post


class ThreadsBulkValidator(BulkValidator):
    async def __call__(
        self, threads: List[Any], errors: ErrorsList, field_name: str
    ) -> List[Thread]:
        return await super().__call__(threads, errors, field_name)


class UserIsAuthorizedRootValidator(AsyncValidator):
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, data: Any, *_) -> Any:
        user = await get_authenticated_user(self._context)
        if not user:
            raise NotAuthorizedError()
        return data


class UsernameIsAvailableValidator(AsyncValidator):
    _exclude_user: Optional[int]

    def __init__(self, exclude_user: Optional[int] = None):
        self._exclude_user = exclude_user

    async def __call__(self, username: str, *_) -> str:
        query = select([users.c.id]).where(users.c.slug == username.lower())
        if self._exclude_user:
            query = query.where(users.c.id != self._exclude_user)
        if await database.fetch_one(query):
            raise UsernameNotAvailableError()
        return username
