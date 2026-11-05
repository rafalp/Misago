# `anonymize_user_data_hook`

`anonymize_user_data_hook` is a **filter** hook.


## Location

This hook can be imported from `misago.users.hooks`:

```python
from misago.users.hooks import anonymize_user_data_hook
```


## Filter

```python
def custom_anonymize_user_data_filter(
    action: AnonymizeUserDataHookAction,
    user: User,
    anonymous_username: str,
) -> None:
    ...
```


## Action

```python
def anonymize_user_data_action(user: User, anonymous_username: str) -> None:
    ...
```