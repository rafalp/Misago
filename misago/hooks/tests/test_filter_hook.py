import pytest

from ..filter import FilterHook


ACTION = 0
FIRST_FILTER = 1
SECOND_FILTER = 2


class MockFilterHook(FilterHook):
    async def call_action(self, action):
        return await self.filter(action, [])


async def action(data):
    data.append(ACTION)
    return data


async def first_filter(action, data):
    data = await action(data)
    data.append(FIRST_FILTER)
    return data


async def second_filter(action, data):
    data = await action(data)
    data.append(SECOND_FILTER)
    return data


@pytest.fixture
def hook():
    return MockFilterHook()


@pytest.mark.asyncio
async def test_filter_hook_without_filters_just_calls_action(hook):
    assert await hook.call_action(action) == [ACTION]


@pytest.mark.asyncio
async def test_filter_hook_calls_filter_before_action(hook):
    hook.append(first_filter)
    assert await hook.call_action(action) == [ACTION, FIRST_FILTER]


@pytest.mark.asyncio
async def test_filter_hook_calls_filters_in_order_of_adding(hook):
    hook.append(first_filter)
    hook.append(second_filter)
    assert await hook.call_action(action) == [ACTION, FIRST_FILTER, SECOND_FILTER]


@pytest.mark.asyncio
async def test_filter_can_be_inserted_before_other_filters(hook):
    hook.append(first_filter)
    hook.prepend(second_filter)
    assert await hook.call_action(action) == [ACTION, SECOND_FILTER, FIRST_FILTER]
