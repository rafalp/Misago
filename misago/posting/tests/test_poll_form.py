from unittest.mock import ANY

from ...conf.test import override_dynamic_settings
from ...polls.enums import PublicPollsAvailability
from ..forms import PollForm


def test_poll_form_sets_request(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PollForm(request=request)
    assert form.request is request


@override_dynamic_settings(poll_question_max_length=42)
def test_poll_form_sets_question_max_length_from_setting(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PollForm(request=request)
    assert form.fields["question"].max_length == 42


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.ENABLED)
def test_poll_form_includes_public_voting_option_if_its_enabled(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PollForm(request=request)
    assert "is_public" in form.fields


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.DISABLED)
def test_poll_form_removes_public_voting_option_if_they_are_forbidden(
    rf, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PollForm(request=request)
    assert "is_public" not in form.fields


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.DISABLED_NEW)
def test_poll_form_removes_public_voting_option_if_new_are_forbidden(
    rf, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PollForm(request=request)
    assert "is_public" not in form.fields


def test_poll_form_validation_without_data_passes(rf, dynamic_settings):
    request = rf.post("/")
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert form.is_valid()


def test_poll_form_validation_with_empty_data_passes(rf, dynamic_settings):
    request = rf.post(
        "/",
        {
            "question": "",
            "choices_new": [],
            "choices_new_noscript": "",
            "duration": "",
            "max_choices": "",
        },
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert form.is_valid()


def test_poll_form_validation_requires_choices_if_question_is_set(rf, dynamic_settings):
    request = rf.post(
        "/",
        {
            "question": "Lorem ipsum",
            "choices_new": [],
            "choices_new_noscript": "",
            "duration": "",
            "max_choices": "",
        },
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {
        "choices": ["This field is required."],
    }


def test_poll_form_validation_requires_question_if_choices_list_is_set(
    rf, dynamic_settings
):
    request = rf.post(
        "/",
        {
            "question": "",
            "choices_new": ["Lorem", "Ipsum"],
            "choices_new_noscript": "",
            "duration": "",
            "max_choices": "",
        },
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"question": ["This field is required."]}


def test_poll_form_validation_requires_question_if_choices_text_is_set(
    rf, dynamic_settings
):
    request = rf.post(
        "/",
        {
            "question": "",
            "choices_new": [],
            "choices_new_noscript": "Lorem\nIpsum",
            "duration": "",
            "max_choices": "",
        },
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"question": ["This field is required."]}


def test_poll_form_validation_parses_choices_list(rf, dynamic_settings):
    request = rf.post(
        "/",
        {
            "question": "Lorem ipsum",
            "choices_new": ["Lorem", "", "Ipsum"],
            "choices_new_noscript": "",
            "duration": "",
            "max_choices": "",
        },
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert form.is_valid()
    assert form.cleaned_data == {
        "question": "Lorem ipsum",
        "choices": ANY,
        "choices": ANY,
        "duration": None,
        "max_choices": None,
        "can_change_vote": False,
        "is_public": False,
    }

    assert form.cleaned_data["choices"].new == ["Lorem", "Ipsum"]


def test_poll_form_validation_parses_choices_text(rf, dynamic_settings):
    request = rf.post(
        "/",
        {
            "question": "Lorem ipsum",
            "choices_new": [],
            "choices_new_noscript": "  \n  Lorem  \n  Ipsum  \n  ",
            "duration": "",
            "max_choices": "",
        },
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert form.is_valid()
    assert form.cleaned_data == {
        "question": "Lorem ipsum",
        "choices": ANY,
        "duration": None,
        "max_choices": None,
        "can_change_vote": False,
        "is_public": False,
    }

    assert form.cleaned_data["choices"].new == ["Lorem", "Ipsum"]


def test_poll_form_validation_validates_question(rf, dynamic_settings):
    request = rf.post(
        "/",
        {
            "question": "I",
            "choices_new": [],
            "choices_new_noscript": "  \n  Lorem  \n  Ipsum  \n  ",
            "duration": "",
            "max_choices": "",
        },
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {
        "question": [
            "Poll question should be at least 8 characters long (it has 1).",
        ],
    }


def test_poll_form_validation_validates_choices_text(rf, dynamic_settings):
    request = rf.post(
        "/",
        {
            "question": "Lorem ipsum",
            "choices_new": [],
            "choices_new_noscript": "  \n  Lorem  \n    \n  ",
            "duration": "",
            "max_choices": "",
        },
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"choices": ["Poll must have at least two choices."]}


def test_poll_form_validation_validates_choices_list(rf, dynamic_settings):
    request = rf.post(
        "/",
        {
            "question": "Lorem ipsum",
            "choices_new": ["Lorem"],
            "choices_new_noscript": "",
            "duration": "",
            "max_choices": "",
        },
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"choices": ["Poll must have at least two choices."]}
