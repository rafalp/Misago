from typing import TYPE_CHECKING, Protocol, Union

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...users.models import User
    from ..models import PostEdit


class HidePostEditHookAction(Protocol):
    """
    Misago function used to hide a `PostEdit` object.

    # Arguments

    ## `post_edit: PostEdit`

    A `PostEdit` instance to hide.

    ## `user: Union["User", str] = None`

    The user who hid the edit, a `User` instance or a `str` with the user's name.

    ## `commit: bool = True`

    A `bool` indicating whether the updated `PostEdit` instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.
    """

    def __call__(
        self,
        post_edit: "PostEdit",
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ): ...


class HidePostEditHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: HidePostEditHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `post_edit: PostEdit`

    A `PostEdit` instance to hide.

    ## `user: Union["User", str] = None`

    The user who hid the edit, a `User` instance or a `str` with the user's name.

    ## `commit: bool = True`

    A `bool` indicating whether the updated `PostEdit` instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.
    """

    def __call__(
        self,
        action: HidePostEditHookAction,
        post_edit: "PostEdit",
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ): ...


class HidePostEditHook(
    FilterHook[
        HidePostEditHookAction,
        HidePostEditHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to hide a `PostEdit` object.

    # Example

    The code below implements a custom filter function that records the user's
    IP address:

    ```python
    from django.http import HttpRequest
    from misago.edits.hooks import hide_post_edit_hook
    from misago.edits.models import PostEdit
    from misago.users.models import User


    @hide_post_edit_hook.append_filter
    def hide_post_edit_record_user_ip(
        action,
        post_edit: PostEdit,
        user: User | str,
        commit: bool = True,
        request: HttpRequest | None = None,
    ):
        action(post_edit, user, False, request)

        if request:
            post_edit.plugin_data["hidden_by_ip"] = request.user_ip

        if commit:
            post_edit.save()
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: HidePostEditHookAction,
        post_edit: "PostEdit",
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ):
        super().__call__(
            action,
            post_edit,
            user,
            commit,
            request,
        )


hide_post_edit_hook = HidePostEditHook()
