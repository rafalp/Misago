from unittest.mock import ANY

from ..choices import PollChoices


def test_poll_choices_from_sequence_initializes_choices_instance_from_sequence():
    poll_choices = PollChoices.from_sequence(("lorem", "ipsum", "dolor"))
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
