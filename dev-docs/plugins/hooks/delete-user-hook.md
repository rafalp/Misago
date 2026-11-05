# `delete_user_hook`

Hook that wraps the standard function used by Misago to delete a user.

Plugins can execute custom logic before and after deletion, modify arguments, or prevent the original action.


## Location

This hook can be imported from `misago.users.hooks`:

```python
from misago.users.hooks import delete_user_hook
```


## Filter

```python
def custom_delete_user_filter(
    action: DeleteUserHookAction,
    user: User,
    content_action: DeleteUserContentAction,
    *,
    context: dict[str, Any] | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


## Action

```python
def delete_user_action(
    user: User,
    content_action: DeleteUserContentAction,
    *,
    context: dict[str, Any] | None=None,
) -> None:
    ...
```

Standard function used by Misago to delete a user.

Arguments:

user:     User instance that will be deleted.

content_action:     Action determining what happens to user's content.

context:     Additional context passed to the deletion action.