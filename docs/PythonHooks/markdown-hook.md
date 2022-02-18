# `parse_markup_hook`

```python
from misago.richtext.hooks import markdown_hook

markdown_hook.call_action(
    action: MarkdownAction,
    context: Context,
    markup: str,
    metadata: dict,
)
```

A synchronous filter for the function used to parse str with markup into abstract syntax tree.

Returns list containing abstract syntax tree nodes for parsed markup.


## Required arguments

### `action`

```python
async def parse_markup(
    context: Context, markup: str
) -> List[dict]:
    ...
```

Next filter or built-in function used to parse markup string.


### `context`

```python
Context
```

A dict with GraphQL query context.


### `markup`

```python
str
```

Python string containing unparsed markup.


### `metadata`

```python
Dict[str, Any]
```

A mutable dict with all metadata for parsed markup.