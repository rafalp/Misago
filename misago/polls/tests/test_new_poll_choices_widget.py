from django.http import QueryDict

from ..choices import PollChoices
from ..forms import NewPollChoicesWidget


def test_new_poll_choices_widget_returns_empty_poll_choices_for_empty_query_dict():
    widget = NewPollChoicesWidget()
    result = widget.value_from_datadict(QueryDict(), {}, "choices")

    assert isinstance(result, PollChoices)
    assert not result
    assert not result.ids()
    assert not result.names()


def test_new_poll_choices_widget_returns_one_new_poll_choice_from_query_dict():
    widget = NewPollChoicesWidget()
    result = widget.value_from_datadict(QueryDict("choices=first"), {}, "choices")

    assert isinstance(result, PollChoices)
    assert result
    assert not result.ids()
    assert result.names() == ["first"]


def test_new_poll_choices_widget_strips_whitespace_from_choice_names():
    widget = NewPollChoicesWidget()
    result = widget.value_from_datadict(QueryDict("choices=  first   "), {}, "choices")

    assert isinstance(result, PollChoices)
    assert result
    assert not result.ids()
    assert result.names() == ["first"]


def test_new_poll_choices_widget_returns_multiple_new_poll_choices_from_query_dict():
    widget = NewPollChoicesWidget()
    result = widget.value_from_datadict(
        QueryDict("choices=first&choices=second&choices=third"),
        {},
        "choices",
    )

    assert isinstance(result, PollChoices)
    assert result
    assert not result.ids()
    assert result.names() == ["first", "second", "third"]


def test_new_poll_choices_widget_skips_empty_new_poll_choices():
    widget = NewPollChoicesWidget()
    result = widget.value_from_datadict(
        QueryDict("choices=first&choices=second&choices="),
        {},
        "choices",
    )

    assert isinstance(result, PollChoices)
    assert result
    assert not result.ids()
    assert result.names() == ["first", "second"]
