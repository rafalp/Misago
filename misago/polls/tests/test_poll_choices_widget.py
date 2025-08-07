from ..fields import PollChoicesWidget, PollChoicesValue


def test_poll_choices_widget_get_context_without_value():
    widget = PollChoicesWidget()
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
            "required": False,
            "template_name": "misago/widgets/poll_choices.html",
        },
    }


def test_poll_choices_widget_get_context_with_compressed_value():
    value = PollChoicesValue(new=["Lorem", "Ipsum", "Dolor"])

    widget = PollChoicesWidget()
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
            "required": False,
            "template_name": "misago/widgets/poll_choices.html",
        },
    }


def test_poll_choices_widget_get_context_with_decompressed_value():
    value = [
        ["Lorem", "Ipsum", "Dolor"],
        ["Met", "Sit", "Amet"],
    ]

    widget = PollChoicesWidget()
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
            "required": False,
            "template_name": "misago/widgets/poll_choices.html",
        },
    }


def test_poll_choices_widget_decompress_none():
    widget = PollChoicesWidget()
    assert widget.decompress(None) == [[], []]


def test_poll_choices_widget_decompress_poll_choices_value():
    value = PollChoicesValue(new=["Lorem", "Ipsum", "Dolor"])
    widget = PollChoicesWidget()
    assert widget.decompress(value) == [
        ["Lorem", "Ipsum", "Dolor"],
        ["Lorem", "Ipsum", "Dolor"],
    ]
