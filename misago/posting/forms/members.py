from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import pgettext

from ...permissions.proxy import UserPermissionsProxy
from ...privatethreads.validators import validate_new_private_thread_member
from ...users.fields import UserMultipleChoiceField
from ..state import PrivateThreadStartState
from .base import PostingForm

if TYPE_CHECKING:
    from ...users.models import User


class MembersForm(PostingForm):
    form_prefix = "posting-members"
    template_name = "misago/posting/members_form.html"

    request: HttpRequest
    add_members: list["User"]

    users = UserMultipleChoiceField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.add_members: list["User"] = []

        super().__init__(*args, **kwargs)

        self.setup_users_field(self.fields["users"])

    def setup_users_field(self, field: UserMultipleChoiceField):
        field.queryset = get_user_model().objects.filter(is_active=True)
        field.max_choices = self.request.user_permissions.private_thread_members_limit

    def clean_users(self):
        data: list["User"] = self.cleaned_data["users"]

        errors: list[forms.ValidationError] = []
        if self.request.user in data:
            data.remove(self.request.user)
            if not data:
                errors.append(
                    forms.ValidationError(
                        pgettext(
                            "posting form", "You must enter at least one other user."
                        ),
                        code="self",
                    )
                )

        request = self.request
        cache_versions = request.cache_versions

        for user in data:
            try:
                validate_new_private_thread_member(
                    UserPermissionsProxy(user, cache_versions),
                    request.user_permissions,
                    cache_versions,
                    request,
                )
            except forms.ValidationError as error:
                errors.append(
                    forms.ValidationError(
                        pgettext("posting form", "%(user)s: %(error)s"),
                        code="member",
                        params={"user": user.username, "error": error.message},
                    )
                )

        if errors:
            raise forms.ValidationError(errors, code="invalid_users")

        return data

    def update_state(self, state: PrivateThreadStartState):
        state.set_members(self.cleaned_data["users"])


def create_members_form(request: HttpRequest) -> MembersForm:
    if request.method == "POST":
        return MembersForm(
            request.POST,
            request=request,
            prefix=MembersForm.form_prefix,
        )

    return MembersForm(request=request, prefix=MembersForm.form_prefix)
