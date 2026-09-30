# `parse_search_query_hook`

This hook wraps a Misago function used to parse a search query for the forum search.

It returns a 'SearchQuery' object that search backends can translate to a backend-specific search query.


## Location

This hook can be imported from `misago.search.hooks`:

```python
from misago.search.hooks import parse_search_query_hook
```


## Filter

```python
def custom_parse_search_query_filter(
    action: ParseSearchQueryHookAction, search_query: str
) -> Optional['SearchQuery']:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ParseSearchQueryHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `search_query: str`

A search query `str`.


### Return value

A `SearchQuery` object, or `None` if the query couldn't be parsed.


## Action

```python
def parse_search_query_action(search_query: str) -> Optional['SearchQuery']:
    ...
```

Misago function used to parse a `str` to a `SearchQuery` object.


### Arguments

#### `search_query: str`

A search query `str`.


### Return value

A `SearchQuery` object, or `None` if the query couldn't be parsed.


## Example

Add a naive cache for queries shorter than a specified length:

```python
from misago.search.hooks import parse_search_query_hook
from misago.search.query import SearchQuery

CACHED_QUERY_LEN = 100

_search_query_cache: dict[str, SearchQuery] = {}

@parse_search_query_hook.append_filter
def cache_parsed_query(action, search_query: str) -> SearchQuery | None:
    if len(search_query) > CACHED_QUERY_LEN:
        return action(search_query)

    if search_query not in _search_query_cache:
        _search_query_cache[search_query] = action(search_query)

    return _search_query_cache[search_query]
```