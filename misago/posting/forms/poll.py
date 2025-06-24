from django import forms
from django.http import HttpRequest
from django.utils.translation import pgettext

from ...polls.choices import PollChoices
from ...polls.enums import AllowedPublicPolls
from ...polls.models import Poll
from ..state import StartThreadState
from ..validators import validate_poll_choices, validate_poll_question
from .base import PostingForm


class PollForm(PostingForm):
    form_prefix = "posting-poll"
    template_name = "misago/posting/poll_form.html"

    request: HttpRequest

    question = forms.CharField(max_length=255, required=False)
    choices = forms.CharField(max_length=255, required=False)
    duration = forms.IntegerField(
        initial=0, min_value=0, max_value=1825, required=False
    )
    max_choices = forms.IntegerField(initial=1, min_value=1, required=False)
    can_change_vote = forms.BooleanField(required=False)
    is_public = forms.BooleanField(required=False)

    choices_obj: PollChoices | None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

        self.setup_form_fields(self.request.settings)

    def setup_form_fields(self, settings):
        self.fields["question"].max_length = settings.poll_question_max_length

        if settings.allow_public_polls != AllowedPublicPolls.ALLOWED:
            del self.fields["is_public"]

    def clean_question(self):
        data = self.cleaned_data["question"]
        validate_poll_question(
            data,
            self.request.settings.poll_question_min_length,
            self.request.settings.poll_question_max_length,
            self.request,
        )
        return data

    def clean_choices(self):
        data = self.cleaned_data["choices"]
        self.choices_obj = PollChoices.from_str(data)

        validate_poll_choices(
            self.choices_obj,
            self.request.settings.poll_max_choices,
            self.request.settings.poll_choice_max_length,
            self.request,
        )

        return self.choices_obj.get_str()

    def clean(self):
        cleaned_data = super().clean()

        question = cleaned_data.get("question")
        choices = cleaned_data.get("choices")

        if not question and not choices:
            return cleaned_data

        if not question and not self.errors.get("question"):
            self.add_error(
                "question", pgettext("form validation", "This field is required.")
            )

        if not choices and not self.errors.get("choices"):
            self.add_error(
                "choices", pgettext("form validation", "This field is required.")
            )

        return cleaned_data

    def update_state(self, state: StartThreadState):
        if not self.cleaned_data["question"] and not self.choices_obj:
            return

        poll = Poll(
            category=state.category,
            thread=state.thread,
            starter=state.user,
            starter_name=state.user.username,
            starter_slug=state.user.slug,
            question=self.cleaned_data["question"],
            choices=self.choices_obj.get_json(),
            duration=self.cleaned_data.get("duration", 0),
            max_choices=self.cleaned_data.get("max_choices", 1),
            can_change_vote=self.cleaned_data.get("can_change_vote") or False,
            is_public=self.cleaned_data.get("is_public") or False,
        )

        state.set_poll(poll)


def create_poll_form(request: HttpRequest) -> PollForm:
    kwargs = {
        "request": request,
        "prefix": PollForm.form_prefix,
    }

    if request.method == "POST":
        return PollForm(request.POST, **kwargs)

    return PollForm(**kwargs)
