from django.http import HttpRequest

from .hooks import delete_post_edit_hook
from .models import PostEdit


def delete_post_edit(
    post_edit: PostEdit,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    delete_post_edit_hook(_delete_post_edit_action, post_edit, commit, request)


def _delete_post_edit_action(
    post_edit: PostEdit,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    if commit:
        post_edit.delete()
