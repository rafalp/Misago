# `filter_user_data_hook`

This hook wraps the standard function used by Misago to filter a Python `dict` containing the user data retrieved from the OAuth 2 server.

This code extends standard filter logic with email normalization logic for Gmail domain:

```python

def normalize_gmail_email(

action, request: HttpRequest, user: Optional[User], user_data: dict

) -> dict:

if (

isinstance(user_data.get("email"), str)

and user_data["email"].lower().endswith("@gmail.com")

):

new_user_data = user_data.copy()

new_user_email = user_data["email"][:-10].replace(".", "")

new_user_data["email"] = new_user_email + "@gmail.com"

return action(new_user_data, request, user, user_data)

return action(user_data, request, user, user_data)

filter_user_data_hook.append(normalize_gmail_email)

```

`filter_user_data_hook` is a **filter** hook.


## Location

This hook can be imported from `misago.oauth2.hooks`:

```python
# exaple_plugin/register_hooks.py
from misago.oauth2.hooks import filter_user_data_hook

from .override_filter_user_data_hook import filter_user_data_hook
```


## Filter


## Action