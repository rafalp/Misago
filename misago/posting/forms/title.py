from django import forms
from django.http import HttpRequest

from ..state import StartPrivateThreadState, StartThreadState
from .base import PostingForm

PREFIX = "posting-title"


class TitleForm(PostingForm):
    request: HttpRequest

    template_name = "misago/posting/title_form.html"

    title = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def update_state(self, state: StartPrivateThreadState | StartThreadState):
        state.set_thread_title(self.cleaned_data["title"])


def create_title_form(request: HttpRequest, initial: str | None = None) -> TitleForm:
    if request.method == "POST":
        return TitleForm(
            request.POST,
            request=request,
            prefix=PREFIX,
        )

    if initial:
        initial_data = {"title": initial}
    else:
        initial_data = None

    return TitleForm(request=request, prefix=PREFIX, initial=initial_data)
