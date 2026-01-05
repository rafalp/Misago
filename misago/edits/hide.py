from typing import TYPE_CHECKING, Union

from django.http import HttpRequest

from .hooks import delete_post_edit_hook
from .models import PostEdit

if TYPE_CHECKING:
    from ..users.models import User


def hide_post_edit(
    post_edit: PostEdit,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    pass


def unhide_post_edit(
    post_edit: PostEdit,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    pass
