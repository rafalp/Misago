# `validate_search_query_hook`

This hook wraps a standard Misago function used to validate a search query for the forum search.

It returns nothing, but should raise `ValidationError` if the query fails to validate.


## Location

This hook can be imported from `misago.search.hooks`:

```python
from misago.search.hooks import validate_search_query_hook
```


## Filter

```python
def custom_validate_search_query_filter(
    action: ValidateSearchQueryHookAction,
    query: 'SearchQuery',
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ValidateSearchQueryHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `query: SearchQuery`

A `SearchQuery` object to validate.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def validate_search_query_action(
    query: 'SearchQuery', request: HttpRequest | None=None
) -> None:
    ...
```

Misago function used to validate a `SearchQuery` object.

Raises `ValidationError` if query is not valid.


### Arguments

#### `query: SearchQuery`

A `SearchQuery` object to validate.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Validate that search doesn't contain too many keywords:

```python
from django.core.exceptions import ValidationError
from misago.search.hooks import validate_search_query_hook
from misago.search.query import SearchQuery

@validate_search_query_hook.append_filter
def validate_search_query_keywords(action, query: SearchQuery):
    action(query)

    if count_keywords(query) > 5:
        raise ValidationError(
            "Search query can't contain more than 5 keywords."
        )


def count_keywords(query: SearchQuery) -> int:
    ...  # Plugin provided...
```