from typing import Protocol

from django.http import HttpRequest, HttpResponse

from ...plugins.hooks import FilterHook
from ...posts.models import Post


class RedirectToPostHookAction(Protocol):
    """
    Misago function used to get a HTTP redirect response to a post.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    A post to redirect to. It's `category` attribute is already populated.

    # Return value

    Django's `HttpResponse` with redirect to a post.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
    ) -> HttpResponse: ...


class RedirectToPostHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: RedirectToPostHookAction`

    Misago function used to get a HTTP redirect response to a post.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    A post to redirect to. It's `category` attribute is already populated.

    # Return value

    Django's `HttpResponse` with redirect to a post.
    """

    def __call__(
        self,
        action: RedirectToPostHookAction,
        request: HttpRequest,
        post: Post,
    ) -> HttpResponse: ...


class RedirectToPostHook(
    FilterHook[
        RedirectToPostHookAction,
        RedirectToPostHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get a HTTP
    redirect response to a post.

    # Example

    The code below implements a custom filter function that creates custom redirect
    response for posts in non-standard category type:

    ```python
    from django.http import HttpRequest
    from django.shortcuts import redirect
    from django.urls import reverse

    from misago.postredirect.hooks import redirect_to_post_hook
    from misago.posts.models import Post

    BLOG_CATEGORY_TREE = 500

    @redirect_to_post_hook.append_filter
    def redirect_to_blog_comment(
        action, request: HttpRequest, post: Post
    ) -> HttpResponse:
        if post.category.tree_id == BLOG_CATEGORY_TREE:
            return redirect(
                reverse(
                    "blog:story",
                    kwargs={"id": post.thread_id},
                ) + f"#comment-{post.id}"
            )

        return action(request, post)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: RedirectToPostHookAction,
        request: HttpRequest,
        post: Post,
    ) -> HttpResponse:
        return super().__call__(action, request, post)


redirect_to_post_hook = RedirectToPostHook()
