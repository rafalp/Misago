# `check_see_post_permission_hook`

This hook wraps the standard Misago function used to check if the user has a permission to see a post. Raises Django's `Http404` if they can't see it or `PermissionDenied` with an error message if they can't see it's contents.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_see_post_permission_hook
```


## Filter

```python
def custom_check_see_post_permission_filter(
    action: CheckSeePostPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    post: Post,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckSeePostPermissionHookAction`

A standard Misago function used to check if the user has a permission to see a post. Raises Django's `Http404` if they can't see it or `PermissionDenied` with an error message if they can't see it's contents.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


#### `post: Post`

A post to check permissions for.


## Action

```python
def check_see_post_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    post: Post,
) -> None:
    ...
```

A standard Misago function used to check if the user has a permission to see a post. Raises Django's `Http404` if they can't see it or `PermissionDenied` with an error message if they can't see it's contents.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


#### `post: Post`

A post to check permissions for.


## Example

The code below implements a custom filter function that blocks a user from seeing a specified thread's post if there is a custom flag set on their account.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.categories.models import Category
from misago.permissions.hooks import check_see_post_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Post, Thread

@check_see_post_permission_hook.append_filter
def check_user_can_see_thread_post(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
) -> None:
    # Run standard permission checks
    action(permissions, category, thread, post)

    if thread.id in permissions.user.plugin_data.get("hidden_post", []):
        raise PermissionDenied(
            pgettext(
                "post permission error",
                "Site admin has removed your access to this post."
            )
        )
```