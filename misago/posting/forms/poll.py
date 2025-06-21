from django import forms
from django.http import HttpRequest
from django.utils.crypto import get_random_string
from django.utils.translation import pgettext_lazy

from ...polls.models import Poll
from ..state import StartThreadState
from .base import PostingForm


class PollForm(PostingForm):
    form_prefix = "posting-poll"
    template_name = "misago/posting/poll_form.html"

    request: HttpRequest

    question = forms.CharField(max_length=255, required=False)
    choices = forms.CharField(max_length=255, required=False)
    # length = models.PositiveIntegerField(default=0)
    # max_choices = models.PositiveIntegerField(default=1)
    # can_change_vote = models.BooleanField(default=False)
    # is_public = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

    def update_state(self, state: StartThreadState):
        if not self.cleaned_data["question"] or not self.cleaned_data["choices"]:
            return

        choices_list = []
        for choice in self.cleaned_data["choices"].splitlines():
            choice = choice.strip()
            if not choice:
                continue

            choices_list.append(
                {
                    "id": get_random_string(8),
                    "name": choice,
                    "votes": 0,
                }
            )

        poll = Poll(
            category=state.category,
            thread=state.thread,
            starter=state.user,
            starter_name=state.user.username,
            starter_slug=state.user.slug,
            question=self.cleaned_data["question"],
            choices=choices_list,
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
