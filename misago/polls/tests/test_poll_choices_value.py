from unittest.mock import ANY

from ..fields import PollChoicesValue


def test_poll_choices_value_empty_is_false():
    assert not PollChoicesValue()


def test_poll_choices_value_with_choices_is_true():
    assert PollChoicesValue(
        choices=[
            {
                "id": "aaaaaaaaaaaa",
                "name": "Lorem",
                "votes": 0,
            },
        ],
    )


def test_poll_choices_value_with_new_choices_is_true():
    assert PollChoicesValue(new=["Lorem", "Ipsum"])


def test_poll_choices_value_with_all_choices_deleted_is_false():
    assert not PollChoicesValue(
        choices=[
            {
                "id": "aaaaaaaaaaaa",
                "name": "Lorem",
                "votes": 0,
            },
        ],
        delete=["aaaaaaaaaaaa"],
    )


def test_poll_choices_value_json_getter_returns_json_with_new_choices():
    data = PollChoicesValue(new=["Lorem", "Ipsum"]).json()
    assert data == [
        {
            "id": ANY,
            "name": "Lorem",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Ipsum",
            "votes": 0,
        },
    ]

    assert [len(choice["id"]) for choice in data] == [12, 12]


def test_poll_choices_value_json_getter_returns_json_with_existing_choices():
    data = PollChoicesValue(
        choices=[
            {
                "id": "aaaaaaaaaaaa",
                "name": "Lorem",
                "votes": 2,
            },
            {
                "id": "bbbbbbbbbbbb",
                "name": "Dolor",
                "votes": 3,
            },
        ],
    ).json()

    assert data == [
        {
            "id": "aaaaaaaaaaaa",
            "name": "Lorem",
            "votes": 2,
        },
        {
            "id": "bbbbbbbbbbbb",
            "name": "Dolor",
            "votes": 3,
        },
    ]


def test_poll_choices_value_json_getter_returns_json_with_existing_and_new_choices():
    data = PollChoicesValue(
        choices=[
            {
                "id": "aaaaaaaaaaaa",
                "name": "Lorem",
                "votes": 2,
            },
            {
                "id": "bbbbbbbbbbbb",
                "name": "Dolor",
                "votes": 3,
            },
        ],
        new=["Extra", "Another"],
    ).json()

    assert data == [
        {
            "id": "aaaaaaaaaaaa",
            "name": "Lorem",
            "votes": 2,
        },
        {
            "id": "bbbbbbbbbbbb",
            "name": "Dolor",
            "votes": 3,
        },
        {
            "id": ANY,
            "name": "Extra",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Another",
            "votes": 0,
        },
    ]

    assert [len(choice["id"]) for choice in data] == [12, 12, 12, 12]


def test_poll_choices_value_json_getter_returns_json_with_existing_and_deleted_choices():
    data = PollChoicesValue(
        choices=[
            {
                "id": "aaaaaaaaaaaa",
                "name": "Lorem",
                "votes": 2,
            },
            {
                "id": "bbbbbbbbbbbb",
                "name": "Dolor",
                "votes": 3,
            },
        ],
        delete=["aaaaaaaaaaaa"],
    ).json()

    assert data == [
        {
            "id": "bbbbbbbbbbbb",
            "name": "Dolor",
            "votes": 3,
        },
    ]


def test_poll_choices_value_json_getter_returns_json_with_existing_new_and_deleted_choices():
    data = PollChoicesValue(
        choices=[
            {
                "id": "aaaaaaaaaaaa",
                "name": "Lorem",
                "votes": 2,
            },
            {
                "id": "bbbbbbbbbbbb",
                "name": "Dolor",
                "votes": 3,
            },
        ],
        new=["Extra", "Another"],
        delete=["aaaaaaaaaaaa"],
    ).json()

    assert data == [
        {
            "id": "bbbbbbbbbbbb",
            "name": "Dolor",
            "votes": 3,
        },
        {
            "id": ANY,
            "name": "Extra",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Another",
            "votes": 0,
        },
    ]

    assert [len(choice["id"]) for choice in data] == [12, 12, 12]


def test_poll_choices_value_json_getter_returns_json_with_existing_and_edited_choices():
    data = PollChoicesValue(
        choices=[
            {
                "id": "aaaaaaaaaaaa",
                "name": "Lorem",
                "votes": 2,
            },
            {
                "id": "bbbbbbbbbbbb",
                "name": "Dolor",
                "votes": 3,
            },
        ],
        edit={"bbbbbbbbbbbb": "Edited"},
    ).json()

    assert data == [
        {
            "id": "aaaaaaaaaaaa",
            "name": "Lorem",
            "votes": 2,
        },
        {
            "id": "bbbbbbbbbbbb",
            "name": "Edited",
            "votes": 3,
        },
    ]


def test_poll_choices_value_json_getter_returns_json_with_existing_edited_deleted_new_choices():
    data = PollChoicesValue(
        choices=[
            {
                "id": "aaaaaaaaaaaa",
                "name": "Lorem",
                "votes": 2,
            },
            {
                "id": "bbbbbbbbbbbb",
                "name": "Dolor",
                "votes": 3,
            },
        ],
        edit={"aaaaaaaaaaaa": "Okay", "bbbbbbbbbbbb": "Edited"},
        delete=["aaaaaaaaaaaa"],
        new=["Another"],
    ).json()

    assert data == [
        {
            "id": "bbbbbbbbbbbb",
            "name": "Edited",
            "votes": 3,
        },
        {
            "id": ANY,
            "name": "Another",
            "votes": 0,
        },
    ]

    assert [len(choice["id"]) for choice in data] == [12, 12]
