import pytest

from ..hooks import ActionHook


class MockActionHook(ActionHook):
    def call_action(self, base: str):
        return self.call(base)


def lowercase_action(base: str) -> str:
    return base.lower()


def uppercase_action(base: str) -> str:
    return base.upper()


@pytest.fixture
def hook():
    return MockActionHook()


def test_action_hook_without_actions_returns_empty_list(hook):
    assert hook.call_action("TeSt") == []


def test_action_hook_calls_action_and_returns_its_result(hook):
    hook.append(lowercase_action)
    assert hook.call_action("TeSt") == ["test"]


def test_action_hook_calls_multiple_actions_and_returns_their_results(hook):
    hook.append(lowercase_action)
    hook.append(uppercase_action)
    assert hook.call_action("TeSt") == ["test", "TEST"]


def test_action_hook_action_can_be_prepended_before_other_actions(hook):
    hook.append(lowercase_action)
    hook.prepend(uppercase_action)
    assert hook.call_action("TeSt") == ["TEST", "test"]
