# `convert_inline_ast_to_text_hook`

```python
convert_inline_ast_to_text_hook.call_action(
    action: ConvertInlineAstToTextAction, context: GraphQLContext, ast: dict
)
```

A synchronous filter for the function used to convert `dict` with inline abstract syntax tree to `str`.

Returns `str` if inline AST is valid or `None`.


## Required arguments

### `action`

```python
def convert_inline_ast_to_text(
    context: GraphQLContext, act: dict
) -> Optional[str]:
    ...
```

Next filter or built-in function used to convert `dict` with inline abstract syntax tree to `str`.


### `context`

```python
Optional[GraphQLContext]
```

A dict with GraphQL query context.


### `ast`

```python
dict
```

`dict` containing abstract syntax tree for inline markup as returned by `mistune.AstRenderer`.