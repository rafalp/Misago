from asyncio import gather
from typing import Any, Awaitable, Callable, List, Optional, Union, cast

from pydantic import PydanticTypeError, PydanticValueError
from pydantic.color import Color

from ..categories import CategoryTypes
from ..categories.models import Category
from ..errors import (
    AuthError,
    CategoryClosedError,
    CategoryNotFoundError,
    ErrorsList,
    NotAuthorizedError,
    NotModeratorError,
    NotPostAuthorError,
    NotThreadAuthorError,
    PostNotFoundError,
    ThreadClosedError,
    ThreadFirstPostError,
    ThreadNotFoundError,
)
from ..graphql import GraphQLContext
from ..loaders import load_category, load_post, load_thread
from ..threads.models import Post, Thread
from ..users.models import User
from ..utils.lists import remove_none_items

Validator = Callable[[Any, ErrorsList, str], Union[Awaitable[Any], Any]]


class BulkValidator:
    _validators: List[Validator]

    def __init__(self, validators: List[Validator]):
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
    location: List[str], data: Any, validators: List[Validator], errors: ErrorsList
) -> Any:
    try:
        for validator in validators:
            data = await validator(data, errors, location[0])
        return data
    except (AuthError, PydanticTypeError, PydanticValueError) as error:
        errors.add_error(location, error)
        return None


class CategoryExistsValidator:
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
            raise CategoryNotFoundError(category_id=category_id)
        return category


class CategoryIsOpenValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, category: Category, *_) -> Category:
        if category.is_closed:
            user = self._context["user"]
            if not (user and user.is_moderator):
                raise CategoryClosedError(category_id=category.id)
        return category


class CategoryModeratorValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, category: Category, *_) -> Category:
        user = self._context["user"]
        if not user or not user.is_moderator:
            raise NotModeratorError()
        return category


class NewThreadIsClosedValidator:
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

        user = self._context["user"]

        if not category or not user or not user.is_moderator:
            raise NotModeratorError()

        return is_closed


class PostAuthorValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, post: Post, *_) -> Post:
        user = self._context["user"]
        if not user:
            raise NotPostAuthorError(post_id=post.id)
        if not user.is_moderator and user.id != post.poster_id:
            raise NotPostAuthorError(post_id=post.id)
        return post


class PostCategoryValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext, category_validator: Validator):
        self._context = context
        self._validator = category_validator

    @property
    def category_validator(self) -> Validator:
        return self._validator

    async def __call__(self, post: Post, errors: ErrorsList, field_name: str) -> Post:
        category = await load_category(self._context, post.category_id)
        category = cast(Category, category)
        await self._validator(category, errors, field_name)
        return post


class PostExistsValidator:
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
            raise PostNotFoundError(post_id=post_id)
        category_type = await _get_category_type(self._context, post.category_id)
        if category_type != self._category_type:
            raise PostNotFoundError(post_id=post_id)
        return post


async def _get_category_type(context: GraphQLContext, category_id: int) -> int:
    category = await load_category(context, category_id)
    if category:
        return category.type
    return 0


class PostThreadValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext, thread_validator: Validator):
        self._context = context
        self._validator = thread_validator

    @property
    def thread_validator(self) -> Validator:
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


class ThreadAuthorValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, thread: Thread, *_) -> Thread:
        user = self._context["user"]
        if not user:
            raise NotThreadAuthorError(thread_id=thread.id)
        if not user.is_moderator and user.id != thread.starter_id:
            raise NotThreadAuthorError(thread_id=thread.id)
        return thread


class ThreadCategoryValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext, category_validator: Validator):
        self._context = context
        self._validator = category_validator

    @property
    def category_validator(self) -> Validator:
        return self._validator

    async def __call__(
        self, thread: Thread, errors: ErrorsList, field_name: str
    ) -> Thread:
        category = await load_category(self._context, thread.category_id)
        category = cast(Category, category)
        await self._validator(category, errors, field_name)
        return thread


class ThreadExistsValidator:
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
            raise ThreadNotFoundError(thread_id=thread_id)
        category_type = await _get_category_type(self._context, thread.category_id)
        if category_type != self._category_type:
            raise ThreadNotFoundError(thread_id=thread_id)
        return thread


class ThreadIsOpenValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, thread: Thread, *_) -> Thread:
        if thread.is_closed:
            user = self._context["user"]
            if not user or not user.is_moderator:
                raise ThreadClosedError(thread_id=thread.id)
        return thread


class ThreadPostExistsValidator:
    _context: GraphQLContext
    _thread: Thread

    def __init__(self, context: GraphQLContext, thread: Thread):
        self._context = context
        self._thread = thread

    async def __call__(self, post_id: Union[int, str], *_) -> Post:
        post = await load_post(self._context, post_id)
        if not post or post.thread_id != self._thread.id:
            raise PostNotFoundError(post_id=post_id)
        return post


class ThreadPostIsReplyValidator:
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


class UserIsAuthorizedRootValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, data: Any, *_) -> Any:
        user = self._context["user"]
        if not user:
            raise NotAuthorizedError()
        return data


def color_validator(color: Union[Color, str], *_) -> str:
    if isinstance(color, Color):
        return color.as_hex().upper()

    return Color(color).as_hex().upper()
