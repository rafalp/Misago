from django.http import HttpRequest
from django.utils.translation import pgettext

from ...polls.forms import StartPollForm
from ..state import ThreadStartState
from .base import PostingForm


class PollForm(StartPollForm, PostingForm):
    form_prefix = "posting-poll"
    template_name = "misago/posting/poll_form.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, required=False)

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

    def update_state(self, state: ThreadStartState):
        if not (self.cleaned_data.get("question") and self.cleaned_data.get("choices")):
            return

        state.set_poll(
            self.create_poll_instance(state.category, state.thread, state.user)
        )


def create_poll_form(request: HttpRequest) -> PollForm:
    kwargs = {
        "request": request,
        "prefix": PollForm.form_prefix,
    }

    if request.method == "POST":
        return PollForm(request.POST, **kwargs)

    return PollForm(**kwargs)
