from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..models import PostEdit


class DeletePostEditHookAction(Protocol):
    """
    Misago function used to delete a `PostEdit` object.

    # Arguments

    ## `post_edit: PostEdit`

    A `PostEdit` instance to delete.

    ## `commit: bool = True`

    A `bool` indicating whether the `PostEdit` instance should be deleted from the database.

    Defaults to `True`.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.
    """

    def __call__(
        self,
        post_edit: "PostEdit",
        commit: bool = True,
        request: HttpRequest | None = None,
    ): ...


class DeletePostEditHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: DeletePostEditHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `post_edit: PostEdit`

    A `PostEdit` instance to delete.

    ## `commit: bool = True`

    A `bool` indicating whether the `PostEdit` instance should be deleted from the database.

    Defaults to `True`.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.
    """

    def __call__(
        self,
        action: DeletePostEditHookAction,
        post_edit: "PostEdit",
        commit: bool = True,
        request: HttpRequest | None = None,
    ): ...


class DeletePostEditHook(
    FilterHook[
        DeletePostEditHookAction,
        DeletePostEditHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to delete a `PostEdit` object.

    # Example

    The code below implements a custom filter function that records
    a number of deleted post edits:

    ```python
    from django.http import HttpRequest
    from misago.edits.hooks import delete_post_edit_hook
    from misago.edits.models import PostEdit


    @delete_post_edit_hook.append_filter
    def count_post_edit_deletions(
        action,
        post_edit: PostEdit,
        commit: bool = True,
        request: HttpRequest | None = None,
    ):
        post = post_edit.post
        action(post_edit, commit, request)

        post.plugin_data.setdefault("deleted_edits", 0) += 1
        post.save(update_fields=["plugin_data"])
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeletePostEditHookAction,
        post_edit: "PostEdit",
        commit: bool = True,
        request: HttpRequest | None = None,
    ):
        super().__call__(
            action,
            post_edit,
            commit,
            request,
        )


delete_post_edit_hook = DeletePostEditHook()
