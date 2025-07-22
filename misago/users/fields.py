from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import get_user_model

from ..forms.fields import ListField
from ..permissions.proxy import UserPermissionsProxy

if TYPE_CHECKING:
    from ..users.models import User


class UserMultipleChoiceField(forms.MultiValueField):
    def __init__(self, **kwargs):
        self.max_choices = kwargs.pop("max_choices", 5)
        self.queryset = kwargs.pop("queryset", get_user_model().objects)

        super().__init__(
            fields=(
                ListField(),
                forms.CharField(),
            ),
            require_all_fields=False,
            **kwargs,
        )

    def compress(self, data_list: tuple[list[str], str]) -> list[str]:
        if not data_list:
            return None
        
        value, value_noscript = data_list
        if not value and value_noscript:
            value = value_noscript.split()

        usernames: list[str] = []
        for username in value:
            username = username.strip()
            if username and username not in usernames:
                usernames.append(username)

        if usernames:
            return self.get_users(usernames)

        return usernames

    def get_users(self, usernames: list[str]) -> list["User"]:
        return self.queryset.filter(
            slug__in=[username.lower() for username in usernames]
        )
