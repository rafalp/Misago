from django import forms
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ..state import PostingState
from ..validators import validate_post
from .base import PostingForm

PREFIX = "posting-post"


class PostForm(PostingForm):
    request: HttpRequest

    template_name = "misago/posting/post_form.html"

    post = forms.CharField(
        widget=forms.Textarea,
        error_messages={
            "required": pgettext_lazy("post validator", "Enter post's content."),
        },
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_post(self):
        data = self.cleaned_data["post"]
        validate_post(
            data,
            self.request.settings.post_length_min,
            self.request.settings.post_length_max,
            request=self.request,
        )
        return data

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
