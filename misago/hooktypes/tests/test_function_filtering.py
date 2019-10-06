from unittest.mock import Mock

from ..applyfilters import apply_filters


def test_filtering_calls_action_with_given_args():
    action = Mock()
    apply_filters(action, [], 1, 2)
    action.assert_called_once_with(1, 2)


def test_filtering_calls_action_with_given_kwargs():
    action = Mock()
    apply_filters(action, [], a=1, b=2)
    action.assert_called_once_with(a=1, b=2)


def test_filtering_returns_action_return_value():
    action = Mock(return_value=42)
    assert apply_filters(action, []) == 42


def test_filter_is_called_with_action_as_first_arg():
    filter_ = Mock()
    action = Mock()
    apply_filters(action, [filter_])
    filter_.assert_called_once_with(action)


def test_filter_is_called_with_given_args():
    filter_ = Mock()
    action = Mock()
    apply_filters(action, [filter_], 1, 2)
    filter_.assert_called_once_with(action, 1, 2)


def test_filter_is_called_with_given_kwargs():
    filter_ = Mock()
    action = Mock()
    apply_filters(action, [filter_], a=1, b=2)
    filter_.assert_called_once_with(action, a=1, b=2)


def test_filters_are_chained():
    action = Mock(return_value=1)

    def multiply_filter(action):
        return action() * 2

    assert apply_filters(action, [multiply_filter, multiply_filter]) == 4
