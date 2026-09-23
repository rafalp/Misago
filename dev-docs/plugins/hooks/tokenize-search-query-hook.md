# `tokenize_search_query_hook`

This hook wraps a standard Misago function used to parse a search query used for forum search to a token stream.

It returns a list of 'Token' objects that the next parsing step will convert into a `SearchQuery`.


## Location

This hook can be imported from `misago.search.hooks`:

```python
from misago.search.hooks import tokenize_search_query_hook
```


## Filter

```python
def custom_tokenize_search_query_filter(action: TokenizeSearchQueryHookAction, query: str) -> Optional[list['Token']]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: TokenizeSearchQueryHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `query: str`

A search query `str`.


### Return value

A `list` of `Token` objects.

This list will be empty if the query didn't contain any valid search text.


## Action

```python
def tokenize_search_query_action(query: str) -> Optional[list['Token']]:
    ...
```

Misago function used to parse a `str` to a token stream.


### Arguments

#### `query: str`

A search query `str`.


### Return value

A `list` of `Token` objects.

This list will be empty if the query didn't contain any valid search text.


## Example

Add synonyms for some words in a parsed search query:

```python
from misago.search.hooks import tokenize_search_query_hook
from misago.search.query import Token, TokenType

@tokenize_search_query_hook.append_filter
def insert_synonyms(action, query: str) -> list[Token]:
    tokens: list[Token] = []

    for token in action(query):
        if token[0] == TokenType.WORD and token[1].lower() == "terran":
            tokens.append((TokenType.GROUP_OPEN,))
            tokens.append(token)
            tokens.append((TokenType.OR,))
            tokens.append((TokenType.WORD, "earthling"))
            tokens.append((TokenType.GROUP_CLOSE,))

        else:
            tokens.append(token)

    return tokens
```