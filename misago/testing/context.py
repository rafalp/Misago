from unittest.mock import Mock

import pytest
import pytest_asyncio

from ..categories.index import get_categories_index
from ..categories.loaders import categories_children_loader, categories_loader
from ..permissions.users import get_user_permissions
from ..threads.loaders import posts_loader, threads_loader
from ..users.loaders import users_groups_loader, users_loader


async def setup_context(context: dict):
    context["categories"] = await get_categories_index()

    categories_loader.setup_context(context)
    categories_children_loader.setup_context(context)
    threads_loader.setup_context(context)
    posts_loader.setup_context(context)
    users_loader.setup_context(context)
    users_groups_loader.setup_context(context)

    if context.get("user"):
        context["permissions"] = await get_user_permissions(context, context["user"])

    return context


@pytest.fixture
def request_mock():
    return Mock(headers={}, base_url="http://test.com/", user=None)


@pytest_asyncio.fixture
async def context(db, request_mock, cache_versions, dynamic_settings):
    context = {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "user": None,
    }

    await setup_context(context)

    return context


@pytest_asyncio.fixture
async def user_context(request_mock, cache_versions, dynamic_settings, user):
    context = {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "user": user,
    }

    await setup_context(context)

    return context


@pytest_asyncio.fixture
async def moderator_context(request_mock, cache_versions, dynamic_settings, moderator):
    context = {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "user": moderator,
    }

    await setup_context(context)

    return context


@pytest_asyncio.fixture
async def admin_context(request_mock, cache_versions, dynamic_settings, admin):
    context = {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "checked_admin_auth": True,
        "user": admin,
    }

    await setup_context(context)

    return context
