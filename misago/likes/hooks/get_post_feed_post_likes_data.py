from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post


class GetPostFeedPostLikesDataHookAction(Protocol):
    """
    Misago function for creating the context data used to render a post's likes
    in the posts feed.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The post for which to create likes context data.

    ## `is_liked: bool`

    `True` if the post is liked by the current user, `False` otherwise.

    ## `likes_url: str`

    URL of the post's likes list view.

    ## `like_url: str`

    URL of the view used to like the post.

    ## `unlike_url: str`

    URL of the view used to unlike the post.

    Defaults to `True`.

    ## Return value

    Returns `dict` with the context data.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
        is_liked: bool,
        likes_url: str,
        like_url: str,
        unlike_url: str,
    ) -> dict: ...


class GetPostFeedPostLikesDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPostFeedPostLikesDataHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The post for which to create likes context data.

    ## `is_liked: bool`

    `True` if the post is liked by the current user, `False` otherwise.

    ## `likes_url: str`

    URL of the post's likes list view.

    ## `like_url: str`

    URL of the view used to like the post.

    ## `unlike_url: str`

    URL of the view used to unlike the post.

    Defaults to `True`.

    ## Return value

    Returns `dict` with the context data.
    """

    def __call__(
        self,
        action: GetPostFeedPostLikesDataHookAction,
        request: HttpRequest,
        post: Post,
        is_liked: bool,
        likes_url: str,
        like_url: str,
        unlike_url: str,
    ) -> dict: ...


class GetPostFeedPostLikesDataHook(
    FilterHook[
        GetPostFeedPostLikesDataHookAction,
        GetPostFeedPostLikesDataHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to create
    the context data used to render a post's likes in the posts feed.

    # Example

    Customize the "likes" description:

    ```python
    from django.http import HttpRequest
    from misago.likes.hooks import get_post_feed_post_likes_data_hook
    from misago.threads.models import Post


    @get_post_feed_post_likes_data_hook.append_filter
    def use_heart_emoji_for_likes(
        action,
        request: HttpRequest,
        post: Post,
        is_liked: bool,
        likes_url: str,
        like_url: str,
        unlike_url: str,
    ) -> dict:
        context = action(request, post, is_liked, likes_url, like_url, unlike_url)

        if context["likes"] and context["description"]:
            if context["is_liked"]:
                context["description"] = {
                    "custom": "%s ❤️ (including You!)" % context["likes"]
                }
            else:
                context["description"] = {"custom": "%s ❤️" % context["likes"]}

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPostFeedPostLikesDataHookAction,
        request: HttpRequest,
        post: Post,
        is_liked: bool,
        likes_url: str,
        like_url: str,
        unlike_url: str,
    ) -> dict:
        return super().__call__(
            action,
            request,
            post,
            is_liked,
            likes_url,
            like_url,
            unlike_url,
        )


get_post_feed_post_likes_data_hook = GetPostFeedPostLikesDataHook()
