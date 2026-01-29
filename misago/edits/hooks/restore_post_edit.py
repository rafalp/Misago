from typing import TYPE_CHECKING, Protocol, Union

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...threads.models import Post
    from ...users.models import User
    from ..models import PostEdit


class RestorePostEditHookAction(Protocol):
    """
    Misago function used to restore post content from a related `PostEdit` object.

    # Arguments

    ## `post_edit: PostEdit`

    A `PostEdit` instance to restore the post from.

    ## `user: Union["User", str] = None`

    The user who restored the post, a `User` instance or a `str` with the user's name.

    ## `commit: bool = True`

    A `bool` indicating whether the updated `Post` and the new `PostEdit`
    instances should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A `tuple` with the updated `Post` instance and the new `PostEdit` instance.
    """

    def __call__(
        self,
        post_edit: "PostEdit",
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> tuple["Post", "PostEdit"]: ...


class RestorePostEditHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: RestorePostEditHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `post_edit: PostEdit`

    A `PostEdit` instance to restore the post from.

    ## `user: Union["User", str] = None`

    The user who restored the post, a `User` instance or a `str` with the user's name.

    ## `commit: bool = True`

    A `bool` indicating whether the updated `Post` and the new `PostEdit`
    instances should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A `tuple` with the updated `Post` instance and the new `PostEdit` instance.
    """

    def __call__(
        self,
        action: RestorePostEditHookAction,
        post_edit: "PostEdit",
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> tuple["Post", "PostEdit"]: ...


class RestorePostEditHook(
    FilterHook[
        RestorePostEditHookAction,
        RestorePostEditHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to restore post content
    from a related PostEdit object.

    # Example

    The code below implements a custom filter function that sets
    restored post's edit reason:

    ```python
    from django.http import HttpRequest
    from misago.edits.hooks import restore_post_edit_hook
    from misago.edits.models import PostEdit
    from misago.posting.shortcuts import save_edited_post
    from misago.threads.models import Post
    from misago.users.models import User


    @restore_post_edit_hook.append_filter
    def restore_post_edit_record_user_ip(
        action,
        post_edit: PostEdit,
        user: User | str,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> tuple[Post, PostEdit]:
        post, new_post_edit = action(post_edit, user, False, request)

        post.last_edit_reason = f"Restored from #{new_post_edit.id}"

        if commit:
            new_post_edit.save()
            save_edited_post(post)

        return post, new_post_edit
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: RestorePostEditHookAction,
        post_edit: "PostEdit",
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> tuple["Post", "PostEdit"]:
        return super().__call__(
            action,
            post_edit,
            user,
            commit,
            request,
        )


restore_post_edit_hook = RestorePostEditHook()
