from django.http import QueryDict

from ...conf.test import override_dynamic_settings
from ...polls.enums import AllowedPublicPolls
from ..forms import PollForm


def test_poll_form_sets_request(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PollForm(request=request)
    assert form.request is request


def test_poll_form_sets_empty_choices_obj(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PollForm(request=request)
    assert form.choices_obj is None


@override_dynamic_settings(poll_question_max_length=42)
def test_poll_form_sets_question_max_length_from_setting(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PollForm(request=request)
    assert form.fields["question"].max_length == 42


@override_dynamic_settings(allow_public_polls=AllowedPublicPolls.ALLOWED)
def test_poll_form_includes_public_voting_option_if_its_enabled(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PollForm(request=request)
    assert "is_public" in form.fields


@override_dynamic_settings(allow_public_polls=AllowedPublicPolls.FORBIDDEN)
def test_poll_form_removes_public_voting_option_if_they_are_forbidden(
    rf, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings

    form = PollForm(request=request)
    assert "is_public" not in form.fields


@override_dynamic_settings(allow_public_polls=AllowedPublicPolls.FORBIDDEN_NEW)
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
        "/", QueryDict("question=&choices_text=&choices_list[]=&duration=&max_choices=")
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert form.is_valid()


def test_poll_form_validation_requires_choices_if_question_is_set(rf, dynamic_settings):
    request = rf.post(
        "/",
        QueryDict(
            "question=lorem_ipsum&choices_text=&choices_list[]=&duration=&max_choices="
        ),
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {
        "choices_text": ["This field is required."],
        "choices_list": ["This field is required."],
    }


def test_poll_form_validation_requires_question_if_choices_text_is_set(
    rf, dynamic_settings
):
    request = rf.post(
        "/",
        QueryDict(
            "question=&choices_text=lorem\nipsum&choices_list[]=&duration=&max_choices="
        ),
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"question": ["This field is required."]}


def test_poll_form_validation_requires_question_if_choices_list_is_set(
    rf, dynamic_settings
):
    request = rf.post(
        "/",
        QueryDict(
            "question=&choices_text=&choices_list[]=lorem&choices_list[]=ipsum&duration=&max_choices="
        ),
    )
    request.settings = dynamic_settings

    form = PollForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"question": ["This field is required."]}
