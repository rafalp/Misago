from django import forms
from django.http import HttpRequest
from django.utils.crypto import get_random_string
from django.utils.translation import pgettext

from ...polls.choices import PollChoices
from ...polls.models import Poll
from ..state import StartThreadState
from .base import PostingForm


class PollForm(PostingForm):
    form_prefix = "posting-poll"
    template_name = "misago/posting/poll_form.html"

    request: HttpRequest

    question = forms.CharField(min_length=5, max_length=255, required=False)
    choices = forms.CharField(max_length=255, required=False)
    length = forms.IntegerField(initial=0, min_value=0, max_value=1825, required=False)
    max_choices = forms.IntegerField(initial=1, min_value=1, required=False)
    can_change_vote = forms.BooleanField(required=False)
    is_public = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        question = cleaned_data.get("question")
        choices = cleaned_data.get("choices")

        if not cleaned_data["question"] and not cleaned_data["choices"]:
            return cleaned_data

        if not question:
            self.add_error(
                "question", pgettext("form validation", "This field is required.")
            )

        if not choices:
            self.add_error(
                "choices", pgettext("form validation", "This field is required.")
            )

        return cleaned_data

    def update_state(self, state: StartThreadState):
        if not self.cleaned_data["question"] and not self.cleaned_data["choices"]:
            return

        choices_json = PollChoices.from_sequence(
            self.cleaned_data["choices"].splitlines()
        ).to_json()

        poll = Poll(
            category=state.category,
            thread=state.thread,
            starter=state.user,
            starter_name=state.user.username,
            starter_slug=state.user.slug,
            question=self.cleaned_data["question"],
            choices=choices_json,
            length=self.cleaned_data.get("length", 0),
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
