# `clean_displayed_url_hook`

This hook wraps the standard function that Misago uses to clean URLs for display in HTML


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import clean_displayed_url_hook
```


## Filter

```python
def custom_clean_displayed_url_filter(action: CleanDisplayedURLHookAction, url: str) -> str:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CleanDisplayedURLHookAction`

A standard Misago function used to clean URLs for display in HTML or the next filter function from another plugin.

See the [action](#action) section for details.


#### `url: str`

A `str` with URL to be cleaned.


### Return value

A `str` with the cleaned URL.


## Action

```python
def clean_displayed_url_action(url: str) -> str:
    ...
```

A standard Misago function used to clean URLs for display in HTML or the next filter function from another plugin.


### Arguments

#### `url: str`

A `str` with URL to be cleaned.


### Return value

A `str` with the cleaned URL.


## Example

The code below implements a custom filter function that disables cleaning for the Wikipedia URLS:

```python
from misago.parser.hooks import clean_displayed_url_hook


@clean_displayed_url_hook.append_filter
def clean_displayed_url(action, url: str) -> str:
    if "wikipedia" in url:
        return url

    return action(url)
```