from django import forms
from django.http import HttpRequest

from ..state import PostingState
from .base import PostingForm

PREFIX = "posting-post"


class PostForm(PostingForm):
    request: HttpRequest

    template_name = "misago/posting/post_form.html"

    post = forms.CharField(max_length=2000, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def update_state(self, state: PostingState):
        state.set_post_message(self.cleaned_data["post"])


def create_post_form(request: HttpRequest, initial: str | None = None) -> PostForm:
    kwargs = {
        "request": request,
        "prefix": PREFIX,
    }

    if request.method == "POST":
        return PostForm(request.POST, request.FILES, **kwargs)

    if initial:
        kwargs["initial"] = {"post": initial}

    return PostForm(**kwargs)
