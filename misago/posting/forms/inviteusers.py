from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import npgettext, pgettext

from ...core.utils import slugify
from ...users.fields import UserMultipleChoiceField
from ..state import StartPrivateThreadState
from .base import PostingForm

if TYPE_CHECKING:
    from ...users.models import User


class InviteUsersForm(PostingForm):
    form_prefix = "posting-invite-users"
    template_name = "misago/posting/invite_users_form.html"

    request: HttpRequest
    invite_users: list["User"]

    users = UserMultipleChoiceField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.invite_users: list["User"] = []

        super().__init__(*args, **kwargs)

        self.setup_users_field(self.fields["users"])

    def setup_users_field(self, field: UserMultipleChoiceField):
        field.queryset = get_user_model().objects.filter(is_active=True)
        field.max_choices = self.request.user_permissions.private_thread_users_limit

    def clean_users(self):
        data: list["User"] = self.cleaned_data["users"]

        if self.request.user in data:
            data.remove(self.request.user)

            if not data:
                raise forms.ValidationError(
                    pgettext("posting form", "You can't invite yourself.")
                )

        data_length = len(data)

        if not data_length:
            raise forms.ValidationError(
                pgettext("posting form", "Enter at least one username.")
            )

        limit = self.request.user_permissions.private_thread_users_limit
        if data_length > limit:
            raise forms.ValidationError(
                npgettext(
                    "posting form",
                    "You can't invite more than %(limit)s user.",
                    "You can't invite more than %(limit)s users.",
                    data_length,
                ),
                params={"limit": limit},
            )

        return data

    def update_state(self, state: StartPrivateThreadState):
        state.set_invite_users(self.cleaned_data["users"])


def create_invite_users_form(request: HttpRequest) -> InviteUsersForm:
    if request.method == "POST":
        return InviteUsersForm(
            request.POST,
            request=request,
            prefix=InviteUsersForm.form_prefix,
        )

    return InviteUsersForm(request=request, prefix=InviteUsersForm.form_prefix)
