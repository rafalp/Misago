import json
from typing import Optional
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from ..asgi import app
from ..categories.index import get_categories_index
from ..categories.loaders import categories_children_loader, categories_loader
from ..threads.loaders import posts_loader, threads_loader
from ..users.loaders import users_loader
from ..users.models import User


async def setup_context(context: dict):
    context["categories"] = await get_categories_index()

    categories_loader.setup_context(context)
    categories_children_loader.setup_context(context)
    threads_loader.setup_context(context)
    posts_loader.setup_context(context)
    users_loader.setup_context(context)

    return context


@pytest.fixture
def request_mock():
    return Mock(headers={}, base_url="http://test.com/", user=None)


@pytest.fixture
async def graphql_context(request_mock, cache_versions, dynamic_settings):
    context = {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "user": None,
    }

    await setup_context(context)

    return context


@pytest.fixture
def graphql_info(graphql_context):
    return Mock(context=graphql_context)


@pytest.fixture
async def user_graphql_context(request_mock, cache_versions, dynamic_settings, user):
    context = {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "user": user,
    }

    await setup_context(context)

    return context


@pytest.fixture
def user_graphql_info(user_graphql_context):
    return Mock(context=user_graphql_context)


@pytest.fixture
async def moderator_graphql_context(
    request_mock, cache_versions, dynamic_settings, moderator
):
    context = {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "user": moderator,
    }

    await setup_context(context)

    return context


@pytest.fixture
def moderator_graphql_info(moderator_graphql_context):
    return Mock(context=moderator_graphql_context)


@pytest.fixture
async def admin_graphql_context(request_mock, cache_versions, dynamic_settings, admin):
    context = {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "checked_admin_auth": True,
        "user": admin,
    }

    await setup_context(context)

    return context


@pytest.fixture
def admin_graphql_info(admin_graphql_context):
    return Mock(context=admin_graphql_context)


@pytest.fixture
def http_client():
    def create_http_client():
        return httpx.AsyncClient(app=app, base_url="http://example.com")

    return create_http_client


@pytest.fixture
def query_admin_api(http_client, admin, monkeypatch):
    async def query_admin_schema(
        query, variables=None, *, include_auth: bool = True, expect_error: bool = False
    ):
        if include_auth:
            monkeypatch.setattr(
                "misago.auth.auth.get_user_from_context",
                AsyncMock(return_value=admin),
            )

        async with http_client() as client:
            r = await client.post(
                "/admin/graphql/", json={"query": query, "variables": variables}
            )
            result = r.json()
            if not expect_error:
                assert not "errors" in result, "GraphQL query could not be completed"
            else:
                assert "errors" in result, "GraphQL expected to error"

            return result

    return query_admin_schema


@pytest.fixture
def query_public_api(http_client, monkeypatch):
    async def query_public_schema(
        query,
        variables=None,
        *,
        auth: Optional[User] = None,
        files=None,
    ):
        if auth:
            monkeypatch.setattr(
                "misago.auth.auth.get_user_from_context",
                AsyncMock(return_value=auth),
            )

        async with http_client() as client:
            files_map: dict = {}
            files_data: dict = {}

            if variables:
                extract_uploads_from_variables(files_map, files_data, variables)

            if files_map and files_data:
                r = await client.post(
                    "/graphql/",
                    data={
                        "operations": json.dumps(
                            {"query": query, "variables": variables}
                        ),
                        "map": json.dumps(files_map),
                    },
                    files=files_data,
                )
            else:
                r = await client.post(
                    "/graphql/", json={"query": query, "variables": variables}
                )

            return r.json()

    return query_public_schema


def extract_uploads_from_variables(
    files_map, files_data, variables, prefix="variables"
):
    for name, value in variables.items():
        if not isinstance(value, tuple) or len(value) != 3:
            continue

        index = str(len(files_map))
        files_map[index] = ["%s.%s" % (prefix, name)]
        files_data[index] = value
        variables[name] = None
