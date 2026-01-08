from typing import TYPE_CHECKING, Union

from django.http import HttpRequest
from django.utils import timezone

from ..core.utils import slugify
from .hooks import hide_post_edit_hook, unhide_post_edit_hook
from .models import PostEdit

if TYPE_CHECKING:
    from ..users.models import User


def hide_post_edit(
    post_edit: PostEdit,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    hide_post_edit_hook(_hide_post_edit_action, post_edit, user, commit, request)


def _hide_post_edit_action(
    post_edit: PostEdit,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    if isinstance(user, str):
        hidden_by = None
        hidden_by_name = user
        hidden_by_slug = slugify(user)
    else:
        hidden_by = user
        hidden_by_name = user.username
        hidden_by_slug = user.slug

    post_edit.is_hidden = True
    post_edit.hidden_by = hidden_by
    post_edit.hidden_by_name = hidden_by_name
    post_edit.hidden_by_slug = hidden_by_slug
    post_edit.hidden_at = timezone.now()

    if commit:
        post_edit.save()


def unhide_post_edit(
    post_edit: PostEdit,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    unhide_post_edit_hook(_unhide_post_edit_action, post_edit, commit, request)


def _unhide_post_edit_action(
    post_edit: PostEdit,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    post_edit.is_hidden = False
    post_edit.hidden_by = None
    post_edit.hidden_by_name = None
    post_edit.hidden_by_slug = None
    post_edit.hidden_at = None

    if commit:
        post_edit.save()
