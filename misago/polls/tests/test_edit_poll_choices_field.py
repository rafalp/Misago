from django.forms import Form

from ..fields import EditPollChoicesField, PollChoicesValue


def test_edit_poll_choices_field_widget_attrs_returns_max_choices():
    field = EditPollChoicesField(max_choices=10)
    assert field.widget_attrs(None) == {"max_choices": 10}


def test_edit_poll_choices_field_bound_data_returns_bound_data_without_initial_value():
    field = EditPollChoicesField(max_choices=10)
    data = field.bound_data([[], [], {}, set()], None)
    assert data == [[], [], {}, set()]


def test_edit_poll_choices_field_bound_data_returns_default_data_if_field_is_disabled():
    field = EditPollChoicesField(disabled=True)
    data = field.bound_data(None, None)
    assert data == [[], [], {}, set()]


def test_edit_poll_choices_field_bound_data_returns_initial_data_if_field_is_disabled():
    field = EditPollChoicesField(
        disabled=True,
        initial=PollChoicesValue(
            choices=[
                {
                    "id": "aaaaaaaaaaaa",
                    "name": "Lorem",
                    "values": 1,
                },
                {
                    "id": "bbbbbbbbbbbb",
                    "name": "Ipsum",
                    "values": 2,
                },
                {
                    "id": "cccccccccccc",
                    "name": "Dolor",
                    "values": 3,
                },
            ],
            new=["Lorem", "Ipsum"],
            delete=["cccccccccccc"],
        ),
    )
    data = field.bound_data(None, field.initial)
    assert data == [
        ["Lorem", "Ipsum"],
        ["Lorem", "Ipsum"],
        {
            "aaaaaaaaaaaa": "Lorem",
            "bbbbbbbbbbbb": "Ipsum",
            "cccccccccccc": "Dolor",
        },
        {"cccccccccccc"},
    ]


def test_edit_poll_choices_field_bound_data_returns_new_data_if_initial_is_not_set():
    field = EditPollChoicesField()
    data = field.bound_data(
        [
            ["New"],
            ["Other"],
            {"aaaaaaaaaaaa": "", "bbbbbbbbbbbb": "Edited"},
            {"cccccccccccc"},
        ],
        field.initial,
    )
    assert data == [
        ["New"],
        ["Other"],
        {"aaaaaaaaaaaa": "", "bbbbbbbbbbbb": "Edited"},
        {"cccccccccccc"},
    ]


def test_edit_poll_choices_field_bound_data_returns_new_and_initial_data_combined():
    field = EditPollChoicesField(
        initial=PollChoicesValue(
            choices=[
                {
                    "id": "aaaaaaaaaaaa",
                    "name": "Lorem",
                    "values": 1,
                },
                {
                    "id": "bbbbbbbbbbbb",
                    "name": "Ipsum",
                    "values": 2,
                },
                {
                    "id": "cccccccccccc",
                    "name": "Dolor",
                    "values": 3,
                },
            ],
            new=["Lorem", "Ipsum"],
            delete=["cccccccccccc"],
        ),
    )
    data = field.bound_data(
        [
            ["New"],
            ["Other"],
            {"aaaaaaaaaaaa": "", "bbbbbbbbbbbb": "Edited"},
            {"cccccccccccc"},
        ],
        field.initial,
    )
    assert data == [
        ["New"],
        ["Other"],
        {
            "aaaaaaaaaaaa": "Lorem",
            "bbbbbbbbbbbb": "Edited",
            "cccccccccccc": "Dolor",
        },
        {"cccccccccccc"},
    ]


def test_edit_poll_choices_field_compress_returns_empty_poll_choices_value_from_none():
    field = EditPollChoicesField(max_choices=10)
    value = field.compress(None)

    assert isinstance(value, PollChoicesValue)
    assert not value
    assert value.new == []
    assert value.edit == {}
    assert value.delete == set()


def test_edit_poll_choices_field_compress_returns_poll_choices_value_from_none_and_initial_value():
    field = EditPollChoicesField(
        max_choices=10,
        initial=PollChoicesValue(
            choices=[
                {
                    "id": "aaaaaaaaaaaa",
                    "name": "Lorem",
                    "values": 1,
                },
                {
                    "id": "bbbbbbbbbbbb",
                    "name": "Ipsum",
                    "values": 2,
                },
                {
                    "id": "cccccccccccc",
                    "name": "Dolor",
                    "values": 3,
                },
            ],
        ),
    )
    value = field.compress(None)

    assert isinstance(value, PollChoicesValue)
    assert value
    assert value.choices == [
        {
            "id": "aaaaaaaaaaaa",
            "name": "Lorem",
            "values": 1,
        },
        {
            "id": "bbbbbbbbbbbb",
            "name": "Ipsum",
            "values": 2,
        },
        {
            "id": "cccccccccccc",
            "name": "Dolor",
            "values": 3,
        },
    ]
    assert value.new == []
    assert value.edit == {}
    assert value.delete == set()


def test_edit_poll_choices_field_compress_returns_poll_choices_value_from_list():
    field = EditPollChoicesField(max_choices=10)
    value = field.compress(
        [
            ["Lorem", "Ipsum"],
            ["Dolor", "Met"],
            {"aaaaaaaaaaaa": "Edited"},
            {"cccccccccccc"},
        ]
    )

    assert isinstance(value, PollChoicesValue)
    assert value
    assert value.new == ["Lorem", "Ipsum"]
    assert value.edit == {"aaaaaaaaaaaa": "Edited"}
    assert value.delete == {"cccccccccccc"}


def test_edit_poll_choices_field_compress_returns_poll_choices_value_from_list_and_initial_value():
    field = EditPollChoicesField(
        max_choices=10,
        initial=PollChoicesValue(
            choices=[
                {
                    "id": "aaaaaaaaaaaa",
                    "name": "Lorem",
                    "values": 1,
                },
                {
                    "id": "bbbbbbbbbbbb",
                    "name": "Ipsum",
                    "values": 2,
                },
                {
                    "id": "cccccccccccc",
                    "name": "Dolor",
                    "values": 3,
                },
            ],
        ),
    )
    value = field.compress(
        [
            ["Lorem", "Ipsum"],
            ["Dolor", "Met"],
            {"aaaaaaaaaaaa": "Edited"},
            {"cccccccccccc"},
        ]
    )

    assert isinstance(value, PollChoicesValue)
    assert value
    assert value.choices == [
        {
            "id": "aaaaaaaaaaaa",
            "name": "Lorem",
            "values": 1,
        },
        {
            "id": "bbbbbbbbbbbb",
            "name": "Ipsum",
            "values": 2,
        },
        {
            "id": "cccccccccccc",
            "name": "Dolor",
            "values": 3,
        },
    ]
    assert value.new == ["Lorem", "Ipsum"]
    assert value.edit == {"aaaaaaaaaaaa": "Edited"}
    assert value.delete == {"cccccccccccc"}


def test_edit_poll_choices_field_get_bound_field_returns_bound_field_with_max_choices_attr():
    class TestForm(Form):
        field = EditPollChoicesField(max_choices=10)

    form = TestForm()
    bound_field = form.fields["field"].get_bound_field(form, "field")

    assert bound_field.max_choices == 10
