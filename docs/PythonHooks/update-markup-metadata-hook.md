# `update_markup_metadata_hook`

```python
update_markup_metadata_hook.call_action(
    context: GraphQLContext,
    ast: dict,
    metadata: dict,
)
```

An action enabling markup parser plugins to inspect the abstract syntax tree and asynchronously update the metadata (eg. by loading mentioned users from database).


## Required arguments

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

A dict with all metadata for parsed markup. Should be mutated in place by actions.


## Action example

Actions are async callables taking three arguments and mutating the `metadata`:

```python
@update_markup_metadata_hook.append
async def load_mentioned_users_data(
    context: GraphQLContext,
    ast: dict,
    metadata: dict,
):
    usernames = extract_usernames_from_ast(ast)
    metadata["mentioned_users"] = await load_mentioned_users(context, usernames)
```