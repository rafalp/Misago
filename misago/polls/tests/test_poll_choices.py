from unittest.mock import ANY

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


def test_poll_choices_from_str_initializes_choices_instance_from_str():
    poll_choices = PollChoices.from_str("lorem\nipsum\ndolor")
    assert len(poll_choices.choices) == 3

    choices_list = list(poll_choices.choices.values())
    assert choices_list == [
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

    choices_ids = set(choice["id"] for choice in choices_list)
    assert len(choices_ids) == 3
    assert [len(choice_id) for choice_id in choices_ids] == [12, 12, 12]


def test_poll_choices_from_str_excludes_empty_lines():
    poll_choices = PollChoices.from_str("lorem\n\nipsum\n\n\ndolor\n\n")
    assert len(poll_choices.choices) == 3

    choices_list = list(poll_choices.choices.values())
    assert choices_list == [
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

    choices_ids = set(choice["id"] for choice in choices_list)
    assert len(choices_ids) == 3
    assert [len(choice_id) for choice_id in choices_ids] == [12, 12, 12]


def test_poll_choices_from_str_excludes_duplicates():
    poll_choices = PollChoices.from_str("lorem\n\nipsum\n\nlorem\ndolor\n\n")
    assert len(poll_choices.choices) == 3

    choices_list = list(poll_choices.choices.values())
    assert choices_list == [
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

    choices_ids = set(choice["id"] for choice in choices_list)
    assert len(choices_ids) == 3
    assert [len(choice_id) for choice_id in choices_ids] == [12, 12, 12]


def test_poll_choices_from_str_strips_items_whitespaces():
    poll_choices = PollChoices.from_str("lorem   \n\n   ipsum  \n\n   dolor")
    assert len(poll_choices.choices) == 3

    choices_list = list(poll_choices.choices.values())
    assert choices_list == [
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

    choices_ids = set(choice["id"] for choice in choices_list)
    assert len(choices_ids) == 3
    assert [len(choice_id) for choice_id in choices_ids] == [12, 12, 12]


def test_poll_choices_get_names_returns_names_list():
    poll_choices = PollChoices.from_str("lorem   \n\n   ipsum  \n\n   dolor")
    assert poll_choices.get_names() == ["lorem", "ipsum", "dolor"]


def test_poll_choices_get_str_returns_str_for_textarea_value():
    poll_choices = PollChoices.from_str("lorem   \n\n   ipsum  \n\n   dolor")
    assert poll_choices.get_str() == "lorem\nipsum\ndolor"


def test_poll_choices_get_list_returns_json_for_model_json_field():
    poll_choices = PollChoices.from_str("lorem   \n\n   ipsum  \n\n   dolor")
    assert poll_choices.get_list() == [
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
