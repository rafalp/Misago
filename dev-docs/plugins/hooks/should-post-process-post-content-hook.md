# `should_post_process_post_content_hook`

This hook wraps a standard Misago function used to determine whether post content should be post-processed.

If True is returned, a Celery task will be scheduled to post-process the post content.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import should_post_process_post_content_hook
```


## Filter

```python
def custom_should_post_process_post_content_filter(
    action: ShouldPostProcessPostContentHookAction, post: Post
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ShouldPostProcessPostContentHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `post: Post`

The `Post` instance to check.


### Return value

Returns `bool` with `True` if post content should be post-processed.


## Action

```python
def should_post_process_post_content_action(post: Post) -> bool:
    ...
```

Misago function used to determine whether post content should be post-processed.


### Arguments

#### `post: Post`

The `Post` instance to check.


### Return value

Returns `bool` with `True` if post content should be post-processed.


## Example

The code below implements a custom filter function that returns `True` if the post contains HTML markup that requires post-processing.

```python
from misago.posting.hooks import should_post_process_post_content_hook
from misago.threads.models import Post


@should_post_process_post_content_hook.append_filter
def should_post_process_post_plugin_content(action, post: Post) -> bool:
    if "<plugin-html" in post.content_parsed:
        return True

    return action(post)
```