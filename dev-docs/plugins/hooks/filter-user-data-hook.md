# `filter_user_data_hook` hook

> Filter the user data from the OAuth 2 server.

This hook wraps the standard logic used by Misago to filter a Python `dict` containing the user data retrieved from the OAuth 2 server.

`filter_user_data_hook` is a **filter** hook.

This hook can be imported from `misago.oauth2.hooks`:

```python
# exaple_plugin/register_hooks.py
from misago.oauth2.hooks import filter_user_data_hook

from .override_filter_user_data_hook import filter_user_data_hook
```


## Filter


## Action