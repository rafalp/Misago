from ..choices import PollChoices
from ..forms import PollChoicesField


def test_poll_choices_field_clean_returns_only_new_choices():
    value = PollChoices()
    value.add("lorem")
    value.add("ipsum")

    field = PollChoicesField()
    data = field.clean(value)

    assert data
    assert not data.ids()
    assert data.names() == ["lorem", "ipsum"]


def test_poll_choices_field_clean_updates_initial_choices():
    initial = PollChoices(
        [
            {
                "id": "id1",
                "name": "first",
                "votes": 1,
            },
            {
                "id": "id2",
                "name": "second",
                "votes": 2,
            },
        ]
    )

    value = PollChoices(
        [
            {
                "id": "id1",
                "name": "first_updated",
            },
            {
                "id": "id2",
                "name": "second_updated",
            },
        ]
    )

    field = PollChoicesField(initial=initial)
    data = field.clean(value)

    assert data
    assert data.ids() == ["id1", "id2"]
    assert data.names() == ["first_updated", "second_updated"]


def test_poll_choices_field_clean_deletes_initial_choices():
    initial = PollChoices(
        [
            {
                "id": "id1",
                "name": "first",
                "votes": 1,
            },
            {
                "id": "id2",
                "name": "second",
                "votes": 2,
            },
        ]
    )

    value = PollChoices()
    value.add("third")

    field = PollChoicesField(initial=initial)
    data = field.clean(value)

    assert data
    assert not data.ids()
    assert data.names() == ["third"]


def test_poll_choices_field_clean_updates_one_initial_choice_and_deletes_other():
    initial = PollChoices(
        [
            {
                "id": "id1",
                "name": "first",
                "votes": 1,
            },
            {
                "id": "id2",
                "name": "second",
                "votes": 2,
            },
        ]
    )

    value = PollChoices(
        [
            {
                "id": "id1",
                "name": "first_updated",
            },
        ]
    )

    field = PollChoicesField(initial=initial)
    data = field.clean(value)

    assert data
    assert data.ids() == ["id1"]
    assert data.names() == ["first_updated"]


def test_poll_choices_field_clean_updates_one_initial_choice_deletes_other_and_adds_new():
    initial = PollChoices(
        [
            {
                "id": "id1",
                "name": "first",
                "votes": 1,
            },
            {
                "id": "id2",
                "name": "second",
                "votes": 2,
            },
        ]
    )

    value = PollChoices(
        [
            {
                "id": "id1",
                "name": "first_updated",
            },
        ]
    )
    value.add("third")

    field = PollChoicesField(initial=initial)
    data = field.clean(value)

    assert data
    assert data.ids() == ["id1"]
    assert data.names() == ["first_updated", "third"]
