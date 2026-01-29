# `check_see_private_thread_post_permission_hook`

This hook wraps a standard Misago function used to check if the user has a permission to see a private thread post. Raises Django's `Http404` if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_see_private_thread_post_permission_hook
```


## Filter

```python
def custom_check_see_private_thread_post_permission_filter(
    action: CheckSeePrivateThreadPostPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    thread: Thread,
    post: Post,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckSeePrivateThreadPostPermissionHookAction`

Misago function used to check if the user has a permission to see a private thread. Raises Django's `Http404` if they don't.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread to check permissions for.


#### `post: Post`

A post to check permissions for.


## Action

```python
def check_see_private_thread_post_permission_action(
    permissions: 'UserPermissionsProxy', thread: Thread, post: Post
) -> None:
    ...
```

Misago function used to check if the user has a permission to see a private thread post. Raises Django's `Http404` if they don't.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread to check permissions for.


#### `post: Post`

A post to check permissions for.


## Example

The code below implements a custom filter function that blocks a user from seeing a specified post if there is a custom flag set on their account.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.permissions.hooks import check_see_private_thread_post_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Post, Thread


@check_see_private_thread_post_permission_hook.append_filter
def check_user_can_see_thread(
    action,
    permissions: UserPermissionsProxy,
    thread: Thread,
    post: Post,
) -> None:
    # Run standard permission checks
    action(permissions, category, thread, post)

    if post.id in permissions.user.plugin_data.get("hidden_post", []):
        raise PermissionDenied(
            pgettext(
                "post permission error",
                "Site admin has removed your access to this post."
            )
        )
```