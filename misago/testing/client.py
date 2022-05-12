import json
from typing import Optional
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from ..asgi import app
from ..users.models import User


@pytest.fixture
def graphql_info(context):
    return Mock(context=context)


@pytest.fixture
def user_graphql_info(user_context):
    return Mock(context=user_context)


@pytest.fixture
def moderator_graphql_info(moderator_context):
    return Mock(context=moderator_context)


@pytest.fixture
def admin_graphql_info(admin_context):
    return Mock(context=admin_context)


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
        files_map[index] = [f"{prefix}.{name}"]
        files_data[index] = value
        variables[name] = None
