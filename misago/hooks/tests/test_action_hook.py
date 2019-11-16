import pytest

from ..action import ActionHook


class MockActionHook(ActionHook):
    async def call_action(self, base):
        return await super().call_action(base)


async def lowercase_action(base: str) -> str:
    return base.lower()


async def uppercase_action(base: str) -> str:
    return base.upper()


@pytest.fixture
def hook():
    return MockActionHook()


@pytest.mark.asyncio
async def test_action_hook_without_actions_returns_empty_list(hook):
    assert await hook.call_action("TeSt") == []


@pytest.mark.asyncio
async def test_action_hook_calls_action_and_returns_its_result(hook):
    hook.append(lowercase_action)
    assert await hook.call_action("TeSt") == ["test"]


@pytest.mark.asyncio
async def test_action_hook_calls_multiple_actions_and_returns_their_results(hook):
    hook.append(lowercase_action)
    hook.append(uppercase_action)
    assert await hook.call_action("TeSt") == ["test", "TEST"]


@pytest.mark.asyncio
async def test_action_hook_action_can_be_prepended_before_other_actions(hook):
    hook.append(lowercase_action)
    hook.prepend(uppercase_action)
    assert await hook.call_action("TeSt") == ["TEST", "test"]
