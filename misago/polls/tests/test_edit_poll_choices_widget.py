from ..fields import EditPollChoicesWidget, PollChoicesValue


def test_edit_poll_choices_widget_get_context_without_value():
    widget = EditPollChoicesWidget()
    context = widget.get_context("name", None, None)

    assert context == {
        "widget": {
            "attrs": {},
            "is_hidden": False,
            "name": "name",
            "new": {
                "attrs": {},
                "is_hidden": False,
                "name": "name_new",
                "required": False,
                "template_name": None,
                "value": [],
            },
            "new_noscript": {
                "attrs": {
                    "cols": "40",
                    "rows": "10",
                },
                "is_hidden": False,
                "name": "name_new_noscript",
                "required": False,
                "template_name": None,
                "value": None,
            },
            "edit": {
                "attrs": {},
                "is_hidden": False,
                "name": "name_edit",
                "required": False,
                "template_name": None,
                "value": {},
            },
            "delete": {
                "attrs": {},
                "is_hidden": False,
                "name": "name_delete",
                "required": False,
                "template_name": None,
                "value": [],
            },
            "choices": [],
            "required": False,
            "template_name": "misago/widgets/poll_choices.html",
        },
    }


def test_edit_poll_choices_widget_get_context_with_compressed_value():
    value = PollChoicesValue(
        choices=[
            {
                "id": "aaaaaaaaaaaa",
                "name": "First",
                "votes": 1,
            },
            {
                "id": "bbbbbbbbbbbb",
                "name": "Second",
                "votes": 2,
            },
            {
                "id": "cccccccccccc",
                "name": "Third",
                "votes": 3,
            },
        ],
        new=["Lorem", "Ipsum", "Dolor"],
        edit={"bbbbbbbbbbbb": "Edited"},
        delete=["cccccccccccc"],
    )

    widget = EditPollChoicesWidget()
    context = widget.get_context("name", value, None)

    assert context == {
        "widget": {
            "attrs": {},
            "is_hidden": False,
            "name": "name",
            "new": {
                "attrs": {},
                "is_hidden": False,
                "name": "name_new",
                "required": False,
                "template_name": None,
                "value": ["Lorem", "Ipsum", "Dolor"],
            },
            "new_noscript": {
                "attrs": {
                    "cols": "40",
                    "rows": "10",
                },
                "is_hidden": False,
                "name": "name_new_noscript",
                "required": False,
                "template_name": None,
                "value": "Lorem\nIpsum\nDolor",
            },
            "edit": {
                "attrs": {},
                "is_hidden": False,
                "name": "name_edit",
                "required": False,
                "template_name": None,
                "value": {
                    "aaaaaaaaaaaa": "First",
                    "bbbbbbbbbbbb": "Second",
                    "cccccccccccc": "Third",
                },
            },
            "delete": {
                "attrs": {},
                "is_hidden": False,
                "name": "name_delete",
                "required": False,
                "template_name": None,
                "value": {"cccccccccccc"},
            },
            "choices": [
                {
                    "checked": False,
                    "delete_name": "name_delete",
                    "edit_name": "name_edit[aaaaaaaaaaaa]",
                    "id": "aaaaaaaaaaaa",
                    "value": "First",
                },
                {
                    "checked": False,
                    "delete_name": "name_delete",
                    "edit_name": "name_edit[bbbbbbbbbbbb]",
                    "id": "bbbbbbbbbbbb",
                    "value": "Second",
                },
                {
                    "checked": True,
                    "delete_name": "name_delete",
                    "edit_name": "name_edit[cccccccccccc]",
                    "id": "cccccccccccc",
                    "value": "Third",
                },
            ],
            "required": False,
            "template_name": "misago/widgets/poll_choices.html",
        },
    }


def test_edit_poll_choices_widget_get_context_with_decompressed_value():
    value = [
        ["Lorem", "Ipsum", "Dolor"],
        ["Met", "Sit", "Amet"],
        {"bbbbbbbbbbbb": "Edited"},
        ["cccccccccccc"],
    ]

    widget = EditPollChoicesWidget()
    context = widget.get_context("name", value, None)

    assert context == {
        "widget": {
            "attrs": {},
            "is_hidden": False,
            "name": "name",
            "new": {
                "attrs": {},
                "is_hidden": False,
                "name": "name_new",
                "required": False,
                "template_name": None,
                "value": ["Lorem", "Ipsum", "Dolor"],
            },
            "new_noscript": {
                "attrs": {
                    "cols": "40",
                    "rows": "10",
                },
                "is_hidden": False,
                "name": "name_new_noscript",
                "required": False,
                "template_name": None,
                "value": "Met\nSit\nAmet",
            },
            "edit": {
                "attrs": {},
                "is_hidden": False,
                "name": "name_edit",
                "required": False,
                "template_name": None,
                "value": {"bbbbbbbbbbbb": "Edited"},
            },
            "delete": {
                "attrs": {},
                "is_hidden": False,
                "name": "name_delete",
                "required": False,
                "template_name": None,
                "value": [
                    "cccccccccccc",
                ],
            },
            "choices": [
                {
                    "checked": False,
                    "delete_name": "name_delete",
                    "edit_name": "name_edit[bbbbbbbbbbbb]",
                    "id": "bbbbbbbbbbbb",
                    "value": "Edited",
                },
            ],
            "required": False,
            "template_name": "misago/widgets/poll_choices.html",
        },
    }


def test_edit_poll_choices_widget_decompress_none():
    widget = EditPollChoicesWidget()
    assert widget.decompress(None) == [[], [], {}, set()]


def test_edit_poll_choices_widget_decompress_poll_choices_value():
    value = PollChoicesValue(
        choices=[
            {
                "id": "aaaaaaaaaaaa",
                "name": "First",
                "votes": 1,
            },
            {
                "id": "bbbbbbbbbbbb",
                "name": "Second",
                "votes": 2,
            },
            {
                "id": "cccccccccccc",
                "name": "Third",
                "votes": 3,
            },
        ],
        new=["Lorem", "Ipsum", "Dolor"],
        edit={"bbbbbbbbbbbb": "Edited"},
        delete=["cccccccccccc"],
    )
    widget = EditPollChoicesWidget()
    assert widget.decompress(value) == [
        ["Lorem", "Ipsum", "Dolor"],
        ["Lorem", "Ipsum", "Dolor"],
        {
            "aaaaaaaaaaaa": "First",
            "bbbbbbbbbbbb": "Second",
            "cccccccccccc": "Third",
        },
        {"cccccccccccc"},
    ]
