# `update_markup_metadata_hook`

```python
update_markup_metadata_hook.call_action(
    action: UpdateMarkupMetadataAction,
    context: GraphQLContext,
    ast: dict,
    metadata: dict,
)
```

An asynchronous filter for the function used to update `dict` parsed markup's metadata with data from database (eg. mentioned users).


## Required arguments

### `action`

```python
async def update_markup_metadata(
    context: GraphQLContext, act: dict, metadata: dict
):
```

Next filter or built-in function used to update `dict` with parsed markup `metadata`.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `ast`

```python
list
```

`list` containing abstract syntax tree for parsed markup as returned by `mistune.AstRenderer`.


### `metadata`

```python
Dict[str, Any]
```

A dict with all metadata for parsed markup. Should be mutated in place by plugin's filter.