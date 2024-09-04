# `get_redirect_to_post_response_hook`

This hook wraps the standard function that Misago uses to get a HTTP redirect response to a post.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_redirect_to_post_response_hook
```


## Filter

```python
def custom_get_redirect_to_post_response_filter(
    action: GetRedirectToPostResponseHookAction,
    request: HttpRequest,
    post: Post,
) -> HttpResponse:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetRedirectToPostResponseHookAction`

A standard Misago function used to get a HTTP redirect response to a post.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `post: Post`

A post to redirect to. It's `category` attribute is already populated.


### Return value

Django's `HttpResponse` with redirect to a post.


## Action

```python
def get_redirect_to_post_response_action(request: HttpRequest, post: Post) -> HttpResponse:
    ...
```

A standard Misago function used to get a HTTP redirect response to a post.


### Arguments

#### `request: HttpRequest`

The request object.


#### `post: Post`

A post to redirect to. It's `category` attribute is already populated.


### Return value

Django's `HttpResponse` with redirect to a post.


## Example

The code below implements a custom filter function that creates custom redirect response for posts in non-standard category type:

```python
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from misago.threads.hooks import get_redirect_to_post_response_hook
from misago.threads.models import Post

BLOG_CATEGORY_TREE = 500

@get_redirect_to_post_response_hook.append_filter
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