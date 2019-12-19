from typing import Optional, Union

from sqlalchemy.sql import select

from ..database import database
from ..errors import (
    CategoryDoesNotExistError,
    EmailIsNotAvailableError,
    PostDoesNotExistError,
    ThreadDoesNotExistError,
    UsernameIsNotAvailableError,
)
from ..loaders import load_category, load_post, load_thread
from ..tables import users
from ..types import AsyncValidator, Category, GraphQLContext, Post, Thread
from ..users.email import get_email_hash


def validate_category_exists(context: GraphQLContext) -> AsyncValidator:
    async def validate_category_exists_in_db(
        category_id: Union[int, str], _=None
    ) -> Category:
        category = await load_category(context, category_id)
        if not category:
            raise CategoryDoesNotExistError(category_id=category_id)
        return category

    return validate_category_exists_in_db


def validate_email_is_available(exclude_user: Optional[int] = None) -> AsyncValidator:
    async def validate_email_is_available_in_db(email: str, _=None) -> str:
        email_hash = get_email_hash(email)
        query = select([users.c.id]).where(users.c.email_hash == email_hash)
        if exclude_user:
            query = query.where(users.c.id != exclude_user)

        if await database.fetch_one(query):
            raise EmailIsNotAvailableError()

        return email

    return validate_email_is_available_in_db


def validate_post_exists(context: GraphQLContext) -> AsyncValidator:
    async def validate_post_exists_in_db(post_id: Union[int, str], _=None) -> Post:
        post = await load_post(context, post_id)
        if not post:
            raise PostDoesNotExistError(post_id=post_id)
        return post

    return validate_post_exists_in_db


def validate_thread_exists(context: GraphQLContext) -> AsyncValidator:
    async def validate_thread_exists_in_db(
        thread_id: Union[int, str], _=None
    ) -> Thread:
        thread = await load_thread(context, thread_id)
        if not thread:
            raise ThreadDoesNotExistError(thread_id=thread_id)
        return thread

    return validate_thread_exists_in_db


def validate_username_is_available(
    exclude_user: Optional[int] = None,
) -> AsyncValidator:
    async def validate_username_is_available_in_db(username: str, _=None) -> str:
        query = select([users.c.id]).where(users.c.slug == username.lower())
        if exclude_user:
            query = query.where(users.c.id != exclude_user)

        if await database.fetch_one(query):
            raise UsernameIsNotAvailableError()

        return username

    return validate_username_is_available_in_db
