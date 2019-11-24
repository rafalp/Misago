from unittest.mock import Mock

import pytest

from .context import get_graphql_context


@pytest.fixture
async def graphql_context(db):
    context = {}
    await get_graphql_context(None, context)
    return context


@pytest.fixture
def graphql_info(graphql_context):
    return Mock(context=graphql_context)
