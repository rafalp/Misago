from django import forms
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ...threads.enums import ThreadWeight
from ...threads.hide import hide_thread
from ...threads.lock import lock_thread
from ...threads.pin import pin_thread_globally, pin_thread_in_category
from ..state import StartState
from .base import PostingForm


class ThreadModerationForm(PostingForm):
    form_prefix = "posting-moderation"
    template_name = "misago/posting/thread_moderation_form.html"

    request: HttpRequest

    is_locked = forms.BooleanField(required=False)
    is_hidden = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        is_global_moderator = kwargs.pop("is_global_moderator")

        super().__init__(*args, **kwargs)

        if is_global_moderator:
            self.fields["pin"] = forms.TypedChoiceField(
                choices=ThreadWeight.get_choices(),
                coerce=int,
                required=False,
                initial=ThreadWeight.NOT_PINNED,
            )
        else:
            self.fields["pin_in_category"] = forms.BooleanField(required=False)

    def update_state(self, state: StartState):
        if self.cleaned_data["is_locked"]:
            lock_thread(state.thread, commit=False, request=self.request)

        if self.cleaned_data["is_hidden"]:
            hide_thread(state.thread, commit=False, request=self.request)

        if (
            self.cleaned_data.get("pin_in_category")
            or self.cleaned_data.get("pin") == ThreadWeight.PINNED_IN_CATEGORY
        ):
            pin_thread_in_category(state.thread, commit=False, request=self.request)
        elif self.cleaned_data.get("pin") == ThreadWeight.PINNED_GLOBALLY:
            pin_thread_globally(state.thread, commit=False, request=self.request)


def create_thread_moderation_form(
    request: HttpRequest, global_moderator: bool
) -> ThreadModerationForm:
    if request.method == "POST":
        return ThreadModerationForm(
            request.POST,
            request=request,
            is_global_moderator=global_moderator,
            prefix=ThreadModerationForm.form_prefix,
        )

    return ThreadModerationForm(
        request=request,
        is_global_moderator=global_moderator,
        prefix=ThreadModerationForm.form_prefix,
    )


class PrivateThreadModerationForm(PostingForm):
    form_prefix = "posting-moderation"
    template_name = "misago/posting/private_thread_moderation_form.html"

    request: HttpRequest

    is_locked = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def update_state(self, state: StartState):
        if self.cleaned_data["is_locked"]:
            lock_thread(state.thread, commit=False, request=self.request)


def create_private_thread_moderation_form(
    request: HttpRequest,
) -> PrivateThreadModerationForm:
    if request.method == "POST":
        return PrivateThreadModerationForm(
            request.POST,
            request=request,
            prefix=ThreadModerationForm.form_prefix,
        )

    return PrivateThreadModerationForm(
        request=request,
        prefix=ThreadModerationForm.form_prefix,
    )
