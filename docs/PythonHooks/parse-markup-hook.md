# `parse_markup_hook`

```python
parse_markup_hook.call_action(
    action: ParseMarkupAction,
    context: GraphQLContext,
    markup: str,
)
```

A filter for the function used to parse str with markup into `RichText`.

Returns JSON-serializable `RichText`.


## Required arguments

### `action`

```python
async def parse_markup(context: GraphQLContext, markup: str) -> RichText:
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