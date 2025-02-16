from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import npgettext, pgettext

from ...core.utils import slugify
from ..state import StartPrivateThreadState
from .base import PostingForm

if TYPE_CHECKING:
    from ...users.models import User
else:
    User = get_user_model()


class InviteUsersForm(PostingForm):
    form_prefix = "posting-invite-users"
    template_name = "misago/posting/invite_users_form.html"

    request: HttpRequest
    invite_users: list["User"]

    users = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.invite_users: list["User"] = []

        super().__init__(*args, **kwargs)

    def clean_users(self):
        uniques: dict[str, str] = {}
        for username in self.cleaned_data["users"].split():
            slug = slugify(username)
            if slug not in uniques:
                uniques[slug] = username

        if self.request.user.slug in uniques and len(uniques) == 1:
            raise forms.ValidationError(
                pgettext("posting form", "You can't invite yourself.")
            )

        uniques.pop(self.request.user.slug, None)

        if not uniques:
            raise forms.ValidationError(
                pgettext("posting form", "Enter at least one username.")
            )

        limit = self.request.user_permissions.private_thread_users_limit
        if len(uniques) > limit:
            raise forms.ValidationError(
                npgettext(
                    "posting form",
                    "You can't invite more than %(limit)s user.",
                    "You can't invite more than %(limit)s users.",
                    len(uniques),
                ),
                params={"limit": limit},
            )

        users = list(User.objects.filter(slug__in=uniques, is_active=True))

        if len(users) != len(uniques):
            found_users: set[str] = set([u.slug for u in users])
            missing_users: list[str] = set(uniques).difference(found_users)
            missing_usernames: list[str] = [uniques[slug] for slug in missing_users]

            if len(missing_usernames) == 1:
                raise forms.ValidationError(
                    pgettext(
                        "posting form",
                        "One user could not be found: %(username)s",
                    ),
                    params={"username": missing_usernames[0]},
                )

            raise forms.ValidationError(
                pgettext(
                    "posting form",
                    "Users could not be found: %(usernames)s",
                ),
                params={"usernames": ", ".join(missing_usernames)},
            )

        self.invite_users = users
        return " ".join([u.username for u in users])

    def update_state(self, state: StartPrivateThreadState):
        state.set_invite_users(self.invite_users)


def create_invite_users_form(request: HttpRequest) -> InviteUsersForm:
    if request.method == "POST":
        return InviteUsersForm(
            request.POST,
            request=request,
            prefix=InviteUsersForm.form_prefix,
        )

    return InviteUsersForm(request=request, prefix=InviteUsersForm.form_prefix)
