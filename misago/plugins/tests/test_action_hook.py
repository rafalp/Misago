import pytest

from ..hooks import ActionHook


class MockActionHook(ActionHook):
    def __call__(self, base: str):
        return super().__call__(base)


def lowercase_action(base: str) -> str:
    return base.lower()


def uppercase_action(base: str) -> str:
    return base.upper()


def reverse_action(base: str) -> str:
    return "".join(reversed(base))


@pytest.fixture
def hook():
    return MockActionHook()


def test_action_hook_without_actions_returns_empty_list(hook):
    assert hook("TeSt") == []


def test_action_hook_without_actions_is_falsy(hook):
    assert not hook


def test_action_hook_with_actions_is_truthy(hook):
    hook.append_action(lowercase_action)
    assert hook


def test_action_hook_calls_action_and_returns_its_result(hook):
    hook.append_action(lowercase_action)
    assert hook("TeSt") == ["test"]


def test_action_hook_calls_multiple_actions_and_returns_their_results(hook):
    hook.append_action(lowercase_action)
    hook.append_action(uppercase_action)
    assert hook("TeSt") == ["test", "TEST"]


def test_action_hook_action_can_be_prepended_before_other_actions(hook):
    hook.prepend_action(uppercase_action)
    hook.append_action(lowercase_action)
    hook.prepend_action(reverse_action)
    assert hook("TeSt") == ["tSeT", "TEST", "test"]
