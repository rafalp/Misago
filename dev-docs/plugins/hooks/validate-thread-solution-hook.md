# `validate_thread_solution_hook`

This hook allows plugins to replace or extend the logic used to validate if post can be selected as a thread solution.

This hook allows plugins to replace or extend the logic used to validate if a post can be selected as a thread solution.


## Location

This hook can be imported from `misago.solutions.hooks`:

```python
from misago.solutions.hooks import validate_thread_solution_hook
```


## Filter

```python
def custom_validate_thread_solution_filter(
    action: ValidateThreadSolutionHookAction,
    post: Post,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ValidateThreadSolutionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post: Post`

The post to validate.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def validate_thread_solution_action(post: Post, request: HttpRequest | None=None) -> None:
    ...
```

Misago function used to validate if a post can be selected as a thread solution.


### Arguments

#### `post: Post`

The post to validate.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Prevent a post made by the thread’s starter from being selected as the thread’s solution:

```python
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext
from misago.solutions.hooks import validate_thread_solution_hook
from misago.threads.models import Post


@validate_thread_solution_hook.append_filter
def validate_thread_solution_not_by_op(
    action,
    post: Post,
    request: HttpRequest | None = None,
) -> None:
    action(post, request)

    if post.poster_id and post.poster_id == post.thread.starter_id:
        raise ValidationError(
            message=pgettext(
                "thread solution validator",
                "This post can't be selected as a thread solution.",
            ),
            code="solution",
        )
```