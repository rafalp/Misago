# `shorten_url_hook`

This hook wraps the standard function that Misago uses to shorten URLs in text.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import shorten_url_hook
```


## Filter

```python
def custom_shorten_url_filter(action: ShortenURLHookAction, url: str) -> str:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ShortenURLHookAction`

Misago function used to shorten URLs in text or the next filter function from another plugin.

See the [action](#action) section for details.


#### `url: str`

A `str` with URL to be shortened.


### Return value

A `str` with the shortened URL.


## Action

```python
def shorten_url_action(url: str) -> str:
    ...
```

Misago function used to shorten URLs in text or the next filter function from another plugin.


### Arguments

#### `url: str`

A `str` with URL to be shortened.


### Return value

A `str` with the shortened URL.


## Example

The code below implements a custom filter function that disables shortening for the Wikipedia URLS:

```python
from misago.parser.hooks import shorten_url_hook


@shorten_url_hook.append_filter
def shorten_url(action, url: str) -> str:
    if "wikipedia" in url:
        return url

    return action(url)
```