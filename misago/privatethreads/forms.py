from typing import TYPE_CHECKING, Optional

from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import pgettext

from ..permissions.proxy import UserPermissionsProxy
from ..privatethreads.validators import validate_new_private_thread_member
from ..users.fields import UserMultipleChoiceField

if TYPE_CHECKING:
    from ..users.models import User


class MembersAddForm(forms.Form):
    request: HttpRequest
    owner: Optional["User"]
    members: list["User"]

    users = UserMultipleChoiceField()

    def __init__(
        self,
        *args,
        request: HttpRequest,
        owner: Optional["User"],
        members: list["User"],
        **kwargs
    ):
        self.request = request
        self.owner = owner
        self.members = members

        super().__init__(*args, **kwargs)

        self.setup_users_field(self.fields["users"])

    def setup_users_field(self, field: UserMultipleChoiceField):
        field.queryset = get_user_model().objects.filter(is_active=True)

        members = len(self.members)
        if self.request.user in self.members:
            members -= 1

        field.max_choices = max(
            self.request.user_permissions.private_thread_members_limit - members,
            0,
        )

    def clean_users(self):
        data: list["User"] = self.cleaned_data["users"]

        request = self.request
        cache_versions = request.cache_versions

        errors: list[forms.ValidationError] = []

        cleaned_data: list["User"] = []
        for user in data:
            try:
                if user == self.owner or user in self.members:
                    continue

                validate_new_private_thread_member(
                    UserPermissionsProxy(user, cache_versions),
                    request.user_permissions,
                    cache_versions,
                    request,
                )
            except forms.ValidationError as error:
                errors.append(
                    forms.ValidationError(
                        pgettext("add thread members form", "%(user)s: %(error)s"),
                        code="member",
                        params={"user": user.username, "error": error.message},
                    )
                )
            else:
                cleaned_data.append(user)

        if errors:
            raise forms.ValidationError(errors, code="invalid_users")

        return cleaned_data
