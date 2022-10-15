# `delete_user_hook`

```python
from misago.users.hooks import delete_user_hook

delete_user_hook.call_action(
    action: DeleteUserAction,
    user: User,
)
```

A filter for the function used to delete user account from the database.


## Required arguments

### `action`

```python
async def delete_user(user: User):
    ...
```

Next filter or built-in function used to delete user account from the database.


### `user`

```python
User
```

`User` dataclass representing user to delete.
