from django import forms
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ..state import StartPrivateThreadState, StartThreadState
from ..validators import validate_thread_title
from .base import PostingForm


class TitleForm(PostingForm):
    form_prefix = "posting-title"
    template_name = "misago/posting/title_form.html"

    request: HttpRequest

    title = forms.CharField(
        max_length=255,
        error_messages={
            "required": pgettext_lazy(
                "thread title validator",
                "Enter a thread title.",
            ),
        },
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["title"].max_length = self.request.settings.thread_title_length_max

    def clean_title(self):
        data = self.cleaned_data["title"]
        validate_thread_title(
            data,
            self.request.settings.thread_title_length_min,
            self.request.settings.thread_title_length_max,
            request=self.request,
        )
        return data

    def update_state(self, state: StartPrivateThreadState | StartThreadState):
        state.set_thread_title(self.cleaned_data["title"])


def create_title_form(request: HttpRequest, initial: str | None = None) -> TitleForm:
    if request.method == "POST":
        return TitleForm(
            request.POST,
            request=request,
            prefix=TitleForm.form_prefix,
        )

    if initial:
        initial_data = {"title": initial}
    else:
        initial_data = None

    return TitleForm(
        request=request, prefix=TitleForm.form_prefix, initial=initial_data
    )
