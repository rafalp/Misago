import pytest

from ..threads import load_updated_threads_count


@pytest.mark.asyncio
async def test_loader_returns_0_when_no_threads_exist(graphql_context):
    updated_threads = await load_updated_threads_count(graphql_context, 1)
    assert updated_threads == 0


@pytest.mark.asyncio
async def test_loader_returns_1_when_there_are_updated_threads(
    graphql_context, thread, reply
):
    updated_threads = await load_updated_threads_count(
        graphql_context, thread.first_post_id
    )
    assert updated_threads == 1
