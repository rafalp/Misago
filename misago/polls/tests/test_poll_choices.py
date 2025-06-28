from unittest.mock import ANY

import pytest

from ..choices import PollChoices


def test_poll_choices_is_falsy_if_empty():
    poll_choices = PollChoices()
    assert not poll_choices


def test_poll_choices_is_truthy_if_choices_exist():
    poll_choices = PollChoices(
        [
            {
                "id": "1",
                "name": "Lorem",
                "votes": 0,
            },
            {
                "id": "2",
                "name": "Ipsum",
                "votes": 0,
            },
        ],
    )
    assert poll_choices


def test_poll_choices_length_can_be_tested():
    poll_choices = PollChoices(
        [
            {
                "id": "1",
                "name": "Lorem",
                "votes": 0,
            },
            {
                "id": "2",
                "name": "Ipsum",
                "votes": 0,
            },
        ],
    )
    assert len(poll_choices) == 2


def test_poll_choices_supports_item_access():
    poll_choices = PollChoices(
        [
            {
                "id": "1",
                "name": "Lorem",
                "votes": 0,
            },
            {
                "id": "2",
                "name": "Ipsum",
                "votes": 0,
            },
        ],
    )

    assert poll_choices["2"] == {
        "id": "2",
        "name": "Ipsum",
        "votes": 0,
    }


def test_poll_choices_raises_key_error_on_non_existing_item_access():
    poll_choices = PollChoices(
        [
            {
                "id": "1",
                "name": "Lorem",
                "votes": 0,
            },
            {
                "id": "2",
                "name": "Ipsum",
                "votes": 0,
            },
        ],
    )

    with pytest.raises(KeyError):
        poll_choices["invalid"]


def test_poll_choices_supports_item_deletion():
    poll_choices = PollChoices(
        [
            {
                "id": "1",
                "name": "Lorem",
                "votes": 0,
            },
            {
                "id": "2",
                "name": "Ipsum",
                "votes": 0,
            },
        ],
    )

    del poll_choices["2"]

    assert poll_choices.ids() == ["1"]
    assert poll_choices.values() == [
        {
            "id": "1",
            "name": "Lorem",
            "votes": 0,
        },
    ]


def test_poll_choices_raises_key_error_on_non_existing_item_deletion():
    poll_choices = PollChoices(
        [
            {
                "id": "1",
                "name": "Lorem",
                "votes": 0,
            },
            {
                "id": "2",
                "name": "Ipsum",
                "votes": 0,
            },
        ],
    )

    with pytest.raises(KeyError):
        del poll_choices["invalid"]


def test_poll_choices_supports_membership_test():
    poll_choices = PollChoices(
        [
            {
                "id": "1",
                "name": "Lorem",
                "votes": 0,
            },
            {
                "id": "2",
                "name": "Ipsum",
                "votes": 0,
            },
        ],
    )

    assert "1" in poll_choices
    assert "3" not in poll_choices


def test_poll_choices_from_str_initializes_choices_instance_from_str():
    poll_choices = PollChoices.from_str("lorem\nipsum\ndolor")
    assert poll_choices.values() == [
        {
            "id": None,
            "name": "lorem",
        },
        {
            "id": None,
            "name": "ipsum",
        },
        {
            "id": None,
            "name": "dolor",
        },
    ]


def test_poll_choices_from_str_excludes_empty_lines():
    poll_choices = PollChoices.from_str("lorem\n\nipsum\n\n\ndolor\n\n")
    assert poll_choices.values() == [
        {
            "id": None,
            "name": "lorem",
        },
        {
            "id": None,
            "name": "ipsum",
        },
        {
            "id": None,
            "name": "dolor",
        },
    ]


def test_poll_choices_from_str_strips_items_whitespaces():
    poll_choices = PollChoices.from_str("lorem   \n\n   ipsum  \n\n   dolor")
    assert poll_choices.values() == [
        {
            "id": None,
            "name": "lorem",
        },
        {
            "id": None,
            "name": "ipsum",
        },
        {
            "id": None,
            "name": "dolor",
        },
    ]


def test_poll_choices_ids_returns_ids_list():
    poll_choices = PollChoices(
        [
            {
                "id": "123",
                "name": "lorem",
                "votes": 0,
            },
            {
                "id": "345",
                "name": "ipsum",
                "votes": 0,
            },
            {
                "id": "567",
                "name": "dolor",
                "votes": 0,
            },
        ]
    )
    assert poll_choices.ids() == ["123", "345", "567"]


def test_poll_choices_add_new_choice():
    poll_choices = PollChoices.from_str("lorem\n\nipsum\ndolor\n\n")
    poll_choices.add("met")
    poll_choices.add("elit")

    assert poll_choices.values() == [
        {
            "id": None,
            "name": "lorem",
        },
        {
            "id": None,
            "name": "ipsum",
        },
        {
            "id": None,
            "name": "dolor",
        },
        {
            "id": None,
            "name": "met",
        },
        {
            "id": None,
            "name": "elit",
        },
    ]


def test_poll_choices_names_returns_names_list():
    poll_choices = PollChoices.from_str("lorem   \n\n   ipsum  \n\n   dolor")
    assert poll_choices.names() == ["lorem", "ipsum", "dolor"]


def test_poll_choices_inputvalue_returns_str_for_textarea_value():
    poll_choices = PollChoices.from_str("lorem   \n\n   ipsum  \n\n   dolor")
    assert poll_choices.inputvalue() == "lorem\nipsum\ndolor"


def test_poll_choices_json_json_for_model_json_field():
    poll_choices = PollChoices.from_str("lorem   \n\n   ipsum  \n\n   dolor")

    choices_json = poll_choices.json()
    assert choices_json == [
        {
            "id": ANY,
            "name": "lorem",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "ipsum",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "dolor",
            "votes": 0,
        },
    ]

    assert [len(choice["id"]) for choice in choices_json] == [12, 12, 12]
