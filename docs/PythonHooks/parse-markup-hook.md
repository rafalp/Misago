# `parse_markup_hook`

```python
from misago.richtext.hooks import parse_markup_hook

parse_markup_hook.call_action(
    action: ParseMarkupAction,
    context: GraphQLContext,
    markup: str,
    metadata: dict,
)
```

A filter for the function used to parse str with markup into `RichText`.

Returns a tuple with JSON-serializable `RichText` and `dict` with metadata.s


## Required arguments

### `action`

```python
async def parse_markup(
    context: GraphQLContext, markup: str
) -> Tuple[RichText, dict]:
    ...
```

Next filter or built-in function used to parse markup string.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `markup`

```python
str
```

Python string containing unparsed markup.


### `metadata`

```python
dict
```

`dict` containing metadata set during parsing (eg. list of mentioned users).