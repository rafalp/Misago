from typing import TYPE_CHECKING, Protocol, Union

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Post

if TYPE_CHECKING:
    from ...users.models import User


class HidePostHookAction(Protocol):
    """
    Misago function for hiding a post.

    # Arguments

    ## `post: Post`

    A `Post` to hide.

    ## `hidden_by: User | str`

    The user who hid the post.

    ## `hide_reason: str | None`

    A `str` with a short description of why the post was hidden, or `None`.

    ## `commit: bool = True`

    Whether the updated post instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the post was hidden, `False` otherwise.
    """

    def __call__(
        self,
        post: Post,
        hidden_by: Union["User", str],
        hide_reason: str | None = None,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class HidePostHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: HidePostHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `post: Post`

    A `Post` to hide.

    ## `hidden_by: User | str`

    The user who hid the post.

    ## `hide_reason: str | None`

    A `str` with a short description of why the post was hidden, or `None`.

    ## `commit: bool = True`

    Whether the updated post instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the post was hidden, `False` otherwise.
    """

    def __call__(
        self,
        action: HidePostHookAction,
        post: Post,
        hidden_by: Union["User", str],
        hide_reason: str | None = None,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class HidePostHook(
    FilterHook[
        HidePostHookAction,
        HidePostHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    hide a post.

    # Example

    Register ip of user who hid the post:

    ```python
    from django.http import HttpRequest
    from misago.posts.hooks import hide_post_hook
    from misago.posts.models import Post
    from misago.users.models import User


    @hide_post_hook.append_filter
    def register_user_that_hid_post(
        action,
        post: Post,
        hidden_by: User | str,
        hide_reason: str | None = None,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        if not action(post, hidden_by, hide_reason, commit=False, request=request):
            return False

        if request:
            post.plugin_data["hidden_by_ip"] = request.user_ip

        if commit:
            post.save()

        return True
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: HidePostHookAction,
        post: Post,
        hidden_by: Union["User", str],
        hide_reason: str | None = None,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        return super().__call__(
            action,
            post,
            hidden_by,
            hide_reason,
            commit,
            request,
        )


hide_post_hook = HidePostHook()
