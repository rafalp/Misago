# `clean_search_query_hook`

This hook wraps a standard Misago function used to validate and clean a search query for the forum search.

It returns the cleaned search query, or raises `ValidationError` if the query fails to validate.


## Location

This hook can be imported from `misago.search.hooks`:

```python
from misago.search.hooks import clean_search_query_hook
```


## Filter

```python
def custom_clean_search_query_filter(
    action: CleanSearchQueryHookAction,
    query: str,
    max_length: int,
    min_term_length: int,
    request: HttpRequest | None=None,
) -> str:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CleanSearchQueryHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `query: str`

The search query string to clean.


#### `max_length: int`

The maximum length of a search query.


#### `min_term_length: int`

The minimum length of a term (a keyword or a phrase) in a search query.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Raises

Raises `ValidationError` if the query string is not valid.


### Returns

A `str` with the cleaned search query.


## Action

```python
def clean_search_query_action(
    query: str,
    max_length: int,
    min_term_length: int,
    request: HttpRequest | None=None,
) -> str:
    ...
```

Misago function used to validate and clean a search query string.


### Arguments

#### `query: str`

The search query string to clean.


#### `max_length: int`

The maximum length of a search query.


#### `min_term_length: int`

The minimum length of a term (a keyword or a phrase) in a search query.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Raises

Raises `ValidationError` if the query string is not valid.


### Returns

A `str` with the cleaned search query.


## Example

Validate that a search query doesn't contain common words:

```python
from django.core.exceptions import ValidationError
from misago.search.hooks import clean_search_query_hook

COMMON_WORDS = (
    "forum",
    "thread",
)

@clean_search_query_hook.append_filter
def clean_search_query_words(
    action,
    query: str,
    max_length: int,
    min_term_length: int,
    request: HttpRequest | None = None,
) -> str:
    query = action(query, max_length, min_term_length, request)

    query_lowered = query.lower()
    for word in COMMON_WORDS:
        if word in query_lowered:
            raise ValidationError(
                message='Query cannot contain a common word "%(word)s".',
                params={"word": word},
            )

    return query
```