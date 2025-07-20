from django.forms import Form

from ..fields import PollChoicesField, PollChoicesValue


def test_poll_choices_field_widget_attrs_returns_max_choices():
    field = PollChoicesField(max_choices=10)
    assert field.widget_attrs(None) == {"max_choices": 10}


def test_poll_choices_field_compress_returns_empty_poll_choices_value_from_bone():
    field = PollChoicesField(max_choices=10)
    value = field.compress(None)

    assert isinstance(value, PollChoicesValue)
    assert not value
    assert value.new == []


def test_poll_choices_field_compress_returns_poll_choices_value_from_list():
    field = PollChoicesField(max_choices=10)
    value = field.compress([["Lorem", "Ipsum"], ["Dolor", "Met"]])

    assert isinstance(value, PollChoicesValue)
    assert value
    assert value.new == ["Lorem", "Ipsum"]


def test_poll_choices_field_get_bound_field_returns_bound_field_with_max_choices_attr():
    class TestForm(Form):
        field = PollChoicesField(max_choices=10)

    form = TestForm()
    bound_field = form.fields["field"].get_bound_field(form, "field")

    assert bound_field.max_choices == 10
