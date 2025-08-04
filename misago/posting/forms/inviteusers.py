from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import pgettext

from ...permissions.proxy import UserPermissionsProxy
from ...privatethreads.validators import validate_can_invite_user
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

        errors: list[forms.ValidationError] = []
        if self.request.user in data:
            data.remove(self.request.user)
            if not data:
                errors.append(
                    forms.ValidationError(
                        pgettext("posting form", "You can't invite yourself."),
                        code="invite_self",
                    )
                )

        request = self.request
        cache_versions = request.cache_versions

        for user in data:
            try:
                validate_can_invite_user(
                    UserPermissionsProxy(user, cache_versions),
                    request.user_permissions,
                    cache_versions,
                    request,
                )
            except forms.ValidationError as error:
                errors.append(
                    forms.ValidationError(
                        pgettext("posting form", "%(user)s: %(error)s"),
                        code="invite_self",
                        params={"user": user.username, "error": error.message},
                    )
                )

        if errors:
            raise forms.ValidationError(errors, code="invalid_users")

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
