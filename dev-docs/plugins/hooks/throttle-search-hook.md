# `throttle_search_hook`

This hook wraps a Misago function used to throttle search requests.

Returns the number of seconds the client must wait before searching again.


## Location

This hook can be imported from `misago.search.hooks`:

```python
from misago.search.hooks import throttle_search_hook
```


## Filter

```python
def custom_throttle_search_filter(
    action: ThrottleSearchHookAction, request: HttpRequest
) -> int:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ThrottleSearchHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request to throttle.


### Return value

An `int` specifying the number of seconds the client must wait before searching again, or `0` if they can search immediately.


## Action

```python
def throttle_search_action(request: HttpRequest) -> int:
    ...
```

Misago function used to throttle searches for the request.


### Arguments

#### `request: HttpRequest`

The request to throttle.


### Return value

An `int` specifying the number of seconds the client must wait before searching again, or `0` if they can search immediately.


## Example

Disable search throttling for a special IP address:

```python
from django.http import HttpRequest
from misago.search.hooks import throttle_search_hook

@throttle_search_hook.append_filter
def throttle_discouraged_user_search(
    action, request: HttpRequest
) -> int:
    if request.user_ip == "38.0.0.14":
        return 0

    return action(request)
```