# `validate_user_data_hook`

`validate_user_data_hook` is a **filter** hook.


## Location

This hook can be imported from `misago.oauth2.hooks`:

```python
from misago.oauth2.hooks import validate_user_data_hook
```


## Filter

Filter function implemented by a plugin must have the following signature:

```python
def custom_validate_user_data_filter(
    action: ValidateUserDataHookAction,
    request: HttpRequest,
    user: Optional[User],
    user_data: dict,
    response_json: dict,
) -> dict:
    ...
```


## Action

Action callable passed as filter's `action` argument has the following signature:

```python
def validate_user_data_action(
    request: HttpRequest,
    user: Optional[User],
    user_data: dict,
    response_json: dict,
) -> dict:
    ...
```