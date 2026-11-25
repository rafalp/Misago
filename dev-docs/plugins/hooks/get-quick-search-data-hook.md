# `get_quick_search_data_hook`

This hook wraps a Misago function used to get a template context for a quick search component.

This template context is a `dict` that follows this type:

```
class QuickSearchScope(TypedDict):
    id: str
    name: str
    url: str

class QuickSearchData(TypedDict):
    id: str
    template_name: str
    scopes: list[QuickSearchScope]
```

For the quick search component to be displayed the function must return a `dict` with the `scopes` list containing at least one scope.


## Location

This hook can be imported from `misago.search.hooks`:

```python
from misago.search.hooks import get_quick_search_data_hook
```


## Filter

```python
def custom_get_quick_search_data_filter(
    action: GetQuickSearchDataHookAction, request: HttpRequest
) -> dict | None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetQuickSearchDataHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


### Returns

A `dict` with a template context or `None`.


## Action

```python
def get_quick_search_data_action(request: HttpRequest) -> dict | None:
    ...
```

Misago function used to get a template context for a quick search component.


### Arguments

#### `request: HttpRequest`

The request object.


### Returns

A `dict` with a template context or `None`.


## Example

Add a custom quick search scope:

```python
from misago.search.hooks import get_quick_search_data_hook
from misago.search.quicksearch import QuickSearchScope

@get_quick_search_data_hook.append_filter
def set_plugin_search_scope(action, request: HttpRequest) -> dict:
    if data := action(request):
        data["scopes"].append(
            QuickSearchScope(
                id="plugin-scope",
                name="Plugin",
                url="/my-plugin/quick-search",
            )
        )

        return data

    return None
```