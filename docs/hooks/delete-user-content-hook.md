# `delete_user_content_hook`

```python
from misago.users.hooks import delete_user_content_hook

delete_user_content_hook.call_action(
    action: DeleteUserContentAction,
    user: User,
)
```

A filter for the function used to delete content associated with given user account from the database.


## Required arguments

### `action`

```python
async def delete_user_content(user: User):
    ...
```

Next filter or built-in function used to delete user content from the database.


### `user`

```python
User
```

`User` dataclass representing user to delete.
