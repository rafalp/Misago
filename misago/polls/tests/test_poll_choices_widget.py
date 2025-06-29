from django.http import QueryDict

from ..choices import PollChoices
from ..forms import PollChoicesWidget


def test_poll_choices_widget_returns_empty_poll_choices_for_empty_query_dict():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(QueryDict(), {}, "choices")

    assert isinstance(result, PollChoices)
    assert not result
    assert not result.ids()
    assert not result.names()


def test_poll_choices_widget_returns_one_new_poll_choice_from_query_dict():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(QueryDict("choices[]=first"), {}, "choices")

    assert isinstance(result, PollChoices)
    assert result
    assert not result.ids()
    assert result.names() == ["first"]


def test_poll_choices_widget_strips_whitespace_from_choice_names():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(
        QueryDict("choices[]=  first   "), {}, "choices"
    )

    assert isinstance(result, PollChoices)
    assert result
    assert not result.ids()
    assert result.names() == ["first"]


def test_poll_choices_widget_returns_multiple_new_poll_choices_from_query_dict():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(
        QueryDict("choices[]=first&choices[]=second&choices[]=third"),
        {},
        "choices",
    )

    assert isinstance(result, PollChoices)
    assert result
    assert not result.ids()
    assert result.names() == ["first", "second", "third"]


def test_poll_choices_widget_skips_empty_new_poll_choices():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(
        QueryDict("choices[]=first&choices[]=second&choices[]="),
        {},
        "choices",
    )

    assert isinstance(result, PollChoices)
    assert result
    assert not result.ids()
    assert result.names() == ["first", "second"]


def test_poll_choices_widget_skips_poll_choices_without_braces():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(
        QueryDict("choices=first&choices=second&choices=third"),
        {},
        "choices",
    )

    assert isinstance(result, PollChoices)
    assert not result
    assert not result.ids()
    assert not result.names()


def test_poll_choices_widget_returns_one_existing_poll_choice_from_query_dict():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(
        QueryDict("choices[id123]=first"), {}, "choices"
    )

    assert isinstance(result, PollChoices)
    assert result
    assert result.ids() == ["id123"]
    assert result.names() == ["first"]


def test_poll_choices_widget_strips_whitespace_from_choice_ids():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(
        QueryDict("choices[ id123   ]=first"), {}, "choices"
    )

    assert isinstance(result, PollChoices)
    assert result
    assert result.ids() == ["id123"]
    assert result.names() == ["first"]


def test_poll_choices_widget_skips_duplicate_choice_ids():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(
        QueryDict("choices[id123]=first&choices[id123]=second"), {}, "choices"
    )

    assert isinstance(result, PollChoices)
    assert result
    assert result.ids() == ["id123"]
    assert result.names() == ["second"]


def test_poll_choices_widget_sets_empty_choices_with_ids():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(QueryDict("choices[id123]="), {}, "choices")

    assert isinstance(result, PollChoices)
    assert result
    assert result.ids() == ["id123"]
    assert result.names() == [""]


def test_poll_choices_widget_returns_new_and_existing_choices_from_query_dict():
    widget = PollChoicesWidget()
    result = widget.value_from_datadict(
        QueryDict(
            "choices[id123]=lorem&choices[id321]=ipsum&choices[]=dolor&choices[]=met"
        ),
        {},
        "choices",
    )

    assert isinstance(result, PollChoices)
    assert result
    assert result.ids() == ["id123", "id321"]
    assert result.names() == ["lorem", "ipsum", "dolor", "met"]
